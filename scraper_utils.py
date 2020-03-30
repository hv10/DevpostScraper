"""
In here utilities for discovering specific sub objects are collected.
"""
from urllib.request import urlopen

from bs4 import BeautifulSoup


def getTitle(subObj):
    title = subObj.find("h1", {"id": "app-title"})
    return title


def getSubtitle(subObj, title):
    subtitle = title.parent.find("p")
    return subtitle


def getContent(subObj):
    if subObj.find("div", {"id": "gallery"}) is None:
        return subObj.find("div", {"id": "app-details-left"}).find("div").get_text().strip()
    else:
        return subObj.find("div", {"id": "gallery"}).parent.findNext("div").get_text().strip()


def getLikes(subObj):
    software_likes = subObj.find("div", {"class": "software-likes"})
    likes = software_likes.find("span", {"class": "side-count"}).get_text().strip()
    return likes


def getUpdates(subObj):
    updateLst = []
    try:
        updates = subObj.find("div", {"class": "large-12 columns software-updates"}).findAll("article")
        for update in updates:
            author = update.find("a", {"class": "user-profile-link"})
            author_uname = author["href"].split("/")[-1]
            when = update.find("time", {"class": "timeago"})["datetime"]
            content = update.find("p", {"class": "author small"}).find_next_sibling("p", class_="").get_text().strip()
            updateLst.append([author_uname, content, when])
    except:
        print("No Updates found.")
    return updateLst


def getParticipants(subObj):
    participantLst = []
    try:
        participants = subObj.find("section", id="app-team").findAll("li")
        for participant in participants:
            member = participant.find("a", {"class": "user-profile-link"})
            member_uname = member["href"].split("/")[-1]
            participantLst.append(member_uname)
    except:
        print("No team members found.")
    return participantLst


def getSkills(userObj):
    skills = []
    try:
        skillObjs = userObj.find("ul", class_="portfolio-tags no-bullet inline-list").findAll("li")
        for skillObj in skillObjs:
            skills.append(skillObj.get_text().strip())
    except:
        print("No Skills found!")
    return skills


def getinterests(userObj):
    interests = []
    try:
        interObjs = userObj.find("div", class_="tag-list themes clearfix").find("ul",
                                                                                class_="no-bullet inline-list").findAll(
            "li")
        for interObj in interObjs:
            interests.append(interObj.get_text().strip())
    except:
        print("No interests found!")
    return interests


def getUserData(uname):
    url = "https://devpost.com/" + uname
    userObj = BeautifulSoup(urlopen(url), "html.parser")
    natural_name = userObj.find("h1", id="portfolio-user-name").get_text().strip().split("\n")[0]
    image = userObj.find("div", id="portfolio-user-photo").find("img")["src"]
    skills = getSkills(userObj)
    interests = getinterests(userObj)
    return [uname, natural_name, skills, interests, image]


def getImages(subObj):
    imgList = []
    try:
        images = subObj.find("div", {"id": "gallery"}).findAll("li")
        for image in images:
            try:
                imgSrc = image.find("img")["src"]
                imgList.append(imgSrc)
            except:
                print("Non-Image Link Found")
    except:
        print("No Gallery Found")
    return imgList


def getBuiltWith(subObj):
    builtWithList = []
    try:
        builtWith = subObj.find("div", {"id": "built-with"}).findAll(
            "span", {"class": "cp-tag"}
        )
        for tool in builtWith:
            builtWithList.append(tool.get_text().strip())
    except:
        print("No Tools Found")
    return builtWithList
