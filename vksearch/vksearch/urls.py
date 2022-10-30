from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from vksearch.settings import DEBUG
from vksearch import view

urlpatterns = [
    path('', view.home, name='home'),
    path('vksearh/', include('vkgroup.urls', namespace='vkgroup')),
    # path('siteauth/', include('siteauth.urls', namespace='siteauth')),
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
if DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
