from django.urls import path, re_path
from backend import views
from .views import register,login_view, save_health_info

urlpatterns = [
    re_path(r'^add_user$', views.add_user, name='add_user'),  # 添加命名路由
    re_path(r'^show_user$', views.show_user, name='show_user'),  # 添加命名路由
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('health-info/',save_health_info, name='save_health_info'),
]
