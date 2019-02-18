# Generated by Django 2.1.5 on 2019-02-11 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_auto_20190206_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=50)),
            ],
            options={
                'db_table': 'Continent',
            },
        ),
        migrations.CreateModel(
            name='ContinentCountries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('continent_id', models.ForeignKey(db_column='ContinentID', on_delete=django.db.models.deletion.CASCADE, to='reports.Continent')),
            ],
            options={
                'db_table': 'Continent_Countries',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Name', max_length=50)),
                ('code', models.CharField(db_column='Code', max_length=50)),
            ],
            options={
                'db_table': 'Countries',
            },
        ),
        migrations.AlterField(
            model_name='surveydropdownquestiontemplate',
            name='surveyquestiontemplate_ptr',
            field=models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.SurveyQuestionTemplate'),
        ),
        migrations.AddField(
            model_name='continentcountries',
            name='country_code',
            field=models.ForeignKey(db_column='CountryCode', on_delete=django.db.models.deletion.CASCADE, to='reports.Country'),
        ),
        migrations.AddField(
            model_name='continent',
            name='countries',
            field=models.ManyToManyField(through='reports.ContinentCountries', to='reports.Country'),
        ),
    ]
