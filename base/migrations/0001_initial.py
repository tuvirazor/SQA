# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-20 08:18
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base','0013_project_refactoring'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('event_type', models.CharField(choices=[('ACADEMIC_YEAR', 'Academic Year'), ('DISSERTATIONS_SUBMISSION_SESS_1', 'Submission of academic dissertations - exam session 1'), ('DISSERTATIONS_SUBMISSION_SESS_2', 'Submission of academic dissertations - exam session 2'), ('DISSERTATIONS_SUBMISSION_SESS_3', 'Submission of academic dissertations - exam session 3'), ('EXAM_SCORES_SUBMISSION_SESS_1', 'Submission of exam scores - exam session 1'), ('EXAM_SCORES_SUBMISSION_SESS_2', 'Submission of exam scores - exam session 2'), ('EXAM_SCORES_SUBMISSION_SESS_3', 'Submission of exam scores - exam session 3'), ('DELIBERATIONS_SESS_1', 'Deliberations - exam session 1'), ('DELIBERATIONS_SESS_2', 'Deliberations - exam session 2'), ('DELIBERATIONS_SESS_3', 'Deliberations - exam session 3'), ('EXAM_SCORES_DIFFUSION_SESS_1', 'Diffusion of exam scores - exam session 1'), ('EXAM_SCORES_DIFFUSION_SESS_2', 'Diffusion of exam scores - exam session 2'), ('EXAM_SCORES_DIFFUSION_SESS_3', 'Diffusion of exam scores - exam session 3'), ('EXAM_ENROLLMENTS_SESS_1', 'Exam enrollments - exam session 1'), ('EXAM_ENROLLMENTS_SESS_2', 'Exam enrollments - exam session 2'), ('EXAM_ENROLLMENTS_SESS_3', 'Exam enrollments - exam session 3')], max_length=50)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Attribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('function', models.CharField(blank=True, choices=[('COORDINATOR', 'Coordinator'), ('PROFESSOR', 'Professor')], default='UNKNOWN', max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExamEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=70, null=True)),
                ('score_draft', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)])),
                ('score_reencoded', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)])),
                ('score_final', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)])),
                ('justification_draft', models.CharField(blank=True, choices=[('ABSENT', 'Absent'), ('CHEATING', 'Cheating'), ('ILL', 'Ill'), ('JUSTIFIED_ABSENCE', 'Justified absence'), ('SCORE_MISSING', 'Score missing')], max_length=20, null=True)),
                ('justification_reencoded', models.CharField(blank=True, choices=[('ABSENT', 'Absent'), ('CHEATING', 'Cheating'), ('ILL', 'Ill'), ('JUSTIFIED_ABSENCE', 'Justified absence'), ('SCORE_MISSING', 'Score missing')], max_length=20, null=True)),
                ('justification_final', models.CharField(blank=True, choices=[('ABSENT', 'Absent'), ('CHEATING', 'Cheating'), ('ILL', 'Ill'), ('JUSTIFIED_ABSENCE', 'Justified absence'), ('SCORE_MISSING', 'Score missing')], max_length=20, null=True)),
                ('encoding_status', models.CharField(blank=True, choices=[('SAVED', 'Saved'), ('SUBMITTED', 'Submitted')], max_length=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LearningUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('acronym', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LearningUnitEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=70, null=True)),
                ('date_enrollment', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='LearningUnitYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('acronym', models.CharField(max_length=15)),
                ('title', models.CharField(max_length=255)),
                ('credits', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('decimal_scores', models.BooleanField(default=False)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AcademicYear')),
                ('learning_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnit')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('acronym', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OfferEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=50, null=True)),
                ('date_enrollment', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='OfferYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('acronym', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AcademicYear')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Offer')),
            ],
        ),
        migrations.CreateModel(
            name='OfferYearCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('event_type', models.CharField(choices=[('ACADEMIC_YEAR', 'Academic Year'), ('DISSERTATIONS_SUBMISSION_SESS_1', 'Submission of academic dissertations - exam session 1'), ('DISSERTATIONS_SUBMISSION_SESS_2', 'Submission of academic dissertations - exam session 2'), ('DISSERTATIONS_SUBMISSION_SESS_3', 'Submission of academic dissertations - exam session 3'), ('EXAM_SCORES_SUBMISSION_SESS_1', 'Submission of exam scores - exam session 1'), ('EXAM_SCORES_SUBMISSION_SESS_2', 'Submission of exam scores - exam session 2'), ('EXAM_SCORES_SUBMISSION_SESS_3', 'Submission of exam scores - exam session 3'), ('DELIBERATIONS_SESS_1', 'Deliberations - exam session 1'), ('DELIBERATIONS_SESS_2', 'Deliberations - exam session 2'), ('DELIBERATIONS_SESS_3', 'Deliberations - exam session 3'), ('EXAM_SCORES_DIFFUSION_SESS_1', 'Diffusion of exam scores - exam session 1'), ('EXAM_SCORES_DIFFUSION_SESS_2', 'Diffusion of exam scores - exam session 2'), ('EXAM_SCORES_DIFFUSION_SESS_3', 'Diffusion of exam scores - exam session 3'), ('EXAM_ENROLLMENTS_SESS_1', 'Exam enrollments - exam session 1'), ('EXAM_ENROLLMENTS_SESS_2', 'Exam enrollments - exam session 2'), ('EXAM_ENROLLMENTS_SESS_3', 'Exam enrollments - exam session 3')], max_length=50)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('academic_calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AcademicCalendar')),
                ('offer_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.OfferYear')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('global_id', models.CharField(blank=True, max_length=10, null=True)),
                ('gender', models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unknown')], default='U', max_length=1, null=True)),
                ('national_id', models.CharField(blank=True, max_length=25, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SessionExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('number_session', models.IntegerField()),
                ('status', models.CharField(choices=[('IDLE', 'Idle'), ('OPEN', 'Open'), ('CLOSED', 'Closed')], max_length=10)),
                ('learning_unit_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnitYear')),
                ('offer_year_calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.OfferYearCalendar')),
            ],
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('acronym', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('part_of', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Structure')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('registration_id', models.CharField(max_length=10)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=40, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Person')),
            ],
        ),
        migrations.AddField(
            model_name='programmemanager',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Structure'),
        ),
        migrations.AddField(
            model_name='programmemanager',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Person'),
        ),
        migrations.AddField(
            model_name='offeryear',
            name='structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Structure'),
        ),
        migrations.AddField(
            model_name='offerenrollment',
            name='offer_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.OfferYear'),
        ),
        migrations.AddField(
            model_name='offerenrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Student'),
        ),
        migrations.AddField(
            model_name='learningunitenrollment',
            name='learning_unit_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnitYear'),
        ),
        migrations.AddField(
            model_name='learningunitenrollment',
            name='offer_enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.OfferEnrollment'),
        ),
        migrations.AddField(
            model_name='examenrollment',
            name='learning_unit_enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnitEnrollment'),
        ),
        migrations.AddField(
            model_name='examenrollment',
            name='session_exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.SessionExam'),
        ),
        migrations.AddField(
            model_name='attribution',
            name='learning_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnit'),
        ),
        migrations.AddField(
            model_name='attribution',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Tutor'),
        ),
        migrations.AddField(
            model_name='academiccalendar',
            name='academic_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AcademicYear'),
        ),
    ]