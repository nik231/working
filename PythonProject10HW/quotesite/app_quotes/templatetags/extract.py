from django import template
from bson.objectid import ObjectId

from ..utils import get_mongodb

register = template.Library()

def get_author(id_):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    return author['fullname']

register.filter('author', get_author)

def tags(note_tags):
    return ', '.join([str(name) for name in note_tags.all()])


register.filter('tags', tags)