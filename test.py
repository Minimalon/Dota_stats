#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-


from fake_useragent import UserAgent
import requests
import sys
import json
from bs4 import BeautifulSoup
import datetime
import re


# Parsing site for info
def get_steam_info(steam_url):
    id_url = f"https://steamid.io/lookup/{steam_url.split('/')[4]}"
    response = requests.get(url=id_url, headers={'user-agent': f'{UserAgent().random}'})
    soup = BeautifulSoup(response.text, 'lxml')
    steam32ID = soup.find_all("dd", {"class": "value short"})[1].find("a")
    steam32ID = re.split(r":|]", steam32ID.text)[-2]
    nickname = soup.find_all("dd", {"class": "value"})[6].text
    return steam32ID, nickname


def get_All_match_info(player_id):
    AllMatchInfo_url = f'http://cdn.dota2.com/apps/dota2/images/heroes/Kunka_sb.png'
    AllMatchInfo_response = requests.get(AllMatchInfo_url)
    AllMatchInfo = json.loads(AllMatchInfo_response.text)

    with open("ALMatchInfo.json"), "w+") as f:
        f.write(json.dumps(AllMatchInfo, sort_keys=True, indent=4))
    return AllMatchInfo[0]["match_id"]


def get_match_info(match_id):
    matchInfo_url = f'https://api.opendota.com/api//matches/{match_id}'
    matchInfo_response = requests.get(matchInfo_url)
    matchInfo = json.loads(matchInfo_response.text)

    with open("matchInfo.json"), "w+") as f:
        f.write(json.dumps(matchInfo, sort_keys=True, indent=4))


def get_heroes():
    heroes_url = f'https://api.opendota.com/api/heroes'
    heroes_response = requests.get(heroes_url)
    heroes = json.loads(heroes_response.text)

    with open("heroes.json"), "w+") as f:
        f.write(json.dumps(heroes, sort_keys=True, indent=4))


def get_steam_profile(player_id):
    steamProfile_url = f'https://api.opendota.com/api/players/{player_id}'
    steamProfile_response = requests.get(steamProfile_url)
    steamProfile = json.loads(steamProfile_response.text)
    return steamProfile


# Work with API and writing to files
def get_data(steam_url):
    player_id = get_steam_info(steam_url)[0]
    get_All_match_info(player_id)

    match_id = get_All_match_info(player_id)
    get_match_info(match_id)

    get_heroes()

    get_steam_profile(player_id)


steam = get_steam_profile(116401716)
print(steam)
