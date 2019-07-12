from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import hello.views

# To add a new path, first import the app:
# import blog
admin.autodiscover()
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path(r'^api-auth/', include('rest_framework.urls')),
    path('image_upload', hello.views.index, name='image_upload'),
    path('success', hello.views.success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
