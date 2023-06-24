from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.custom import Custom
from urllib.request import urlretrieve
import os

urlretrieve(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/320px-Amazon_logo.svg.png",
    "./Amazon.png",
)
urlretrieve(
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTHgknZg7izLfAmpGQSyD5GY-0MjjH_HBBFaj0l26krkYmAnrQ2XGuvn4zhRnscteTWAA&usqp=CAU",
    "./airflow.png",
)

with Diagram(
    "Amazon.sa Best Sellers Diagram, Built By: Abdulaziz Alharbi", show="false"
):
    with Cluster("Orchestration", direction="TB"):
        airflow = Custom("Airflow", icon_path="./airflow.png")
    with Cluster("ETL", direction="LR"):
        with Cluster("Extract"):
            extract = Custom("Amazon (Scrapping)", "./Amazon.png", width="2")
        with Cluster("Transform"):
            transform = Custom("Python + Pandas", icon_path="./pandasIcon.png")
        with Cluster("Load"):
            load = S3("aws s3 bucket")

            extract - Edge(color="blue") - airflow
            airflow - Edge(color="blue") - [extract >> transform >> load]
