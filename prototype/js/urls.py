from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='js'
urlpatterns = [
    path('', views.HomeView.as_view(), name='all'),
]
