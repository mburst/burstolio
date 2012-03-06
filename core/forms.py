from django import forms
from core.models import Comment, Entry

class CommentForm(forms.ModelForm):
    ancestor = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'ancestor'}), required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': '65', 'rows': '6'}))
    
    class Meta:
        model = Comment
        fields = ('name', 'website', 'content',)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    cc_myself = forms.BooleanField(required=False, label='CC Myself')
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': '65', 'rows': '6'}))
    
class Alert(forms.Form):
    entry = forms.ModelChoiceField(queryset=Entry.objects.all())
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': '65', 'rows': '6'}))
    email = forms.BooleanField(required=False, label='Send Subscribers E-Mail')