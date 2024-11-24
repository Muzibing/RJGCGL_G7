from django.contrib import admin
from django.urls import path, include

from backend import views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),  # 指向 backend 应用的 urls.py
    path('', TemplateView.as_view(template_name='frontend/index.html')),
]
