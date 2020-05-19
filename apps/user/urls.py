from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from user.views import RegisterView,LoginView,UserInfoView,LogoutView,ChangeView
urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(),name='login'),
    url(r'^logout$',LogoutView.as_view(),name='logout'),
    url(r'^change$', ChangeView.as_view(),name="change"),
    url(r'^$',UserInfoView.as_view(), name='user'),

]
