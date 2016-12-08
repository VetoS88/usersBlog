from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin

from blogProject import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("blog.urls")),
    url(r'^auth/', include('loginsys.urls')),
    # url(r'^auth/', include('django.contrib.auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


