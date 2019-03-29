# Generated by Django 2.1.7 on 2019-03-27 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('name', models.CharField(db_column='Name', max_length=50)),
                ('code', models.CharField(db_column='Code', max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('first_name', models.TextField(db_column='FirstName')),
                ('last_name', models.TextField(db_column='Surname')),
                ('email', models.EmailField(db_column='Email', max_length=254)),
            ],
            options={
                'db_table': 'Member',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('class_name', models.TextField(db_column='ClassName', max_length=50, null=True)),
                ('is_test', models.BooleanField(db_column='IsTest')),
                ('state', models.CharField(db_column='State', max_length=50)),
                ('lang', models.CharField(db_column='Lang', max_length=10)),
                ('last_edited', models.DateTimeField(db_column='LastEdited')),
            ],
            options={
                'db_table': 'Survey',
            },
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('value', models.TextField(db_column='Value', null=True)),
            ],
            options={
                'db_table': 'SurveyAnswer',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionTemplate',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('class_name', models.CharField(db_column='ClassName', max_length=50, null=True)),
                ('name', models.TextField(db_column='Name')),
                ('label', models.TextField(db_column='Label')),
                ('is_mandatory', models.BooleanField(db_column='Mandatory')),
            ],
            options={
                'db_table': 'SurveyQuestionTemplate',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionValueTemplate',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('value', models.TextField(db_column='Value')),
                ('label', models.TextField(db_column='Label')),
                ('order', models.IntegerField(db_column='Order')),
            ],
            options={
                'db_table': 'SurveyQuestionValueTemplate',
            },
        ),
        migrations.CreateModel(
            name='SurveyStep',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('state', models.CharField(db_column='State', max_length=50)),
                ('class_name', models.CharField(db_column='ClassName', max_length=50, null=True)),
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
                ('friendly_name', models.TextField(db_column='FriendlyName')),
            ],
            options={
                'db_table': 'SurveyStepTemplate',
            },
        ),
        migrations.CreateModel(
            name='SurveyTemplate',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('class_name', models.CharField(db_column='ClassName', max_length=50)),
                ('title', models.TextField(db_column='Title')),
                ('start_date', models.DateTimeField(db_column='StartDate')),
                ('end_date', models.DateTimeField(db_column='EndDate')),
                ('enabled', models.BooleanField(db_column='Enabled')),
            ],
            options={
                'db_table': 'SurveyTemplate',
            },
        ),
        migrations.CreateModel(
            name='EntitySurvey',
            fields=[
                ('survey_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Survey')),
            ],
            options={
                'db_table': 'EntitySurvey',
            },
            bases=('reports.survey',),
        ),
        migrations.CreateModel(
            name='EntitySurveyTemplate',
            fields=[
                ('name', models.TextField(db_column='Name')),
                ('surveytemplate_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.SurveyTemplate')),
                ('parent_template', models.ForeignKey(db_column='ParentID', on_delete=django.db.models.deletion.CASCADE, related_name='entity_surveys', to='reports.SurveyTemplate')),
            ],
            options={
                'db_table': 'EntitySurveyTemplate',
            },
            bases=('reports.surveytemplate',),
        ),
        migrations.CreateModel(
            name='SurveyDropDownQuestionTemplate',
            fields=[
                ('is_multi_value', models.BooleanField(db_column='IsMultiSelect', default=0)),
                ('is_country_selector', models.BooleanField(db_column='IsCountrySelector', default=0)),
                ('surveyquestiontemplate_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.SurveyQuestionTemplate')),
            ],
            options={
                'db_table': 'SurveyDropDownQuestionTemplate',
            },
            bases=('reports.surveyquestiontemplate',),
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
            model_name='surveyquestionvaluetemplate',
            name='question',
            field=models.ForeignKey(db_column='OwnerID', on_delete=django.db.models.deletion.CASCADE, related_name='value_options', to='reports.SurveyQuestionTemplate'),
        ),
        migrations.AddField(
            model_name='surveyquestiontemplate',
            name='step_template',
            field=models.ForeignKey(db_column='StepID', on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='reports.SurveyStepTemplate'),
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='question',
            field=models.ForeignKey(db_column='QuestionID', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='reports.SurveyQuestionTemplate'),
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='step',
            field=models.ForeignKey(db_column='StepID', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='reports.SurveyStep'),
        ),
        migrations.AddField(
            model_name='survey',
            name='owner',
            field=models.ForeignKey(db_column='CreatedByID', on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='reports.Member'),
        ),
        migrations.AddField(
            model_name='survey',
            name='survey_template',
            field=models.ForeignKey(db_column='TemplateID', on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='reports.SurveyTemplate'),
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
        migrations.AddField(
            model_name='entitysurvey',
            name='parent_survey',
            field=models.ForeignKey(db_column='ParentID', on_delete=django.db.models.deletion.CASCADE, related_name='entity_surveys', to='reports.Survey'),
        ),
    ]
