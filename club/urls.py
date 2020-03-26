from django.urls import include, path
from . import views

app_name = "club"

urlpatterns = [
    path('r/<int:id>/<slug:category_slug>/', views.reading_club_detail, name='reading_club_detail'),
    path('d/<int:id>/<slug:category_slug>/', views.discussion_club_detail, name='discussion_club_detail'),
    path('create/', views.create_group, name='create_group'),
    path('list-view/', views.club_list_view, name='list_view'),
    path('toggle/', views.toggle, name="toggle"),
    path('my_clubs/', views.my_clubs, name="club_selection"),


]