from django import forms


class GrammarForm(forms.Form):
    password = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "Need a secret word :D"}))
    text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
                                 attrs={'class': 'grammar form-control', 'placeholder': "Limit 10,000 chars. "
                                                                                            "Required"}))