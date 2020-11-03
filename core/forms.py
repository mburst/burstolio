from django import forms
from core.models import Entry
    
class Alert(forms.Form):
    entry = forms.ModelChoiceField(queryset=Entry.objects.all())
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': '65', 'rows': '6'}))
    email = forms.BooleanField(required=False, label='Send Subscribers E-Mail')