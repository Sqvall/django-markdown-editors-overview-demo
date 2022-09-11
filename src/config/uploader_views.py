import json
import os
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import BaseFormView
from markdownx.forms import ImageForm
from martor.utils import LazyEncoder
from mdeditor.configs import MDConfig


@login_required
def martor_uploader(request):
    """
    Markdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size)s MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            full_path = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)

            try:
                default_storage.save(full_path, ContentFile(image.read()))
            except Exception as exc:
                data = json.dumps({
                    'status': 405,
                    'error': str(exc)
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            data = json.dumps({
                'status': 200,
                'link': default_storage.url(full_path),
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))


MDEDITOR_CONFIGS = MDConfig('default')


@login_required
@method_decorator(csrf_exempt)
def mdeditor_uploader(request):
    """
    Markdown image upload for locale storage
    and represent as json to markdown editor.
    """
    upload_image = request.FILES.get("editormd-image-file", None)

    # image none check
    if not upload_image:
        return JsonResponse({
            'success': 0,
            'message': "未获取到要上传的图片",
            'url': ""
        })

    # image format check
    file_name_list = upload_image.name.split('.')
    file_extension = file_name_list.pop(-1)

    if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
        return JsonResponse({
            'success': 0,
            'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                MDEDITOR_CONFIGS['upload_image_formats']),
            'url': ""
        })

    file_full_name = '%s_%s.%s' % ('{0:%Y%m%d}'.format(datetime.now()),
                                   uuid.uuid4().hex[:10],
                                   file_extension)
    full_path = os.path.join(MDEDITOR_CONFIGS['image_folder'], file_full_name)

    try:
        default_storage.save(full_path, ContentFile(upload_image.read()))
    except Exception as err:
        return JsonResponse({
            'success': 0,
            'message': "上传失败：%s" % str(err),
            'url': ""
        })

    return JsonResponse({'success': 1,
                         'message': "上传成功！",
                         'url': default_storage.url(full_path)})


class FixedMarkdownxImageUploadView(BaseFormView):
    """
    Handling requests for uploading images.
    """

    # template_name = "dummy.html"
    form_class = ImageForm
    success_url = '/'

    def form_invalid(self, form):
        """
        Handling of invalid form events.

        :param form: Django form instance.
        :type form: django.forms.Form
        :return: JSON response with the HTTP-400 error message for AJAX requests
                 and the default response for HTTP requests.
        :rtype: django.http.JsonResponse, django.http.HttpResponse
        """
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)

        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        """
        If the form is valid, the contents are saved.

        If the **POST** request is AJAX (image uploads), a JSON response will be
        produced containing the Markdown encoded image insertion tag with the URL
        using which the uploaded image may be accessed.

        JSON response would be as follows:

        .. code-block:: bash

            { image_code: "![](/media/image_directory/123-4e6-ga3.png)" }

        :param form: Django form instance.
        :type form: django.forms.Form
        :return: JSON encoded Markdown tag for AJAX requests, and an appropriate
                 response for HTTP requests.
        :rtype: django.http.JsonResponse, django.http.HttpResponse
        """
        response = super().form_valid(form)

        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            image_path = form.save(commit=True)
            image_code = '![]({})'.format(image_path)
            return JsonResponse({'image_code': image_code})

        return response
