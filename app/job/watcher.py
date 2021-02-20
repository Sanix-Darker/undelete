# We loop all over undeletes
# if the array of fetch is > array saved, we update the Undelete

# else, we try to get those elements that are not present

# Then we send that on all watcher in the Watchme of the Undelete
from app.model import UnDelete, WatchMe, Sends
from app.utils import *
from hashlib import md5
import time

Ud = UnDelete.UnDelete
Wm = WatchMe.WatchMe
Sds = Sends.Sends


def build_message(rep, url):
    """
    We just build the message here !

    """
    text = "Deleted tweet/comment on :"
    text += "\n{}".format(url)
    text += "\n----"
    text += "\n{} :".format(rep["author-name"])
    text += "\n'{}'".format(rep["tweet-text"])
    text += "\n----"
    text += "\nBot by @sanixdarker"

    return text


def send_message_and_update_db(w, rep, text):
    """
    We send the message and update the database

    """
    sds = list(Sds().find_by({
        "hash": md5(json.dumps(rep).encode()).hexdigest()
    }))

    if len(sds) == 0:
        print("[+] Sending the message here...")
        # We send the message here
        if send_message(w, text):
            sd = Sds({
                "hash": md5(json.dumps(rep).encode()).hexdigest(),
                "chat-ids": [w]
            })
            sd.save()
    else:
        # if not we send
        if w not in sds[0]["chat-ids"]:
            print("[+] | Sending the message here...")
            # We send the message here
            if send_message(w, text):
                sds[0]["chat-ids"].append(w)
                Sds().update({
                    "hash": md5(json.dumps(rep).encode()).hexdigest(),
                }, sds[0])


def proceed():
    """
    The main method for the watcher

    """
    print("[+] Fetching...")

    for u in Ud().find_all():
        try:
            print("[+] hash: ", u["origin-hash"])
            url = u["origin"]["link"]

            result = get_tweet_and_comments(url, u["chat-id"])

            # some comments are missing,
            # probably deleted...
            # si les 2 tableaux des reply sont differents
            # Je check un a un
            if result["replies"] != u["replies"]:

                for rep0 in result["replies"]:
                    if rep0 not in u["replies"]:
                        print("[+] Updating replies...")
                        u["replies"].append(rep0)
                        Ud().update({
                            "origin-hash": md5(json.dumps(result["origin"]).encode()).hexdigest()
                        }, u)

                # we get all watchers...
                wms = list(Wm().find_by({
                    "origin-id": get_ud_id(Ud, result)
                }))

                for rep in u["replies"]:
                    # if that reply is not in the result then maybe it have been deleted
                    if rep not in result["replies"]:
                        # we send the message to all watcher for the reply that have been deleted
                        print("[-] Missing reply '{}' from '{}' ".format(rep["tweet-text"], rep["author-name"]))

                        # The message text to respond
                        text = build_message(rep, url)

                        # we check for each of them
                        # if they already received the message
                        for w in wms[0]["chat-ids"]:
                            send_message_and_update_db(w, rep, text)
            else:
                print("[+] Nothing to do...")
        except Exception as es:
            print(es)


while True:
    try:
        # always run lol
        proceed()
    except Exception as es:
        print(es)

    time.sleep(30)
