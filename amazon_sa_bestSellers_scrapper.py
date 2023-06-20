import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import numpy as np
from parsel import Selector
from selectolax.parser import HTMLParser

import httpx


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept-Language": "en-US, en:q=0.5",
}

search_query = ""
base_url = (
    "https://www.amazon.sa/-/en/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2"
)


def amazonScrapper():
    # response = requests.get(base_url, headers)
    # html = HTMLParser(response.text)
    # data = html.css("div.p13n-sc-uncoverable-faceout")

    # for item in data:
    #     print(item.css("span")[-1].text())

    # products = html.css("p13n-sc-uncoverable-faceout")

    # for product in products:
    #     print(product.text())

    response = httpx.get(
        base_url
    )  # because requests.get() does not get all the html elements such as price, while httpx was able to

    soup = BeautifulSoup(response.text, "html.parser")
    products_Categories = soup.find_all("h2", attrs={"class": "a-carousel-heading"})

    arrayOfCategories = []

    for category in products_Categories:
        arrayOfCategories.append(category.text.replace("Best Sellers in ", ""))

    # products_container = soup.find_all(
    #     "div", attrs={"class": "zg-carousel-general-faceout"}
    # )

    products_container = soup.find_all("li", attrs={"class": "a-carousel-card"})

    arrayOfCategories = list(np.repeat(arrayOfCategories, 6))

    arrayOfProductsInfo = []

    print(len(products_container))
    for i, product in enumerate(products_container):

        try:
            product_rank = product.find("span", attrs={"class": "zg-bdg-text"}).text
        except:
            product_rank = np.nan
        try:
            product_Name = product.find(
                "div", attrs={"class": "p13n-sc-truncate-desktop-type2"}
            ).text
        except:
            product_Name = np.nan

        try:
            product_SellerBrand = product.find(
                "div", attrs={"class": "_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"}
            ).text
        except:
            product_SellerBrand = np.nan

        try:
            product_StartsRate = product.find(
                "span", attrs={"class": "a-icon-alt"}
            ).text.split(" ")[0]
        except:
            product_StartsRate = np.nan

        try:
            # product_ReviewsNum = product.find(
            #     "span", attrs={"class": "a-size-small"}
            # ).text
            product_ReviewsNum = int(
                product.select_one("span.a-size-small:not(.a-color-base)").text.replace(
                    ",", ""
                )
            )
        except:
            product_ReviewsNum = np.nan

        try:
            product_PriceSAR = float(
                product.find("span", attrs={"class": "a-size-base"})
                .text.replace("SAR", "")
                .replace(",", "")
                .strip()
            )
        except:
            product_PriceSAR = np.nan

        try:
            product_Url = f'amazon.sa{product.find("a", attrs={"class": "a-link-normal"})["href"]}'
        except:
            product_Url = np.nan

        dict_product_info = {
            "Category": arrayOfCategories[i],
            "Category_Rank": product_rank,
            "Name": product_Name,
            "Brand": product_SellerBrand,
            "Rate_Out_Of_5.0": product_StartsRate,
            "Number_Of_Reviews": product_ReviewsNum,
            "Price_In_SAR": product_PriceSAR,
            "Product_Url": product_Url,
        }

        arrayOfProductsInfo.append(dict_product_info)

    print(arrayOfProductsInfo)
    # categories = soup.find_all("h2", {"class": "a-carousel-heading"})
    # products_titles = soup.find_all(
    #     "div", attrs={"class": "p13n-sc-truncate-desktop-type2"}
    # )
    # startsRate = soup.find_all("span", attrs={"class": "a-icon-alt"})  # need fix
    # reviews_num = soup.find_all("span", attrs={"class": "a-size-small"})

    # print(len(products_titles))
    # for i in range(0, len(categories)):
    #     print(str(categories[i].text).replace("Best Sellers in ", ""))
    # print(len(reviews_num))
    # for i in range(0, len(reviews_num)):
    #     print(reviews_num[i].text)

    # product_container = soup.find_all(
    #     "div", attrs={"class": "p13n-sc-uncoverable-faceout"}
    # )

    arrayOfProducts = []

    # print(len(product_container))
    # for i in range(0, len(product_container)):
    #     print("=======================================================")
    #     # product_Name = product_container[i].find(
    #     #     "div", attrs={"class": "p13n-sc-truncate-desktop-type2"}
    #     # )
    #     # product_StartsRate = product_container[i].find(
    #     #     "span", attrs={"class": "a-icon-alt"}
    #     # )
    #     # product_ReviewsNum = product_container[i].find(
    #     #     "span", attrs={"class": "a-size-small"}
    #     # )
    #     # product_SellerBrand = product_container[i].find(
    #     #     "div", attrs={"class": "_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"}
    #     # )
    #     product_PriceSAR = product_container[i].find(
    #         "span", attrs={"class": "a-size-base"}
    #     )

    #     print(product_PriceSAR)

    # print(product_container[i].text)

    # print(f"Name: {'Null' if product_Name.text is None else product_Name.text}")
    # print(
    #     f"StartsRate: {'Null' if product_StartsRate.text is None else product_StartsRate.text}"
    # )
    # print(
    #     f"Review Num: {'Null' if product_ReviewsNum.text is None else product_ReviewsNum.text}"
    # )
    # print(
    #     f"Seller Brand: {'Null' if product_SellerBrand.text is None else product_SellerBrand.text}"
    # )
    # print(
    #     f"Price: {'Null' if product_PriceSAR.text is None else product_PriceSAR.text}"
    # )

    # product_info_dict = {
    #     "product_Name": product_Name.text if product_Name.text else np.nan,
    #     "product_StartsRate": product_StartsRate.text
    #     if product_StartsRate.text
    #     else np.nan,
    #     "product_ReviewsNum": product_ReviewsNum.text
    #     if product_ReviewsNum.text
    #     else np.nan,
    #     "product_SellerBrand": product_SellerBrand.text
    #     if product_SellerBrand.text
    #     else np.nan,
    #     "product_PriceSAR": product_PriceSAR.text
    #     if product_PriceSAR.text
    #     else np.nan,
    # }
    # print(product_info_dict)


amazonScrapper()
