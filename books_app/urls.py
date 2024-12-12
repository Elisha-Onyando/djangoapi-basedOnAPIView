from django.urls import path
from .views import CreateBook, GetAllBooks
from .views import GetBookById, UpdateBook, DeleteBook
from .auth_views import SignUpView, LoginView

urlpatterns = [
    path('books', GetAllBooks.as_view(), name='book-list'),  # List all books
    path('books/create', CreateBook.as_view(), name='book-create'),  # Create a new book
    path('books/<int:pk>/', GetBookById.as_view(), name='book-detail'),  # Retrieve a book by ID
    path('books/<int:pk>/update', UpdateBook.as_view(), name='book-update'),  # Update a book
    path('books/<int:pk>/delete', DeleteBook.as_view(), name='book-delete'),  # Delete a book
    path('auth/signup', SignUpView.as_view(), name='signup'), # Signup endpoint
    path('auth/login', LoginView.as_view(), name='login'), # Login endpoint
]
