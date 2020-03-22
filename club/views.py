from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Profile, ReadingGroup, DiscussionGroup


@login_required
def my_clubs(request):
    user_id = request.user.id
    my_user = User.objects.get(id=user_id)
    my_profile = Profile.objects.get(user=my_user)

    my_reading_clubs = my_profile.reading_group_members.all()
    my_discussion_club = my_profile.discussion_group_members.all()

    # return the two club to the template, for it to render it
    print("Hello world")
    return render(request, 'club/selection_page.html', {'reading_clubs': my_reading_clubs,
                                                        'discussion_clubs': my_discussion_club})


def reading_club_detail(request, id, category_slug):
    club = get_object_or_404(ReadingGroup,
                             id=id,)

    return render(request, 'club/reading_club_detail.html', {'club': club})


def discussion_club_detail(request, id, category_slug):
    club = get_object_or_404(DiscussionGroup,
                             id=id)

    return render(request, 'club/discussion_club_detail.html', {'club': club})



