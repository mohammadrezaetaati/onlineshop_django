from django import forms

class SearchProductForm(forms.Form):

    search=forms.CharField(max_length=100)