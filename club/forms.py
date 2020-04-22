from django import forms
from .models import DiscussionComment, ReadingComment, DiscussionGroup, ReadingGroup
from ajaximage.widgets import AjaxImageWidget


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
    group_image = forms.URLField(widget=AjaxImageWidget(upload_to='images/group_pictures'))

    class Meta:
        model = ReadingGroup
        fields = ('group_name', 'group_description', 'id')
        widget = {'id': forms.HiddenInput()}



