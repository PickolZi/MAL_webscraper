"""
    Author: Pickolzi
    Purpose: Scrape data from the anime website, myanimelist.net, through a CustomGUI
"""
import requests
from openpyxl import Workbook
from openpyxl.worksheet.properties import WorksheetProperties, PageSetupProperties
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
        try:
            score = float(anime.find(class_="score ac fs14").span.text)
        except ValueError:
            score = "N/A"
        link = anime.h3.a["href"]

        anime_object = Anime(rank, title, anime_type, num_of_episodes, release_date, members, score, link)
        animes.append(anime_object)
        # print(f"The anime {title} is a {anime_type} ranked #{rank} with {num_of_episodes} episodes, released on {release_date}, with {members} total members, and a score of {score}")

    return animes


def save_to_excel(animes):
    """
    :param animes: Anime object
    Creates xlsx file and saves the Anime object's data to the spreadsheet.
    """
    filename = "results.xlsx"
    wb = Workbook()

    ws = wb.active
    ws.title = "Top Animes"

    # Create header information
    ws["A1"] = "Rank:"
    ws["B1"] = "Title:"
    ws["C1"] = "Anime type:"
    ws["D1"] = "Number of episodes:"
    ws["E1"] = "Release date:"
    ws["F1"] = "Number of members:"
    ws["G1"] = "Score:"
    ws["H1"] = "Link:"

    # Add anime information
    for anime in animes:
        col = anime.rank + 1
        ws[f"A{col}"] = anime.rank
        ws[f"B{col}"] = anime.title
        ws[f"C{col}"] = anime.anime_type
        ws[f"D{col}"] = anime.num_of_episodes
        ws[f"E{col}"] = anime.release_date
        ws[f"F{col}"] = anime.members
        ws[f"G{col}"] = anime.score
        ws[f"H{col}"] = anime.link

    # Configuration settings
    ws.column_dimensions["B"].width = 64
    ws.column_dimensions["C"].width = 24
    ws.column_dimensions["D"].width = 24
    ws.column_dimensions["E"].width = 24
    ws.column_dimensions["F"].width = 24
    ws.column_dimensions["G"].width = 24
    ws.column_dimensions["H"].width = 64

    # Close the workbook
    wb.save(filename=filename)
    print("Finished saving to xlsx file...")

# animes = retrieve_data("https://myanimelist.net/topanime.php?type=airing")
animes = retrieve_data("https://myanimelist.net/topanime.php?type=upcoming")
save_to_excel(animes)
