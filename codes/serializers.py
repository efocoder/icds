from rest_framework import serializers

from codes.models import Category, Code


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'category_code', 'status', 'created_at']
        extra_kwargs = {'created_at': {'read_only': True}}


class CodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['id', 'diagnosis_code', 'full_code', 'abbrev_desc', 'full_desc', 'status', 'category']


class CodeRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Code
        fields = ['id', 'diagnosis_code', 'full_code', 'abbrev_desc', 'full_desc', 'status', 'category', 'created_at']
