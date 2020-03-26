from django import forms
from .models import DiscussionComment, ReadingComment, DiscussionGroup, ReadingGroup


class ReadingCommentForm(forms.ModelForm):
    class Meta:
        model = ReadingComment
        fields = ('body',)


class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ('body',)


class GroupForm(forms.ModelForm):
    class Meta:
        model = ReadingGroup
        fields = ('group_name', 'is_private_group', 'group_image', 'group_description', 'current_book')

