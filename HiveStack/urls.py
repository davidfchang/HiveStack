from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HiveStack.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',"hs.views.index"),
    #url(r'^$',"hs.views.register"),
    #url(r'^fdn/', include(foundation.urls)),
)
urlpatterns += staticfiles_urlpatterns()
