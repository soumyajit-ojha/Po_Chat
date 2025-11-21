from django import forms
from .models import Message

class PrivateChatMessaageForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Message
        fields = ["content"]  # Ensure content is included
