from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Book
from account.models import Profile


class BasicGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=False)
    is_private_group = models.BooleanField(default=False, max_length=255)  # False=group is public, True=group is private
    group_image = models.ImageField(upload_to='images/group_pictures/',
                                    default='images/group_pictures/no_img.jpg', max_length=10000)
    group_description = models.CharField(max_length=500)  # describes the reason for the group
    slug = models.SlugField(blank=True, max_length=500)

    def __str__(self):
        return str(self.group_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.group_name)
        super(BasicGroup, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['group_name']


class ReadingGroup(BasicGroup):
    # a group for users to read a book together

    #  page number that indicates how far the group wants to read
    reading_goal = models.IntegerField(blank=True, null=True)
    current_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True,
                                     related_name='reading_group_book')

    reading_goal_chapter_name = models.CharField(max_length=30, blank=True, null=True)  # the reading goal chapter name

    # group creator
    group_creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                      related_name="reading_group_creator")

    # group members
    group_members = models.ManyToManyField(User, related_name="reading_group_members", blank=True)

    # page count
    current_book_page_count = models.IntegerField(null=True, blank=True)

    # current page
    current_book_current_page = models.IntegerField(null=True, blank=True, default=0)

    # field for all the members that read to the current club goal for reading
    current_goal_achieved = models.ManyToManyField(User, related_name="current_goal_achieved",
                                                   blank=True)

    # field for all members that have not yet reached the current club goal for reading
    current_goal_reaching = models.ManyToManyField(User, related_name="current_goal_reaching",
                                                   blank=True)

    def get_absolute_url(self):
        return reverse('club:reading_club_detail', args=[self.id, self.slug])


class DiscussionGroup(BasicGroup):
    current_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='discussion_group_book')

    # group creator
    group_creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                      related_name="discussion_group_creator")

    # group members
    group_members = models.ManyToManyField(User, related_name="discussion_group_members", blank=True)

    def get_absolute_url(self):
        return reverse('club:discussion_club_detail', args=[self.id, self.slug])


class RecommendationGroup(BasicGroup):
   pass


class BaseComment(models.Model):
    name = models.ForeignKey(User, max_length=100, on_delete=models.CASCADE)  # add it automatically by getting the name form the current user
    profile = models.ForeignKey(Profile, max_length=100, on_delete=models.CASCADE, default=1)
    body = models.TextField(max_length=5000)
    created_on = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_on']
        abstract = True

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class DiscussionComment(BaseComment):
    club = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE, related_name='discussion_comments')

    def set_user(self, user):  # set the name of the commenter automatically
        current_comment = DiscussionGroup.objects.get(id=self.id)
        current_comment.name = user.username

    def set_profile(self, profile):
        current_comment = DiscussionGroup.objects.get(id=self.id)
        current_comment.profile = profile


class ReadingComment(BaseComment):
    club = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE, related_name='reading_comments')

    def set_user(self, user):  # set the name of the commenter automatically
        current_comment = ReadingGroup.objects.get(id=self.id)
        current_comment.name = user.username

    def set_profile(self, profile):
        current_comment = ReadingGroup.objects.get(id=self.id)
        current_comment.profile = profile







