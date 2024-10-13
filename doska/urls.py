from ckeditor_uploader.views import upload, browse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.decorators.cache import never_cache

from doska_ob.views import PostDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('doska_ob/', include('doska_ob.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(r'^upload/', login_required(upload), name='ckeditor_upload'),
    re_path(r'^browse/', login_required(never_cache(browse)), name='ckeditor_browse'),

]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)