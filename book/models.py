from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from account.models import Profile
from django.contrib.auth.models import User
from .utils import file_cleanup
from django.db.models.signals import post_delete
import datetime


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    # genres related or similar to this one
    related_genres = models.ForeignKey('self', null=True, blank=True,  on_delete=models.SET_NULL)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.genre_name

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created genre
            self.slug = slugify(self.genre_name)
        super(Genre, self).save(*args, **kwargs)

    class Meta:
        ordering = ['genre_name']


class Book(models.Model):
    # the model for all the book
    book_name = models.CharField(max_length=50)
    book_author = models.CharField(max_length=50)
    book_description = models.TextField(max_length=1000, blank=True, null=True)

    slug = models.SlugField(blank=True)

    # who has read the book, are reading the book and want to read the book
    people_read_book = models.ManyToManyField(Profile, related_name="people_read_book", blank=True)
    people_reading_book = models.ManyToManyField(Profile, related_name="people_reading_book", blank=True)
    people_want_to_read_book = models.ManyToManyField(Profile, related_name="people_want_to_read_book", blank=True)

    # set max year of release year to current year
    now = datetime.datetime.now()
    book_release_year = models.IntegerField(blank=True, null=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(now.year)])
    book_language = models.CharField(max_length=25, blank=True, null=True)
    book_categories = models.CharField(max_length=30, null=True, blank=True)
    book_cover_image = models.ImageField(upload_to='images/book_covers/',
                                         default='images/book_covers/no_cover.png')
    book_isbn_number = models.CharField(max_length=17)

    book_page_number = models.IntegerField(blank=True, null=True)  # the number of pages in the book
    book_read_pages = models.IntegerField(blank=True, null=True)  # indicates how far one has read the book

    # likes disliked of the book expressed in two ManyTwoMany Relationships
    likes = models.ManyToManyField(User, related_name='book_likes', blank=True)

    amazon_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.book_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.book_name)
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book:book_detail', args=[self.id, self.slug])

    class Meta:
        ordering = ['book_name']

    post_delete.connect(file_cleanup, sender=book_cover_image, dispatch_uid="book.image.file_cleanup")
