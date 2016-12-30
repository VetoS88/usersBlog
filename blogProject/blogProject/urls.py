from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin

from blogProject import settings
import debug_toolbar

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("blog.urls")),
    url(r'^auth/', include('loginsys.urls')),
    # url(r'^auth/', include('django.contrib.auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
