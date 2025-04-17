class s3:
    # def __init__(self, bucket: str, prefix: str = ""):
    #     self.bucket = bucket
    #     self.prefix = prefix

    def S3Resource(self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str = "us-east-1",
    ):
        print("aws_access_key_id", aws_access_key_id)
        print("aws_secret_access_key", aws_secret_access_key)
        return {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "region_name": region_name,
            # "bucket": self.bucket,
            # "prefix": self.prefix,
        }