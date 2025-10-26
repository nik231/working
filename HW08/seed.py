import json

from models import Author, Quote
from mongoengine.errors import NotUniqueError

if __name__ == "__main__":
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError as err:
                print("Author already exists")

    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author = Author.objects.get(fullname=el.get('author'))
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()