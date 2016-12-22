# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 03:41
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
            options={
                'swappable': 'SIMPLECMS_CONTENT_MODEL',
                'verbose_name_plural': 'CMS Content',
                'verbose_name': 'CMS Content',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CMSPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('slug', models.CharField(blank=True, max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-z0-9_/]*$', 32))])),
            ],
            options={
                'verbose_name': 'CMS Page',
            },
        ),
        migrations.CreateModel(
            name='CMSSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name': 'CMS Site',
            },
        ),
        migrations.AddField(
            model_name='cmspage',
            name='cmssite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='simplecms.CMSSite', verbose_name='CMS Site'),
        ),
        migrations.AddField(
            model_name='cmspage',
            name='content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to=settings.SIMPLECMS_CONTENT_MODEL),
        ),
    ]
