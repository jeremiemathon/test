# Generated by Django 4.2.7 on 2023-11-24 15:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirdParty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('contact_info', models.TextField(blank=True)),
                ('projects', models.ManyToManyField(related_name='third_parties', to='project.project')),
            ],
        ),
        migrations.CreateModel(
            name='TP_Assessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('completed', models.BooleanField(default=False)),
                ('public_token', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('public_password', models.CharField(blank=True, max_length=128, null=True)),
                ('public', models.BooleanField(default=False)),
                ('third_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='thirdparty.thirdparty')),
            ],
        ),
        migrations.CreateModel(
            name='TP_Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('description', models.TextField()),
                ('details', models.TextField(blank=True, null=True)),
                ('max_score', models.IntegerField(default=3)),
                ('weight', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TP_Score',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('value', models.FloatField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TP_AssessmentQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.TextField(blank=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_questions', to='thirdparty.tp_assessment')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_questions', to='thirdparty.tp_question')),
                ('score', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment_score', to='thirdparty.tp_score')),
            ],
            options={
                'unique_together': {('assessment', 'question')},
            },
        ),
    ]
