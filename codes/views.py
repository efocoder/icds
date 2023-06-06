import logging

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from codes.models import Category, Code
from codes.pagination import DefaultPagination
from codes.serializers import CategorySerializer, CodeRetrieveSerializer, CodeCreateSerializer
from codes.tasks import create_bulk_codes

logger = logging.getLogger('django')


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(status='active')
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]


class CodeViewSet(ModelViewSet):
    queryset = Code.objects.filter(status='active').select_related('category')
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CodeRetrieveSerializer
        else:
            return CodeCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'deleted'
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        fs = FileSystemStorage(location='tmp/')
        file = request.FILES.get('file')
        filename = file.__dict__['_name']

        if file is None:
            raise ValidationError({'file': 'This field is required'})

        if not filename.endswith('.csv'):
            raise ValidationError({'file': 'Upload a valid csv file'})

        content = ContentFile(file.read())
        fs.save(filename, content)

        create_bulk_codes.delay(data={'filename': filename, 'user_email': request.user.email})

        return Response({'msg': 'Processing request.'}, status=status.HTTP_200_OK)
