from django.db import models
from markdownx.models import MarkdownxField
from martor.models import MartorField
from mdeditor.fields import MDTextField
from simplemde.fields import SimpleMDEField


class MartorExample(models.Model):
    content = MartorField(blank=True)


class MDEditorExample(models.Model):
    content = MDTextField(blank=True)


class MarkdownxExample(models.Model):
    content = MarkdownxField(blank=True)


class SimpleMDEExample(models.Model):
    content = SimpleMDEField(blank=True)
