# Generated by Django 2.1.5 on 2019-02-11 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_auto_20190211_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='id',
        ),
        migrations.AlterField(
            model_name='country',
            name='code',
            field=models.CharField(db_column='Code', max_length=50, primary_key=True, serialize=False),
        ),
    ]