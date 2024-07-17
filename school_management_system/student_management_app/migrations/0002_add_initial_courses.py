from django.db import migrations

def create_initial_courses(apps, schema_editor):
    Course = apps.get_model('student_management_app', 'Course')
    initial_courses = [
        {'name': 'Mathematics', 'description': 'Course covering algebra, geometry, and calculus'},
        {'name': 'Science', 'description': 'Course covering physics, chemistry, and biology'},
        {'name': 'English', 'description': 'Course covering literature, grammar, and composition'},
        {'name': 'History', 'description': 'Course covering ancient, medieval, and modern history'},
        {'name': 'Physical Education', 'description': 'Course focusing on physical fitness and sports'}
    ]
    for course_data in initial_courses:
        Course.objects.create(**course_data)

class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_courses),
    ]
