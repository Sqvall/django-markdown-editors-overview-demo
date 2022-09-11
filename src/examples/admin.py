from django.contrib import admin
from django.contrib.admin import ModelAdmin

from examples.models import MartorExample, MDEditorExample, MarkdownxExample, SimpleMDEExample

admin.site.register(MartorExample, ModelAdmin)
admin.site.register(MDEditorExample, ModelAdmin)
admin.site.register(MarkdownxExample, ModelAdmin)
admin.site.register(SimpleMDEExample, ModelAdmin)
