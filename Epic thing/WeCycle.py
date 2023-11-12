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
banana = 2
litter = 0
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
    def incrementLitter(self, val):
        global litter, date, username
        date = datetime.now().strftime("%Y-%m-%d")
        litter = jsn.load(username, date)
        litter = litter + val
        self.litterCount.text = f"{litter}"
        jsn.save(username, date, litter)

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
    def __init__(self):
        super().__init__()

        dailyChallenge1 = ObjectProperty(None)
        dailyChallenge2 = ObjectProperty(None)
        dailyChallenge3 = ObjectProperty(None)

    def back(self):
        myapp.screen_manager.current = "select"

    def randomChallenge(self):
        types = ["Garbage", "Compost", "Metal", "Paper", "Plastic"]
        selectedType = random.choice(types)
        n = random.randint(1, 10)

        challengeStr = str(f"Correctly recycle {n} pieces of {selectedType}")
        return challengeStr
    
    def assignChallenge(self):
        global dc
        for i in range(3):
            if dc[i] == "":
                dc[i] = self.randomChallenge()

    def updateChallengeText(self):
        global dc
        self.assignChallenge()
        self.dailyChallenge1.text = dc[0]
        self.dailyChallenge2.text = dc[1]
        self.dailyChallenge3.text = dc[2]



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

        self.select = SelectPage()
        screen = Screen(name="select")
        screen.add_widget(self.select)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

myapp = WeCycleApp()
myapp.run()