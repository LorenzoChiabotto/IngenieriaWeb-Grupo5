# Generated by Django 3.1 on 2020-09-28 04:27

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('chatRoom', '0003_auto_20200928_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kicked_out_user',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, to='catalog.user_validable'),
        ),
    ]