from django.urls import include, path
from . import views

app_name = "club"

urlpatterns = [
    path('r/<int:id>/<slug:category_slug>/', views.reading_club_detail, name='reading_club_detail'),
    path('d/<int:id>/<slug:category_slug>/', views.discussion_club_detail, name='discussion_club_detail'),
    path('create/', views.create_group, name='create_group'),
    path('edit/r/<int:id>/', views.edit_reading_club, name="edit_reading"),
    path('edit/r/<int:id>/response/', views.receive_json_update_r_group, name="edit_group_response"),
    path('edit/r/<int:id>/delete/', views.delete_r_group, name='delete_group_response'),
    path('edit/d/<int:id>/', views.edit_discussion_club, name="edit_discussion"),
    path('edit/d/<int:id>/response/', views.receive_json_update_d_group, name="edit_group_response"),
    path('edit/d/<int:id>/delete/', views.delete_d_group, name='delete_group_response'),

    path('list-view/', views.club_list_view, name='list_view'),
    path('create/response/', views.receive_json_data, name="receive_json"),
    path('toggle/', views.toggle, name="toggle"),
    path('my_clubs/', views.my_clubs, name="club_selection"),


]