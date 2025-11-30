from django.urls import path

from . import views

app_name = 'app_quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('quotes/' , views.quotes, name='quotes'),
    path('quotes/<int:page>' , views.quotes, name='quotes_paginate'),
    path('authors/' , views.authors, name='authors'),
    path('authors/<int:page>' , views.authors, name='authors_paginate'),
    path('upload_quote/' , views.upload_quote, name='upload_quote'),
    path('upload_author/' , views.upload_author, name='upload_author')
]