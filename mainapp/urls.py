from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^view_note_list/$', views.view_note_list, name='view_note_list'),
    url(r'^add_note/$', views.add_note, name='add_note'),
    url(r'^add_note_auto/$', views.add_note_auto, name='add_note_auto'),
    url(r'^add_note_manual/$', views.add_note_manual, name='add_note_manual'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^about/$', views.about, name='about'),
    url(r'^test/$', views.abt, name='abt'),
    url(r'^user_center/$',views.user_center,name='user_center'),
    url(r'^user/$',views.user_center_user,name='user'),
    url(r'^teams/$',views.user_center_team,name='teams'),
    url(r'^delnote/$',views.delnote,name='delnote'),
    url(r'^pdf_viewer/$',views.pdf_viewer,name='pdf_viewer'),
]
