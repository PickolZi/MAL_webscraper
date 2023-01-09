"""
    Author: Pickolzi
    Purpose: Scrape data from the anime website, myanimelist.net, through a CustomGUI
"""
import requests
from bs4 import BeautifulSoup
from anime import Anime

LINK = "https://myanimelist.net/topanime.php"

def retrieve_data(link="https://myanimelist.net/topanime.php"):
    """
    :param link: grabs html from the link.
    :return: list of Anime objects with their attributes.
    """
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.table

    animes = []

    # Collecting individual anime attributes.
    ranking_list = table.find_all(class_="ranking-list")
    for anime in ranking_list:
        info = anime.find(class_="information di-ib mt4").text
        info = info.split("\n")
        info = [i.strip() for i in info if i.strip() != ""]

        rank = int(anime.find(class_="rank ac").text.strip())
        title = anime.h3.text
        anime_type = info[0].split(" ")[0]
        num_of_episodes = info[0].split("(")[1].split(" ")[0]
        release_date = info[1]
        members = info[2].split(" ")[0]
        score = float(anime.find(class_="score ac fs14").span.text)

        anime_object = Anime(rank, title, anime_type, num_of_episodes, release_date, members, score)
        animes.append(anime_object)
        # print(f"The anime {title} is a {anime_type} ranked #{rank} with {num_of_episodes} episodes, released on {release_date}, with {members} total members, and a score of {score}")

    return animes


animes = retrieve_data("https://myanimelist.net/topanime.php?type=airing")
for anime in animes:
    print(anime.title)
    break