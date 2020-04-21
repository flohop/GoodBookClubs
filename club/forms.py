from django import forms
from .models import DiscussionComment, ReadingComment, DiscussionGroup, ReadingGroup


class ReadingCommentForm(forms.ModelForm):
    class Meta:
        model = ReadingComment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Add comment'})
        }


class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ('body', )


class GroupForm(forms.ModelForm):
    class Meta:
        model = ReadingGroup
        fields = ('group_name', 'group_image', 'group_description', 'id')
        widget = {'id': forms.HiddenInput()}


