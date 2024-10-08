
from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('user.urls',namespace='user')),

    path('api/recipe/', include('recipe.urls',namespace='recipe')),

    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-docs')
]
