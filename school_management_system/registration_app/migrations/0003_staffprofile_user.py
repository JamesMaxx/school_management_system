# Generated by Django 4.2.13 on 2024-07-08 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0002_rename_employee_id_adminprofile_admin_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='registration_app.user'),
            preserve_default=False,
        ),
    ]
