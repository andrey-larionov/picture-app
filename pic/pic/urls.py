from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views
from rest_framework.request import Request
from pics import views as pic_views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^pictures/$', pic_views.PictureList.as_view()),
    url(r'^pictures/(?P<pk>[0-9]+)/$', pic_views.PictureDetail.as_view()),
    url(r'^users/$', pic_views.CreateUserView.as_view()),
    url(r'^', include(router.urls)),
]