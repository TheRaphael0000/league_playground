from utils import cache
import bs4
import re
import itertools


domain = "https://gol.gg/"

def get_games_from_schedule(schedule_url, refresh_schedule_cache=False):
    schedule_page = cache(schedule_url, "schedule_",
                          refresh_cache=refresh_schedule_cache)
    schedule_soup = bs4.BeautifulSoup(schedule_page, features="html.parser")

    links = schedule_soup.find_all('a')
    links_href = [l.get("href") for l in links]
    matches_links = list([l for l in links_href if re.match(
        "^../game/stats/.*$", str(l)) is not None])
    
    matches_links = [link.replace("/page-game/", "/page-summary/").replace("../", "") for link in matches_links]
    print(len(matches_links))

    games = []

    for match_link in matches_links:
        url = f"{domain}{match_link}"
        try:
            new_games = get_games_from_match(url)
            games.extend(new_games)
        except Exception as e:
            print(e)
    return games

def get_games_from_match(url):
    match_page = cache(url, "match_")
    match_soup = bs4.BeautifulSoup(match_page, features="html.parser")
    games_ = []
    links = match_soup.find_all("a")
    team_links = [link for link in links if link.get("href").startswith("../teams/team-stats/")]
    teams = [team_link.text for team_link in team_links]

    champions = [re.match(r"\.\./_img/champions_icon/(.*)\.png", c.get("src"))[1] for c in match_soup.find_all(class_="champion_icon_medium")]
    champions_by_phase = list(itertools.batched(champions, n=5))
    champions_by_game = list(itertools.batched(champions_by_phase, n=2))

    for (A_bans, A_picks), (B_bans, B_picks) in zip(champions_by_game[0::2], champions_by_game[1::2]):
        games_.append((((teams[0], A_picks)),(teams[1], B_picks)))
    return games_
