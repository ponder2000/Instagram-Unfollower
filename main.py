import time
import details
from selenium import webdriver

load_time = 2.5

class instagram_handler():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        driver_path = '/usr/local/bin/geckodriver'  # getting the location of the geckodriver
        self.bot = webdriver.Firefox(executable_path=driver_path)   # setting the driver

    # log into your account
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

    # log out from the account
    def logout(self):
        self._my_profile()
        # opening settings
        bot = self.bot
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div/button').click()
        time.sleep(1)
        bot.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()
        print("You are logged out!")

    # nevigate to the your profile page
    def _my_profile(self):
        try:
            self.bot.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a").click()
            print('Profile found using xpath')
        except:
            self.bot.get('https://www.instagram.com/'+self.username+'/')
            print('nevigated to your profile page')
        time.sleep(load_time)

    # nevigaet to profile of people with their username
    def profile_page(self, username):
        self.bot.get('https://www.instagram.com/'+username+'/')
        time.sleep(load_time)

    # return a touple of verified user and non verified user
    # people with and without blue right tick resp.) from given list of users
    def _get_verified_user(self, users):
        verified_usr = []
        not_verified_usr = []
        for usr in users:
            self.profile_page(usr)  # loading their profile page
            try:
                self.bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/span')
                # above will not give error if the user is varified
                verified_usr.append(usr)
            except:
                not_verified_usr.append(usr)
        rslt = (verified_usr, not_verified_usr)
        return rslt

    # prints the users that are not big personality but still
    # doesn't follow you back although you follow them!
    def splitting_verified_and_nonverified(self):
        users = self.get_unfollowers()
        white_list = details.white_list     # this will have list of people whom I don't want to unfollow
        for usr in white_list:
            try:
                users.remove(usr)
                print("White_listed {}".format(usr))
            except:
                print("{} is not in the unfollower list".format(usr))

        result = self._get_verified_user(users)

        print(result[0])
        print(len(result[0]))

        print(result[1])
        print(len(result[1]))

        return result

    def unfollow_users(self):
        res = self.splitting_verified_and_nonverified()
        non_verified = res[1]

        f = open('unfollower_list.txt', 'a')    # saving the names whom I will unfollow for analysis

        for usr in non_verified:
            self.profile_page(usr)
            try:
                # click on following
                self.bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
                # click on unfollow
                self.bot.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]').click()
                time.sleep(load_time)
                print("Unfollowed -> {}".format(usr))
                f.write(str(usr))

            except:
                print("Can't unfollow {}".format(usr))

    # returns a list of user from the follower and following window
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

    # returns list of followers
    def get_followers(self):
        bot = self.bot
        self._my_profile()
        # to open follwer list from your profile
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
        followers = self._get_usernames_from_list()
        return followers

    # returns list of following
    def get_following(self):
        bot = self.bot
        self._my_profile()
        # to open following list from the profile
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
        following = self._get_usernames_from_list()
        return following

    # seperating people who don't follow you
    def get_unfollowers(self):
        followers = self.get_followers()
        followings = self.get_following()

        people_that_dont_followback = [user for user in followings if user not in followers]
        print(people_that_dont_followback)
        print(len(people_that_dont_followback))

        return people_that_dont_followback


def start_operation(username, password):
    ponder = instagram_handler(username, password)
    ponder.login()              # log in to my account
    ponder.unfollow_users()     # unfollow those who doesn't follow me back
    ponder.logout()             # log out from the browser
    time.sleep(5*load_time)
    ponder.bot.quit()           # closing the browser
