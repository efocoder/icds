import uuid

from django.db import models

from utils.shared import STATUSES


class Category(models.Model):
    title = models.CharField(max_length=255)
    category_code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class Code(models.Model):
    diagnosis_code = models.CharField(max_length=50)
    full_code = models.CharField(max_length=50)
    abbrev_desc = models.CharField(max_length=255)
    full_desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=STATUSES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        unique_together = ['category', 'full_code']
