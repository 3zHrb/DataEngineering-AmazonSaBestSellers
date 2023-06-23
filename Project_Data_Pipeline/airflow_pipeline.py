import extract
import transform
import load

url = (
    base_url
) = "https://www.amazon.sa/-/en/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2"


def runPipeline():
    responseText = extract.getBestSellersHtml(url)
    df = transform.transformSellerInfo(responseText)
    load.loadToCloudStorage(df)


runPipeline()
