from pathlib import Path
from datetime import datetime

from bson import ObjectId
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator

from .forms import QuoteForm, AuthorForm
from .models import Quote, Author
from.utils import get_mongodb
# Create your views here.

def main(request):
    db = get_mongodb()
    quotes = db.quotes.find()
    return render(request, 'app_quotes/quotes.html', context={'quotes':quotes})

def home(request):
    return render(request,'app_quotes/home.html', context={"msg":"Hello stranger!"})


def quotes(request, page=1):
    db = get_mongodb()
    quotes_cursor = db.quotes.find()
    quotes_list = []
    per_page = 10

    for quote in quotes_cursor:
        author = db.authors.find_one({'_id': quote['author']})
        quote['author_name'] = author['fullname'] if author else 'Unknown'
        quotes_list.append(quote)
    paginator = Paginator(quotes_list, per_page)
    quotes_on_page = paginator.page(page)

    return render(request, 'app_quotes/quotes.html', context={"quotes": quotes_on_page})


def authors(request, page=1):
    db =  get_mongodb()
    authors = list(db.authors.find())
    per_page = 10
    paginator = Paginator(authors, per_page)
    authors_on_page = paginator.page(page)
    return render(request,'app_quotes/authors.html', context={"authors":authors_on_page})


@login_required
def upload_quote(request):
    db = get_mongodb()
    authors_cursor = db.authors.find()
    
    # Transform MongoDB documents to remove underscore prefix from _id
    authors_list = []
    for author in authors_cursor:
        authors_list.append({
            'id': str(author['_id']),  # Convert ObjectId to string and rename
            'fullname': author.get('fullname', 'Unknown')
        })
    
    if request.method == 'POST':
        quote_text = request.POST.get('quote', '').strip()
        author_id = request.POST.get('author', '').strip()
        tags_input = request.POST.get('tags', '').strip()

        # Parse tags (comma-separated)
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        if quote_text and author_id:
            try:
                db.quotes.insert_one({
                    'quote': quote_text,
                    'tags': tags,
                    'author': ObjectId(author_id)
                })
                return redirect(to="app_quotes:quotes")
            except Exception as e:
                error_message = f"Error saving quote: {str(e)}"
                return render(request, 'app_quotes/upload_quote.html',
                              context={"authors": authors_list, "error": error_message})
        else:
            error_message = "Quote text and author are required."
            return render(request, 'app_quotes/upload_quote.html',
                          context={"authors": authors_list, "error": error_message})

    return render(request, 'app_quotes/upload_quote.html', context={"authors": authors_list})


@login_required
def upload_author(request):
    db = get_mongodb()

    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        born_date = request.POST.get('born_date', '').strip()
        born_location = request.POST.get('born_location', '').strip()
        description = request.POST.get('description', '').strip()

        if fullname and born_date and born_location and description:
            try:
                # Convert date string to datetime object
                born_date_obj = datetime.strptime(born_date, '%Y-%m-%d')

                db.authors.insert_one({
                    'fullname': fullname,
                    'born_date': born_date_obj,
                    'born_location': born_location,
                    'description': description
                })
                return redirect(to="app_quotes:authors")
            except ValueError:
                error_message = "Invalid date format. Use YYYY-MM-DD."
                return render(request, 'app_quotes/upload_author.html',
                              context={"error": error_message})
            except Exception as e:
                error_message = f"Error saving author: {str(e)}"
                return render(request, 'app_quotes/upload_author.html',
                              context={"error": error_message})
        else:
            error_message = "All fields are required."
            return render(request, 'app_quotes/upload_author.html',
                          context={"error": error_message})

    return render(request, 'app_quotes/upload_author.html')
