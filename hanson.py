import time
import fluidsynth
from grovepi import *

# Start up fluidsynth and set the driver to alsa
fs = fluidsynth.Synth()
fs.start(driver="alsa")

# Set the volume to any value between 0 - 127
volume = 127

# Load the SoundFont2 file
sfid = fs.sfload("x.sf2")
fs.program_select(0, sfid, 0, 0)

# Holds to value where the hanson should stop playing sounds when there is not enough
# light. Value between 0 - 1024. 100 is recommended.
light_sensor_cutoff = 100

# Light Sensor is on pin A0
light_sensor = 0
pinMode(light_sensor, "INPUT")

#Set up all the buttons according to their pin location
button_one = 5
pinMode(light_sensor, "INPUT")

button_two = 4
pinMode(light_sensor, "INPUT")

button_three = 3
pinMode(light_sensor, "INPUT")

button_four = 2
pinMode(light_sensor, "INPUT")

# Reads the light sensor for its current value and returns it
def readLightSensor():
    light_sensor_value = analogRead(light_sensor)
    # print("light_sensor_value = %d" % (light_sensor_value))
    return light_sensor_value;

# Checks the button status of the button passed through and returns it
def getButtonStatus(button_number):
    button_status = digitalRead(button_number)
    # print("button = %d" % (button_number))
    # print("status = %d" % (button_status))
    return button_status

# Turns off the no button sound and starts the note passed through. An empty loop is used
# so the note doesn't play a jerky sound, but a continuous sound while the conditions are met
# Then turns off the note and returns to the main loop
def playNote(note, button_number):
    fs.noteoff(0, 60)
    fs.noteon(0, note, volume)
    while readLightSensor() >= light_sensor_cutoff and getButtonStatus(button_number):
        pass
    fs.noteoff(0, note)

# The main loop to check of there is enough light to play music and which button is down to
# start playing a note.
while True:
    try:
        if (readLightSensor() >= light_sensor_cutoff):
            if getButtonStatus(button_one):
                playNote(62, button_one)
            elif getButtonStatus(button_two):
                playNote(64, button_two)
            elif getButtonStatus(button_three):
                playNote(67, button_three)
            elif getButtonStatus(button_four):
                playNote(69, button_four)
            else:
                fs.noteon(0, 60, volume)
        else:
            fs.noteoff(0, 60)
    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")
