#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-


import datetime
import io
import os

import json
import re

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


# Parsing site for info
def get_steam_info(steam_url):
    id_url = f"https://steamid.io/lookup/{steam_url.split('/')[4]}"
    response = requests.get(url=id_url, headers={'user-agent': f'{generate_user_agent()}'})
    soup = BeautifulSoup(response.text, 'lxml')
    steam32ID = soup.find_all("dd", {"class": "value short"})[1].find("a")
    steam32ID = re.split(r":|]", steam32ID.text)[-2]
    nickname = soup.find_all("dd", {"class": "value"})[6].text
    return steam32ID, nickname


def get_All_match_info(player_id):
    AllMatchInfo_url = f'https://api.opendota.com/api/players/{player_id}/matches?limit=100'
    AllMatchInfo_response = requests.get(AllMatchInfo_url)
    AllMatchInfo = json.loads(AllMatchInfo_response.text)
    AllMatchInfo_result = []

    with open(os.getcwd() + "/json/ALMatchInfo.json", "w+", encoding="utf-8") as f:
        for i in AllMatchInfo:
            # Heroes
            with open(os.getcwd() + "/json/heroes.json", "r") as heroes:
                heroes = json.load(heroes)
                for index in heroes:
                    if index["id"] == i["hero_id"]:
                        hero = index["localized_name"]
                        hero_name = index["name"]

            # lobby_type
            with open(os.getcwd() + "/json/lobby_type.json", "r") as lobbyType:
                lobbyType = json.load(lobbyType)
                lobby_type = lobbyType[f"{i['lobby_type']}"]["name"].split("_")
                lobby_type.remove("lobby")
                lobby_type.remove('type')

            # Match_result
            if i['radiant_win'] and i['player_slot'] < 128:
                match_result = 'Win'
            if i['radiant_win'] and i['player_slot'] > 127:
                match_result = 'Lose'
            if i['radiant_win'] == False and i['player_slot'] > 127:
                match_result = 'Win'
            if i['radiant_win'] == False and i['player_slot'] < 128:
                match_result = 'Lose'

            # skill
            if i['skill'] == 1:
                skill = "Normal"
            elif i['skill'] == 2:
                skill = "High skill"
            elif i['skill'] == 3:
                skill = " Very high skill"
            else:
                skill = ''

            AllMatchInfo_result.append({
                "assists": i['assists'],
                "deaths": i['deaths'],
                'duration': str(datetime.timedelta(seconds=i["duration"])),
                "game_mode": i['game_mode'],
                "hero": hero,
                "hero_name": hero_name,
                "kills": i['kills'],
                "leaver_status": i['leaver_status'],
                "lobby_type": ' '.join(w[0].upper() + w[1:] for w in lobby_type),
                "match_id": i['match_id'],
                "party_size": i['party_size'],
                "player_slot": i['player_slot'],
                "radiant_win": i['radiant_win'],
                "match_result": match_result,
                "skill": skill,
                'start_time': datetime.datetime.fromtimestamp(i["start_time"]).strftime('%d %B %Y %H:%M:%S'),
                "version": i['version']
            })
        f.write(json.dumps(AllMatchInfo_result, sort_keys=True, indent=4, ensure_ascii=False))

    return AllMatchInfo[0]["match_id"]


def get_match_info(match_id):
    matchInfo_url = f'https://api.opendota.com/api//matches/{match_id}'
    matchInfo_response = requests.get(matchInfo_url)
    matchInfo = json.loads(matchInfo_response.text)

    with open(os.getcwd() + "/json/matchInfo.json", "w+", encoding="utf-8") as f:
        f.write(json.dumps(matchInfo, sort_keys=True, indent=4, ensure_ascii=False))


def get_heroes():
    heroes_url = f'https://api.opendota.com/api/heroes'
    heroes_response = requests.get(heroes_url)
    heroes = json.loads(heroes_response.text)

    with open(os.getcwd() + "/json/heroes.json", "w+", encoding='utf-8') as f:
        f.write(json.dumps(heroes, sort_keys=True, indent=4, ensure_ascii=False))


def get_steam_profile(player_id):
    steamProfile_url = f'https://api.opendota.com/api/players/{player_id}'
    steamProfile_response = requests.get(steamProfile_url)
    steamProfile = json.loads(steamProfile_response.text)
    return steamProfile


def get_wl_profile(player_id):
    wl_url = f'https://api.opendota.com/api/players/{player_id}/wl'
    wl_response = requests.get(wl_url)
    wl = json.loads(wl_response.text)
    return wl


# Work with API and writing to files
def get_data(steam_url):
    player_id = get_steam_info(steam_url)[0]
    get_All_match_info(player_id)
    get_heroes()

    steamProfile = get_steam_profile(player_id)
    with open(os.getcwd() + "/json/SteamProfile.json", "w+", encoding='utf-8') as f:
        f.write(json.dumps(steamProfile, sort_keys=True, indent=4))

    wl = get_wl_profile(player_id)
    with open(os.getcwd() + "/json/wl.json", "w+", encoding='utf-8') as f:
        f.write(json.dumps(wl, sort_keys=True, indent=4))


def short_info_profile():
    profile_list = []
    with open(os.getcwd() + "/json/ProfileInfo.json", "w+", encoding='utf-8') as GameProfileInfo:
        with open(os.getcwd() + "/json/SteamProfile.json", "r", encoding='utf-8') as SteamProfile:
            SteamProfile = json.load(SteamProfile)

        with open(os.getcwd() + "/json/wl.json", "r", encoding='utf-8') as wl:
            wl = json.load(wl)

        if f"/static/images/rank_star/{list(str(SteamProfile['rank_tier']))[1]}.png" != "0":
            rank_star = f"/static/images/rank_star/{list(str(SteamProfile['rank_tier']))[1]}.png"
            rank_icon = f"/static/images/rank_icon/{list(str(SteamProfile['rank_tier']))[0]}.png"
        else:
            rank_icon = f"/static/images/rank_icon/{list(str(SteamProfile['rank_tier']))[0]}.png"
            rank_star = ""

        profile_list.append({
            'win': wl["win"],
            'lose': wl["lose"],
            'winrate': round(wl["win"] / ((wl["win"] + wl["lose"]) / 100), 2),
            'avatar': SteamProfile['profile']['avatarfull'],
            'personaname': SteamProfile['profile']['personaname'],
            'profileurl': SteamProfile['profile']['profileurl'],
            'rank_icon': rank_icon,
            'rank_star': rank_star
        })
        GameProfileInfo.write(json.dumps(profile_list, sort_keys=True, indent=4))


# Parsing info from json files
def create_result():
    with open(os.getcwd() + "/json/matchInfo.json", "r", encoding='utf-8') as f:
        f = json.load(f)
        result = []

        for i in f["players"]:
            # Steam info
            try:
                steam = get_steam_profile(i["account_id"])
                avatar_medium = steam["profile"]["avatarmedium"]
                profileurl = steam["profile"]["profileurl"]
                nickname = i["personaname"]
            except:
                nickname = "?"
                avatar_medium = ""
                profileurl = ''

            # if str(i["account_id"]) == get_steam_info(steam_url)[0]:
            with open(os.getcwd() + "/json/heroes.json", "r") as heroes:
                heroes = json.load(heroes)
                for b in heroes:
                    if b["id"] == i["hero_id"]:
                        hero = b["localized_name"]
                        hero_localized_name = b["name"].split("npc_dota_hero_")[1]
                        hero_png = f"https://cdn.dota2.com/apps/dota2/images/heroes/{hero_localized_name}_sb.png"

            # Match result
            if i["win"] == 1:
                match_result = "Won"
            else:
                match_result = "Loss"

            # Side
            if i["isRadiant"]:
                side = "Radiant"
            else:
                side = "Dire"

            result.append({
                'match_id': i["match_id"],
                'profileurl': profileurl,
                'nickname': nickname,
                'match_result': match_result,
                'avatar': avatar_medium,
                'kills': i["kills"],
                'deaths': i["deaths"],
                'assists': i["assists"],
                'level': i["level"],
                'xp_per_min': i["xp_per_min"],
                'gold_per_min': i["gold_per_min"],
                'total_value': i["total_gold"],
                'hero_damage': i["hero_damage"],
                'hero_healing': i["hero_healing"],
                # 'party_size': i["party_size"],
                'tower_damage': i["tower_damage"],
                'last_hits': i["last_hits"],
                'denies': i["denies"],
                'CPM': round(i["last_hits"] / (i["duration"] / 60), 1),
                'KDA': i["kda"],
                'hero': hero,
                'hero_png': hero_png,
                # 'lane_role': lane_role,
                'side': side,
                'dire_score': f["dire_score"],
                'radiant_score': f["radiant_score"],
                'radiant_win': f["radiant_win"],
                'duration': str(datetime.timedelta(seconds=i["duration"])),
                'start_time': datetime.datetime.fromtimestamp(i["start_time"]).strftime('%d %B %Y %H:%M:%S'),
            })

        with io.open(os.getcwd() + "/json/result.json", "w+", encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4))


def Main(steam_url):
    get_data(steam_url)
    short_info_profile()


if __name__ == "__main__":
    # Main(sys.argv[1]) # Take first parametr from autostart.sh
    Main("https://steamcommunity.com/profiles/76561198092347401/")
