from django import forms
from django.contrib.auth.models import User
from models import Page, Category, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Link the CategoryForm to the Category model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the page's URL.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If the url is nonempty and doesn't start with 'http://', add 'http://'
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        # Link the PageForm to the Page model
        model = Page

        # Hide category's foreign key
        exclude = ('category',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
