from django.urls import path
from . import views

app_name = "book"


urlpatterns = [
    path('<int:id>/<slug:slug>/', views.book_detail_view, name="book_detail"),
    path('my-books/', views.all_books_view, name="all_books_view"),
    path('my-books/add-book/', views.add_book, name="add_book_to_library"),
    path('search/', views.book_search, name='book_search'),
    path("list-view/", views.list_view, name='list_view'),
    path("list-view/add-book/", views.add_book, name='add_book'),
    path('change-status/', views.change_book_status, name="change_status"),
    path('search/response/', views.receive_json_data, name="book_response"),
    path('like/', views.book_like, name="like"),


]