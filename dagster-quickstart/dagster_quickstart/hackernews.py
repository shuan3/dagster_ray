import base64
from io import BytesIO
# import matpolotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import requests
from wordcloud import STOPWORDS,wordcloud
from tqdm import tqdm

def extract()->pd.DataFrame:
    newstories_url="https://hacker-news.firebaseio.com/v0/topstories.json"
    hackernews_topstory_ids=requests.get(newstories_url).json()
    results=[]
    for item_id in tqdm(hackernews_topstory_ids):
        item=requests.get(f"https://hacker-news.firebaseio.com/v0//item/{item_id}.json")
        results.append(item)
    hackernews_topstories=pd.DataFrame(results)
    return hackernews_topstories

def transform(hackernews_topstories: pd.DataFrame)->bytes:
    stopwords=set(STOPWORDS)
    stopwords.update(["Ask","Show","HN"])
    titles_text="".join(str(item) for item in hackernews_topstories["title"])
    titles_cloud=wordcloud(stopwords=stopwords, backgroud_color="white").generate(titles_text)
    plt.fiture(figsize=(8,8),facecolor=None)
    plt.imshow(titles_cloud,interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)

    buffer=BytesIO()
    plt.sacefig(buffer,format="png")
    image_data=base64.b64encode(buffer.getvalue())
    return f"""![img](data(imgge/png;base64,{image_data.decode()}))""".strip()()

def load(md_content:str):
    with open("output.md","w") as f:
        f.write(md_content)
if __name__=="__main__":
    input=extract()
    output=transform(input)
    load(output)


# lol=extract()
# print(lol)