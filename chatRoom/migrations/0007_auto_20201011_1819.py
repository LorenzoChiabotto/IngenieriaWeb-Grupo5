# Generated by Django 3.1 on 2020-10-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_motivosdenuncias'),
        ('chatRoom', '0006_auto_20201011_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='denuncias',
            name='description',
        ),
        migrations.RemoveField(
            model_name='denuncias',
            name='name',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='denuncias',
            field=models.ManyToManyField(blank=True, related_name='Chat_denuncias', to='chatRoom.Denuncias'),
        ),
        migrations.AddField(
            model_name='denuncias',
            name='Usuarios',
            field=models.ManyToManyField(blank=True, related_name='Denuncias_users', to='catalog.User_validable'),
        ),
    ]