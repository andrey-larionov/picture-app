from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views
from rest_framework.request import Request
from pics import views as pic_views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token, name='get-auth-token'),
    url(r'^pictures/rate/$', pic_views.PictureRateList.as_view(), name='picture-rate-list'),
    url(r'^pictures/rate/(?P<pk>[0-9]+)/$', pic_views.PictureRateDetail.as_view(), name='picturerate-detail'),
    url(r'^pictures/$', pic_views.PictureList.as_view(), name='pictures-list'),
    url(r'^pictures/rated/$', pic_views.PictureRated.as_view(), name='picture-rated'),
    url(r'^pictures/(?P<pk>[0-9]+)/$', pic_views.PictureDetail.as_view()),
    url(r'^users/$', pic_views.UserList.as_view(), name='users-list'),
    url(r'^', include(router.urls)),
]