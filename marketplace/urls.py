"""marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from marketplace import settings
from django.conf.urls.static import static

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(openapi.Info(title='команда мы все можем но не сейчас', description='our_team', default_version='v1'), public=True)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger')),
    path('api/', include('product.urls')),
    path('api/', include('account.urls')),
<<<<<<< Updated upstream
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('showimage/', include('showimage.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> Stashed changes
