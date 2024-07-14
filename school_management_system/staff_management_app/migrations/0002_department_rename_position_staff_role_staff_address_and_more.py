# Generated by Django 5.0.3 on 2024-07-14 04:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_management_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='staff',
            old_name='position',
            new_name='role',
        ),
        migrations.AddField(
            model_name='staff',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='email',
            field=models.EmailField(default='slim@mail.com', max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='first_name',
            field=models.CharField(default='James', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='last_name',
            field=models.CharField(default='Max', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='phone_number',
            field=models.CharField(default='22222222222', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='staff/profile_pics/'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staff',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_members', to='staff_management_app.department'),
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=100)),
                ('year_completed', models.IntegerField(blank=True, null=True)),
                ('upload_certificate', models.FileField(blank=True, null=True, upload_to='staff/certificates/')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_qualifications', to='staff_management_app.staff')),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='qualifications',
            field=models.ManyToManyField(blank=True, related_name='staff_members', to='staff_management_app.qualification'),
        ),
        migrations.CreateModel(
            name='Responsibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_responsibilities', to='staff_management_app.staff')),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='responsibilities',
            field=models.ManyToManyField(blank=True, related_name='staff_members', to='staff_management_app.responsibility'),
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='staff/profile_pics/')),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='staff_management_app.staff')),
            ],
        ),
    ]
