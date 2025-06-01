# in clients/forms.py (the new file)

from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        # We list the fields in the order we want them to appear
        fields = [
            # "Line 1" fields
            'case',
            'entry_date',
            'form_type',
            'i765_category',
            # "Line 2" fields
            'receipt_number',
            'received_date',
            'processing_center',
        ]

        # This allows us to add helpful widgets, like a date picker for date fields
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
            'received_date': forms.DateInput(attrs={'type': 'date'}),
        }