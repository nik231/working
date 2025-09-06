import json
import sys
import aiohttp
import asyncio
import platform
from datetime import datetime, timedelta




class HTTPError(Exception):
    pass

def pretty_view(cur: list, currencies: list):
    usd_eur = []
    for el in cur:
        string = el
        date = string["date"]
        exchange = string["exchangeRate"]
        rate_dict = {}
        for tp in exchange:
            currency_code = tp["currency"]
            if currency_code in currencies:
                sale = tp["saleRateNB"]
                purchase = tp["purchaseRateNB"]
                ex = {"sale": sale, "purchase": purchase}
                cur = {tp["currency"]: ex}
                rate_dict.update(cur)
            else:
                continue
        pre_view = {date:rate_dict}
        usd_eur.append(pre_view)
    return usd_eur

async def request(url:str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HTTPError(f"Error status: {resp.status} for {url}")
        except(aiohttp.ClientConnectionError, aiohttp.InvalidURL) as err:
            raise HTTPError(f"Connection error: {url}", str(err))

async def main(arg=1, arg2=None):
    try:
        currencies = ["USD", "EUR"] + arg2
    except TypeError:
        currencies = ["USD", "EUR"]
    list_of_json = []
    if int(arg) < 10:
        for i in range(int(arg)):

            date1 = datetime.now() - timedelta(days=i)
            sub_for_url = datetime.strftime(date1, "%d.%m.%Y")
            try:
                response = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={sub_for_url}")
                list_of_json.append(response)
            except HTTPError as err:
                print(err)
                return None
        final_view = pretty_view(list_of_json, currencies)
        return final_view
    else:
        raise ValueError(f"Days argument {arg} must be less than 10")

if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(sys.argv[1], sys.argv[2:]))
    print(r)