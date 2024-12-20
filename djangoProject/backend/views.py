from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt
from backend.models import *
from django.contrib.auth.hashers import make_password,check_password
import json

@csrf_exempt
def index(request):
    return HttpResponse("cjw 软工管项目")

@csrf_exempt
def register(request):
    if request.method == "POST":
        print("post以下")
        import json
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        print("register: ", username, password)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message":'用户名已经存在'}, status=400)

        User.objects.create(username=username, password=make_password(password))
        return JsonResponse({"success": True, "message": "注册成功"}, status=201)
    elif request.method == "GET":
        return JsonResponse({"success": False, "message": "这次是GET请求o(╥﹏╥)o"}, status=405)
    return JsonResponse({"success": False, "message": "仅支持POST请求"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        print("login: ", username, password)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)

        if check_password(password, user.password):
            return JsonResponse({'success': True, 'message': '登录成功', 'username': user.username})
        else:
            return JsonResponse({'success': False, 'message': '密码错误'}, status=400)
    elif request.method == "GET":
        return JsonResponse({"success": False, "message": "这次是GET请求o(╥﹏╥)o"}, status=405)
    return JsonResponse({"success": False, "message": "仅支持 POST 请求"}, status=405)

@csrf_exempt
def save_health_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        health_info = data.get("healthInfo")

        if not username or not health_info:
            return JsonResponse({"success": False, "message": "数据不完整"}, status=400)

        # 模拟保存健康信息（可使用数据库）
        print(f"保存健康信息: 用户名={username}, 健康信息={health_info}")
        return JsonResponse({"success": True, "message": "健康信息保存成功"})

    return JsonResponse({"success": False, "message": "仅支持 POST 请求"}, status=405)

@require_http_methods(['GET'])
def add_user(request):
    response = {}
    try:
        user = User(name=request.GET.get('name'), password=request.GET.get('password'))
        user.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(['GET'])
def show_user(request):
    response = {}
    try:
        user = User.objects.filter()
        response['msg'] = 'success'
        response['error_num'] = 0
        response['list'] = json.loads(serializers.serialize(("json",user)))
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)