"""django_markdown_overview_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from markdownx.views import MarkdownifyView

from config.uploader_views import martor_uploader, mdeditor_uploader, FixedMarkdownxImageUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    # Martor
    path('martor/', include('martor.urls')),
    path('martor/uploads/', martor_uploader, name='martor_markdown_uploader'),

    # mdeditor
    path('mdeditor/uploads/', mdeditor_uploader, name='mdeditor_markdown_uploader'),

    # markdownx
    path('markdownx/markdownify/', MarkdownifyView.as_view(), name='markdownx_markdownify'),
    path('markdownx/upload/', FixedMarkdownxImageUploadView.as_view(), name='markdownx_upload'),
]
