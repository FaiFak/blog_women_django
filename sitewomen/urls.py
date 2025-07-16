"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sitewomen import settings
from women import views
from women.handler_error import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),  # Главная страница
    path("__debug__/", include("debug_toolbar.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = bad_request
handler403 = denied_access
handler404 = page_not_found
handler500 = server_error

admin.site.site_header = "Панель администрирования"
admin.site.index_title = 'Популярные женщины'
