from django.urls import path

from . import chat_views

# 确保 DeepSeekChatView 作为一个类视图被正确地调用
urlpatterns = [
    path('chat/', chat_views.DeepSeekChatView.as_view()),  # 使用 as_view() 方法
]