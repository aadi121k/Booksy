from django.contrib import admin
from django.urls import path
from books.views import get_books, get_book, recommend_books, ask_question

urlpatterns = [
    path('admin/', admin.site.urls),

    path('books/', get_books),
    path('books/<int:id>/', get_book),
    path('books/<int:id>/recommend/', recommend_books),

    path('ask/', ask_question),
]