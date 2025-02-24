from pyautogui import *
import pyautogui as pg
import time
import keyboard
import random
# import win32api, win32con

gob_images = [r"images\gob_facing_left_down_v2.png",r"images\gob_facing_left_down.png", r"images\gob_facing_right_down.png", r"images\gob_facing_up_right.png"]
# Step 1 -> Find mob and start fight, Step 2 -> Change map and repeat Step 1, Step 3 -> Fighting, Step 4 -> End Fight Screen -> Repeat from Step 1
current_step = 1

def findMobStartFight():
  global current_step
  random_sleep = random.randint(1,2)
  mob_found = False
  fight_started = False

  mouse_click_offset = 25
  game_region = (570,25,1345,775)

  if not mob_found:
    for image_path in gob_images:
      try:
        mob_pos = pg.locateOnScreen(image_path ,region=game_region, confidence=0.5)
        print(f"DBG: mob_pos.height = {mob_pos.height}")
        print(f"DBG: mob_pos.width = {mob_pos.width}")
        print(f"DBG: Mob found at ({mob_pos[0]},{mob_pos[1]})")
        pg.moveTo(mob_pos[0] + mouse_click_offset , mob_pos[1] + mouse_click_offset)
        pg.leftClick()
        time.sleep(random_sleep)
        mob_found = True
        break
        
      except Exception as error:
        print(f"DBG: error in mob finder = {error}")
  
  if mob_found:
    try:
      attack_pop_up = pg.locateOnScreen(r"images\attack_pop_up.png",region=game_region, confidence=0.7)
      print(f"DBG: Attack_window found at ({attack_pop_up[0]},{attack_pop_up[1]})")
      pg.moveTo(attack_pop_up[0] + mouse_click_offset , attack_pop_up[1] + mouse_click_offset)
      time.sleep(random_sleep)
      pg.leftClick()
      time.sleep(random_sleep)

      start_fight_button = pg.locateOnScreen(r"images\ready_button.png",region=game_region, confidence=0.7)
      pg.moveTo(start_fight_button[0] + mouse_click_offset , start_fight_button[1] + mouse_click_offset)
      time.sleep(random_sleep)
      pg.leftClick()

      fight_started = True
      
    except Exception as error:
      print(f"DBG: error in mob finder = {error}")

  if mob_found and fight_started:
    print(f"DBG: current_step before setting to 3 --> {current_step}")
    current_step = 3
    return


def fight_sequence():
  time.sleep(1)
  print("DBG: Fighting Sequence....")



while keyboard.is_pressed('q') == False:
  if current_step == 1:
    findMobStartFight()
  if current_step == 3:
    fight_sequence()
