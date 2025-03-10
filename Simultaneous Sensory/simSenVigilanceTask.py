# Import necessary libraries
import pandas as pd
import statistics
from psychopy import visual, core, event
import random
import math
import os
from psychopy.data import ExperimentHandler

#If we want to use random numbers:
#import time
#random.seed(time.gmtime())
random.seed(0)

#----------------[LOAD IMAGES]-----------------#
# Arrays to hold critical and noncritical images
critical_images = []
regular_images = []

# Load and sort images into arrays based on their filenames
for filename in os.listdir('graphics'):
    if filename.startswith('critical'):
        critical_images.append(os.path.join('graphics', filename))
    elif filename.startswith('neutral'):
        regular_images.append(os.path.join('graphics', filename))
        
critical_length = len(critical_images) - 1
regular_length = len(regular_images) - 1

#-------------[Creating Functions]-------------#

# Function that generates integer from 0 to number passed
def randUpTo(num):
    return random.randint(0, num)

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
    
    
    # Code specifically to render the participant number screen
    if screen_text == text_screen0:
        response=visual.TextBox2(
            win,
            text="",
            color=[1,1,1],
            borderColor=[1,1,1],
            colorSpace='rgb',
            size=(1,.1),
            pos=(0,0),
            editable=True,
            units='norm')
            
        while True:
            screen_text.draw()
            response.draw()
            button2.draw()
            button2_text.draw()
        
            keys = event.getKeys()
            win.flip()
            
            if mouse.isPressedIn(button2):
                core.wait(0.2)
                stored_data['participant'] = int(response.getText())
                print(stored_data['participant'])
                return button2_action
            
    win.flip()

    while True:
        if button1_check and mouse.isPressedIn(button1):
            core.wait(0.2)
            return button1_action
        
        if mouse.isPressedIn(button2):
            core.wait(0.2)
            return button2_action

# Function that saves the data
def save_data(stored_data, is_practice, block):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_long = os.path.join(script_dir, f"participant{stored_data['participant']}_experiment_data_long.csv")

    PracHitMeanRt = 0
    PracFaMeanRt = 0
    PracMissMeanRt = 0
    
    PracHitMedianRt = 0
    PracFaMedianRt = 0
    PracMissMedianRt = 0
    
    MainHitMeanRt = 0
    MainFaMeanRt = 0
    MainMissMeanRt = 0
    
    MainHitMedianRt = 0
    MainFaMedianRt = 0
    MainMissMedianRt = 0
    
    if len(stored_data['practice_hit_rt']) != 0:
        PracHitMeanRt = statistics.mean(stored_data['practice_hit_rt'])
        PracHitMedianRt = statistics.median(stored_data['practice_hit_rt'])
    if len(stored_data['practice_fa_rt']) != 0:
        PracFaMeanRt = statistics.mean(stored_data['practice_fa_rt'])
        PracFaMedianRt = statistics.median(stored_data['practice_fa_rt'])
    if len(stored_data['practice_miss_rt']) != 0:
        PracMissMeanRt = statistics.mean(stored_data['practice_miss_rt'])
        PracMissMedianRt = statistics.median(stored_data['practice_miss_rt'])
    
    if len(stored_data['main_hit_rt']) != 0:
        MainHitMeanRt = statistics.mean(stored_data['main_hit_rt'])
        MainHitMedianRt = statistics.median(stored_data['main_hit_rt'])
    if len(stored_data['main_fa_rt']) != 0:
        MainFaMeanRt = statistics.mean(stored_data['main_fa_rt'])
        MainFaMedianRt = statistics.median(stored_data['main_fa_rt'])
    if len(stored_data['main_miss_rt']) != 0:
        MainMissMeanRt = statistics.mean(stored_data['main_miss_rt'])
        MainMissMedianRt = statistics.median(stored_data['main_miss_rt'])
         
    new_practice_row = {'Participant': stored_data['participant'], 'Session': 0, 'Block': block, 'n_hits': stored_data['practice_hits'],
            'n_misses': stored_data['practice_miss'], 'n_falsealarms': stored_data['practice_fa'], 
            'n_correctrejections': stored_data['practice_reject'], 'n_misses_isi': len(stored_data['practice_miss_rt']),
            'n_falsealarms_isi': stored_data['practice_fa_isi'], 'hit_mean_rt': PracHitMeanRt, 
            'fa_mean_rt': PracFaMeanRt, 'miss_mean_rt': PracMissMeanRt, 'hit_median_rt': PracHitMedianRt, 'fa_median_rt': PracFaMedianRt,
            'miss_median_rt': PracMissMeanRt}
    new_main_row = {'Participant': stored_data['participant'], 'Session': 1, 'Block': block, 'n_hits': stored_data['main_hits'],
        'n_misses': stored_data['main_miss'], 'n_falsealarms': stored_data['main_fa'], 
        'n_correctrejections': stored_data['main_reject'], 'n_misses_isi': len(stored_data['main_miss_rt']),
        'n_falsealarms_isi': stored_data['main_fa_isi'], 'hit_mean_rt': MainHitMeanRt, 
        'fa_mean_rt': MainFaMeanRt, 'miss_mean_rt': MainMissMeanRt, 'hit_median_rt': MainHitMedianRt, 'fa_median_rt': MainFaMedianRt,
        'miss_median_rt': MainMissMedianRt}
    new_row = 0
    
    if is_practice:
        new_row = new_practice_row
    else:
        new_row = new_main_row
    try:
        # Check if the file exists
        if os.path.exists(file_path_long):
            # Read existing data
            df = pd.read_csv(file_path_long)
        else:
            # Create an empty DataFrame with the same structure
            df = pd.DataFrame(columns=new_row.keys())
        
        # Append the new row
        df = df._append(new_row, ignore_index=True)
        
        # Save the updated DataFrame back to the file
        df.to_csv(file_path_long, index=False)
        print(f"Data successfully saved to: {file_path_long}")
    except Exception as e:
        print(f"Error saving data: {e}")
            
# Function with the outline of the experiment
def experiment(max_count, stored_data, is_practice, block):
    # setting the beginning variables
    count = 0
    critical_index = 15
    hit_interval = 30
    clock = core.Clock()
    
    while count < max_count: #runs as long as specified in function parameter
        i = count % hit_interval # Current index (0-29) in this set of 30
        
        # Generate indecies every 30 numbers
        if i == 0:
            critical_index = randUpTo(hit_interval - 1)
        
        img = None
        
        # If a critical signal is needed, generate critical img
        if (i == critical_index):
            img = visual.ImageStim(win, image=critical_images[randUpTo(critical_length)])
                
        # Otherwise, generate non-critical img
        else:
            img = visual.ImageStim(win, image=regular_images[randUpTo(regular_length)])
            
        count += 1
        
        if is_practice:
            stored_data['practice_count'] += 1
            print(stored_data['practice_count'])
        else:
            stored_data['main_count'] += 1
            print(stored_data['main_count'])
        
        
        
        #-------------[Display + Input Section]-------------#
        
        # drawing image
        img.draw()
        win.flip()
        clock.reset()
        core.wait(1)
        
        hit_already = False

        # Check for keyboard input
        keys = event.getKeys(keyList=['space'], timeStamped=clock)

        if keys:
            response_time = keys[0][1]               # seconds
            response_time_ms = response_time * 1000  # milliseconds
            
            print(response_time_ms)
            
            # Check if the response is correct or incorrect
            if i == critical_index:
                if is_practice:
                    feedback_text = "Correct ✓"
                    text.color = '#03C04A'
                    text.bold = True
                    
                    stored_data['practice_hits'] += 1
                    stored_data['practice_hit_rt'].append(response_time_ms)
                    
                else: 
                    feedback_text = "Saved"
                    
                    stored_data['main_hits'] += 1
                    stored_data['main_hit_rt'].append(response_time_ms)
                    
                hit_already = True

            else:
                if is_practice:
                    feedback_text = "Wrong ❌"
                    text.color = '#FF0000'
                    text.bold = True
                    
                    stored_data['practice_fa'] += 1
                    stored_data['practice_fa_rt'].append(response_time_ms)
                    
                else: 
                    feedback_text = "Saved"
                    
                    stored_data['main_fa'] += 1
                    stored_data['main_fa_rt'].append(response_time_ms)
            
            # Display feedback
            text.text = feedback_text
            text.draw()
            win.flip()
            core.wait(1) # Display feedback for 1 second

        else:
            # Was it a correct rejection?
            response_time_ms = None
            if i == critical_index:
                if is_practice:
                    feedback_text = "Miss ❌"
                    text.color = '#FF0000'
                    text.bold = True
                    
                    stored_data['practice_miss'] += 1
                    if response_time_ms is not None:
                        stored_data['practice_miss_rt'].append(response_time_ms)
                        
                else:
                    feedback_text = "+"
                    
                    stored_data['main_miss'] += 1
                    if response_time_ms is not None:
                        stored_data['main_miss_rt'].append(response_time_ms)

            else:
                feedback_text = "+"
                text.color = 'white'
                
                if max_count == max_count_practice:
                    stored_data['practice_reject'] += 1
                if max_count == max_count_experiment:
                    stored_data['main_reject'] += 1
            
            text.text = feedback_text
            text.draw()
            win.flip()
            core.wait(1)
        
        text.bold = False
        
        
        # Check for ISI keyboard input
        keys = event.getKeys(keyList=['space'], timeStamped=clock)
        if keys and not hit_already:
            isi_response_time = keys[0][1]               # seconds
            isi_response_time_ms = isi_response_time * 1000  # milliseconds
            
            print(isi_response_time_ms)
            
            # Check if the response is correct or incorrect
            if i == critical_index:
                # is it practice?
                if is_practice:
                    stored_data['practice_miss_rt'].append(isi_response_time_ms)
                else:
                    stored_data['main_miss_rt'].append(isi_response_time_ms)

            else:
                # is it practice?
                if is_practice:
                    stored_data['practice_fa_isi'] += 1
                else:
                    stored_data['main_fa_isi'] += 1 
        
        if count % 150 == 0:
            save_data(stored_data, is_practice, block)
            stored_data['practice_hits'] = 0
            stored_data['practice_miss'] = 0
            stored_data['practice_fa'] = 0
            stored_data['practice_fa_isi'] = 0
            stored_data['practice_reject'] = 0
            stored_data['practice_hit_rt'].clear()
            stored_data['practice_fa_rt'].clear()
            stored_data['practice_miss_rt'].clear()
            
            stored_data['main_hits'] = 0
            stored_data['main_miss'] = 0
            stored_data['main_fa'] = 0
            stored_data['main_fa_isi'] = 0
            stored_data['main_reject'] = 0
            stored_data['main_hit_rt'].clear()
            stored_data['main_fa_rt'].clear()
            stored_data['main_miss_rt'].clear()
            
            block += 1
            
    return block
            
#-------------[Declaring Variables]-------------#

# Create a window
win = visual.Window([1500,800], monitor="testMonitor", units="deg")

# Create text stimuli
text = visual.TextStim(win, height = 3)

# Screen buttons/texts
text_screen0 = visual.TextStim(win, text='Enter participant number:', height=1, color='black', pos=(0,5))
text_screen1 = visual.TextStim(win, text='Insert instructions here.', height=1, color='black', pos=(0,5))
text_screen2 = visual.TextStim(win, text='Insert task details here.', height = 1, color='black', pos=(0,5))
text_screen3 = visual.TextStim(win, text='Are you ready to begin a practice run? Click "next" to begin the task.', height = 1, color='black', pos=(0,5))
text_screen4 = visual.TextStim(win, text='You have completed the practice run, you will now complete the entire task.', height = 1, color='black', pos=(0,5))
text_screen5 = visual.TextStim(win, text='Are you ready to begin the task? Click "next" to begin the task.', height = 1, color='black', pos=(0,5))
text_screen6 = visual.TextStim(win, text='You have completed the task, good job! Thank you for participating!', height = 1, color='black', pos=(0,5))

# Time for each experiment session
''' For Yessenia bc she keeps forgetting:
      30 counts = 1 minute
      15 counts = 30 seconds
      1 count = 2 seconds '''
max_count_practice = 150 # 5 minutes 
max_count_experiment = 900 # 30 minutes 

# Data to save
stored_data = {
    'participant': 0,
    
    'practice_count': 0,
    'practice_hits': 0,    
    'practice_miss': 0,     
    'practice_fa': 0,
    'practice_fa_isi': 0,
    'practice_reject': 0,
    'practice_hit_rt': [],
    'practice_fa_rt': [],
    'practice_miss_rt': [],
    
    'main_count': 0,
    'main_hits': 0,
    'main_miss': 0,
    'main_fa': 0,
    'main_fa_isi': 0,
    'main_reject': 0,
    'main_hit_rt': [],
    'main_fa_rt': [],
    'main_miss_rt': []
}


#-------------[The Actual Experiment Process Below]-------------#

#---[Start At Screens 1-3]---#

current = 0

while current <= 5:
    if current == 0:
        action = screen_changer(screen_text=text_screen0, button1_check=False, button1_action='previous', button2_action='next')
    
    elif current == 1:
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

#---[Practice Experiment Loop]---#

if action == 'start_task':
    experiment(max_count_practice, stored_data, True, 0)
    

#---[Continue To Screens 4-5]---#

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


#---[Main Experiment Loop]---#

if action == 'start_task':
    experiment(max_count_experiment, stored_data, False, 1)

current = 6

while current == 6:
    action = screen_changer(screen_text=text_screen6, button1_check=False, button1_action='previous', button2_action='next')
    
    if action == 'next':
        win.close()
        core.quit()