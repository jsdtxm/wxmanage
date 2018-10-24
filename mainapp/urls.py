from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^view_note_list/$', views.index, name='view_note_list'),
    url(r'^add_book/$', views.index, name='add_book'),
    url(r'^add_note/$', views.add_note, name='add_note'),
    url(r'^add_note_auto/$', views.add_note_auto, name='add_note_auto'),
    url(r'^add_note_manual/$', views.add_note_manual, name='add_note_manual'),
    url(r'^about/$', views.about, name='about'),
    # url(r'^view_note_list/$', views.index, name='view_note_list'),

]
