#starting fresh
#Made By Jack0wack0  https://www.github.com/jack0wack0 
import cv2 
import time
import os
import sys
from pydub import AudioSegment
from pydub.playback import play
from colorama import init, Fore, Style

# for playing mp3 file
song = AudioSegment.from_mp3("/Users/jacksonyoes/Downloads/confirm-ding.mp3")
song2 = AudioSegment.from_mp3("/Users/jacksonyoes/Downloads/negative-beep.mp3")

#QR CODE NAMES GO HERE!!!
#if you want to add a new battery, create a new variable and put it here! also add the variable number to  wherever the other ones are idk
bat1 = "Battery 1"
bat2 = "Battery 2"
bat3 = "Battery 3"
bat4 = "Battery 4"
bat5 = "Battery 5"
bat6 = "Battery 6"
bat7 = "Battery 7"
bat8 = "Battery 8"
bat9 = "Battery 9"
bat10 = "Battery 10"
bat11 = "Battery 11"
bat12 = "Battery 12"
bat13 = "Battery 13"
bat14 = "Battery 14"
bat15 = "Battery 15"
bat16 = "Battery 16"
bat17 = "Battery 17"
bat18 = "Battery 18"
bat19 = "Battery 19"
bat20 = "Battery 20"

#////////////////////////////////////////////////////////////////
#start timer
def start_timer():
    return time.time()

#stop timer, calculate time
def stop_timer(start_time):
    return time.time() - start_time

#init camera + constant
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
start_time = None
os.system("clear")
#bro is excited!
print("ready to scan!")

# Initialize colorama
init()

# Create a dictionary to store the start times for each battery
battery_timers = {bat1: None, bat2: None, bat3: None, bat4: None, bat5: None, bat6: None, bat7: None, bat8: None, bat9: None, bat10: None, bat11: None, bat12: None, bat13: None, bat14: None, bat15: None, bat16: None, bat17: None, bat18: None, bat19: None, bat20: None}

# Initialize a timer for updating the display
update_interval = 2  #in seconds

#do the thing
next_update_time = time.time() + update_interval

# QR code scanning timeout (adjust as needed)
qr_code_scan_timeout = 5  # in seconds

# Redirect standard output to ensure immediate display
sys.stdout = sys.stderr

# Continuous loop until "StopProcess" QR code is detected. If you want to make this qr code just generate one with
# the text "StopProcess" or just change it wherever it is idk 
while True:
    start_time_qr_scan = time.time()  # Record the start time of QR code scanning

    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            break

        # Check if QR code scanning has taken too long, and proceed if necessary
        if time.time() - start_time_qr_scan >= qr_code_scan_timeout:
            break

    if data in [bat1, bat2, bat3, bat4, bat5, bat6, bat7, bat8, bat9, bat10, bat11, bat12, bat13, bat14, bat15, bat16, bat17, bat18, bat19, bat20]:
        if battery_timers[data] is None:
            print(f"QR code scanned. Starting timer for {data}.", flush=True)
            battery_timers[data] = time.time()
            play(song) #unfortunately this stupid thing adds a bunch of clutter to the terminal. Idk how to get it to go away but whatever
        else:
            elapsed_time = time.time() - battery_timers[data]
            print(f"QR code scanned again. Timer stopped for {data}. Elapsed time: {elapsed_time:.2f} seconds", flush=True)
            battery_timers[data] = None
            play(song2)

    #here is the thing i was talking about earlier. if you want to change it, change it.
    if data == "StopProcess":
        print("StopProcess detected. Stopping the process.", flush=True)
        break

    time.sleep(3)  # Sleep for 3 seconds for QR code scanning, so it doesnt just scan it again immediately.

    # Check if it's time to update the display
    #theres defo a better way to do all of this, but i finished the project so i dont care anymore.
    current_time = time.time()
    if current_time >= next_update_time:
        # get the gross ugly terminal junk outta here
        os.system("clear")

        # Calculate the charging times for all batteries and sort them
        charging_times = {battery: current_time - timer if timer is not None else 0 for battery, timer in battery_timers.items()}
        sorted_charging_times = sorted(charging_times.items(), key=lambda x: x[1], reverse=True)

        # Display the batteries in the order of their charging times and make it all pretty
        print("Batteries in order of charging time:", flush=True)
        for i, (battery, charging_time) in enumerate(sorted_charging_times):
            if charging_time == 0:
                print(f"{battery}: Not charging", flush=True)
            else:
                # Color the first two batteries green
                if i < 2:
                    print(f"{Fore.GREEN}{battery}: {charging_time:.2f} seconds{Style.RESET_ALL}", flush=True)
                # Color the next three batteries yellow
                elif 2 <= i < 5:
                    print(f"{Fore.YELLOW}{battery}: {charging_time:.2f} seconds{Style.RESET_ALL}", flush=True)
                else:
                    print(f"{battery}: {charging_time:.2f} seconds", flush=True)

        # Reset the update timer
        next_update_time = current_time + update_interval

# Find the battery with the longest charging time
longest_charging_battery = max(battery_timers, key=lambda x: battery_timers[x] if battery_timers[x] is not None else 0)
print(f"IGNORE THIS ITS FOR DEBUGGING!!! The battery with the longest charging time is {longest_charging_battery}.", flush=True)

#make the camera thing shut up
cap.release()
cv2.destroyAllWindows()