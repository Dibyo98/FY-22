# Generated by Django 4.0.3 on 2022-04-12 13:20

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_alter_question_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
