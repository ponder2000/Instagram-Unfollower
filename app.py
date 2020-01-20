import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import main

kv = Builder.load_file('login.kv')

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def unfollow_button(self):
        print("Unfollow Button Pressed")
        sm.current = "unfollowing"
        main.start_operation(self.email.text, self.password.text)

class UnfollowingWindow(Screen):
    pass
    
sm = ScreenManager()
screens = [LoginWindow(name="login"), UnfollowingWindow(name="unfollowing")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class FirstApp(App):
    def build(self):
        return sm
    
if __name__ == "__main__":
    FirstApp().run()