from django import forms
from .models import Comment, Post
from django.contrib.auth import get_user_model
from jalali_date.fields import SplitJalaliDateTimeField
from jalali_date.widgets import AdminSplitJalaliDateTime
from django.utils.safestring import mark_safe
from blog.widgets import CustomMedia, TinyMceWidget
import jdatetime
from django.utils.timezone import localtime
User = get_user_model()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'author',
            'email',
            'text'
        ]


class PostShareForm(forms.Form):
    name = forms.CharField(label="نام فرستنده")
    from_email = forms.EmailField(label='ایمیل فرستنده')
    to_email = forms.EmailField(label='ایمیل گیرنده')
    extra_explanation = forms.CharField(
        widget=forms.Textarea,
        label="توضیحات اضافه",
        required=False
    )


class PostEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.fields['publish'] = SplitJalaliDateTimeField(
            widget=AdminSplitJalaliDateTime(),
        )

    body = forms.CharField(
        widget=TinyMceWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = "__all__"


class AdminPostEditForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMceWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = "__all__"
