# Generated by Django 3.2.5 on 2021-07-25 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20210725_1417'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='task',
            name='check_answer_not_null',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='answer_text',
            new_name='answer',
        ),
        migrations.RemoveField(
            model_name='task',
            name='answer_pic',
        ),
    ]
