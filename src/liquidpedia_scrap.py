from utils import cache

import bs4
import re

domain = "https://liquipedia.net"


def get_games_from_match(url, refresh_cache=False):
    match_page = cache(url, "match_", refresh_cache)
    match_soup = bs4.BeautifulSoup(match_page, features="html.parser")
    games_ = []
    teams = [team.find("a").get("title") for team in match_soup.find_all(
        class_="team-template-image-icon")][:2]
    last_ = None
    # print(teams)
    for game in match_soup.find_all(class_="match-bm-lol-game-veto-overview"):
        # print(game)
        for team_id, team_picks in enumerate(game.find_all(attrs={"aria-labelledby": "picks"})):
            # print(team_picks)
            champions = [a.get("title") for a in team_picks.find_all("a")]

            if len(champions) <= 0:
                raise Exception(f"No champs found for match {url}")

            current_ = teams[team_id], champions

            if last_ == None:
                last_ = teams[team_id], champions
            else:
                games_.append((last_, current_))
                last_ = None
    return games_


def get_games_from_schedule(schedule_url, refresh_cache=False):
    schedule_page = cache(schedule_url, "schedule_",
                          refresh_cache=refresh_cache)
    schedule_soup = bs4.BeautifulSoup(schedule_page, features="html.parser")

    links = schedule_soup.find_all('a')
    links_href = [l.get("href") for l in links]
    matches_links = list([l for l in links_href if re.match(
        "^/leagueoflegends/Match:.*$", str(l)) is not None])
    print(len(matches_links))

    games = []

    for match_link in matches_links:
        url = f"{domain}{match_link}"
        try:
            new_games = get_games_from_match(url, refresh_cache)
            games.extend(new_games)
        except Exception as e:
            print(e)
            # break
    return games
