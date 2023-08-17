import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Booking, Rating, Reply
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class TourSearchForm(forms.Form):
    query = forms.CharField(label=_('key search'), max_length=100, required=False)
    min_price = forms.DecimalField(label=_('Minimum Price'), min_value=0, required=False)
    max_price = forms.DecimalField(label=_('Maximum Price'), min_value=0, required=False)
    start_date = forms.DateField(label=_('Start day'), required=False)
    end_date = forms.DateField(label=_('End day'), required=False)
    location = forms.CharField(label=_('Address'), max_length=100, required=False)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_people', 'departure_date', 'end_date']  
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_departure_date(self):
        departure_date = self.cleaned_data['departure_date']
        current_date = timezone.localtime(timezone.now()).date()

        if departure_date <= current_date:
            raise forms.ValidationError("Ngày khởi hành phải lớn hơn ngày hiện tại.")
        
        return departure_date

class RatingForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Text goes here!!!','rows':'3','cols':'20'}))
    rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        label='Rating',
        help_text='Choose a rating from 1 to 5.'
    )

    class Meta:
        model = Rating
        fields = ['rating', 'content']

class ReplyForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Text goes here!!!','rows':'2','cols':'20'}))
    class Meta:
        model = Reply
        fields = ['content'] 


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("Mật khẩu phải có ít nhất 8 ký tự.")
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9\W]', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất 3 loại ký tự: chữ thường, viết hoa, số, và ký tự đặc biệt.")
        return password
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class FavoriteTourForm(forms.Form):
    pass

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CustomUserChangeForm(UserChangeForm):

    current_password = forms.CharField(
        label="Current Password", widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label="New Password", widget=forms.PasswordInput, min_length=8, required=False
    )
    new_password2 = forms.CharField(
        label="Confirm New Password", widget=forms.PasswordInput, min_length=8, required=False
    )

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.instance.user.check_password(current_password):
            raise forms.ValidationError("Incorrect current password.")
        return current_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("New passwords must match.")
        return new_password2

    def save(self, commit=True):
        user = self.instance.user
        new_password1 = self.cleaned_data.get("new_password1")
        if new_password1:
            user.set_password(new_password1)
        user.username = self.cleaned_data.get("username")
        if commit:
            user.save()
        return user
