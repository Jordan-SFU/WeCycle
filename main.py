from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

litter = 0

class MyLayout(BoxLayout):
    def __init__(self):
        super().__init__()
        
        litter = 0

        self.screen_manager = ScreenManager()

        self.firstpage = FirstPage()
        screen = Screen(name='first')
        screen.add_widget(self.firstpage)
        self.screen_manager.add_widget(screen)

        self.button1 = Button(text="Litter Counter")
        self.button1.bind(on_press=self.new_label)

        self.button2 = Button(text="History")
        self.button2.bind(on_press=self.myFunc)

        self.button3 = FirstPage()
        self.button3.bind(on_press=self.button3.switch)

        self.add_widget(self.button1)
        self.add_widget(self.button2)
        self.add_widget(self.button3)

    def myFunc(self, button):
        global litter
        print(f"\n{litter}")
        litter = litter + 1

    def betterFunc(self, button):
        print("pressed again")

    def new_label(self, button):
        self.label = Label(text="new label")
        self.add_widget(self.label)
        self.remove_widget(self.button1)
        self.remove_widget(self.button2)

class FirstPage(Button):
    def __init__(self):
        super().__init__()
        self.text = 'hi 1'
        self.bind(on_press=self.switch)
    def switch(self,item):
        myapp.screen_manager.current = 'second'


class SecondPage(Button):
    def __init__(self):
        super().__init__()
        self.text = 'hi 2'
        self.bind(on_press=self.switch)
    def switch(self,item):
        myapp.screen_manager.current = 'first'



class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.firstpage = FirstPage()
        screen = Screen(name='first')
        screen.add_widget(self.firstpage)
        self.screen_manager.add_widget(screen)

        self.secondpage = SecondPage()
        screen = Screen(name='second')
        screen.add_widget(self.secondpage)
        self.screen_manager.add_widget(screen)

        #layout = FloatLayout()
        #label1 = Label(text='hi', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.2, 'center_y': 0.5})
        #layout.add_widget(label1)

        return MyLayout()
    
    
myapp = MyApp()
myapp.run()


