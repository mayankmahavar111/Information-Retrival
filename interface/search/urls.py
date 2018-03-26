from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index.as_view(),name='index'),
    url(r'^result$',views.result,name='result')
]