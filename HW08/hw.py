import redis
from redis_lru import RedisLRU
import sys
import json

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)
r = redis.Redis(host='localhost', port=6379, db=0)


# @cache
def find_by_tag(tag: str) -> list[str | None]:
    cache_key = f"tag:{tag}"
    cached_result = r.get(cache_key)
    if cached_result:
        print("Взято з кешу")
        return json.loads(cached_result)

    quotes = Quote.objects(tags__iregex=tag)
    result = [quote.quote for quote in quotes]
    r.set(cache_key, json.dumps(result))
    return result


@cache
def find_by_tags(tags: str) -> list[str | None]:
    individual_tags = tags.split(',')
    result = []
    for el in individual_tags:
        quotes = Quote.objects(tags__iregex=str(el))
        [result.append(quote.quote) for quote in quotes]
    return result


# @cache
def find_by_author(author: str) -> dict | list[str | None | list]:
    cache_key = f"author:{author}"
    cached_result = r.get(cache_key)
    if cached_result:
        print("Getting from cache")
        return json.loads(cached_result)

    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    r.set(cache_key, json.dumps(result))
    return result


def main():
    while True:
        string = input("Enter the query in the following format 'command:value'")
        try:
            command, value = string.split(':')
            match command:
                case "tag":
                    print(find_by_tag(str(value)))
                    continue
                case "tags":
                    print(find_by_tags(str(value)))
                    continue
                case "name":
                    print(find_by_author(str(value)))
                    continue
                case _:
                    print("Incorrect command or format entered")
                    continue
        except ValueError:
            if string == "exit":
                sys.exit(0)
            else:
                print("Incorrect command or format entered")
                continue


if __name__ == "__main__":
    main()
