from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import kivy.utils
from datetime import datetime, timedelta
import JSONStuff as jsn
import random

# Global Litter Count
litter = 0
breakdown = {
    "Garbage": 0,
    "Compost": 0,
    "Metal": 0,
    "Paper": 0,
    "Plastic": 0
}


username = "Guest User"
date = datetime.now().strftime("%Y-%m-%d")
dc = ["", "", ""]

# Opening Screen
class Main(BoxLayout):
    def __init__(self):
        super().__init__()

    def switch(self, guest):
        if(guest):
            myapp.screen_manager.current = "select"

            select_page = myapp.select
            select_page.usernameLabel.text = f"Welcome, {username}!"
        else:
            myapp.screen_manager.current = "login"

class Login(BoxLayout):
    def __init__(self):
        super().__init__()

        usernameInput = ObjectProperty(None)

    def login(self):
        global username
        username = self.usernameInput.text
        myapp.screen_manager.current = "select"

        select_page = myapp.select
        select_page.usernameLabel.text = f"Welcome, {username}!"

# Select Page Screen
class SelectPage(BoxLayout):
    def __init__(self):
        super().__init__()

        usernameLabel = ObjectProperty(None)
        dateLabel = ObjectProperty(None)

        global username, date

        # Update the date first
        self.update_date()

        # Now you can load the score using the updated date
        activities_page = myapp.activities
        activities_page.updateLitterCount()

        stats_page = myapp.stats
        stats_page.update_date()
        stats_page.update_score()

        highscore_page = myapp.leaderboard
        highscore_page.updateHighscore()

        challenge_page = myapp.challenges
        challenge_page.updateChallengeText()

    def switch(self, item):
        myapp.screen_manager.current = item
        activities_page = myapp.activities
        activities_page.updateLitterCount()

        challenges_page = myapp.challenges
        challenges_page.updateChallengeText()

        stats_page = myapp.stats
        stats_page.update_date()
        stats_page.update_score()

        highscore_page = myapp.leaderboard
        highscore_page.updateHighscore()

    def update_date(self):
        # Get the current date and format it as a string
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Update the text of the dateLabel
        self.dateLabel.text = f"{current_date}"

        # Update the global date variable
        global date
        date = current_date


# Activities Screen
class Activities(BoxLayout):
    def __init__(self):
        super().__init__()

        # Litter Count Text Label
        litterCount = ObjectProperty(None)

        global date, username
        self.litterCount.text = f"{jsn.load(username, date)}"

    def updateLitterCount(self):
        global date, username
        date = datetime.now().strftime("%Y-%m-%d")
        self.litterCount.text = f"{jsn.load(username, date)}"

    # Increment Litter Count
    def incrementLitter(self, val, type):
        global litter, date, username
        date = datetime.now().strftime("%Y-%m-%d")
        litter = jsn.load(username, date)
        litter = litter + val
        self.litterCount.text = f"{litter}"
        jsn.save(username, date, litter)

        breakdown[type] = breakdown[type] + 1

        stats_screen = myapp.stats
        stats_screen.scoreLabel.text = f"{jsn.load(username, date)}"
        stats_screen.update_score()

        highscore_screen = myapp.leaderboard
        highscore_screen.highscoreLabel.text = f"{jsn.max_entry()[1]}"
        highscore_screen.highscoreDateLabel.text = f"{jsn.max_entry()[2]}"
        highscore_screen.highscoreUserLabel.text = f"{jsn.max_entry()[0]}"

    # Return to Select Page Screen
    def back(self):
        myapp.screen_manager.current = "select"

class Stats(BoxLayout):
    def __init__(self):
        super().__init__()

        dateLabel2 = ObjectProperty(None)
        scoreLabel = ObjectProperty(None)

        self.update_date()
        self.update_score()

    # Return to Select Page Screen
    def back(self):
        myapp.screen_manager.current = "select"

    def update_date(self):
        # Get the current date and format it as a string
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Update the text of the dateLabel
        self.dateLabel2.text = f"{current_date}"
    
    def update_score(self):
        global date, username
        current_score = jsn.load(username, date)
        self.scoreLabel.text = f"{current_score}"

    def preview(self, inc):
        global date
        # Convert the current date to a datetime object
        current_date = datetime.strptime(date, "%Y-%m-%d")

        # Increment or decrement the date by the specified number of days
        new_date = current_date + timedelta(days=inc)

        # Convert the new date back to a string in the same format
        date = new_date.strftime("%Y-%m-%d")

        # Update the dateLabel2 and scoreLabel
        self.dateLabel2.text = f"{date}"
        self.update_score()

    def jumpToToday(self):
        global date
        date = datetime.now().strftime("%Y-%m-%d")
        self.dateLabel2.text = f"{date}"
        self.update_score()

class Leaderboard(BoxLayout):
    def __init__(self):
        super().__init__()

        highscoreLabel = ObjectProperty(None)
        highscoreDateLabel = ObjectProperty(None)
        highscoreUserLabel = ObjectProperty(None)

    def updateHighscore(self):
        self.highscoreLabel.text = f"{jsn.max_entry()[1]}"
        self.highscoreDateLabel.text = f"{jsn.max_entry()[2]}"
        self.highscoreUserLabel.text = f"{jsn.max_entry()[0]}"

    # Return to Select Page Screen
    def back(self):
        myapp.screen_manager.current = "select"

class Challenges(BoxLayout):
    challenges = {
        "DailyChallenge1" : ["", 0, ""],
        "DailyChallenge2" : ["", 0, ""],
        "DailyChallenge3" : ["", 0, ""]
    }
    def __init__(self):
        super().__init__()
        self.updateChallengeText()

    def back(self):
        myapp.screen_manager.current = "select"

    def randomChallenge(self):
        types = ["Garbage", "Compost", "Metal", "Paper", "Plastic"]
        selectedType = random.choice(types)
        n = random.randint(1, 10)

        challengeStr = str(f"Correctly recycle {n} pieces of {selectedType}")
        return [challengeStr, n, selectedType]

    def assignChallenge(self):
        for i in self.challenges:
            if self.challenges[i][0] == "":
                self.challenges[i] = self.randomChallenge()

    def verifyChallenges(self):
        print("banana")
        for i in self.challenges:
            if breakdown[self.challenges[i][2]] >= self.challenges[i][1]:
                self.challenges[i][0] = "Challenge Complete!"
    
    ## Should be used when changing between days
    def resetChallenges(self):
        for i in self.challenges:
            self.challenges[i] = ["", 0, ""]
                
    def updateChallengeText(self):
        self.assignChallenge()
        self.verifyChallenges()
        self.dailyChallenge1.text = self.challenges["DailyChallenge1"][0]
        self.dailyChallenge2.text = self.challenges["DailyChallenge2"][0]
        self.dailyChallenge3.text = self.challenges["DailyChallenge3"][0]

class About(BoxLayout):
    def __init__(self):
        super().__init__()

    # Return to Select Page Screen
    def back(self):
        myapp.screen_manager.current = "select"

class WeCycleApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main = Main()
        screen = Screen(name="main")
        screen.add_widget(self.main)
        self.screen_manager.add_widget(screen)

        self.login = Login()
        screen = Screen(name="login")
        screen.add_widget(self.login)
        self.screen_manager.add_widget(screen)

        self.stats = Stats()
        screen = Screen(name="stats")
        screen.add_widget(self.stats)
        self.screen_manager.add_widget(screen)

        self.activities = Activities()
        screen = Screen(name="activities")
        screen.add_widget(self.activities)
        self.screen_manager.add_widget(screen)

        self.leaderboard = Leaderboard()
        screen = Screen(name="leaderboards")
        screen.add_widget(self.leaderboard)
        self.screen_manager.add_widget(screen)

        self.challenges = Challenges()
        screen = Screen(name="challenges")
        screen.add_widget(self.challenges)
        self.screen_manager.add_widget(screen)

        self.about = About()
        screen = Screen(name="about")
        screen.add_widget(self.about)
        self.screen_manager.add_widget(screen)

        self.select = SelectPage()
        screen = Screen(name="select")
        screen.add_widget(self.select)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

myapp = WeCycleApp()
myapp.run()