# Generated by Django 4.0.3 on 2022-04-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_alter_answer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]