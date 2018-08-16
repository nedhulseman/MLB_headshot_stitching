from bs4 import BeautifulSoup, Comment
import requests
import re
import urllib.request


'''
    author:  @Ned Hulseman
    date:    @ 8/16/2018
    purpose: The purpose is to save a players headshot but can iterate through entire MLB and locate
             all player's headshots 
'''
class baseballData:

    # We don't need our constructor to do muuch, just save the baseball reference url as an attribute
    def __init__(self):
        self.url = 'https://www.baseball-reference.com'
        
    # This method will return a dict of the team names, and url extensions
    def getTeams(self):
        soup = self.getSoup('/teams/')
        teams_table = soup.find('table', id='teams_active')
        rows = teams_table.find_all("tr")
        team_row = [row for row in rows if "href=\"/teams/" and "scope=\"row\"" in str(row)]

        teams = {}
        for team in team_row:
            td = team.find_all("td")
            teams[td[0].text] = td[0].find("a")['href']

        return teams


    # This method will return the names of players on a roster
    def getRoster(self, team):
        # @team is the only argument and it should be in the form of a url extension
        # returned from the getTeams method
        
        # we need to make a few corrections to the team url extensions
        if team == '/teams/ANA/':
            team = '/teams/LAA/'
        elif team == '/teams/FLA/':
            team = '/teams/MIA/'
        elif team == '/teams/TBD/':
            team = '/teams/TBR/'

        #team should be url extension obtain from the dict getTeame... /teams/BOS/
        soup = self.getSoup(url_ext = team + "2018.shtml", remove_comments=True)
        current_roster_table = soup.find('table', id='the40man')

        rows = current_roster_table.find_all('tr')
        player_rows = [row for row in rows if "<a href=" in str(row)]
        players = []
        for player in player_rows:
            td = player.find_all('td')
            players.append(td[1].text)
        
        players = [player.lower() for player in players]
        return players


    # This method will locate the headshot of a player and save the png to the local directory
    def get_headshot(self, playername):
        playername = playername.split(' ')
        playername_code = playername[1][0:5] + playername[0][0:2]
        url = 'https://www.baseball-reference.com/players/'+playername[1][0:1]+'/'+playername_code+'01.shtml'
        # get contents from url
        content = requests.get(url).content
        # get soup
        soup = BeautifulSoup(content,'lxml') # choose lxml parser
        # find the tag : <img ... >
        image_tags = soup.findAll('img')
        headshot_img = str([src for src in image_tags if 'headshots' in str(src)][0])
        headshot_url = headshot_img.split('src="')[1].split('"/>')[0]
        urllib.request.urlretrieve(headshot_url, 'headshot.png')
        

    
    # This method is used throughout the class to get the Beautiful Soup HTML
    def getSoup(self, url_ext="", remove_comments=False):
        if remove_comments == False:
            raw_html = requests.get(self.url + url_ext).content
            soup = BeautifulSoup(raw_html, "lxml")

        else:
            raw_html = requests.get(self.url + url_ext).content
            rem_com = re.sub(r"(<!--)", "", str(raw_html))
            rem_com = re.sub(r"(-->)", "", rem_com)
            soup = BeautifulSoup(rem_com, "lxml")
            
        return soup




