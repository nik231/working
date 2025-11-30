from django.forms import ModelForm, CharField, TextInput, JSONField, DateField, DateInput, ModelChoiceField, Select

from .models import Quote, Author


class QuoteForm(ModelForm):
    author = ModelChoiceField(
        queryset=Author.objects.all(),
        widget=Select(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}),
        empty_label="Select an author"
    )
    tags = CharField(
        widget=TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1', 'placeholder': 'Enter tags separated by commas (e.g., wisdom, life, inspiration)'}))
    quote = CharField(min_length=5,
                      widget=TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))

    # path = ImageField(widget=FileInput(attrs={'class': 'form-control', 'id': 'formFile', 'accept': 'image/*'    }))

    class Meta:
        model = Quote
        fields = ['author', 'tags', 'quote']

    def clean_tags(self):
        """Convert comma-separated tags to a list"""
        tags_input = self.cleaned_data.get('tags', '')

        if not tags_input or tags_input.strip() == '':
            return []

        # Split by comma and clean up whitespace
        tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        return tags_list

class AuthorForm(ModelForm):
    fullname = CharField(max_length=300, min_length=5,
                       widget=TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))
    born_date = DateField(widget=DateInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))
    born_location = CharField(max_length=300, min_length=5,
                      widget=TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))
    description = CharField(min_length=5,
                              widget=TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))

    # path = ImageField(widget=FileInput(attrs={'class': 'form-control', 'id': 'formFile', 'accept': 'image/*'    }))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
