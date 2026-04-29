from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # ← ДОБАВИТЬ ЭТУ СТРОКУ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    # Редирект с /accounts/login/ на /login/
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),  # ← ДОБАВИТЬ ЭТУ СТРОКУ
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)