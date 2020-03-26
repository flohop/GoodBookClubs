from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Book
from account.views import Profile


@login_required
def all_books_view(request):
    # get all the book associated with the user in the 3 categories and show them in the template
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)

    read_books = profile.people_read_book.all()
    current_books = profile.people_reading_book.all()
    want_to_read_books = profile.people_want_to_read_book.all()

    print("User id: " + str(profile.user.id))

    return render(request, 'book/all_books_showcase.html', {'read_books': read_books,
                                                            'current_books': current_books,
                                                            'want_to_read_books': want_to_read_books})


def book_detail_view(request, id, slug):
    book = Book.objects.get(id=id)

    return render(request, 'book/book_detail.html', {'book': book})


@login_required
@require_POST
def book_like(request):
        book_id = request.POST.get("id")
        action = request.POST.get('action')
        if book_id and action:
            try:
                book = Book.objects.get(id=book_id)
                if action == 'like':
                    book.likes.add(request.user)
                else:
                    book.likes.remove(request.user)
                return JsonResponse({'status': 'ok'})
            except:
                pass
        return JsonResponse({'status': 'ko'})