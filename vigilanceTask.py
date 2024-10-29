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

# Function that changes "screens"
def screen_changer(screen_text, button1_check = None, button1_action='previous', button2_action='next'): 
    mouse = event.Mouse(win=win)
    screen_text.draw()
    
    if button1_check:
        button1 = visual.Rect(win, width=6, height=2, fillColor='white', pos=(-5,-5))
        button1_text = visual.TextStim(win, text='Previous', height=1, color='black', pos=(-5,-5))
        button2 = visual.Rect(win, width=6, height=2, fillColor='white', pos=(5,-5))
        button2_text = visual.TextStim(win, text='Next', height=1, color='black', pos=(5,-5))        
        button1.draw()
        button1_text.draw()
        button2.draw()
        button2_text.draw()
    else:
        button2 = visual.Rect(win, width=6, height=2, fillColor='white', pos=(0,-5))
        button2_text = visual.TextStim(win, text='Next', height=1, color='black', pos=(0,-5))        
        button2.draw()
        button2_text.draw()
    
    win.flip()

    while True:
        if button1_check and mouse.isPressedIn(button1):
            core.wait(0.2)
            return button1_action
        
        if mouse.isPressedIn(button2):
            core.wait(0.2)
            return button2_action

#-------------[Declaring Variables]-------------#
# Create a window
win = visual.Window([800,600], monitor="testMonitor", units="deg")

# Create text stimuli
text = visual.TextStim(win, height = 3)

# Screen buttons/texts
text_screen1 = visual.TextStim(win, text='Insert instructions here.', height=1, color='black', pos=(0,5))
text_screen2 = visual.TextStim(win, text='Insert task details here.', height = 1, color='black', pos=(0,5))
text_screen3 = visual.TextStim(win, text='Are you ready to begin a practice run? Click "next" to begin the task.', height = 1, color='black', pos=(0,5))
text_screen4 = visual.TextStim(win, text='You have completed the practice run, you will now complete the entire task.', height = 1, color='black', pos=(0,5))
text_screen5 = visual.TextStim(win, text='Are you ready to begin the task? Click "next" to begin the task.', height = 1, color='black', pos=(0,5))

# setting the beginning variables
count = 0
max_count = 150
hit_interval = 30
first_index = 0
second_index = 15

#-------------[Start At Screens 1-3]-------------#

current = 1

while current <= 5:
    if current == 1:
        action = screen_changer(screen_text=text_screen1, button1_check=False, button1_action='previous', button2_action='next')
        
    elif current == 2:
        action = screen_changer(screen_text=text_screen2, button1_check=True, button1_action='previous', button2_action='next')
    
    elif current == 3:
        action = screen_changer(screen_text=text_screen3, button1_check=True, button1_action='previous', button2_action='start_task')
    
    if action == 'start_task':
        break
    
    if action == 'previous':
        current -= 1
    elif action == 'next':
        current += 1

#-------------[Main Experiment Loop]-------------#

if action == 'start_task':
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
                text.color = '#03C04A'
                text.bold = True
                

            else:
                feedback_text = "Wrong ❌"
                text.color = '#FF0000'
                text.bold = True
                text.outlineColor = 'black'
                text.outline = 100


            # Display feedback
            text.text = feedback_text
            text.draw()
            win.flip()
            core.wait(1) # Display feedback for 1 second

        else:
            # Was it a correct rejection?
            if is_critical(digit, next_digit):
                feedback_text = "Miss ❌"
                text.color = '#FF0000'
                text.bold = True

            else:
                feedback_text = "+"
                text.color = 'white'
            
            text.text = feedback_text
            text.draw()
            win.flip()
            core.wait(1)
        
        text.bold = False
        
        # Clear keyList to ignore accidental key presses during the ISI
        event.getKeys(keyList=['space'], timeStamped=True)

#-------------[Continue To Screens 4-5]-------------#

current = 4

while current <= 5:
    if current == 4:
        action = screen_changer(screen_text=text_screen4, button1_check=False, button1_action='previous', button2_action='next')
    elif current == 5:
        action = screen_changer(screen_text=text_screen5, button1_check=True, button1_action='previous', button2_action='next')
    
    if action == 'previous':
        current -= 1
    elif action == 'next':
        current+= 1

