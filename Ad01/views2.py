from django.http import HttpResponse
from django.template import loader

def user_page(reques):
    template = loader.get_template('layout.html')
    return HttpResponse(template.render())
# -- coding: utf-8 --