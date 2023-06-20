import requests  ## don't use as it does not get you all the elements of the scrapped html
import httpx  ## better alternative to requests library for this project
from bs4 import BeautifulSoup
import numpy as np


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept-Language": "en-US, en:q=0.5",
}

base_url = (
    "https://www.amazon.sa/-/en/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2"
)


def amazonScrapper():

    response = httpx.get(
        base_url
    )  # because requests.get() does not get all the html elements such as price, while httpx was able to

    soup = BeautifulSoup(response.text, "html.parser")
    products_Categories = soup.find_all("h2", attrs={"class": "a-carousel-heading"})

    arrayOfCategories = []

    for category in products_Categories:
        arrayOfCategories.append(category.text.replace("Best Sellers in ", ""))

    products_container = soup.find_all("li", attrs={"class": "a-carousel-card"})

    arrayOfCategories = list(np.repeat(arrayOfCategories, 6))

    arrayOfProductsInfo = []

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
            product_Url = f'https://www.amazon.sa{product.find("a", attrs={"class": "a-link-normal"})["href"]}'
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
    # dtypes dict was not used due to an unknown error
    dtypes = {
        "Category": str,
        "Category_Rank": str,
        "Name": str,
        "Brand": str,
        "Rate_Out_Of_5.0": float,
        "Number_Of_Reviews": int,
        "Price_In_SAR": float,
        "Product_Url": str,
    }

    return arrayOfProductsInfo
