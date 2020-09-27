import requests
from bs4 import BeautifulSoup
import json

from app.settings import HOST
from hashlib import md5

def clean_text(strr: str):
    """
    This will remove spaces...

    """
    return " ".join(strr.split())

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
            .get_text()
    
    origin_author_text = origin_tweet \
        .find("div", {"class": "tweet-text"}) \
            .get_text()

    # Because we are not sure to always have media here
    try:
        origin_media = origin_tweet.find("td", {"class": "tweet-content"}) \
            .find("div", {"class": "media"}).find("img")["src"]
    except Exception as es:
        origin_media = ""

    return {
        "link": url,
        "avatar": origin_avatar,
        "media": origin_media,
        "author-link": clean_text(origin_author_link),
        "author-name": clean_text(origin_author_name),
        "tweet-text": clean_text(origin_author_text),
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
        }).get_text()

    author_link = user_info.find("a")["href"]

    tweet_text = item.find("td", {
        "class": "tweet-content"
    }).find("div", {"class": "tweet-text"}) \
    .get_text()

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
            "author-name": clean_text(author_name),
            "author-link": author_link,
            "tweet-text": clean_text(tweet_text)
        })

    return replies_json


def get_tweet_and_comments(url: str, chat_id:str):
    """
    This method will make the request

    """
    # We make the request
    r = requests.get(HOST + url.split("twitter.com/")[1])

    org_tweet = get_origin_tweet(url, r.content.decode())
    org_hash = md5(json.dumps(org_tweet).encode()).hexdigest()
    # We return results as object
    return {
        "chat-id": chat_id,
        "origin-hash": org_hash,
        "origin": org_tweet,
        "replies": get_replies(r.content.decode()),
    }


def get_ud_id(Ud, result):
    """
    Let's get ObjectId from the origin tweet

    """
    # We fetch the object id
    return str(list(Ud().find_by({
        "origin": result["origin"]
    }))[0]["_id"]).replace("ObjectId(", "").replace(")", "")


def save_watcher(Wm, ud_id, result, chat_id):
    """
    THis method will only save the new watching

    """
    wm = Wm({
        "origin-id": ud_id, 
        "origin-url": result["origin"]["link"], 
        "chat-ids": [chat_id]
    })
    wm.save()


def save_undelete(url, Ud, Wm, chat_id, result, undelete_fetch):
    """
    This method will just save the Undelete using pyMongo

    """
    print("{+} Saving undelete ")
    ud = Ud(result)
    ud.save()

    print("[+] Successfully saved...")

    # We fetch the object id 
    # and we save the WatchMe
    save_watcher(Wm, get_ud_id(Ud, result), result, chat_id)
    
    return {
        "status": "success",
        "message": "{}, your tweet {} is been watching by UnDelete".format(chat_id, url.split("/")[-1])
    }


def append_new_watcher(Ud, Wm, url, result, chat_id, watchme_fetch):
    """
    We append a new watcher or we just don't do it if it's already in the list

    """
    # if NO, we save it
    if len(watchme_fetch) == 0:
        # We fetch the object id
        # and we save the WatchMe
        save_watcher(Wm, get_ud_id(Ud, result), result, chat_id)

        return {
            "status": "success",
            "message": "{}, An entry already exist for this tweet, ".format(chat_id) +
                        "{} is been watching for you !".format(url.split("/")[-1])
        }
    else:
        # let's check if the chat_id is in the array of chat_id
        if chat_id in watchme_fetch[0]["chat-ids"]:
            print("[-] You are already watching this tweet !")

            return {
                "status": "error",
                "message": "{}, An entry allready exist for this UnDelete, ".format(chat_id) +
                            "and you're already watching this tweet !"
            }
        else:
            print("{+} Update watchme_fetch chat-ids ")

            watchme_fetch[0]["chat-ids"].append(chat_id)

            Wm().update({
                "origin-url": result["origin"]["link"]
            }, watchme_fetch[0])

            return {
                "status": "success",
                "message": "{}, An entry allready exist for this tweet, ".format(chat_id) +
                            "now you have been added to the watcher list (" + 
                            str(len(watchme_fetch[0]["chat-ids"])) + ") !"
            }


def remove_new_watcher(Ud, Wm, url, result, chat_id, watchme_fetch):
    """
    We remove a new watcher

    """
    # if NO, we save it
    if len(watchme_fetch) != 0:

        if chat_id in watchme_fetch[0]["chat-ids"]:
            # We fetch the object id
            # and we save the WatchMe
            watchme_fetch[0]["chat-ids"].remove(chat_id)

            Wm().update({
                "origin-url": result["origin"]["link"]
            }, watchme_fetch[0])

            return {
                "status": "success",
                "message": "{}, you have been removed from watcher for this tweet, ".format(chat_id)
            }
        else:
            # not there
            return {
                "status": "success",
                "message": "{}, you're not watching this tweet at the moment, ".format(chat_id)
            }
    else:
        # not there
        return {
            "status": "success",
            "message": "{}, you're not watching this tweet at the moment, ".format(chat_id)
        }


def unwatch(Ud, Wm, url: str, chat_id: str):

    result = get_tweet_and_comments(url, chat_id)

    # we check if that Undelete already exist
    watchme_fetch = list(Wm().find_by({
        "origin-url": result["origin"]["link"]
    }))
    
    return remove_new_watcher(Ud, Wm, url, result, chat_id, watchme_fetch)


def watch_this(Ud, Wm, url: str, chat_id: str):
    """
    Start watching this tweet...

    """
    result = get_tweet_and_comments(url, chat_id)

    # Save on MongoDb
    # we check if that Undelete already exist
    undelete_fetch = list(Ud().find_by({
        "origin": result["origin"]
    }))

    # if NO, we save it
    if len(undelete_fetch) == 0:
        return save_undelete(url, Ud, Wm, chat_id, result, undelete_fetch)
    else:
        print("[x] An entry allready exist for this UnDelete...")
        # if an unDelete allready exist then let's try to save the WatchMe

        # we check if that Undelete already exist
        watchme_fetch = list(Wm().find_by({
            "origin-url": result["origin"]["link"]
        }))

        return append_new_watcher(Ud, Wm, url, result, chat_id, watchme_fetch)

    print("[+] done - - - - - - ")
