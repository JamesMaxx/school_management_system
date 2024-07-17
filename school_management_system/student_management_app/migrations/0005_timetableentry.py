# Generated by Django 4.2.13 on 2024-07-17 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0001_initial'),
        ('student_management_app', '0004_assignment_file_assignment_uploaded_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimetableEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('subject', models.CharField(max_length=100)),
                ('teacher', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event_management.event')),
            ],
        ),
    ]