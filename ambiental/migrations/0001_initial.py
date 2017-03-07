# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 01:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
                ('score_a', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6)),
                ('score_b', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6)),
                ('score_c', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6)),
                ('score_d', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6)),
                ('score_e', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6)),
                ('total_score', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(default=b'Nothing here yet', max_length=300)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='RatingElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, max_length=50)),
                ('index', models.CharField(blank=True, max_length=4)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('wd', models.CharField(blank=True, default=b'H/P', max_length=100)),
                ('wf', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4)),
                ('mv', models.CharField(blank=True, choices=[(b'1', b'Slow'), (b'2', b'Kinda Slow'), (b'3', b'Okay'), (b'4', b'Fastish'), (b'5', b'Fast')], default=b'N/A', max_length=1)),
                ('score', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4)),
                ('comment', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField()),
                ('cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ambiental.CD')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ambiental.UserProfile'),
        ),
        migrations.AddField(
            model_name='cd',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ambiental.Project'),
        ),
    ]