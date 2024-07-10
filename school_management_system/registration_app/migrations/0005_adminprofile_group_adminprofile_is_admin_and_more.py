# Generated by Django 4.2.13 on 2024-07-10 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0004_alter_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='group',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='staffprofile',
            name='group',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='staffprofile',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='group',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
    ]
