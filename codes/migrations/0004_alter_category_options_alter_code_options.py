# Generated by Django 4.2.1 on 2023-06-06 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0003_alter_code_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='code',
            options={'ordering': ['id']},
        ),
    ]
