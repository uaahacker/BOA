# Generated by Django 4.2.6 on 2023-12-26 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0002_deposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='usr_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='atm.accdetail'),
        ),
    ]
