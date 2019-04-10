import json
from django.http import HttpResponse, JsonResponse
from lib.sms import send_sms
from lib.http import render_json
from common import errors
from django.core.cache import cache
from common import keys
from user.models import User, Profile
from user.forms import ProfileForm
from django import forms
from user.logics import upload_avatar_to_server



def submit_phone(request):
    """获取短信验证码"""
    if not request.method == "POST":
        return render_json("request method error", errors.REQUEST_ERROR)
    phone = request.POST.get('phone')
    result, msg = send_sms(phone)
    print(result)
    print(msg)
    return render_json(msg)

def submit_vcode(request):
    """通过验证码登录注册"""
    # 判断是否为post请求
    if not request.method == 'POST':
        return render_json("request method error", errors.REQUEST_ERROR)
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    cache_vcode = cache.get(keys.VCODE_KEY % phone)

    # 对比验证码是否一致
    if vcode == cache_vcode:
        # users = User.objects.get(phonenum=phone)
        # if not users:
            # return render_json('NO THIS USER', errors.NO_THIS_USER)
            # User.objects.create(phonenum=phone, nickname=phone)
        user, _ = User.objects.get_or_create(phonenum=phone, nickname=phone)

        request.session['uid'] = user.id
        return render_json(user.to_string())
    else:
        return render_json('verify code error', errors.VCODE_ERROR)


def get_profile(request):
    """获取个人资料"""
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)

    # profile = Profile.objects.get(id=user.id)
    profile = user.profile
    return render_json(profile.to_string())


def set_profile(request):
    """修改个人资料"""
    # 判断是否是post请求
    if not request.method == 'POST':
        return render_json("request method error", errors.REQUEST_ERROR)
    uid = request.session.get('uid')
    profile_form = ProfileForm(request.POST)
    print(profile_form)
    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.id = uid
        profile.save()
        return render_json('modify profile success')
    else:
        return render_json(profile_form.errors, errors.FORM_VALID_ERROR)



def upload_profile(request):
    """头像上传"""
    # 判断是否是post请求
    if not request.method == 'POST':
        return render_json("request method error", errors.REQUEST_ERROR)

    avatar = request.FILES.get('avatar')
    uid = request.session.get('uid')
    upload_avatar_to_server(uid, avatar)

    return render_json('uploads success')


