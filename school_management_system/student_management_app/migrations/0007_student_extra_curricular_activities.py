# Generated by Django 4.2.13 on 2024-07-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0006_assignment_pdf_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='extra_curricular_activities',
            field=models.TextField(blank=True, null=True),
        ),
    ]
