from typing import List, Dict
import csv
import json
from time import sleep
from bs4 import BeautifulSoup
from linkedIn_base import Linkedin


def get_profile_data(html_page: str) -> List[Dict]:
    """
    Extracts information about LinkedIn user profiles from an HTML page.

    :param html_page: str, the HTML page to extract data from
    :return: list of dictionaries, containing information about each LinkedIn user profile, including the user's name, LinkedIn profile link, job title, profile image, and location

    """
    soup = BeautifulSoup(html_page, 'html.parser')
    profiles_data = json.loads(soup.find_all('code')[-3].text)

    profiles = []
    for profile in profiles_data["included"]:

        try:
            if profile["template"]:
                try:
                    location = profile['secondarySubtitle']['text']
                except:
                    location = None

                try:
                    image = profile['image']['attributes'][0]['detailData']['nonEntityProfilePicture']['vectorImage']['artifacts'][0]['fileIdentifyingUrlPathSegment'].replace("amp;", "")
                except TypeError:
                    image = None

                profile_dict = {
                    "name": profile["title"]['text'],
                    "link": profile['navigationUrl'].split('?')[0],
                    "title": profile['primarySubtitle']['text'],
                    "image": image,
                    "location": location
                }
                profiles.append(profile_dict)

        except KeyError:
            pass

    return profiles


def search(query: str, pages=1, save_csv=False) -> List[Dict]:
    """
    Searches for people on LinkedIn based on the given query, and returns a list of dictionaries with information about each person.

    :param query: str, the search query to use on LinkedIn
    :param pages: int, optional, the number of pages of search results to retrieve (default is 1)
    :param save_csv: bool, optional, whether to save the search results to a CSV file (default is False)
    :return: list of dictionaries, containing information about each person, including their name, LinkedIn profile link, job title, profile image, and location
    """

    all_data = []
    for page in range(1, pages+1):
        driver.get(f"https://www.linkedin.com/search/results/people/?keywords={query}&page={page}")
        sleep(2)
        html = driver.page_source
        one_page_data = get_profile_data(html)
        all_data.extend(one_page_data)

    if save_csv:
        with open('output.csv', 'w',  newline='', encoding="utf-8") as file_output:
            headers = ["name", "link", "title", "image", "location"]
            writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_data)
    else:
        return all_data


if __name__ == "__main__":
    obj = Linkedin()
    driver = obj.load_cookies(path="linkedin_cookies.json")
    print(search(query="james", pages=2))
