from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query/<str:query_string>', views.query, name='query'),
    path('add', views.add, name='add'),
    path('remove', views.remove, name='remove'),
    path('update', views.update, name='update')

]
