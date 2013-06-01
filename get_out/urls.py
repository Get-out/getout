from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns(''
    , url(r'^$', 'get_out.views.index', name='home')

    , url(r'^list$', 'get_out.views.list_view', name='list')
    , url(r'^species$', 'get_out.views.species', name='species')
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

