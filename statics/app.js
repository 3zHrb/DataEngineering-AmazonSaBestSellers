// // import axios from 'axios';
// import axios from 'axios';
// var axios = require('axios');
// const jsdom = require('jsdom');
// const { JSDOM } = jsdom;
// import axios from 'axios';

function getBestSellers() {
    console.log('getBestSeller Is Triggered');
    var bestProducts = amazonScrapper();
    console.log(bestProducts);
};

function amazonScrapper() {

    var amazonUrl = "https://www.amazon.sa/-/en/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2"
    var document_string = '';

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







    //     $.ajax({
    //         url: 'http://127.0.0.1:5000/getAmazonBestSellers',
    //         method: 'GET',
    //         success: function (data) {
    //             document_string = data;
    //         },
    //         error: function (error) {
    //             console.log(error);
    //         }
    //     })

    //     htmlParser(document_string);

};

function htmlParser(htmlContent) {


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

};

//     axios.get(amazonUrl).then(response => {
//         var htmlContent = response.data;
//         var dom = new JSDOM(htmlContent);

//         var doc = dom.window.document;

//         var products = doc.querySelectorAll('[class="p13n-sc-uncoverable-faceout"]')

//         var arrayOfProducts = []

//         for (i = 0; i < products.length; i++) {

//             var product_Name = products[i].querySelector('.p13n-sc-truncate-desktop-type2')?.textContent;
//             var product_SellerBrand = products[i].querySelector('._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')?.textContent ?? 'Not A Brand';
//             var product_StarsRate = products[i].querySelector('.a-icon-alt')?.textContent.split(' ')[0] ?? 'Not Rated';
//             var product_ReviewsNum = products[i].querySelector('span.a-size-small:not(.a-color-base)')?.textContent ?? 'Not Rated';
//             var product_Price = products[i].querySelector('span._cDEzb_p13n-sc-price_3mJ9Z')?.textContent

//             var product_info = {
//                 'product_Name': product_Name,
//                 'product_SellerBrand': product_SellerBrand,
//                 'product_StarsRate': parseFloat(product_StarsRate),
//                 'product_ReviewsNum': parseInt(product_ReviewsNum.replace(',', '')),
//                 'product_Price': parseFloat(product_Price.replace('SAR', '').trim())
//             }

//             arrayOfProducts.push(product_info);
//         }


//     }).catch(error => {
//         console.log(error)
//     })

//     return arrayOfProducts;
// };