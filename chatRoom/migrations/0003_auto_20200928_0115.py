# Generated by Django 3.1 on 2020-09-28 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatRoom', '0002_message_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(default='chat_message', max_length=255),
        ),
    ]
