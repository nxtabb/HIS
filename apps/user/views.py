from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
import re
from user.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from utils.mixin import LoginRequiredMixin


class RegisterView(View):
    def get(self,request):
        # 显示注册界面
        return render(request, 'register.html')

    def post(self,request):
        # 进行注册处理
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 进行数据校验
        if not all([username, password, email]):
            # 如果数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})
        # 校验协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        #检验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request,'register.html',{'errmsg': '用户名已存在'})
        # 进行业务处理:注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 返回应答,跳入
        return redirect(reverse('plat:index'))

class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            password = request.COOKIES.get('password')
            checked = 'checked'
        else:
            username = ''
            password = ''
            checked = ''
        return render(request, 'login.html',{'username':username,'checked':checked,'password':password})
    def post(self,request):
        #登录校验
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})#接受数据
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request,'login.html',{'errmsg':'无此用户'})
        pwd = user.password
        if check_password(password, pwd):
            if user.is_active:
                #记录用户登录状态
                login(request, user)
                next_url = request.GET.get('next', reverse('plat:index'))
                response = redirect(next_url)
                remember = request.POST.get('remember')
                if remember=='on':
                    response.set_cookie('username',username,max_age=7*24*3600)
                    response.set_cookie('password', password, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')
                    response.delete_cookie('password')
                #获取登录后所要跳转到的地址
                #默认跳转到首页
                return response
            else:
                return render(request, 'login.html', {'errmsg': '用户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名密码错误'})#校验数据业务处理


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        #page='/user'
        #request.user.is_authenticated()
        #如果用户登录，则为User类的实例，
        #不然为Anony_mouse_User的实例，
        #调用.is_au...方法，返回true或false
        #获取用户的个人信息
        #获取默认信息
        user = request.user
        #获取user的身份
        #获取用户的历史浏览记
        #from redis import StrictRedis
        #sr = StrictRedis(host='127.0.0.1', port='6379', db='9')
        context = {'page': 'user'}
        return render(request, 'user_center_info.html', context)
class LogoutView(View):
    def get(self,request):
        #清除用户session
        logout(request)
        return redirect(reverse('plat:index'))
class ChangeView(View):
    def get(self,request):
        user = request.user
        if not user.is_authenticated:
            return render(request, 'login.html')
        context = {'user':user,'page':'change'}
        return render(request, 'user_center_info_change.html', context)
    def post(self,request):
        user=request.user
        orcode = request.POST.get('orcode')
        code = request.POST.get('code')
        code1 = request.POST.get('code1')
        email = request.POST.get('email')
        if not user.is_authenticated:
            return render(request,'login.html')
        if not check_password(orcode,user.password):
            return render(request,'user_center_info_change.html',{'errmsg':'原密码不正确'})
        if not all([code,code1,email]):
            return render(request, 'user_center_info_change.html', {'errmsg’:‘数据不完整'})#接受数据
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'user_center_info_change.html', {'errmsg': '邮箱不合法'})
        if check_password(code,user.password) and email == user.email:
            return render(request, 'user_center_info_change.html', {'errmsg': '密码和邮箱都与之前相同'})
        if code ==code1 and len(code) >=8 and len(code)<=20:
            user.set_password(code)
            user.email=email
            user.save()
        else:
            return render(request,'user_center_info_change.html',{'errmsg':'密码不符合规定或两次输入不相同'})
        return redirect(reverse('user:logout'))
