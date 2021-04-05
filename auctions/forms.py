from django import forms
from .models import Category
class NewListing(forms.Form):
    categories = list(Category.objects.values_list('id', 'name'))
    title = forms.CharField(label = "Title", max_length = 100, required = True)
    start_bid = forms.DecimalField(label = "Starting Bid", decimal_places = 2, required = True, widget = forms.NumberInput(attrs={'placeholder': '0.00'}))
    category = forms.ChoiceField(widget = forms.Select, choices = categories, label = "Category")
    description = forms.CharField(widget = forms.Textarea, label = "Description of the Item")
    url = forms.URLField(required = False, label = "URL link to an image of the item")


class NewBid(forms.Form):
    bid = forms.DecimalField(label = "Your Bid", decimal_places=2) 
    def __init__(self, *args, **kwargs):
        try:
            current_min = kwargs.pop('current_min')
        except KeyError:
            current_min = 0
        super(NewBid, self).__init__(*args, **kwargs)
        self.fields['bid'].widget.attrs['min'] = "{:.2f}".format(current_min)
        self.fields['bid'].widget.attrs['placeholder'] = "{:.2f}".format(current_min)
class NewComment(forms.Form):
    text = forms.CharField(label = "Your comment", widget = forms.Textarea(attrs={"rows":3, "cols":30, "placeholder": "Write your comment here."}), max_length = 200)
