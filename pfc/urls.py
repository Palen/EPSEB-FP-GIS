from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from django.conf import settings
from django.views.static import serve

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'map.views.home', name='home'),
    url(r'^add/$', 'map.views.add', name='add'),
    url(r'^ajax/init/$', 'map.views.ajax_get_initial_data', name='ajax_init_data'),
    url(r'^ajax/getJob/$', 'map.views.ajax_get_job_properties', name='ajax_get_job_properties'),
    url(r'^ajax/form/$', 'map.views.ajax_get_form_data', name='ajax_get_form_data'),

    url(r'^back/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
   ]