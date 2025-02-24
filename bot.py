from pyautogui import *
import pyautogui as pg
import time
import keyboard
import random
# import win32api, win32con

gob_images = [r"images\gob_facing_left_down_v2.png",r"images\gob_facing_left_down.png", r"images\gob_facing_right_down.png", r"images\gob_facing_up_right.png"]
# Step 1 -> Find mob and start fight, Step 2 -> Change map and repeat Step 1, Step 3 -> Fighting, Step 4 -> End Fight Screen -> Repeat from Step 1
current_step = 0 #start to check hp
mob_found = False
fight_started = False
round_counter = 0
random_sleep = random.uniform(0.5 , 1)

game_region = (570,25,1345,775)

def findMobStartFight():
  global current_step, mob_found, fight_started, random_sleep

  mouse_click_offset = 25

  if not mob_found:
    for image_path in gob_images:
      try:
        print(f"DBG: Trying to find mob with path: {image_path}")
        mob_pos = pg.locateOnScreen(image_path, region=game_region, confidence=0.6)
        print(f"DBG: Mob found at ({mob_pos[0]},{mob_pos[1]})")
        pg.moveTo(mob_pos[0] + mouse_click_offset , mob_pos[1] + mouse_click_offset)
        pg.leftClick()
        time.sleep(random_sleep)
        mob_found = True
        print(f"DBG: mob found before breaking = {mob_found}")
        break
        
      except:
        print(f"DBG: Error with finding mob...")
  
  if mob_found:
    try:
      attack_pop_up = pg.locateOnScreen(r"images\attack_pop_up.png",region=game_region, confidence=0.6)
      print(f"DBG: Attack_window found at ({attack_pop_up[0]},{attack_pop_up[1]})")
      pg.moveTo(attack_pop_up[0] + mouse_click_offset , attack_pop_up[1] + mouse_click_offset)
      time.sleep(random_sleep)
      pg.leftClick()

      time.sleep(5) #Running time for char

      keyboard.press_and_release("r") #Rdy up/start fight

      fight_started = True
      print(f"DBG: current_step before setting to 3 --> {current_step}")
      current_step = 3

    except:
      mob_found = False # Retry finding mob
      pg.moveTo(1200,400)
      print(f"DBG: Error with attack pop up and ready button")

def fight_sequence():

  global round_counter, current_step, random_sleep
  print("DBG: Fighting Sequence....")
  time.sleep(random_sleep)

  if pg.pixelMatchesColor(1838, 984, (190,185,152)) and not pg.pixelMatchesColor(1745, 700, (255,117,30)): # Indicates that fight has ended by checking bottom right slot of inv and not seeing "Tactical mode" (start of fight)      
      current_step = 4 # Sets to reset fight step
      return


  if pg.pixelMatchesColor(1363,848, (255,102,0)): # Player turn started
    print("DBG: Player turn started, orange tick in clock...")
    print(f"DBG: round counter =  {round_counter}")
    try:
      if round_counter == 0:
        pg.moveTo(1636,930) # EQ button (x,y) cords
        pg.rightClick()
        time.sleep(random_sleep)
        pg.moveTo(1688 , 930) # Sylvan Button
        time.sleep(random_sleep)
        pg.rightClick()
        keyboard.press_and_release("r")
        round_counter += 1
      
      elif round_counter >= 5:
        round_counter = 0
      
      else:
        time.sleep(random_sleep)
        keyboard.press_and_release("r")
        round_counter += 1

    except:
      print("DBG: Error during EQ spell, Sylvan and Next turn")

def fight_over_reset():

  global current_step, mob_found, fight_started, round_counter

  keyboard.press_and_release('esc')

  current_step = 0 #check hp again
  mob_found = False
  fight_started = False
  round_counter = 0



def recover_hp():
  global current_step
  if pg.pixelMatchesColor(1303,820, (255,255,148)): # HP is low (checking yellow ish area of heart)
    pg.moveTo(663,823) # moves moouse to sit position
    time.sleep(random_sleep)
    pg.leftClick()
  while pg.pixelMatchesColor(1303,820, (255,255,148)):
    time.sleep(0.5)
  print("DBG: HP OKAY, current step --> 1 (checking for mobs)")
  current_step = 1



while keyboard.is_pressed('q') == False:
  if current_step == 0:
    recover_hp()
  if current_step == 1:
    findMobStartFight()
  if current_step == 3:
    fight_sequence()
  if current_step == 4:
    fight_over_reset()
