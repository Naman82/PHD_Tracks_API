# Generated by Django 5.0.6 on 2024-05-19 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_examiner_is_assigned_examiner_is_indian_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='form3c',
            name='progress',
            field=models.CharField(default='Satisfactory', max_length=255),
            preserve_default=False,
        ),
    ]
