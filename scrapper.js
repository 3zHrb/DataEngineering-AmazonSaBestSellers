// Note: This file is not needed, since we sis the scrapping using python Beautiful Soup
// But is kept to show you how to do the same thing in Javascript

const axios = require('axios');
const { response } = require('express');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fetch = require("node-fetch");
const cheerio = require('cheerio');


function amazonScrapper() {

    var amazonUrl = "https://www.amazon.sa/-/en/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2"

    axios.get(amazonUrl).then(response => {
        var htmlContent = response.data;
        var dom = new JSDOM(htmlContent);

        var doc = dom.window.document;

        var products = doc.querySelectorAll('[class="p13n-sc-uncoverable-faceout"]')

        var arrayOfProducts = []


        console.log(products.length)
        for (i = 0; i < products.length; i++) {

            var product_Name = products[i].querySelector('.p13n-sc-truncate-desktop-type2')?.textContent;
            var product_SellerBrand = products[i].querySelector('._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')?.textContent ?? 'Not A Brand';
            var product_StarsRate = products[i].querySelector('.a-icon-alt')?.textContent.split(' ')[0] ?? 'Not Rated';
            var product_ReviewsNum = products[i].querySelector('span.a-size-small:not(.a-color-base)')?.textContent ?? 'Not Rated';
            var product_Price = products[i].querySelector('span._cDEzb_p13n-sc-price_3mJ9Z')?.textContent

            // some elements in the python scrapper is not included here, but you can include them following the same scrapping
            var product_info = {
                'product_Name': product_Name,
                'product_SellerBrand': product_SellerBrand,
                'product_StarsRate': parseFloat(product_StarsRate),
                'product_ReviewsNum': parseInt(product_ReviewsNum.replace(',', '')),
                'product_Price': parseFloat(product_Price.replace('SAR', '').trim())
            }

            arrayOfProducts.push(product_info);
        }

        console.log(arrayOfProducts);

    }).catch(error => {
        console.log(error)
    })

};