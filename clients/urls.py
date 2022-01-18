from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('create', views.UserViewSet)
router.register(r'(?P<user_id>[\d]+)/match', views.MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
