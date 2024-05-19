# Generated by Django 5.0.6 on 2024-05-19 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_form2_month_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='form6',
            name='comments',
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='designation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='cgpa',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='education',
            name='year_of_passing',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='form6',
            name='comment',
            field=models.ManyToManyField(to='users.comment'),
        ),
    ]