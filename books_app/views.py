from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer
from .responses import ApiResponse
from .exceptions import CustomIsAuthenticated


# Create your views here.
class CreateBook(APIView):
	# Protecting the endpoint
	permission_classes = [CustomIsAuthenticated]
	"""Create a new book."""
	def post(self, request):
		try:
			# Validate incoming data
			serializer = BookSerializer(data=request.data)

			# If data is valid, save it to the db
			if serializer.is_valid():
				# Save the new book to the database
				serializer.save()
				# Return created response
				print(serializer.data)
				res = ApiResponse.success_response('Book created successfully', '00', serializer.data)
				return Response(res, status=status.HTTP_201_CREATED)
			# Return errors if invalid
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			res = ApiResponse.error_response(e, '01')
			return  Response(res, status.HTTP_400_BAD_REQUEST)

class GetAllBooks(APIView):
	#Protecting this endpoint
	permission_classes = [CustomIsAuthenticated]
	"""List all books"""
	def get(self, request):
		try:
			# Fetch all books from the database
			books = Book.objects.all()
			# Serialize the book data
			serializer = BookSerializer(books, many=True)
			# Return the serialized data
			response = ApiResponse.success_response( "Books fetched successfully", "00", serializer.data)
			return Response(response, status=status.HTTP_200_OK)
		except Exception as e:
			response = ApiResponse.error_response(e, "01")
			return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetBookById(APIView):
	"""Retrieve a specific book by ID."""
	def get(self, request, pk):
		try:
			# Fetch book by ID
			book = Book.objects.get(pk=pk)
			# book = get_object_or_404(Book, pk=pk)
			# Serialize the book data
			serializer = BookSerializer(book)
			# Return the serialized data
			response = ApiResponse.success_response('Book fetched successfully', '00', serializer.data)
			return Response(response, status=status.HTTP_200_OK)
		except Exception as e:
			# Return 404 if book is not found
			response = ApiResponse.error_response(e, '01')
			return Response(response, status=status.HTTP_404_NOT_FOUND)


class UpdateBook(APIView):
	"""Update a specific book by ID."""
	def put(self, request, pk):
		try:
			# Fetch the book to update
			book = Book.objects.get(pk=pk)
			# Serialize and validate the data
			serializer = BookSerializer(book, data=request.data)
			# If data is valid
			if serializer.is_valid():
				# Update the book
				serializer.save()
				# Return the updated data
				res = ApiResponse.success_response('Book updated successfully', '00', serializer.data)
				return Response(res, status=status.HTTP_200_OK)
			return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			# Return 404 if not found
			res = ApiResponse.error_response(e, '01')
			return Response(res, status=status.HTTP_404_NOT_FOUND)


class DeleteBook(APIView):
	"""Delete a specific book by ID."""
	def delete(self, request, pk):
		try:
			# Fetch the book to delete
			book = Book.objects.get(pk=pk)
			# Delete the book from the database
			book.delete()
			# Return 204 No Content for success
			res = ApiResponse.success_response("Book Deleted successfully.", '00', None)
			return Response(res, status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			# Return 404 if not found
			res = ApiResponse.error_response(e, '01')
			return Response(res, status=status.HTTP_404_NOT_FOUND)