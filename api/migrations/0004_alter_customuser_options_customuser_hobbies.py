# Generated by Django 5.1.1 on 2025-01-15 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_hobby_options_remove_customuser_hobbies_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='customuser',
            name='hobbies',
            field=models.TextField(blank=True),
        ),
    ]
