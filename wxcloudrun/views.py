# coding=UTF-8
import json
import logging
import requests

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters


logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """
    return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count(request)
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count(request):
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    # b = requests.get("https://www.baidu.com/")
    # logger.info("baidu snippet: %s", b.text[:1000])
    logger.info(request.headers)
    return JsonResponse(
        {
            'code': 0,
            'data': data.count,
        },
        json_dumps_params={'ensure_ascii': False}
    )


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})


def push(request, _):
    data = {
        "template_id": "Akw6PSGAcqzp0Ws12sv_Ug1HFaWRhS-6r2hJO0GezQo",
        "page": "pages/index",
        "touser": "o29zt5JTOPF2SB-JX_dGwDfFT1ak",
        "data": str({
            "thing1": { "value": "40.8Kg"},
            "date2": { "value": "2017年01月15日 12:00"}
            }),
        "miniprogram_state": "trial",
        "lang": "zh_CN"
    }
    resp = requests.post("https://api.weixin.qq.com/cgi-bin/message/subscribe/send", data=data)
    # logger.info("push msg response: " + str(resp.status_code))
    # return resp
    return JsonResponse({'code': 0, 'push_data': data, 'weixin response': resp.json()})
