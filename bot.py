from pyautogui import *
import pyautogui as pg
import time
import keyboard
import random
# import win32api, win32con

gob_images = [r"images\gob_facing_left_down_v2.png",r"images\gob_facing_left_down.png", r"images\gob_facing_right_down.png", r"images\gob_facing_up_right.png"]

pig_images = [r"images\piglet_facing_left_down.png",
              r"images\piglet_facing_left_up.png", 
              r"images\piglet_facing_right_down_v2.png", 
              r"images\piglet_facing_right_down.png",
              r"images\piglet_facing_up_right.png",
              r"images\piglet_facing_up_left.png"
              ]
# Step 1 -> Find mob and start fight, Step 2 -> Change map and repeat Step 1, Step 3 -> Fighting, Step 4 -> End Fight Screen -> Repeat from Step 1
current_step = 0 #start to check hp
mob_found = False
fight_started = False
round_counter = 0
random_sleep = random.uniform(0.5 , 1)
error_counter = 0
current_zone = None
moving_down = True
first_round = True
starting_top = False

game_region = (570,25,1345,775)

def findMobStartFight():
  global current_step, mob_found, fight_started, random_sleep, error_counter, current_zone, starting_top

  mouse_click_offset = 20

  if not mob_found:
    for image_path in pig_images:
      try:
        print(f"DBG: Current zone = {current_zone}")
        mob_pos = pg.locateOnScreen(image_path, confidence=0.60, region=game_region, grayscale = True)
        print(f"DBG: Mob found at ({mob_pos[0]},{mob_pos[1]})")
        pg.moveTo(mob_pos[0] + mouse_click_offset , mob_pos[1] + mouse_click_offset)
        pg.leftClick()
        time.sleep(random_sleep)
        mob_found = True
        error_counter = 0
        #print(f"DBG: mob found before breaking = {mob_found}")
        break
        
      except:
        error_counter += 1
        print(f"DBG: incrementing error counter = {error_counter}")
        print(f"DBG: Error with finding mob...")
  
  if mob_found:
    try:
      attack_pop_up = pg.locateOnScreen(r"images\attack_pop_up.png",region=game_region, confidence=0.6)
      print(f"DBG: Attack_window found at ({attack_pop_up[0]},{attack_pop_up[1]})")
      pg.moveTo(attack_pop_up[0] + mouse_click_offset , attack_pop_up[1] + mouse_click_offset)
      time.sleep(random_sleep)
      pg.leftClick()

      #time.sleep(7) #Running time for char
      while not fight_started and error_counter <= 50:
        time.sleep(0.1)
        try:
          attack_pop_up = pg.locateOnScreen(r"images\rdy_button.png",region=game_region, confidence=0.7)
          fight_started = True
          error_counter = 0
        except:
          error_counter += 1
          print(f"DBG: Fight yet not started, error = {error_counter}")
          #print("DBG: fight started but cannot find Ready bbutton")¨
      
      if error_counter >= 50 and not fight_started:
        print("DBG: returning to finding mob due to fight not started")
        current_step = 1
        fight_started = False
        return

      if current_zone == "down_top" and pg.pixelMatchesColor(1852, 320, (255,0,0)):
        print("Should only happen in down_top zone and starting top")
        starting_top = True
        pg.moveTo(1852, 320) # Move out of position to unblock view
        time.sleep(0.5)
        pg.leftClick()
        time.sleep(0.5)
        pg.moveTo(1628, 370) # Move into postion
        time.sleep(0.5)
        pg.leftClick()
      elif current_zone == "down_top":
        print("Down top zone and starting bottom")
        starting_top = False
        pg.moveTo(1773, 648) # Move out of position
        time.sleep(0.5)
        pg.leftClick()
        time.sleep(0.5)
        pg.moveTo(1676, 540) # starting on bottom
        time.sleep(0.5)
        pg.leftClick()

      if current_zone == "up_from_bottom" and pg.pixelMatchesColor(1897, 491, (255,0,0)):
        print("DBG: starting top on zone 'up_from_btoom'")
        starting_top = True
        pg.moveTo(1802 , 391) # Upper square first before moving into position
        time.sleep(0.5)
        pg.leftClick()
        pg.leftClick()
        time.sleep(0.5)
        pg.moveTo(1678, 444) # Correct starting position
        time.sleep(0.5)
        pg.leftClick()
      elif current_zone == "up_from_bottom":
        print("DBG: starting down on zone 'up_from_btoom'")
        starting_top = False
        pg.moveTo(1244 , 525) # Upper square first before moving into position
        time.sleep(0.5)
        pg.leftClick()
        pg.leftClick()
        time.sleep(0.5)
        pg.moveTo(1340, 467) # Correct starting position
        time.sleep(0.5)
        pg.leftClick()
        pg.leftClick()

      keyboard.press_and_release("r") #Rdy up/start fight

      #fight_started = True
      print(f"DBG: current_step before setting to 3 --> {current_step}")
      current_step = 3

    except:
      mob_found = False # Retry finding mob
      pg.moveTo(1200,400)
      print(f"DBG: Error with attack pop up and ready button")

def fight_sequence():

  global round_counter, current_step, random_sleep, current_zone, first_round, starting_top
  print("DBG: Fighting Sequence...")
  time.sleep(random_sleep)

  if (pg.pixelMatchesColor(1838, 984, (190,185,152)) and not pg.pixelMatchesColor(1745, 700, (255,117,30))) or pg.pixelMatchesColor(1726, 653, (230,87,0)): # Indicates that fight has ended by checking bottom right slot of inv and not seeing "Tactical mode" (start of fight) or lvl up window appeard.
      print("DBG: resetting after fight")
      current_step = 4 # Sets to reset fight step
      time.sleep(1)
      return


  if pg.pixelMatchesColor(1363,848, (255,102,0)): # Player turn started
      if first_round and current_zone == "down_top":

        if starting_top:
          print("DBG: starting top, moving before EQ/SYLV (zone= down_top)")
          pg.moveTo(1580, 440) # move into positon before EQ/SYLV
          time.sleep(0.5)
          pg.leftClick()
        else:
          print("DBG: starting bottom, moving before EQ/SYLV (zone= down_top)")
          pg.moveTo(1530, 470)
          time.sleep(0.5)
          pg.leftClick()
        first_round = False

      if first_round and current_zone == "up_from_bottom":

        if starting_top:
          print("DBG: up_from_bottom zone and moving into position before EQ/SYLV (STARTING TOP)")
          pg.moveTo(1536, 370)
          time.sleep(0.5)
          pg.leftClick()
        else:
          print("DBG: up_from_bottom zone and moving into position before EQ/SYLV (STARTING BOTTOM)")
          pg.moveTo(1486, 391)
          time.sleep(0.5)
          pg.leftClick()
        first_round = False

      print("DBG: Player turn started, orange tick in clock...")
      print(f"DBG: round counter =  {round_counter}")
      print(f"current_zone = {current_zone}")
      time.sleep(1)
      try:
        if round_counter == 0:
          pg.moveTo(1636,930) # EQ button (x,y) cords
          pg.rightClick()
          time.sleep(random_sleep)
          pg.moveTo(1586,932) # Poisoned Wind button (x,y) cords
          pg.rightClick()
          time.sleep(random_sleep)
          if pg.pixelMatchesColor(1643, 933, (88,21,21)) and pg.pixelMatchesColor(1595, 928, (53,50, 36)): # EQ and Wind cast OK!, cast sylvan!
            pg.moveTo(1688 , 930) # Sylvan Button
            time.sleep(random_sleep)
            pg.rightClick()

          keyboard.press_and_release("r")
          round_counter += 1

        elif pg.pixelMatchesColor(1625, 931, (176,42,42)) and round_counter < 2: #CF for EQ --> EQ available, cast again
          print("DBG: casting EQ again after CF")
          pg.moveTo(1636,930) # EQ button (x,y) cords
          pg.rightClick()
          time.sleep(random_sleep)

        elif pg.pixelMatchesColor(1583, 933, (106,101,73)) and round_counter < 2: #CF for WIND --> WIND available, cast again
          print("DBG: casting EQ again after CF")
          pg.moveTo(1586,932) # wind button (x,y) cords
          pg.rightClick()
          time.sleep(random_sleep)
          
        
        elif pg.pixelMatchesColor(1686 , 932, (255,255,255)) and round_counter < 2: #CF sylvan, cast again
          print("DBG: casting sylvan again after CF")
          pg.moveTo(1688 , 930) # Sylvan Button
          time.sleep(random_sleep)
          pg.rightClick()

        elif round_counter >= 5:
          round_counter = 0
        
        else:
          time.sleep(random_sleep)
          keyboard.press_and_release("r")
          round_counter += 1

      except:
        print("DBG: Error during EQ spell, Sylvan and Next turn")

def fight_over_reset():

  global current_step, mob_found, fight_started, round_counter, first_round

  time.sleep(2)
  print("DBG: found lvl up window, pressing enter...")
  keyboard.press_and_release("enter")
  time.sleep(1)
  keyboard.press_and_release('esc')

  current_step = 0 #check hp again
  mob_found = False
  fight_started = False
  round_counter = 0
  first_round = True
  print(f"DBG: resetting, current_step = {current_step}")



def recover_hp():
  global current_step
  if pg.pixelMatchesColor(1305,812, (255,255,102)): # Checking if color is red or yeollw (low hp)
    #pg.moveTo(663,823) # moves moouse to sit position
    print("DBG: trying to sit")
    pg.moveTo(672,822) # moves moouse to sit position (laptop)
    time.sleep(random_sleep)
    pg.leftClick()
  #while pg.pixelMatchesColor(1303,825, (255,255,148)):

  while pg.pixelMatchesColor(1305,812, (255,255,102)): #sitting untill this part is no longer yellow-ish (hp is filled)
    print("DBG: hp not yet ok...")
    time.sleep(0.5)
  print("DBG: HP OKAY, current step --> 1 (checking for mobs)")
  current_step = 1


# def change_zone():
#   global error_counter

#   try:
#     pg.locateOnScreen(r"images\top_left_zone.png", grayscale= True, confidence=0.55)
#     pg.moveTo(1293,784)
#     pg.leftClick()
#     print("DBG: Top left zone -> Bottom left Zone")
#     time.sleep(5) # Time for character to move
#     error_counter = 0 # Resetting error counter
#     return
#   except:
#     print("DBG: Don't recoginze top left zone")
#   try:
#     pg.locateOnScreen(r"images\top_right_zone.png", grayscale= True, confidence=0.55)
#     pg.moveTo(618,394)
#     pg.leftClick()
#     print("DBG: Top right zone -> Top Left Zone")
#     time.sleep(5) # Time for character to move
#     error_counter = 0 # Resetting error counter
#     return
#   except:
#     print("DBG: Don't recoginze top right zone")

#   try:
#     pg.locateOnScreen(r"images\bottom_left_zone.png", grayscale= True, confidence=0.55)
#     pg.moveTo(1869,392)
#     pg.leftClick()
#     print("DBG: Bottom Left Zone -> Bottom Right Zone")
#     time.sleep(5) # Time for character to move
#     error_counter = 0 # Resetting error counter
#     return
#   except:
#     print("DBG: Don't recoginze Bottom Left zone")

#   try:
#     pg.locateOnScreen(r"images\bottom_right_zone.png", grayscale= True, confidence=0.55)
#     pg.moveTo(1293,48)
#     pg.leftClick()
#     print("DBG: Bottom Right Zone -> Top Right Zone")
#     time.sleep(5) # Time for character to move
#     error_counter = 0 # Resetting error counter
#     return
#   except:
#     print("DBG: Don't recoginze Bottom Right zone")




def change_zone_piglet():
  global error_counter, current_zone, moving_down

  try:
    pg.locateOnScreen(r"images\top_piglet_zone.png", grayscale= True, confidence=0.55)
    pg.moveTo(1678,785)
    pg.leftClick()
    print("DBG: Top zone -> down from top Zone")
    time.sleep(5) # Time for character to move
    error_counter = 0 # Resetting error counter
    return
  except:
    print("DBG: Don't recoginze top zone")
  try:
    pg.locateOnScreen(r"images\down_from_top_piglet_zone.png", grayscale= True, confidence=0.55)
    if moving_down:
      pg.moveTo(1822,760) #move down
      print("DBG: Down from top -> up from bottom")
    else:
      pg.moveTo(1677, 48) #move up
      print("DBG: Down from top -> top")
    pg.leftClick()
    time.sleep(5) # Time for character to move
    error_counter = 0 # Resetting error counter
    return
  except:
    print("DBG: Don't recoginze down from top zone")

  try:
    pg.locateOnScreen(r"images\up_from_bottom_piglet_zone.png", grayscale= True, confidence=0.55)
    if moving_down:
      pg.moveTo(1581,784) #moving down
      print("DBG: up_from_bottom -> bottom zone")
    else:
      pg.moveTo(1822,73) #moving up
      print("DBG: up_from_bottom -> tdown_from_top")
    pg.leftClick()
    time.sleep(5) # Time for character to move
    error_counter = 0 # Resetting error counter

    return
  except:
    print("DBG: Don't recoginze up from Bottom zone")

  try:
    pg.locateOnScreen(r"images\bottom_piglet_zone.png", grayscale= True, confidence=0.55)
    pg.moveTo(1631,73)
    pg.leftClick()
    print("DBG: Bottom Zone -> up from bottom Zone")
    time.sleep(5) # Time for character to move
    error_counter = 0 # Resetting error counter
    return
  except:
    print("DBG: Don't recoginze Bottom zone")

def check_current_zone():
  global current_zone, moving_down

  while True:

    try:
        pg.locateOnScreen(r"images\top_piglet_zone.png", grayscale= True, confidence=0.55)
        current_zone = "top_zone"
        moving_down = True
        return
    except:
      print(f"DBG: didn't move to top zone.. current_zone = {current_zone}")

    try:
      pg.locateOnScreen(r"images\down_from_top_piglet_zone.png", grayscale= True, confidence=0.55)
      current_zone = "down_top"
      return
    except:
      print(f"DBG: didn't move down_top zone.. current_zone = {current_zone}")
      
    try:
      pg.locateOnScreen(r"images\up_from_bottom_piglet_zone.png", grayscale= True, confidence=0.55)
      current_zone = "up_from_bottom"
      return
    except Exception as error:
      print(f"{error}")

      try:
        pg.locateOnScreen(r"images\bottom_piglet_zone.png", grayscale= True, confidence=0.55)
        current_zone = "bottom"
        moving_down = False
        return
      except:
        print(f"DBG: didn't move to bottom zone.. current_zone = {current_zone}")
  

def check_esc_window():
  #print("DBG: running esc window function")
  try:
      pg.locateOnScreen(r"images\esc_menu.png", grayscale=True, confidence=0.8)
      print("DBG: esc window found... pressing ESC to remove")
      keyboard.press_and_release("esc")
  except:
    print("DBG: No esc window found...")
  

while keyboard.is_pressed('q') == False:
  time.sleep(0.1)
  if current_step == 0:
    recover_hp()
    if current_zone == None:
      check_current_zone()

  if current_step == 1:
    if error_counter >= 35:
      change_zone_piglet()
      check_current_zone()
    else:
      check_esc_window()
      findMobStartFight()

  if current_step == 3:
    fight_sequence()

  if current_step == 4:
    check_esc_window()
    fight_over_reset()





    """
    Notes for v.2

    - Prio: Set zone identiry/tag, which indicates which zone one currently is in
    - Prio: Select best position for each zone at the start of fight
    - Prio: Fix something with the level up window, current "hit enter" does not seem to work, seems like it is stuck in fighting sequence
    - fix different folder of images for each farming area, which has sub folders of zones and monster images
    - fix bug/error when someone else starts the fight that the bot has found before bot gets to the mob (i.e. after it has found the attack window)
    
    """
