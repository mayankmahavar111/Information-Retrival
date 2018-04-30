from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index.as_view(),name='index'),
    url(r'^result$',views.result,name='result'),
    url(r'^globalresult$',views.globalResult,name='globalresult'),
    url(r'^segmentresult$',views.segmentResult,name='segmentresult'),
    url(r'^generaliseresult$',views.generaliseResult,name='generaliseresult'),
    url(r'click/(?P<doc_id>[0-9]{1,10})/(?P<position>[0-9]{1,10})$', views.incClick,name='increaseclick')
]