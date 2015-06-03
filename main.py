import vk
import sqlite3
import sys
import json


def load_credentials():
    "place_your_ads_here"


def add_post(db_connection, post):
    post_id = int(post["id"])
    if "signer_id" in post:
        author_id = post["signer_id"]
    else:
        author_id = 0
    text = post["text"]

    c = db_connection.cursor()
    c.execute('SELECT * FROM main WHERE ID = ?', (post_id,))
    if c.fetchone():
        return False

    c.execute('INSERT INTO main VALUES(?,?,?,?)', (post_id, json.dumps(post), author_id, text))
    db_connection.commit()
    return True

APP_ID = 4353997
GROUP_ID = 89005202


# session = vk.API(APP_ID, *load_credentials(), scope=["offline", "wall"])
session = vk.API(access_token="place_your_ads_here")
print session.access_token
db_connection = sqlite3.connect("archive.db")


if __name__ == "__main__":
    need_load_more_posts = True
    offset = 0
    max_count = 100
    while need_load_more_posts:
        posts = session.wall.get(
                owner_id=-GROUP_ID,
                count=max_count,
                offset=offset)
        for post in posts["items"]:
            if not add_post(db_connection, post):
                need_load_more_posts = False
                break
            else:
                print "Added post: ", post["id"]
        if len(posts["items"]) < max_count:
            need_load_more_posts = False
        offset += max_count

