import json




def get_(locale, key):
    with open(f"./locales/{locale}.json","r" ,encoding="utf-8") as f:
        return json.load(f).get(key)