from django import forms


class ChatForm(forms.Form):
    password = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "Need a secret word :D"}))
    message = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(
                                 attrs={'class': 'message form-control', 'placeholder': "Limit 1000 chars. "
                                                                                            "Required"}))