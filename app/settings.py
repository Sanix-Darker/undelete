import configparser as Configparser

conf = Configparser.RawConfigParser()
conf_path = r'config.txt'
conf.read(conf_path)

DATABASE_HOST = conf.get("ud", "DATABASE_HOST")
DATABASE_NAME = conf.get("ud", "DATABASE_NAME")

BEARER_TOKEN = conf.get("ud", "BEARER_TOKEN")
CSRF_TOKEN = conf.get("ud", "CSRF_TOKEN")

cookies = "personalization_id=\"v1_uGBc/CVzz58okHftG19KRQ==\"; guest_id=v1%3A157857265255937117; " \
          "_ga=GA1.2.1202687542.1578572664; kdt=1Hrr54UEdrKzkX9M36oBsA2weYp1pAnsgNZiClqz; " \
          "mbox=session#17cea973837441a0a89e64d95306781e#1601202925|PC#17cea973837441a0a89e64d95306781e.38_0" \
          "#1664445960; cd_user_id=174cf055ac09-0ae8f2e6d8ac2-31634645-1fa400-174cf055ac210b; " \
          "ct0=f7d40e3f74d54bb0e474cd2480d0e16f33cb06e0b993e3a79483e2b5d85d44ec276bf6dc8af847136"\
          "1e9bcf13f6713a5d60d1d19995f48104aa047b53ea7fc1365ec69cd63b8638da2862d6511d5f632; "\
          "_gid=GA1.2.1360272225.1613834334; gt=1363191791344828423; "\
          "_twitter_sess=BAh7DyIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGF"\
          "zaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCF7hq8B3AToMY3NyZl9p%250AZCIlYzU5NDJhM2Y2OWI1M"\
          "zM0OTFiYWMwNzRiOTUzNjFhYjg6B2lkIiVhN2Ew%250ANzI1OTAxNDFlMzdkY2I0ZGRhMjU3NTg1NzdjMiIJ"\
          "cHJycCIAOgl1c2VybCsJ%250AB5BX4mDgLhI6CHByc2kMOghwcnVsKwkHkFfiYOAuEjoIcHJsIitKQ29WOXQ"\
          "1%250AQUtMV1NIN1BrdGtxYWw4dWl6UXlRckNueGlhOHdRMzoIcHJhaQY%253D--0d88904a9e86b706ed86aa"\
          "d5d9a12f4ad0fe82bd; ads_prefs=\"HBERAAA=\"; remember_checked_on=1; twid=u%3D1310231248330264583;"\
          " auth_token=7cc8d69637b853809fb5cfe6485107ff75d33017; lang=en' -H 'TE: Trailers' "

queue_reply_url = "include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1" \
          + "&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1" \
          + "&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1" \
          + "&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1" \
          + "&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true" \
          + "&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true" \
          + "&referrer=tweet&count=20&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel'"
