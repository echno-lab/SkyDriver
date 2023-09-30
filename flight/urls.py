from django.urls import path, re_path

from .views import book_flight, delete_ticket, get_tickets, index, search

urlpatterns = [
    path("", index, name="index"),
    path("search/", search, name="search"),
    path("book/", book_flight, name="book_flight"),
    path("tickets/", get_tickets, name="get_tickets"),
    path("delete/", delete_ticket, name="delete_ticket"),
]
