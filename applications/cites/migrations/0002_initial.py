# Generated by Django 4.2 on 2023-07-24 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrations', '0002_initial'),
        ('pattients', '0001_initial'),
        ('cites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cites',
            name='pattient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pattients.pattient'),
        ),
        migrations.AddField(
            model_name='cites',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrations.speciality'),
        ),
        migrations.AddField(
            model_name='cites',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrations.status'),
        ),
    ]
