# Test change
# Import necessary libraries
from psychopy import visual, core, event
import random

random.seed(0)

# Function to generate random double digit
def generate_double_digit():
    return random.randint(0, 9)

# Function to determine if the difference between two digits is 0 or 1
def is_correct(digit1, digit2):
    diff = abs(digit1 - digit2)
    return diff == 0 or diff == 1

# Create a window
win = visual.Window([800,600], monitor="testMonitor", units="deg")

# Create text stimuli
text = visual.TextStim(win)

# setting the beginning variables
count = 1
num_hits = 0
max_hits = 2

# Main experiment loop
while True:
    # making sure that the program stops after 900 nums
    if count > 900:
        break

    # Generate random double digit
    digit = generate_double_digit()

    # Generate another random double digit
    next_digit = generate_double_digit()
    
    # counting the amount of hits
    if is_correct(digit, next_digit):
        num_hits = num_hits + 1
    
    # if the number of hits are larger than 2 then make a new number
    # that does not generate a hit
    if num_hits > max_hits:
        while(is_correct(digit, next_digit)):
            digit = generate_double_digit()
            next_digit = generate_double_digit()

    # restarting the hit count after 30 numbers
    if count % 30 == 0:
        num_hits = 0
    

    # putting digit and next_digit together
    new_digit = str(digit) + str(next_digit)
    text.text = str(new_digit)
    text.draw()
    win.flip()
    core.wait(1)

    # Check for keyboard input
    keys = event.getKeys(keyList=['space'], timeStamped=True)

    if keys:
        # Check if the response is correct or incorrect
        if is_correct(digit, next_digit):
            feedback_text = "Correct"

        else:
            feedback_text = "Incorrect"

        # Display feedback
        text.text = feedback_text
        text.draw()
        win.flip()
        core.wait(1) # Display feedback for 1 second

    else:
        # Display fixation cross
        text.text = "+"
        text.draw()
        win.flip()
        core.wait(1)
    
        count = count + 1