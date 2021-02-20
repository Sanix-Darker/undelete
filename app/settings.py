import configparser as Configparser

conf = Configparser.RawConfigParser()
conf_path = r'config.txt'
conf.read(conf_path)

DATABASE_HOST = conf.get("ud", "DATABASE_HOST")
DATABASE_NAME = conf.get("ud", "DATABASE_NAME")

BEARER_TOKEN = conf.get("ud", "BEARER_TOKEN")
CSRF_TOKEN = conf.get("ud", "CSRF_TOKEN")

cookies = "_ga=GA1.2.1810982598.1577183899;" \
          + " dnt=1; ads_prefs=\"HBISAAA=\"; kdt=uqASzquDtfI27qZZVKXeEvzQ3tRwkIEGduoM4DZH; csrf_same_site_set=1;" \
          + " personalization_id=\"v1_emLvayd91BE3Th5cjAyolw==\"; " \
          + "cd_user_id=1754006239910-0f8ab290908b4c-397c095c-1fa400-1754006239a89; " \
          + "remember_checked_on=1; auth_token=a7ea39ac616ff10caca4e8b86810ea661687c487; " \
          + "ct0=f685ee313ea057e7e1347acd20a4dce1c2432a9b1b11154bf85740f1841213a0b4e514fbd3" \
          + "734fb6305223fc94c68d6adf597aaa4f6624e2f26c9f6a4b12027946060f7fcfbcb6644f68f501628e26ec;" \
          + " guest_id=v1%3A160460719347617574; des_opt_in=Y; twid=u%3D1055957666185601024; " \
          + "night_mode=1; lang=en; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6Ok" \
          + "ZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGogE6V3AToMY3NyZl9p%250AZCIlMTVlMTFiMTM5Z" \
          + "DQ1ZjcyZGZjZWJmMzQ1ZDhhZmYxZWM6B2lkIiUwODg3%250AZjhhODJmNjJlYmM3YTFlOTAzYmU0NWQ3OTIxNA%253D%25" \
          + "3D--cf8063584622af37ea6827290beb515683adc064; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX" \
          + "|0|8e8t2xd8A2w%3D; at_check=true; mbox=PC#5713b86255d94f0098c9958e70fa0fae.38_0#1677081194|" \
          + "session#42fae65a832d4d1092914c6dc07ebae2#1613836951"

queue_reply_url = "include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1" \
          + "&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1" \
          + "&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1" \
          + "&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1" \
          + "&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true" \
          + "&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true" \
          + "&referrer=tweet&count=20&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel'"
