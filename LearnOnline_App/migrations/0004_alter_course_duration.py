# Generated by Django 4.0.4 on 2022-06-29 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearnOnline_App', '0003_course_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
