import sys
import threading
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMessageBox,QScrollArea
from PyQt5.QtCore import Qt
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

jscommand = """
    following = document.querySelector("._aano");
    following.scrollTo(0, following.scrollHeight);
    var lenOfPage=following.scrollHeight;
    return lenOfPage;
    """

IG_URL = 'http://instagram.com/'

label_font = QFont("Times", 16)
label_font_right = QFont("Times", 10)
btn_font = QFont("Times", 16, QFont.Bold)

class UserInterFace(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Find Unfollowers")
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        #Left Side
        
        left_side= QWidget()
        left_layout= QVBoxLayout()
        left_side.setLayout(left_layout)
        left_side.setStyleSheet("background-color:rgb(40,44,52)")
        
        self.text_input1 = QLineEdit()
        self.text_input1.setStyleSheet("min-height:30px;border-radius:5px;border:1px solid #999999;padding-left:10px;color:white;")
        self.text_input1.setPlaceholderText("Instagram Username")
        left_layout.addWidget(self.text_input1)
        
        self.text_input2 = QLineEdit()
        self.text_input2.setStyleSheet("min-height:30px;border-radius:5px;border:1px solid #999999;padding-left:10px;color:white;")
        self.text_input2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.text_input2.setPlaceholderText("Instagram Password")
        left_layout.addWidget(self.text_input2)
        
        self.button = QPushButton("Start")
        self.button.setStyleSheet("min-height:40px;border-radius:10;background-color:darkred")
        left_layout.addWidget(self.button)
        self.button.setFont(btn_font)
        self.button.clicked.connect(self.start)
        palette = self.button.palette()
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.white)
        self.button.setPalette(palette)
        
        #Right Side
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
                
        right_side= QWidget()
        right_layout= QVBoxLayout()
        right_side.setLayout(right_layout)
        right_side.setStyleSheet("background-color:rgb(51,56,56)")        
        
        self.label1 = QLabel("Following: 0")
        self.label1.setStyleSheet("color:white")
        self.label1.setFont(label_font_right)
        right_layout.addWidget(self.label1)
    
        self.label2 = QLabel("Followers: 0")
        self.label2.setStyleSheet("color:white")
        self.label2.setFont(label_font_right)
        right_layout.addWidget(self.label2)
        
        self.label3 = QLabel("Unfollowers Number: 0")
        self.label3.setStyleSheet("color:white")
        self.label3.setFont(label_font_right)
        right_layout.addWidget(self.label3)

        self.label4 = QLabel("Unfollowers:")
        self.label4.setStyleSheet("color:white")
        self.label4.setFont(label_font_right)
        self.label4.setAlignment(Qt.AlignTop) 

        scroll_area.setWidget(self.label4) 
        scroll_area.setMaximumHeight(50 * self.label4.fontMetrics().lineSpacing())

        right_layout.addWidget(scroll_area)

        #Main
        
        main_layout.addWidget(left_side, stretch=7) 
        main_layout.addWidget(right_side,3)   
        
        self.setCentralWidget(main_widget)
        self.show()
        self.resize(700,500)

    def load_session(self):
        self.following1 = 0
        self.followers1 = 0
        self.context=[]
        
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--lang=en")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        driver.get(IG_URL)
        wait = WebDriverWait(driver, 10)  
        try:
            #Login
            usernameField = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input")))
            usernameField.send_keys(self.text_input1.text())

            passwordField = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input")))
            passwordField.send_keys(self.text_input2.text())

            LoginButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginForm']/div/div[3]/button")))
            LoginButton.click()
            
            
            #notifications1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text() = "Not Now"]')))
            #notifications1.click()

            #notifications2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text() = "Not Now"]')))
            #notifications2.click()
            sleep(7)
            user_page_url = IG_URL + self.text_input1.text()
            driver.get(user_page_url)

            #GetFollowing

            following_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/following/']")))
            following_element.click()
            sleep(2)

            lenOfPage = driver.execute_script(jscommand)
            match = False
            while(match==False):
                lastCount = lenOfPage
                sleep(1.5)
                lenOfPage = driver.execute_script(jscommand)
                if lastCount == lenOfPage:
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._aacl._aaco._aacw._aacx._aad7._aade")))
                    match = True
            followingList = []
            
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._aacl._aaco._aacw._aacx._aad7._aade")))
            following = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")
            for follow in following:
                followingList.append(follow.text)
                self.following1 += 1
            self.label1.setText("Following: " + str(self.following1))
            
            #GetFollowers

            driver.get(user_page_url)
            followers_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/followers/']")))
            followers_element.click()
            sleep(2)
            match = False
            while not match:
                lastCount = lenOfPage
                sleep(1.5)
                lenOfPage = driver.execute_script(jscommand)
                if lastCount == lenOfPage:
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._aacl._aaco._aacw._aacx._aad7._aade")))
                    match = True   
            sleep(1)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._aacl._aaco._aacw._aacx._aad7._aade")))
            followers = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")  
            followersList = []    
            for follower in followers:
                followersList.append(follower.text)
                self.followers1 += 1
            self.label2.setText("Followers: " + str(self.followers1))
            #Unfollowers
            self.followers_set = set(followersList)
            self.following_set = set(followingList)
            unmatched_following = self.following_set - self.followers_set

            for item in unmatched_following:
                self.context.append(item)
                
            self.label4.setText("Unfollowers:\n" + "\n".join(self.context))
            
            unmatched_following_count = len(unmatched_following)
            self.label3.setText("Total Unfollowers: " + str(unmatched_following_count))

        except TimeoutException:
            error_message = QMessageBox()
            error_message.setWindowTitle("Timeout Error")
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText("Timed out while waiting for an element to load. Please try again.")
            error_message.exec_()
            driver.quit()

        except ElementClickInterceptedException:
            error_message = QMessageBox()
            error_message.setWindowTitle("Click Intercept Error")
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText("Click on an element was intercepted. Please try again.")
            error_message.exec_()
            driver.quit()

        except Exception as e:
            error_message = QMessageBox()
            error_message.setWindowTitle("Error")
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText("Something went wrong. Please try again.")
            error_message.exec_()
            driver.quit()
            
        finally:
            driver.quit()
            self.button.setEnabled(True)
            self.text_input1.clear()
            self.text_input2.clear()
        
    def start(self):
        if not self.text_input1.text() or not self.text_input2.text():
            message = QMessageBox()
            message.setWindowTitle("Input Error")
            message.setText("Please fill in all inputs")
            message.exec_()
        else:
            self.label1.setText("Following: 0")
            self.label2.setText("Followers: 0")
            self.label3.setText("Total Unfollowers: 0")
            self.label4.setText("Unfollowers:")
            self.button.setEnabled(False)
            
            thread = threading.Thread(target=self.load_session)
            thread.start()

if __name__ == "__main__":
    app= QApplication(sys.argv)
    ui = UserInterFace()
    ui.show()
    sys.exit(app.exec_())