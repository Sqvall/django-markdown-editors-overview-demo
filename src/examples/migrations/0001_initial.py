# Generated by Django 4.1.1 on 2022-09-11 12:36

from django.db import migrations, models
import markdownx.models
import martor.models
import mdeditor.fields
import simplemde.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarkdownxExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', markdownx.models.MarkdownxField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MartorExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', martor.models.MartorField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MDEditorExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', mdeditor.fields.MDTextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SimpleMDEExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', simplemde.fields.SimpleMDEField(blank=True)),
            ],
        ),
    ]
