# Generated by Django 4.2.13 on 2024-07-15 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_management_app', '0010_alter_staff_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='departments',
            field=models.ManyToManyField(to='staff_management_app.department'),
        ),
    ]
