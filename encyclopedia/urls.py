from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path('newpage', views.newpage, name='newpage'),
    path('wiki/<str:entry>', views.entry, name='entry'),
    path('edit/<str:entry>', views.edit, name='edit'),
    path('wiki/', views.randomPage, name='random'),
    path('search', views.search, name='seach'),
]
