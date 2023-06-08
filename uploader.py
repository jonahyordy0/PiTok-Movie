import os
import pyautogui
import webbrowser
import time
import pyperclip

url = 'https://www.tiktok.com/upload?lang=en'
clipsloc = r'home/' + os.getlogin() +'/Desktop/tt/clips '

def upload(filename, account):
    # Make sure no chrome browser already exists
    os.system("killall chromium-browser")
    time.sleep(2)

    # Print display size to ensure using virtual display
    sW, sH = pyautogui.size()
    print(sW,sH)

    print(account)
    
    # Open chrome to current profile
    os.system('chromium-browser tiktok.com/upload --profile-directory="Profile ' + str(account) +'" &')
    time.sleep(20)
    # Open Upload Prompt
    for i in range(5):
        pyautogui.press('tab')
        time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    print(clipsloc+filename)

    # Type in file location
    pyautogui.press('/')
    pyperclip.copy(clipsloc+filename)
    time.sleep(3)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)

    # Upload to file input
    pyautogui.press('enter')
    time.sleep(120)

    # Check if upload was successful
    pyautogui.hotkey('shift', 'tab')
    time.sleep(3)
    pyautogui.moveTo(sW*0.475,sH*0.475)
    time.sleep(3)
    
    t = pyautogui.locateOnScreen('button.png', confidence=0.8)
    
    if t is not None:
        print("Upload Success")
        pyautogui.press('enter')
        time.sleep(15)
        os.system("killall chromium-browser")
    else:
        print("Upload Failed Trying Again")
        time.sleep(5)
        upload(filename, account)

if __name__ == "__main__":
    upload("#rick #rickandmorty #foryou #fyp #morty #movie #game #❤️❤️.mp4", 2)
