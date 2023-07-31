from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Booking
from django.utils import timezone

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
