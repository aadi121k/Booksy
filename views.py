from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_book(request, id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"})



@api_view(['GET'])
def recommend_books(request, id):
    try:
        book = Book.objects.get(id=id)
        keyword = book.title.split()[0]

        recommended = Book.objects.filter(title__icontains=keyword).exclude(id=id)
        serializer = BookSerializer(recommended, many=True)

        return Response({
            "based_on": book.title,
            "recommendations": serializer.data
        })

    except Book.DoesNotExist:
        return Response({"error": "Book not found"})


@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question")
    book_id = request.data.get("book_id")

    # 🔒 validation
    if not question or not book_id:
        return Response({"error": "question and book_id required"})

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"})

    # 🧠 simple RAG-like context usage
    context = book.description

    answer = f"""
📖 Book Context:
{context}

❓ Question:
{question}

💡 Answer:
This book explains that {context.lower()}.
Based on this, the answer to your question is related to the themes and ideas described above.
"""

    return Response({
        "book": book.title,
        "question": question,
        "answer": answer.strip()
    })