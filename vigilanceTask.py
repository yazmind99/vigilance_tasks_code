# Import necessary libraries
from psychopy import visual, core, event
import random
import math
random.seed(0)

#-------------[Creating Functions]-------------#
# Function to generate random double digit
def generate_digit():
    return random.randint(0, 9)

# Function that makes a random percentage for the first check
def generate_check1_percent():
    return round(random.uniform(0.50, 0.67), 2)

# Function that makes a random percentage for the second check
def generate_check2_percent():
    return round(random.uniform(0.73, 0.97), 2)

# Function that checks if the digits are a hit or not
def is_correct(digit1, digit2):
    diff = abs(digit1 - digit2)
    if diff == 0 or diff == 1:
        return True
    else:
        return False

# Function that generates the first check number
def check1_generator(hit_interval):
    percent = generate_check1_percent()
    mult = math.ceil(percent * hit_interval)
    return mult

# Function that generates the first check number
def check2_generator(hit_interval):
    percent = generate_check2_percent()
    mult = math.ceil(percent * hit_interval)
    return mult

def array_append(no_double, digit1, digit2):
    if(is_correct(digit1, digit2) == True):
        no_double.append(True)
    else:
        no_double.append(False)
    if len(no_double) > 2:
        no_double.pop(0)

#-------------[Declaring Variables]-------------#
# Create a window
win = visual.Window([800,600], monitor="testMonitor", units="deg")

# Create text stimuli
text = visual.TextStim(win)

# setting the beginning variables
count = 1
max_count = 900

hit_interval = 30
count_per_interval = 1

num_hits = 0
max_hits = 2

no_double = []

# Generate the first and second check numbers
check1 = check1_generator(hit_interval)
check2 = check2_generator(hit_interval)

#-------------[Main Experiment Loop]-------------#
while True:    
    # making sure that the program stops after 900 nums
    if count > max_count:
        break
    
    # Generate random double digits
    digit = generate_digit()
    next_digit = generate_digit()
    
    # Counting the amount of hits   
    if (is_correct(digit, next_digit) == True):
        num_hits = num_hits + 1
    
    # First check to see if we have hit at least once
    if(num_hits < 1):
        if(count_per_interval == check1):
            while(is_correct(digit, next_digit) == False):
                digit = generate_digit()
                next_digit = generate_digit()
            if(is_correct(digit, next_digit) == True):
                num_hits = num_hits + 1        
    
    # Second check to see if we have hit twice
    if(num_hits < 2):
        if(count_per_interval == check2):
            while(is_correct(digit, next_digit) == False):
                digit = generate_digit()
                next_digit = generate_digit()
            if(is_correct(digit, next_digit) == True):
                num_hits = num_hits + 1
    
    
    array_append(no_double, digit, next_digit)
    # Check for doubles
    if(no_double[0] == True and no_double[1] == True):
        num_hits -= 1
        no_double[1] = False
        while(is_correct(digit, next_digit) == True):
            digit = generate_digit()
            next_digit = generate_digit()
    
    # Check to make sure we don't go over 2 hits
    if (num_hits > max_hits):
        num_hits -= 1
        while(is_correct(digit, next_digit) == True):
            digit = generate_digit()
            next_digit = generate_digit()
    
    # Resetting hit count after 30 numbers
    if count % hit_interval == 0:
        num_hits = 0
    
    # Resetting check numbers
    if count_per_interval == hit_interval:
        check1 = check1_generator(hit_interval)
        check2 = check2_generator(hit_interval)

    # Resetting interval count
    if count_per_interval > hit_interval:
        count_per_interval = 1               
    
    #-------------[Display + Input Section]-------------#
    
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
    
        count += 1  
        count_per_interval += 1