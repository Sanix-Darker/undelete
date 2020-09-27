# We loop all over undeletes
# if the array of fetch is > array saved, we update the Undelete

# else, we try to get those elements that are not present 

# Then we send that on all watcher in the Watchme of the Undelete
from app.model import UnDelete , WatchMe
from app.utils import *
from hashlib import md5
import time


Ud = UnDelete.UnDelete
Wm = WatchMe.WatchMe

def proceed():
    uns = Ud().find_all()
    print("[+] Fetching...")

    for u in uns:
        print("[+] hash: ", u["origin-hash"])
        url = u["origin"]["link"]
        chat_id = u["chat-id"]

        result = get_tweet_and_comments(url, chat_id)

        # some comments are missing, 
        # probably deleted...
        if len(result["replies"]) < len(u["replies"]):
            for rep in u["replies"]:
                # if that reply is not in the result then maybe it have been deleted
                if rep not in result["replies"]:
                    # we send the message to all watcher for the reply that have been deleted
                    print("[-] Missing reply : ", rep)
        else:
            if len(result["replies"]) > len(u["replies"]):
                print("[+] Updating replies...")
                u["replies"] = result["replies"]
                Ud().update({
                    "origin-hash": md5(json.dumps(result["origin"]).encode()).hexdigest()
                }, u)
            else:
                print("[+] Nothing to do...")

while True:
    time.sleep(30)
    proceed()