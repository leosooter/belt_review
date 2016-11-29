from django.conf.urls import url
from . import views

app_name='login_reg'
urlpatterns = [
    #home route- displays registration and login forms
    url(r'^$', views.index, name='index'),

    #process registration form
    #sends to books_app index on success
    url(r'^register$', views.register, name='register'),

    #process login form
    #sends to books_app index on success
    url(r'^login$', views.login, name='login'),

    #display form for updating user info and security questions
    url(r'^account$', views.account, name='account'),

    url(r'^show/(?P<id>[\d]{1,})$', views.show, name='show'),
    #process update form
    #sends to success on success
    url(r'^update$', views.update, name='update'),

    #Logs user out
    #Sends to index
    url(r'^delete/(?P<delete_id>[\d]{1,})$', views.delete, name='delete'),

    #Logs user out
    #Sends to index
    url(r'^logout$', views.logout, name='logout'),
]
