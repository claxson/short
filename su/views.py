from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from models import Url
from models import Var

import json

# Create your views here.
def get_url(b58id):
    try:
        url = Url.get(b58id)
        if url is not None:
            ret = url.real
        else:
            ret = None
    except ObjectDoesNotExist:
        ret = Var.get('default_redirect')
    return ret


def get(request,b58id):
    if request.method != 'GET':
        return HttpResponse('', status=400)

    if len(b58id) > 6:
        return HttpResponse('', status=404)

    url = get_url(b58id)
    if url is not None:
        return redirect(url)
    else:
        return HttpResponse('', status=404)

def post(request):
    if request.method != 'POST':
        return HttpResponse('', status=400)
    if 'HTTP_X_SU_APIKEY' not in request.META:
        return HttpResponse('Invalid Header', status=401)

    if request.META['HTTP_X_SU_APIKEY'] != Var.get('apikey'):
        return HttpResponse('header value', status=401)

    body = json.loads(request.body)
    if 'url' not in body:
        return HttpResponse('', status=422)

    try:
        nw  = Url.new_url(Var.get('base_url'), body['url'])
    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)}), status=500)
    ret = {}
    ret['short'] = nw
    ret['real']  = body['url']
    return HttpResponse(json.dumps(ret), status=201)
