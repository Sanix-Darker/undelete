import requests
from bs4 import BeautifulSoup
import json

from app.model import UnDelete , WatchMe
from app.settings import HOST


def get_origin_tweet(url: str, content: str):
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
        "link": url,
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

    # We return results as object
    return {
        "chat_id": chat_id,
        "origin": get_origin_tweet(url, r.content.decode()),
        "replies": get_replies(r.content.decode()),
    }


def watch_this(url: str, chat_id: str):
    """
    Start watching this...

    """

    result = get_tweet_and_comments(url, chat_id)

    Ud = UnDelete.UnDelete
    Wm = WatchMe.WatchMe

    # Save on MongoDb
    # we check if that Undelete already exist
    undelete_fetch = list(Ud().find_by({
        "origin": result["origin"]
    }))

    # if NO, we save it
    if len(undelete_fetch) == 0:
        print("{+} Saving undelete_fetch: ", undelete_fetch)
        ud = Ud(result)
        ud.save()

        print("[+] Successfully saved...")

        # We fetch the object id
        ud_id = str(list(Ud().find_by({
            "origin": result["origin"]
        }))[0]["_id"]).replace("ObjectId(", "").replace(")", "")

        # and we save the WatchMe
        wm = Wm({
            "origin_id": ud_id, 
            "origin_url": result["origin"]["link"], 
            "chat_ids": [chat_id]
        })
        wm.save()

        return {
            "status": "success",
            "message": "{}, your tweet {} is been watching by UnDelete".format(chat_id, url.split("/")[-1])
        }
    else:
        print("[x] An entry allready exist for this UnDelete...")
        # if an unDelete allready exist then let's try to save the WatchMe

        # we check if that Undelete already exist
        watchme_fetch = list(Wm().find_by({
            "origin_url": result["origin"]["link"]
        }))

        # if NO, we save it
        if len(watchme_fetch) == 0:
            wm = Wm({
                "origin_id": ud_id, 
                "origin_url": result["origin"]["link"], 
                "chat_ids": [chat_id]
            })
            wm.save()

            return {
                "status": "success",
                "message": "{}, An entry already exist for this tweet, \
                            {} is been watching for you !".format(chat_id, url.split("/")[-1])
            }
        else:
            # let's check if the chat_id is in the array of chat_id
            if chat_id in watchme_fetch[0]["chat_ids"]:
                print("[-] You are already watching this tweet !")
                return {
                    "status": "error",
                    "message": "{}, An entry allready exist for this UnDelete, \
                                and you're already watching this tweet !".format(chat_id)
                }
            else:
                watchme_fetch[0]["chat_ids"].append(chat_id)

                print("{+} Update watchme_fetch chat-ids ")

                Wm().update({
                    "origin_url": result["origin"]["link"]
                }, watchme_fetch[0])

                return {
                    "status": "success",
                    "message": "{}, An entry allready exist for this tweet, \
                                now you have been added to the watcher list (" + 
                                len(watchme_fetch[0]["chat_ids"]) + ") !".format(chat_id)
                }

                print("[-] Saved as watcher now !")

    print("[+] done - - - - - - ")
