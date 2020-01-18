import time
import details
from selenium import webdriver

load_time = 3

class instagram_handler():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        driver_path = '/usr/local/bin/geckodriver'  # getting the location of the geckodriver
        self.bot = webdriver.Firefox(executable_path=driver_path)   # setting the driver

    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/')
        print("Navigated to instagram page")

        time.sleep(load_time)
        login_button = bot.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[2]/p/a').click()
        time.sleep(load_time)
        # entering the login details
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(self.username)
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(self.password)
        print("Login details entered")
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()
        time.sleep(load_time)
        print("BAM!! You are logged in!")
        # you may get a pop up window for notification to set on to set it we use try except because the window may or may not appear
        try:
            bot.find_elements_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
            print("Pop up notification window is closed!")

        except:
            print("No notification popup window appeared!!")
        # appeared to me that now you are succesfully inside instagram
        # bot.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

    def logout(self):
        self._my_profile()
        # opening settings
        bot = self.bot
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div/button').click()
        time.sleep(1)
        bot.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()
        print("You are logged out!")

    def _my_profile(self):
        try:
            self.bot.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a").click()
            print('Profile found using xpath')
        except:
            self.bot.get('https://www.instagram.com/'+self.username+'/')
            print('profile found using link')
        time.sleep(load_time)

    def profile_page(self, username):
        self.bot.get('https://www.instagram.com/'+username+'/')
        time.sleep(load_time)

    def _get_usernames_from_list(self):
        bot = self.bot
        time.sleep(load_time)
        try:
            sugg = bot.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
            bot.execute_script('arguments[0].scrollIntoView()',sugg)
            time.sleep(load_time)
        except:
            print("suggestions aren't appeared!")

        # getting the scroll box
        scroll_box = bot.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        prev_ht, curr_ht = 0, 1
        while prev_ht != curr_ht:
            prev_ht = curr_ht
            time.sleep(load_time)
            curr_ht = bot.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [each_name.text for each_name in links if each_name.text != '' ]
        # close the window
        bot.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()
        return names

    def get_followers(self):
        bot = self.bot
        self._my_profile()
        # to open follwer list from your profile
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
        followers = self._get_usernames_from_list()
        return followers

    def get_following(self):
        bot = self.bot
        self._my_profile()
        # to open following list from the profile
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
        following = self._get_usernames_from_list()
        return following

    def get_unfollowers(self):
        followers = self.get_followers()
        followings = self.get_following()

        people_that_dont_followback = [user for user in followings if user not in followers]
        print(people_that_dont_followback)
        print(len(people_that_dont_followback))

        # return people_that_dont_followback


ponder = instagram_handler(details.username, details.password)
ponder.login()
ponder.get_unfollowers()
ponder.logout()
time.sleep(load_time)
ponder.bot.quit()
