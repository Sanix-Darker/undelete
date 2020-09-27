import requests
from bs4 import BeautifulSoup
import json
from app.settings import HOST


def get_origin_tweet(content: str):
    """
    This method will return the origin information for the tweet

    """
    origin_tweet = BeautifulSoup(content, "html.parser") \
        .find("table", {
            "class": "main-tweet"
        })

    origin_avatar = origin_tweet.find("td", {"class": "avatar"}) \
        .find("img")["src"]
    origin_author = origin_tweet \
        .find("a", {"class": "user-info-username"})

    origin_author_link = origin_author["href"]

    origin_author_name = origin_author \
        .find("span", {"class": "username"}) \
            .get_text().replace("\n", "")
    
    origin_author_text = origin_tweet \
        .find("div", {"class": "tweet-text"}) \
            .get_text().replace("\n", "")

    origin_media = origin_tweet.find("td", {"class": "tweet-content"}) \
        .find("div", {"class": "media"}).find("img")["src"]

    return {
        "avatar": origin_avatar,
        "media": origin_media,
        "author-link": origin_author_link,
        "author-name": origin_author_name,
        "tweet-text": origin_author_text,
    }


def extract_reply_infos(item):
    """
    Just a basic formater for a reply

    """
    link = item["href"]

    avatar = item.find("td", {
        "class": "avatar"
    }).find("img")["src"]

    user_info = item.find("td", {
        "class": "user-info"
    })

    author_name = user_info.find("div", {
        "class": "username"
        }).get_text().replace("\n", "")

    author_link = user_info.find("a")["href"]

    tweet_text = item.find("td", {
        "class": "tweet-content"
    }).find("div", {"class": "tweet-text"}) \
    .get_text().replace("\n", "")

    return link, avatar, author_name, author_link, tweet_text


def get_replies(content: str):
    """
    This method will return replies from that tweet

    """

    replies_json = []

    replies = BeautifulSoup(content, "html.parser") \
        .find("div", {"class": "replies"}) \
        .find_all("table", {
            "class": "tweet"
        })

    for item in replies:
        
        (link, 
        avatar, 
        author_name, 
        author_link, 
        tweet_text) = extract_reply_infos(item)

        replies_json.append({
            "link": link,
            "avatar": avatar,
            "author-name": author_name,
            "author-link": author_link,
            "tweet-text": tweet_text
        })

    return replies_json


def get_tweet_and_comments(url: str, chat_id:str):
    """
    This method will make the request

    """
    # We make the request
    r = requests.get(HOST + url.split("twitter.com/")[1])
    
    # with open("rf.html", "w") as ffr:
    #     ffr.write(r.content.decode())

    # We return results as object
    return {
        "chat_id": chat_id,
        "origin": get_origin_tweet(r.content.decode()),
        "replies": get_replies(r.content.decode()),
    }

def watch_this(url: str, chat_id: str):
    """
    Start watching this...

    """

    # with open("s.json", "w", encoding='utf-8') as frr:
    #     json.dump(
    #         get_tweet_and_comments(url, chat_id), 
    #         frr, 
    #         ensure_ascii=False, 
    #         indent=4
    #     )

    get_tweet_and_comments(url, chat_id)
    
    print("[+] done - - - - - - ")
