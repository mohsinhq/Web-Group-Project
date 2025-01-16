# Generated by Django 5.1.1 on 2025-01-15 13:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_hobby'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hobby',
            options={'verbose_name_plural': 'Hobbies'},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='hobbies',
        ),
        migrations.AddField(
            model_name='hobby',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='user_hobbies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pageview',
            name='page_name',
            field=models.CharField(default='Default Page', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pageview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Full Name'),
        ),
    ]