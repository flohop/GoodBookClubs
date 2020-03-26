from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Book


class BasicGroup(models.Model):
    group_name = models.CharField(max_length=100)
    is_private_group = models.BooleanField(default=False)  # False=group is public, True=group is private
    group_image = models.ImageField(upload_to='images/group_pictures/',
                                    default='images/group_pictures/no_img.png')
    group_description = models.CharField(max_length=500)  # describes the reason for the group
    slug = models.SlugField(blank=True)

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

    def get_absolute_url(self):
        return reverse('club:reading_club_detail', args=[self.id, self.slug])


class DiscussionGroup(BasicGroup):
    current_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)

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


class ReadingComment(BaseComment):
    club = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE, related_name='reading_comments')

    def set_user(self, user):  # set the name of the commenter automatically
        current_comment = ReadingGroup.objects.get(id=self.id)
        current_comment.name = user.username






