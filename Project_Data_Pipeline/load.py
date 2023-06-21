import boto3
import os
import datetime


s3 = boto3.resource(
    service_name="s3",
    region_name="us-west-2",
    aws_access_key_id=os.environ.get("aws_access_key_id"),
    aws_secret_access_key=os.environ.get("aws_secret_access_key"),
)

currentPath = os.getcwd()


def loadToCloudStorage(df):

    now = datetime.datetime.now()

    df.to_csv("amazonSa_BestSellers{}.csv".format(now))

    s3.Bucket("amazon-best-sellers-bucket").upload_file(
        Filename="amazonSa_BestSellers{}.csv".format(now),
        Key="amazonSa_BestSellers{}.csv".format(now),
    )
    os.remove(f"{currentPath}/amazonSa_BestSellers{now}.csv")

    return "Loading Succeed"
