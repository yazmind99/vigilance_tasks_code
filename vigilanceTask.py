# Import necessary libraries
from psychopy import visual, core, event
import random
import math

#If we want to use random numbers:
#import time
#random.seed(time.gmtime())
random.seed(0)

#-------------[Creating Functions]-------------#
# Function to generate random double digit
def generate_digit():
    return random.randint(0, 9)
    
# Function that generates index from 0 to 29
def index_generator():
    return random.randint(0, 29)

# Function that checks if the digits are a hit or not
def is_critical(digit1, digit2):
    diff = abs(digit1 - digit2)
    if diff == 0 or diff == 1:
        return True
    else:
        return False

#-------------[Declaring Variables]-------------#
# Create a window
win = visual.Window([800,600], monitor="testMonitor", units="deg")

# Create text stimuli
text = visual.TextStim(win, height = 3)

# setting the beginning variables
count = 0
max_count = 150

hit_interval = 30

first_index = 0
second_index = 15

#-------------[Main Experiment Loop]-------------#
while count < max_count: #runs 150 times (count 0-149)
    
    i = count % hit_interval # Current index (0-29) in this set of 30
    
    # Generate indecies every 30 numbers
    if i == 0:
        first_index = index_generator()
        second_index = index_generator()
        
        # Regenerate second_index if indecies are equal by chance
        while first_index == second_index:
            second_index = index_generator()
    
    # Generate random double digits
    digit = generate_digit()
    next_digit = generate_digit()
    
    # If a critical signal is needed, regenerate next_digit until it's critical
    if (i == first_index or i == second_index):
        while(not is_critical(digit, next_digit)):
            next_digit = generate_digit()
            
    # Otherwise, regenerate next_digit until not a critical signal
    else:
        while(is_critical(digit, next_digit)):
            next_digit = generate_digit()
        
    count += 1
    
    #-------------[Display + Input Section]-------------#
    
    # putting digit and next_digit together
    new_digit = str(digit) + str(next_digit)
    text.text = str(new_digit)
    text.color = 'white'
    text.draw()
    win.flip()
    core.wait(1)

    # Check for keyboard input
    keys = event.getKeys(keyList=['space'], timeStamped=True)

    if keys:
        # Check if the response is correct or incorrect
        if is_critical(digit, next_digit):
            feedback_text = "Correct ✓"
            text.color = (0.5, 1, 0.5)

        else:
            feedback_text = "Wrong ❌"
            text.color = 'red',

        # Display feedback
        text.text = feedback_text
        text.draw()
        win.flip()
        core.wait(1) # Display feedback for 1 second

    else:
        # Was it a correct rejection?
        if is_critical(digit, next_digit):
            feedback_text = "Miss ❌"
            text.color = 'red'

        else:
            feedback_text = "+"
            text.color = 'white'
        
        text.text = feedback_text
        text.draw()
        win.flip()
        core.wait(1)
    
    # Clear keyList to ignore accidental key presses during the ISI
    event.getKeys(keyList=['space'], timeStamped=True)