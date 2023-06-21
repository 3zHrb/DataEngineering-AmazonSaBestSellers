import requests  ## don't use as it does not get you all the elements of the scrapped html
import httpx  ## better alternative to requests library for this project


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept-Language": "en-US, en:q=0.5",
}


def getBestSellersHtml(base_url):

    response = httpx.get(base_url)

    return response.text
