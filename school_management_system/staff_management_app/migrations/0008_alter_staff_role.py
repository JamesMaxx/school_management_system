# Generated by Django 4.2.13 on 2024-07-14 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_management_app', '0007_alter_staff_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='role',
            field=models.CharField(choices=[('staff', 'Staff')], default='staff', max_length=20),
        ),
    ]
