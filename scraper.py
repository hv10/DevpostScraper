"""
This is the main script to be called upon.
The main function gets executed automatically on calling the script directly.
The other functions are for entering the data into the sqllite db file.
"""
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scraper_utils import (getBuiltWith, getImages, getLikes, getSubtitle, getTitle, getContent, getUpdates,
                           getParticipants, getUserData)
from database_utils import (makeDatabase, initializeDatabase, insertFollowing, insertImage, insertParticipant,
                            insertParticipation, insertProject, insertUpdate, insertProjectUses, insertTechnology)
import sys

BASEURL = "https://wirvsvirushackathon.devpost.com"
SUBMISSIONS_URL = BASEURL + "//submissions?page="


def main():
    if len(sys.argv) > 1:
        conn, cursor = makeDatabase(sys.argv[1])
    else:
        raise ValueError("provide at least a path where the database should be saved to")
    initializeDatabase(conn, cursor)
    pageCount = 1
    while True:
        subsObj = BeautifulSoup(urlopen(SUBMISSIONS_URL + str(pageCount)), "html.parser")
        submissions = subsObj.findAll(
            "a", {"class": "block-wrapper-link fade link-to-software"}
        )
        if len(submissions) != 0:
            for submission in submissions:
                subUrl = submission.attrs["href"]
                subObj = BeautifulSoup(urlopen(subUrl), "html.parser")
                title = getTitle(subObj)
                title_text = title.get_text().strip()
                project_id = insertProject(
                    cursor,
                    title_text,
                    getSubtitle(subObj, title).get_text().strip(),
                    getContent(subObj),
                    subUrl,
                    getLikes(subObj)
                )
                print(f"Collecting project {project_id}:{title_text}")
                participants = getParticipants(subObj)
                for participant in participants:
                    p_data = getUserData(participant)
                    insertParticipant(cursor, *p_data)
                    insertParticipation(cursor, project_id, participant)
                updates = getUpdates(subObj)
                for update in updates:
                    u_data = getUserData(update[0])
                    insertParticipant(cursor,*u_data)
                    insertUpdate(cursor, project_id,*update)
                images = getImages(subObj)
                for image in images:
                    insertImage(cursor, project_id, image)
                builtWith = getBuiltWith(subObj)
                for tech in builtWith:
                    insertTechnology(cursor, tech)
                    insertProjectUses(cursor, project_id, tech)
                conn.commit()
            pageCount = pageCount + 1
        else:
            break


if __name__ == "__main__":
    main()
