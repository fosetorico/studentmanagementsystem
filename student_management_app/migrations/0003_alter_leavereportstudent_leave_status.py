# Generated by Django 4.1.2 on 2022-11-24 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_alter_attendance_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstudent',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
