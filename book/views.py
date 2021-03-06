from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Book
import json
import urllib.request
from account.views import Profile
from django.views.decorators.clickjacking import xframe_options_sameorigin, xframe_options_exempt


@login_required
def all_books_view(request):
    # get all the book associated with the user in the 3 categories and show them in the template
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user=user)

    read_books = profile.people_read_book.all().exclude(id=125)  # exclude the default book
    current_books = profile.people_reading_book.all().exclude(id=125)
    want_to_read_books = profile.people_want_to_read_book.all().exclude(id=125)
    books = read_books | current_books | want_to_read_books
    # add attributes to all books
    all_books = [read_books, current_books, want_to_read_books]
    book_data = {}
    counter = 0
    for books in all_books:
        for book in books:

            # add number of likes the book has
            like_balance = book.likes.all().count()
            user_liked_book = False

            # if user has read the book or is currently reading the book, let user like book
            can_like = False

            # add if the user likes this book
            if user in book.likes.all():
                user_liked_book = True

            if book in profile.people_read_book.all():
                status = "read"
                can_like = True
            elif book in profile.people_reading_book.all():
                status = "reading"
                can_like = True
            elif book in profile.people_want_to_read_book.all():
                status = "want-to-read"
            else:
                status = "blank"

            book.can_like = can_like
            book.status = status
            book.index = counter
            book.like_balance = like_balance
            book.user_liked_book = user_liked_book
            # replace " " with "-", so that i can use it to search by class name in html, because html classes are
            # separated by space
            book_data[counter] = {'name': str(book.book_name).replace(" ", "-"), 'status': book.status, 'id': book.id}
            counter += 1
    return render(request, 'book/all_books_showcase.html', {'read_books': read_books,
                                                            'current_books': current_books,
                                                            'want_to_read_books': want_to_read_books,
                                                            'books': books,
                                                            'books_count': len(all_books[0]) + len(all_books[1]) + len(all_books[2]),
                                                            'book_data': book_data,
                                                            'section': 'books'})


def book_detail_view(request, id, slug):
    book = Book.objects.get(id=id)
    try:
        profile = Profile.objects.get(user=request.user)
        # add info, if user has liked the book
        has_liked = False
        if request.user in book.likes.all():
            has_liked = True
        book.has_liked = has_liked
    except TypeError:
        has_liked = False
        book.has_liked = has_liked
        pass

    # if the book has no description, add a text to show instead of
    if not book.book_description:
        book.book_description = ""

    can_like = False
    try:
        status = '"blank"'
        # if the user is logged in
        if book in profile.people_read_book.all():
            status = '"read"'
            can_like = True
        elif book in profile.people_reading_book.all():
            status = '"reading"'
            can_like = True
        elif book in profile.people_want_to_read_book.all():
            status = '"want-to-read"'
    except UnboundLocalError:
        status = '"blank'

        pass

    book.status = status

    like_balance = book.likes.all().count()

    # add the info, what groups are currently reading this book
    book.reading_clubs = book.reading_group_book.all()
    book.discussion_clubs = book.discussion_group_book.all()

    return render(request, 'book/book_detail.html', {'book': book,
                                                     'liked_book': has_liked,
                                                     'like_balance': like_balance,
                                                     'can_like': can_like,
                                                     'status': status,
                                                     'section': 'books'})

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
                prev_action = "like"
            else:
                book.likes.remove(request.user)
                prev_action = "unlike"
            return JsonResponse({'status': 'ok', "id": book_id, "prev_action": action})
        except:
            pass
    return JsonResponse({'status': 'ko', "id": book_id})


# test view
def book_search(request):

    return render(request, 'book/search_book.html', {})


@xframe_options_sameorigin
def list_view(request):
    books = Book.objects.all().exclude(id=125)  # id=125 is the default book for RClubs with no book
    paginator = Paginator(books, 25)

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

            # if user has read the book or is currently reading the book, let user like book
            can_like = False

            # add if the user likes this book
            if user in book.likes.all():
                user_liked_book = True

            if book in profile.people_read_book.all():
                status = "read"
                can_like = True
            elif book in profile.people_reading_book.all():
                status = "reading"
                can_like = True
            elif book in profile.people_want_to_read_book.all():
                status = "want-to-read"
            else:
                status = "blank"

            book.can_like = can_like
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

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'book/list_view.html', {'books': page_obj,
                                                   'user': profile,
                                                   'book_data': book_data})


@login_required
def receive_json_data(request):
    # receive the data from the ajax post, for when the user chooses a book to base is group upon
    data = json.loads(request.body.decode('utf-8'))
    print(data)


def change_book_status(request):
    # receive AJAX call with the id of the changed book relationship and the new value
    print("i got called")
    id = request.POST.get("id")
    status = request.POST.get("value")
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except TypeError:
        book = Book.objects.get(id=id)
        # if the user is anonymous
        can_like = "False"
        if status == "read":
            can_like = "True"
        elif status == "reading":
            can_like = "True"
        response = {'status': "GUEST", 'can_like': can_like, "id": id, }
        return HttpResponse(json.dumps(response), content_type="application/json")

    # get the DOM of this book by the id
    try:
        book = Book.objects.get(id=id)

        # remove the user from the old M2M relationship
        if profile in book.people_read_book.all():
            book.people_read_book.remove(profile)
        elif profile in book.people_want_to_read_book.all():
            book.people_want_to_read_book.remove(profile)
        elif profile in book.people_reading_book.all():
            book.people_reading_book.remove(profile)

        # determine the new group of the user and then add it to him
        can_like = "False"
        if status == "read":
            book.people_read_book.add(profile)
            can_like = "True"
        elif status == "reading":
            book.people_reading_book.add(profile)
            can_like = "True"
        elif status == "want-to-read":
            book.people_want_to_read_book.add(profile)
    except KeyError as e:
        print("Internal error, key not found: ",  e.with_traceback())
        pass

    response = {'status': "OK", 'can_like': can_like, "id": id, }
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
@require_POST
def add_book(request):
    data = json.loads(request.body.decode("utf-8"))

    group_book = data.get("volumeInfo")

    # extract data from the book
    book_title = group_book.get("title")
    book_author = group_book.get("authors")[0]
    book_release_year = group_book.get("publishedDate")[:4]
    book_description = group_book.get("description")
    book_isbn = group_book.get("industryIdentifiers")[0].get("identifier")

    book_page_count = group_book.get("pageCount")
    book_language_code = group_book.get("language")

    # check if the values exist, and if not, set blank for them

    # check if categories exist:
    if group_book.get("categories"):
        book_categories = group_book.get("categories")   # a list of all the categories this book belongs to
    else:
        book_categories = [""]

    try:
        book_cover_url = group_book.get("imageLinks").get("thumbnail")
    except AttributeError:
        # set the default book cover image
        book_cover_url = None
    # create the book model, but first, see if this book already exists, and if yes, don't save it, but instead use
    # the old book model instance
    try:
        book_instance = Book.objects.get(book_name=book_title, book_author=book_author)
        return JsonResponse({'status': 'already_exists', 'id': book_instance.id})
    except:
        # if book does not exist
        # download the cover url, and store the path
        try:
            image_path = "/home/flohop/PycharmProjects/bookclub_project/staticfiles/images/book_covers/" + \
                         str(book_title).lower().replace(" ", "_") + \
                         "_" + str(book_author).lower().replace(" ", "_") + ".jpeg"

            urllib.request.urlretrieve(book_cover_url, image_path)
        except:
            image_path = None

        # if not old instance exists, create a new book instance

        # book titles that contain " don't work atm, fix later
        book_title = str(book_title).replace('"', "").replace("'", "")
        book_instance = Book.objects.create(book_name=book_title,
                                            book_author=book_author,
                                            book_description=book_description,
                                            book_release_year=book_release_year,
                                            book_isbn_number=book_isbn,
                                            book_page_number=book_page_count,
                                            book_cover_image=image_path,
                                            book_language=book_language_code,
                                            book_categories=" ".join(str(category) for category in book_categories))

        return_book_json = {
            'status': 'new_book',
            'title': str(book_instance.book_name).replace(" ", "-").replace("(", "").replace(")", ""),
            'id': str(book_instance.id),
            'url': str(book_instance.get_absolute_url()),
            'author': str(book_instance.book_author),
            'cover': str(book_instance.book_cover_image),
        }

        return JsonResponse(return_book_json)
