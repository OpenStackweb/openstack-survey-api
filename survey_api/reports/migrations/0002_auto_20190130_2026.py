# Generated by Django 2.1.5 on 2019-01-30 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('class_name', models.TextField(db_column='ClassName')),
                ('is_test', models.BooleanField(db_column='IsTest')),
                ('state', models.CharField(db_column='State', max_length=50)),
                ('lang', models.CharField(db_column='Lang', max_length=10)),
            ],
            options={
                'db_table': 'Survey',
            },
        ),
        migrations.CreateModel(
            name='SurveyStep',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('state', models.CharField(db_column='State', max_length=50)),
                ('class_name', models.TextField(db_column='ClassName')),
            ],
            options={
                'db_table': 'SurveyStep',
            },
        ),
        migrations.CreateModel(
            name='SurveyStepTemplate',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
            ],
            options={
                'db_table': 'SurveyStepTemplate',
            },
        ),
        migrations.CreateModel(
            name='SurveyTemplate',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.TextField(db_column='Title')),
                ('start_date', models.DateField(db_column='StartDate')),
                ('end_date', models.DateField(db_column='EndDate')),
                ('enabled', models.BooleanField(db_column='Enabled')),
            ],
            options={
                'db_table': 'SurveyTemplate',
            },
        ),
        migrations.AlterField(
            model_name='surveyanswer',
            name='id',
            field=models.IntegerField(db_column='ID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='surveyquestiontemplate',
            name='id',
            field=models.IntegerField(db_column='ID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='surveyquestiontemplate',
            name='name',
            field=models.TextField(db_column='Name'),
        ),
        migrations.CreateModel(
            name='EntitySurvey',
            fields=[
                ('survey_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Survey')),
            ],
            options={
                'db_table': 'EntitySurvey',
            },
            bases=('reports.survey',),
        ),
        migrations.CreateModel(
            name='EntitySurveyTemplate',
            fields=[
                ('surveytemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.SurveyTemplate')),
                ('name', models.TextField(db_column='Name')),
                ('parent_survey_template', models.ForeignKey(db_column='ParentID', on_delete=django.db.models.deletion.CASCADE, related_name='entity_surveys', to='reports.SurveyTemplate')),
            ],
            options={
                'db_table': 'EntitySurveyTemplate',
            },
            bases=('reports.surveytemplate',),
        ),
        migrations.AddField(
            model_name='surveysteptemplate',
            name='survey_template',
            field=models.ForeignKey(db_column='SurveyTemplateID', on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='reports.SurveyTemplate'),
        ),
        migrations.AddField(
            model_name='surveystep',
            name='step_template',
            field=models.ForeignKey(db_column='TemplateID', on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='reports.SurveyStepTemplate'),
        ),
        migrations.AddField(
            model_name='surveystep',
            name='survey',
            field=models.ForeignKey(db_column='SurveyID', on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='reports.Survey'),
        ),
        migrations.AddField(
            model_name='survey',
            name='survey_template',
            field=models.ForeignKey(db_column='TemplateID', on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='reports.SurveyTemplate'),
        ),
        migrations.AddField(
            model_name='entitysurvey',
            name='parent_survey',
            field=models.ForeignKey(db_column='ParentID', on_delete=django.db.models.deletion.CASCADE, related_name='entity_surveys', to='reports.Survey'),
        ),
    ]