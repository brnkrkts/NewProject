
# Instagram Unfollowers Finder

## Overview

The **Instagram Unfollowers Finder** is a Python program built using the PyQt5 framework and the Selenium web automation library. It allows you to find users who were previously following you on Instagram but have unfollowed you since.

The program interacts with the Instagram website, logs in with the provided username and password, and then retrieves the list of users you're following and your followers. By comparing these lists, it identifies the users who are no longer following you back, and displays them along with some statistics.

## Prerequisites

Before using the Instagram Unfollowers Finder, make sure you have the following installed:

- Python 3.x
- PyQt5 (`pip install PyQt5`)
- Selenium (`pip install selenium`)
- ChromeDriver (automatically installed using `webdriver_manager`)

## How to Use

1. Run the program by executing the `main.py` script using Python.
2. The program's graphical user interface will open.
3. Enter your Instagram username and password in the provided input fields.
4. Click the **Start** button to initiate the process.
5. The program will open a Chrome browser window and perform the following steps:
   - Log in to your Instagram account.
   - Retrieve the list of users you're following.
   - Retrieve the list of your followers.
   - Identify users who unfollowed you.
6. Once the process is complete, the program will display the following information:
   - Number of users you're following
   - Number of your followers
   - Number of users who unfollowed you
   - List of usernames who unfollowed you

## Important Notes

- This program requires your Instagram username and password to log in. Please ensure that you are using the program in a secure environment and that you are complying with Instagram's terms of use.
- The program uses the Chrome browser for automation. It automatically installs the necessary ChromeDriver using the `webdriver_manager` library.

## Troubleshooting

If you encounter any issues while using the program, such as timeouts, element not found errors, or any unexpected behavior, you can consider the following steps:

1. Make sure you have a stable internet connection.
2. Verify that you have entered your Instagram username and password correctly.
3. If you encounter any errors related to ChromeDriver or the Chrome browser, consider updating your Chrome browser or manually installing ChromeDriver.

## Disclaimer

This program is provided for educational and informational purposes only. The use of automated tools to interact with websites, including Instagram, might be against the terms of service of these websites. Use this program responsibly and at your own risk. The creators of this program are not responsible for any misuse or violations of terms of service.

