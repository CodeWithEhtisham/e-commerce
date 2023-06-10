# Generated by Django 3.2 on 2023-06-10 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0002_auto_20230609_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='action',
            field=models.CharField(blank=True, default='Deliver', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, default='Confirm', max_length=20, null=True),
        ),
    ]