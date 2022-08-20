from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['customer_id', 'product_id', 'rate', 'text', 'image']
        widgets = {
            "customer_id" : forms.HiddenInput(),
            "product_id" : forms.HiddenInput(),
            "rate" : forms.NumberInput(attrs={'min':1,'max':5,'value':3})
        }   
        
