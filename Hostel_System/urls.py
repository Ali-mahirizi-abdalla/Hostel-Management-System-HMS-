from django.contrib import admin
from django.urls import path, include
# from django.conf import settings  # COMMENT OUT TEMPORARILY
# from django.conf.urls.static import static  # COMMENT OUT TEMPORARILY

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('hms.urls', namespace='hms')),
]

# COMMENT OUT EVERYTHING BELOW TEMPORARILY
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)