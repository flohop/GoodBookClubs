from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
# 404=page not found; 500=internal server error; 400=bad request; 403=Forbidden error

# set custom error handling pages, do later!
# handler404 = 'landing.views.page_not_found'
# handler500 = 'landing.views.internal_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('clubs/', include('club.urls')),
    path('book/', include('book.urls')),
    path('reverse/', include('ajaximage.urls')),
    path('', include('landing.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


