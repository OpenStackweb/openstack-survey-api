# Generated by Django 2.1.5 on 2019-02-06 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_auto_20190204_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyquestionvaluetemplate',
            name='order',
            field=models.IntegerField(db_column='Order', default=0),
            preserve_default=False,
        ),
    ]
