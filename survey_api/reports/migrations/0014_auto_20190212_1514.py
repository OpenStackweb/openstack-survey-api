# Generated by Django 2.1.5 on 2019-02-12 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20190212_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitysurvey',
            name='survey_ptr',
            field=models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Survey'),
        ),
    ]
