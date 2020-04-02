from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .models import Book
import json
import ast
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


# test view
def book_search(request):

    return render(request, 'book/search_book.html', {})


def list_view(request):
    books = Book.objects.all()

    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)

        # add attribute to all book objects, which show the relation the user has to the book
        book_data = {}

        counter = 0

        for book in books:

            # add number of likes the book has
            like_balance = book.likes.all().count()
            user_liked_book = False
            # add if the user likes this book
            if user in book.likes.all():
                user_liked_book = True

            if book in profile.people_read_book.all():
                status = "read"
            elif book in profile.people_reading_book.all():
                status = "reading"
            elif book in profile.people_want_to_read_book.all():
                status = "want-to-read"
            else:
                status = "blank"
            book.status = status
            book.index = counter
            book.like_balance = like_balance
            book.user_liked_book = user_liked_book
            # replace " " with "-", so that i can use it to search by class name in html, because html classes are
            # separated by space
            book_data[counter] = {'name': str(book.book_name).replace(" ", "-"), 'status': book.status, 'id': book.id}
            counter += 1

    else:
        profile = "anonymous"
        book_data = {}

    return render(request, 'book/list_view.html', {'books': books,
                                                   'user': profile,
                                                   'book_data': book_data})


def receive_json_data(request):
    # receive the data from the ajax post, for when the user chooses a book to base is group upon
    data = json.loads(request.body.decode('utf-8'))
    print(data)


def change_book_status(request):
    # receive AJAX call with json data, with the id of the changed element and the new status
    print("i got called")
    data = json.loads(request.POST.get("data"))
    user = request.user
    profile = Profile.objects.get(user=user)
    print(json.loads(request.POST.get("data")))
    x = 0  # iter variable
    counter = len(data)
    for key in data:
        # get the DOM of this book by the id
        try:
            book = Book.objects.get(id=data[str(key)]["id"])
            status = data[str(key)]["value"]

            # remove the user from the old M2M relationship
            if profile in book.people_read_book.all():
                book.people_read_book.remove(profile)
            elif profile in book.people_want_to_read_book.all():
                book.people_want_to_read_book.remove(profile)
            elif profile in book.people_reading_book.all():
                book.people_reading_book.remove(profile)

            # determine the new group of the user and then add it to him
            if status == "read":
                book.people_read_book.add(profile)
            elif status == "reading":
                book.people_reading_book.add(profile)
            elif status == "want-to-read":
                book.people_want_to_read_book.add(profile)
        except KeyError:
            print("Jumped over book with id: ",  x)
            pass
    response = {'status': "OK"}
    return HttpResponse(json.dumps(response), content_type="application/json")

