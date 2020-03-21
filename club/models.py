from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    # genres related or similar to this one
    related_genres = models.ForeignKey('self', null=True, blank=True,  on_delete=models.SET_NULL)

    def __str__(self):
        return self.genre_name

    class Meta:
        ordering = ['genre_name']


class Profile(models.Model):
    # the model for the basic user

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(upload_to='images/profile_pictures/',
                                        default='images/profile_pictures/no_img.png')

    profile_description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user)


class Book(models.Model):
    # the model for all the books
    book_name = models.CharField(max_length=50)
    book_author = models.CharField(max_length=50)
    book_description = models.TextField(max_length=1000, blank=True, null=True)

    # who has read the book, are reading the book and want to read the book
    people_read_book = models.ManyToManyField(Profile, related_name="people_read_book", blank=True)
    people_reading_book = models.ManyToManyField(Profile, related_name="people_reading_book", blank=True)
    people_want_to_read_book = models.ManyToManyField(Profile, related_name="people_want_to_read_book", blank=True)

    # set max year of release year to current year
    now = datetime.datetime.now()
    book_release_year = models.IntegerField(blank=True, null=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(now.year)])
    book_language = models.CharField(max_length=25, blank=True, null=True)
    book_genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    book_cover_image = models.ImageField(upload_to='images/book_covers/',
                                         default='images/book_covers/no_cover.png')
    book_isbn_number = models.CharField(max_length=17)

    book_page_number = models.IntegerField()  # the number of pages in the book
    book_read_pages = models.IntegerField(blank=True, null=True)  # indicates how far one has read the book

    amazon_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.book_name

    class Meta:
        ordering = ['book_name']


class BasicGroup(models.Model):
    group_name = models.CharField(max_length=100)
    is_private_group = models.BooleanField(default=False)  # False=group is public, True=group is private
    group_image = models.ImageField(upload_to='images/group_pictures/',
                                    default='images/group_pictures/no_img.png')

    def __str__(self):
        return str(self.group_name)

    class Meta:
        abstract = True
        ordering = ['group_name']


class ReadingGroup(BasicGroup):
    # a group for users to read a book together

    #  page number that indicates how far the group wants to read
    reading_goal = models.IntegerField(blank=True, null=True)
    current_book = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)

    reading_goal_chapter_name = models.CharField(max_length=30, blank=True, null=True)  # the reading goal chapter name

    # group creator
    group_creator = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True,
                                         related_name="reading_group_creator")

    # group members
    group_members = models.ManyToManyField(Profile, through='ReadingMembership', through_fields=("group", "person"))


class DiscussionGroup(BasicGroup):
    current_book = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True, blank=True)

    # group creator
    group_creator = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True,
                                         related_name="discussion_group_creator")

    # group members
    group_members = models.ManyToManyField(Profile, through="DiscussionMembership", through_fields=("group", "person"))


class RecommendationGroup(BasicGroup):
   pass


class ReadingMembership(models.Model):
    group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE)
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group_admin = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="reading_membership_admin",
    )


class DiscussionMembership(models.Model):
    group = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE)
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group_admin = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="discussion_membership_admin",
    )























