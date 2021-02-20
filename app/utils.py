import requests
import json
from os import system

from bot.settings import TOKEN
from app.settings import BEARER_TOKEN, CSRF_TOKEN, cookies, queue_reply_url
from hashlib import md5


def send_message(chat_id: str, text: str):
    """
    This method will just send a message to the appropriate client

    """
    datas = {
        "chat_id": chat_id,
        "text": text,
    }
    r = requests.post(
        "https://api.telegram.org/bot" + TOKEN + "/sendMessage",
        data=datas
    )

    return True if r.status_code == 200 else False


def dump_tweet_link_validation(url):
    """
    This is a dump check for a valid tweet link lol...

    """

    if "twitter.com" in url and "status" in url:
        # We check if it's a valid link pingable lol
        r = requests.get(url)
        if r.status_code == 200 or r.status_code == 400:
            return True
        else:
            return False
    else:
        return False


def clean_text(strr: str):
    """
    This will remove spaces...

    """
    return " ".join(strr.split())


def get_origin_tweet(tweet_id):
    """
    This method will return the origin information for the tweet

    """

    headers = {'Authorization': 'Bearer ' + BEARER_TOKEN}
    api_url = "https://api.twitter.com/1.1/statuses/show.json?id=" + tweet_id
    response = requests.get(api_url, headers=headers)
    results = response.json()

    return {
        "avatar": results["user"]["profile_image_url_https"],
        "media": "",
        "author-link": "https://twitter.com/" + results["user"]["screen_name"],
        "author-name": results["user"]["name"],
        "link": "https://twitter.com/" + results["user"]["screen_name"] + "/" + tweet_id,
        "tweet-text": results["text"]
    }


def get_replies(tweet_id):
    """
    This method will return replies from that tweet

    """
    command = "curl -s 'https://twitter.com/i/api/2/timeline/conversation/" + tweet_id + ".json?" \
              + queue_reply_url \
              + "   -H 'authority: twitter.com'   -H 'authorization: Bearer " + BEARER_TOKEN \
              + "'   -H 'x-twitter-client-language: en'   -H 'x-csrf-token: " + CSRF_TOKEN \
              + "'   -H 'x-twitter-auth-type: OAuth2Session'   -H 'x-twitter-active-user: yes'" \
              + "   -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" \
              + " Chrome/88.0.4324.150 Safari/537.36'   -H 'accept: */*'   -H 'sec-fetch-site: same-origin'" \
              + "   -H 'sec-fetch-mode: cors'   -H 'sec-fetch-dest: empty'   " \
              + "-H 'referer: https://twitter.com/Florent_GT/status/" + tweet_id + "'" \
              + "   -H 'accept-language: en-US,en;q=0.9,fr;q=0.8' -H 'cookie: " + cookies + "' --compressed > out.json"

    system(command)
    replies_tweets = json.loads(open("./out.json").read())["globalObjects"]["tweets"]
    replies_users = json.loads(open("./out.json").read())["globalObjects"]["users"]

    objs = []
    for r in replies_tweets:
        author = replies_users[replies_tweets[r]["user_id_str"]]
        objs.append({
            "link": "https://twitter.com/status/" + replies_tweets[r]["id_str"],
            "author-link": "https://twitter.com/" + author["screen_name"],
            "author-name": author["name"],
            "avatar": author["profile_image_url_https"],
            "tweet-text": replies_tweets[r]["full_text"]
        })

    return objs


def get_tweet_and_comments(url: str, chat_id: str):
    """
    This method will make the request

    """
    # We extract the tweet id
    tweet_id = url.split("/")[-1].split("?")[0]

    org_tweet = get_origin_tweet(tweet_id)
    org_hash = md5(json.dumps(org_tweet).encode()).hexdigest()

    # We return results as object
    return {
        "chat-id": chat_id,
        "origin-hash": org_hash,
        "origin": org_tweet,
        "replies": get_replies(tweet_id),
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

    print("[+] returning the message...")

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
