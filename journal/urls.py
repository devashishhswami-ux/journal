from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/entries', views.api_entries, name='api_entries'),
    path('api/translate', views.proxy_translate, name='proxy_translate'),
    path('api/ai/grammar', views.ai_check_grammar, name='ai_check_grammar'),
    path('export/zip', views.export_zip, name='export_zip'),
]
