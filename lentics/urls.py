from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('processing.views',
    url(r'^$', 'home', name='home'),
    # Users admin
    url(r'^register/$', 'register_user'),
    url(r'^login/$', 'log_in'),
    url(r'^login/auth/$', 'auth_view'),
    url(r'^logout/$', 'log_out'),
    # Files admin
    url(r'^files/$', 'show_files'),
    url(r'^files/upload/$', 'show_fileupload', name='file_upload'),
    url(r'^files/submit/$', 'filesubmit'),
    #url(r'^files/success/$', 'upload_success', name='upload_success'),
    url(r'^files/delete/(\d+)/$', 'delete_file'),
    url(r'^files/edit/(\d+)/$', 'show_edit_file', name='show_edit_file'),
    url(r'^files/(?P<id_file>\d+)/$', 'download_file', name="download_file"),
    # Proccesses admin
    url(r'^process/show/(?P<process_id>\d+)/$', 'show_specific_process', name="show_specific_process"),
    url(r'^process/error/(?P<process_id>\d+)/$', 'show_error_process', name="show_error_process"),
    url(r'^process/show/$', 'show_process', name='show_process'),
    url(r'^process/$', 'show_processes'), #revisar
    url(r'^editfile/$', 'editfile'),
    # Tools execution
    url(r'^make-fusion/$', 'make_fusion'),
    #HELP
    url(r'^help/video/$', 'show_video'),
    url(r'^help/tutorial/$', 'show_tutorial'),
    # Admin admin
    url(r'^admin/', include(admin.site.urls)),
)
