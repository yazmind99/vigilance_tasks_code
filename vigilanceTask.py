# Import necessary libraries
import pandas as pd
from psychopy import visual, core, event
import random
import math
from psychopy.data import ExperimentHandler

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
win = visual.Window([1500,800], monitor="testMonitor", units="deg")

# Create text stimuli
text = visual.TextStim(win, height = 3)

# Screen buttons/texts
text_screen1 = visual.TextStim(win, text='Insert instructions here.', height=1, color='black', pos=(0,5))
text_screen2 = visual.TextStim(win, text='Insert task details here.', height = 1, color='black', pos=(0,5))
text_screen3 = visual.TextStim(win, text='Are you ready to begin a practice run? Click "next" to begin the task.', height = 1, color='black', pos=(0,5))
text_screen4 = visual.TextStim(win, text='You have completed the practice run, you will now complete the entire task.', height = 1, color='black', pos=(0,5))
text_screen5 = visual.TextStim(win, text='Are you ready to begin the task? Click "next" to begin the task.', height = 1, color='black', pos=(0,5))
text_screen6 = visual.TextStim(win, text='You have completed the task, good job! Thank you for participating!', height = 1, color='black', pos=(0,5))

max_count_practice = 15 # 5 minutes # temporarily changed to 30 seconds
max_count_experiment = 16 # 60 minutes # temporarily changed to 48 seconds

stored_data = {
    'practice_hits': [],
    'main_hits': [],
    'practice_miss': [], 
    'main_miss': [],
    'practice_fa': [],
    'main_fa': [],
    'practice_reject': [],
    'main_reject': [],
    'practice_hit_mean_rt': [],
    'practice_fa_mean_rt': [],
    'practice_miss_mean_rt': [],
    'main_hit_mean_rt': [],
    'main_fa_mean_rt': [],
    'main_miss_mean_rt': []
}

def save_data(stored_data):
    df = pd.DataFrame(columns=['Type', 'Hits', 'Hit Reaction Time', 'Misses', 'Miss Reaction Time', 
    'False Alarms', 'FA Reaction Time', 'Correct Rejections'])
    
    # Storing practice values
    for i in range(len(stored_data['practice_hits'])):
        df = df.append({'Type': 'Practice', 'Hits': stored_data['practice_hits'][i], 'Hit Reaction Time': stored_data['practice_hit_mean_rt'][i]},
        ignore_index=True)
    
    for i in range(len(stored_data['practice_miss'])):
        df = df.append({'Type': 'Practice', 'Misses': stored_data['practice_miss'][i], 'Miss Reaction Time': stored_data['practice_miss_mean_rt'][i]},
        ignore_index=True)
        
    for i in range(len(stored_data['practice_fa'])):
        df = df.append({'Type': 'Practice', 'False Alarms': stored_data['practice_fa'][i], 'FA Reaction Time': stored_data['practice_fa_mean_rt'][i]},
        ignore_index=True)

    for i in range(len(stored_data['practice_reject'])):
        df = df.append({'Type': 'Practice', 'Correct Rejections': stored_data['practice_reject'][i]},
        ignore_index=True)
    
    # Storing main values
    for i in range(len(stored_data['main_hits'])):
        df = df.append({'Type': 'Main', 'Hits': stored_data['main_hits'][i], 'Hit Reaction Time': stored_data['main_hit_mean_rt'][i]},
        ignore_index=True)
    
    for i in range(len(stored_data['main_miss'])):
        df = df.append({'Type': 'Main', 'Misses': stored_data['main_miss'][i], 'Miss Reaction Time': stored_data['main_miss_mean_rt'][i]},
        ignore_index=True)
        
    for i in range(len(stored_data['main_fa'])):
        df = df.append({'Type': 'Main', 'False Alarms': stored_data['main_fa'][i], 'FA Reaction Time': stored_data['main_fa_mean_rt'][i]},
        ignore_index=True)

    for i in range(len(stored_data['main_reject'])):
        df = df.append({'Type': 'Main', 'Correct Rejections': stored_data['main_reject'][i]},
        ignore_index=True)
    
    # to change it to your directory
    df.to_csv(r'C:\Users\yesse\OneDrive\Documents\experiment_data.csv', index=False)

def experiment(max_count, exp_handler, stored_data):
    # setting the beginning variables
    count = 0
    first_index = 0
    second_index = 15
    hit_interval = 30
    #rt_list = []
    
    while count < max_count: #runs as long as specified in function parameter
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
            response_time = keys[0][1]              # seconds
            response_time_ms = response_time * 1000 # milliseconds
            
            # Check if the response is correct or incorrect
            if is_critical(digit, next_digit):
                feedback_text = "Correct ✓"
                text.color = '#03C04A'
                text.bold = True
                # if conditional to tell if its practice
                if max_count == max_count_practice:
                    stored_data['practice_hits'].append(1)
                    stored_data['practice_hit_mean_rt'].append(response_time_ms)
                if max_count == max_count_experiment:
                    stored_data['main_hits'].append(1)
                    stored_data['main_hit_mean_rt'].append(response_time_ms)

                

            else:
                feedback_text = "Wrong ❌"
                text.color = '#FF0000'
                text.bold = True
                if max_count == max_count_practice:
                    stored_data['practice_fa'].append(1)
                    stored_data['practice_fa_mean_rt'].append(response_time_ms)
                if max_count == max_count_experiment:
                    stored_data['main_fa'].append(1)
                    stored_data['main_fa_mean_rt'].append(response_time_ms)
            

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
                if max_count == max_count_practice:
                    stored_data['practice_miss'].append(1)
                    stored_data['practice_miss_mean_rt'].append(response_time_ms)
                if max_count == max_count_experiment:
                    stored_data['main_miss'].append(1)
                    stored_data['main_miss_mean_rt'].append(response_time_ms)

            else:
                feedback_text = "+"
                text.color = 'white'
                if max_count == max_count_practice:
                    stored_data['practice_reject'].append(1)
                if max_count == max_count_experiment:
                    stored_data['main_reject'].append(1)
            
            text.text = feedback_text
            text.draw()
            win.flip()
            core.wait(1)
        
        text.bold = False
        
        # Store data for each trial
        exp_handler.addData('Practice Hits', stored_data['practice_hits'])
        exp_handler.addData('Practice Miss', stored_data['practice_miss'])
        exp_handler.addData('Practice False', stored_data['practice_fa'])
        exp_handler.addData('Practice Rejection', stored_data['practice_reject'])
        exp_handler.addData('practice_hit_mean_rt', stored_data['practice_hit_mean_rt'])
        exp_handler.addData('practice_fa_mean_rt', stored_data['practice_fa_mean_rt'])
        exp_handler.addData('practice_miss_mean_rt', stored_data['practice_miss_mean_rt'])
        
        exp_handler.addData('Main Hits', stored_data['main_hits'])
        exp_handler.addData('Main Miss', stored_data['main_miss'])
        exp_handler.addData('Main False', stored_data['main_fa'])
        exp_handler.addData('Main Rejection', stored_data['main_reject'])
        exp_handler.addData('main_hit_mean_rt', stored_data['main_hit_mean_rt'])
        exp_handler.addData('main_fa_mean_rt', stored_data['main_fa_mean_rt'])
        exp_handler.addData('main_miss_mean_rt', stored_data['main_miss_mean_rt'])
       
        # Clear keyList to ignore accidental key presses during the ISI
        event.getKeys(keyList=['space'], timeStamped=True)

exp_handler = ExperimentHandler()

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

#-------------[Practice Experiment Loop]-------------#

if action == 'start_task':
    experiment(max_count_practice, exp_handler, stored_data)
    

#-------------[Continue To Screens 4-5]-------------#

current = 4

while current <= 5:
    if current == 4:
        action = screen_changer(screen_text=text_screen4, button1_check=False, button1_action='previous', button2_action='next')
    elif current == 5:
        action = screen_changer(screen_text=text_screen5, button1_check=True, button1_action='previous', button2_action='start_task')
    
    if action == 'start_task':
        break
    
    if action == 'previous':
        current -= 1
    elif action == 'next':
        current+= 1


#-------------[Main Experiment Loop]-------------#

if action == 'start_task':
    experiment(max_count_experiment, exp_handler, stored_data)
     
save_data(stored_data)

current = 6

while current == 6:
    action = screen_changer(screen_text=text_screen6, button1_check=False, button1_action='previous', button2_action='start_task')
    
    if action == 'next':
        current+= 1