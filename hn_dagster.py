from hackernews import extract,transform,load
from dagster import asset

@asset
def hackernews_wordcloud():
    # raise RuntimeError("it fail")
    input=extract()
    output=transform(input)
    load(output)
