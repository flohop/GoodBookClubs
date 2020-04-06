from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ReadingGroup, DiscussionGroup
from itertools import chain
from .forms import DiscussionCommentForm, ReadingCommentForm, GroupForm
import urllib.request
import json
from django.views.decorators.clickjacking import xframe_options_sameorigin
from book.models import Book

from account.models import Profile


@login_required
def my_clubs(request):
    user_id = request.user.id
    my_user = User.objects.get(id=user_id)
    my_profile = Profile.objects.get(user=my_user)

    # group i'm a member of
    my_reading_clubs = my_user.reading_group_members.all()
    my_discussion_club = my_user.discussion_group_members.all()

    # groups i'm an admin of
    my_admin_reading_clubs = my_user.reading_group_creator.all()
    my_admin_discussion_clubs = my_user.discussion_group_creator.all()

    # exclude clubs from reading clubs, where user is admin and member, so it only appears once in the list
    for club in my_reading_clubs:
        if club in my_admin_reading_clubs:
            my_reading_clubs = my_reading_clubs.exclude(id=club.id)

    # exclude clubs from discussion clubs, where user is admin and member, so it only appears once in the list
    for club in my_discussion_club:
        if club in my_admin_discussion_clubs:
            my_discussion_club = my_discussion_club.exclude(id=club.id)

    # return the two club to the template, for it to render it
    return render(request, 'club/selection_page.html', {'reading_clubs': my_reading_clubs,
                                                        'discussion_clubs': my_discussion_club,
                                                        'reading_clubs_admin': my_admin_reading_clubs,
                                                        'discussion_clubs_admin': my_admin_discussion_clubs})


def reading_club_detail(request, id, category_slug):
    club = get_object_or_404(ReadingGroup,
                             id=id,)
    book = club.current_book
    user = request.user
    comments = club.reading_comments.filter(disabled=False)
    like_balance = club.current_book.likes.all().count()
    user_liked_book = False

    # check if the user liked the book
    if user in club.current_book.likes.all():
        user_liked_book = True

    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = ReadingCommentForm(data=request.POST)
        if comment_form.is_valid():
            # check if the user already posted the same comment
            print("This is a new comment")
            new_comment = comment_form.save(commit=False)
            # assign values that the user doesnt input by himself
            new_comment.club = club
            new_comment.name = request.user

            new_comment.save()

    else:
        comment_form = ReadingCommentForm()

    return render(request, 'club/reading_club_detail.html', {'club': club,
                                                             'comments': comments,
                                                             'new_comment': new_comment,
                                                             'comment_form': comment_form,
                                                             'like_balance': like_balance,
                                                             'user_liked_book': user_liked_book,
                                                             'book': book})


def discussion_club_detail(request, id, category_slug):
    club = get_object_or_404(DiscussionGroup,
                             id=id)
    comments = club.discussion_comments.filter(disabled=False)
    book = club.current_book
    new_comment = None
    like_balance = club.current_book.likes.all().count()
    user_liked = False

    # check if the user liked the current discussion book
    if request.user in club.current_book.likes.all():
        user_liked = True

    # when comment is posted
    if request.method == 'POST':
        comment_form = DiscussionCommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            new_comment.club = club
            new_comment.name = request.user

            new_comment.save()
    else:
        comment_form = DiscussionCommentForm()

    return render(request, 'club/discussion_club_detail.html', {'club': club,
                                                                'comments': comments,
                                                                'new_comment': new_comment,
                                                                'comment_form': comment_form,
                                                                'like_balance': like_balance,
                                                                'user_liked_book': user_liked,
                                                                'book': book})


@login_required
def create_group(request):
    user = request.user
    new_group = None
    if request.method == 'POST':
        group_form = GroupForm(data=request.POST)
        if group_form.is_valid() and request.POST.get('group_type'):
            if request.POST.get('group_type') == "reading_club":
                cd = group_form.cleaned_data
                # create and save reading club objects
                new_reading_group = ReadingGroup()
                new_reading_group.group_name = cd['group_name']
                new_reading_group.is_private_group = cd['is_private_group']
                new_reading_group.group_image = cd['group_image']
                new_reading_group.group_description = cd['group_description']
                new_reading_group.current_book = cd['current_book']
                new_reading_group.group_creator = user
                new_reading_group.save()

                print("Redirecting user to newly created group")
                # redirect user to their newly created group
                return redirect(new_reading_group)

    else:
        group_form = GroupForm()

    return render(request, 'club/create_group.html', {'new_group': new_group,
                                                      'group_form': group_form})


@xframe_options_sameorigin
def club_list_view(request):
    # show a list of all clubs, and let the user filter them to find one he want to join
    reading_clubs = ReadingGroup.objects.all()
    user = request.user
    # append attribute to clubs, in order to identify, that it's reading group, in the template
    for club in reading_clubs:
        club.is_reading_club = True

    discussion_clubs = DiscussionGroup.objects.all()

    # append value to all clubs, depending on whether the current user is a member, useful to template
    all_clubs = list(chain(reading_clubs, discussion_clubs))
    for club in all_clubs:
        try:
            club.group_members.get(id=user.id)
            club.member = True
        except ObjectDoesNotExist:
            pass

    return render(request, 'club/list_view.html', {'all_clubs': all_clubs,
                                                   'user': user})


def toggle(request):
    print("Toggle button activated")
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    group_id = request.POST.get("id")
    action = request.POST.get("action")
    group_type = request.POST.get("group_type")

    print("AJAX values: user:", user, "\tgroup-id:", group_id, "\taction:", action, "\tgroup-type:", group_type)
    # get the correct group
    if group_type == "reading":
        group = ReadingGroup.objects.get(id=group_id)
    elif group_type == "discussion":
        group = DiscussionGroup.objects.get(id=group_id)
    else:
        pass

    # do the appropriate action
    try:

        if action == 'leave':
            print("Leaving group")
            group.group_members.remove(user)
        elif action == "join":
            print("Joining group")
            user.save()
            group.save()
            group.group_members.add(user)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print("ERROR:" + str(e))


    print("KO")
    return JsonResponse({'status': 'ko'})


def receive_json_data(request):
    data = json.loads(request.body.decode('utf-8'))

    current_user = User.objects.get(id=request.user.id)
    # extract data from group
    group_name = data.get("name")
    group_description = data.get("description")
    if data.get("is_private") == "on":
        group_is_private = False
    else:
        group_is_private = True

    group_image = data.get("image")
    group_type = data.get("type")
    group_book = data.get("book").get("volumeInfo")

    # extract data from the book
    book_title = group_book.get("title")
    book_author = group_book.get("authors")[0]
    book_release_year = group_book.get("publishedDate")[:4]
    book_description = group_book.get("description")
    book_isbn = group_book.get("industryIdentifiers")[0].get("identifier")

    book_page_count = group_book.get("pageCount")
    book_cover_url = group_book.get("imageLinks").get("thumbnail")
    book_language_code = group_book.get("language")
    book_categories = group_book.get("categories")  # a list of all the categories this book belongs to

    # create the book model, but first, see if this book already exists, and if yes, don't save it, but instead use
    # the old book model instance
    try:
        book_instance = Book.objects.get(book_name=book_title, book_author=book_author)
    except:
        # if book does not exist
        # download the cover url, and store the path
        image_path = "/home/flohop/PycharmProjects/bookclub_project/images/book_covers/" +\
                    str(book_title).lower().replace(" ", "_") +\
                     "_" + str(book_author).lower().replace(" ", "_") + ".jpeg"

        urllib.request.urlretrieve(book_cover_url, image_path)

        # if not old instance exists, create a new book instance
        book_instance = Book.objects.create(book_name=book_title,
                                            book_author=book_author,
                                            book_description=book_description,
                                            book_release_year=book_release_year,
                                            book_isbn_number=book_isbn,
                                            book_page_number=book_page_count,
                                            book_cover_image=image_path,
                                            book_language=book_language_code,
                                            book_categories=" ".join(str(category) for category in book_categories))

    # create the group and assign the book to it
    # first, check what kind of group to create, and then create that group
    if group_type == "reading_club":
        group_instance = ReadingGroup.objects.create(group_name=group_name,
                                                     is_private_group=group_is_private,
                                                     group_image=group_image,
                                                     group_description=group_description,
                                                     group_creator=current_user,
                                                     current_book=book_instance)
    else:
        group_instance = DiscussionGroup.objects.create(group_name=group_name,
                                                        is_private_group=group_is_private,
                                                        group_image=group_image,
                                                        group_description=group_description,
                                                        group_creator=current_user,
                                                        current_book=book_instance)

    # redirect user to newly created page, by get the absolute url of the group_instance
    print("Created new objects, will now redirect")
    response = {'url': group_instance.get_absolute_url()}
    return HttpResponse(json.dumps(response), content_type='application/json')



