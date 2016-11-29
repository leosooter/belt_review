"""SemiRestful URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views


app_name = "book_review"
urlpatterns = [
    #Home
    url(r'^$', views.index, name='index'),

    #Show 'new_form'
    url(r'^new$', views.new, name='new'),
    #POST process 'new_form'
    url(r'^create$', views.create, name='create'),

    #Show individual
    url(r'^(?P<id>[\d]{1,6})$', views.show, name="show"),

    #Show 'edit_form'
    url(r'^edit/(?P<id>[\d]{1,6})$', views.edit, name='edit'),
    #POST route to process 'edit_form'
    url(r'^update/(?P<id>[\d]{1,6})$', views.update, name="update"),

    #Delete route shows "are you sure" destroy form
    url(r'^delete/(?P<id>[\d]{1,6})$', views.delete, name="delete"),
    #Destroys book
    url(r'^destroy/(?P<id>[\d]{1,6})$', views.destroy, name="destroy"),
]
