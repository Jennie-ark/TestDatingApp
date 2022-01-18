from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from clients import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/list/', views.ListViewSet.as_view({'get': 'list'})),
    path('api/clients/', include('clients.urls')),
    path('api-token-auth/', csrf_exempt(
        views.CustomObtainAuthToken.as_view())),
]
