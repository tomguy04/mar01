from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^home$', views.home),
  url(r'^logout$', views.logout),
  url(r'^travels/destination/(?P<tid>\d+)/$', views.destination),
  url(r'^jointrip/(?P<tid>\d+)/(?P<uid>\d+)/$', views.jointrip),
  url(r'^trip/processtrip/$', views.processtrip),
  url(r'^travels/add$', views.getatrip),
  url(r'^login$', views.login),
  url(r'^travels$', views.travels),
  url(r'^doregister$', views.doregister),
  url(r'^main$', views.index)     # This line has changed!
]
