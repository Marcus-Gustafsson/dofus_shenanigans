from pyautogui import *
import pyautogui as pg
import time
import keyboard
import random
# import win32api, win32con

gob_images = [r"images\gob_facing_left_down.png", r"images\gob_facing_right_down.png", r"images\gob_facing_up_right.png"]

def findMobStartFight():

  mouse_click_offset = 25

  for image_path in gob_images:
    try:
      pos = pg.locateOnScreen(image_path ,region=(570,25,1345,775), confidence=0.6)
      print(f"DBG: pos.height = {pos.height}")
      print(f"DBG: pos.width = {pos.width}")
      print(f"DBG: image found at ({pos[0]},{pos[1]})")
      #print(pg.mouseInfo())
      #print(f"DBG: located POS = {pos}")
      #print(f"DBG: mouse pos = {pg.displayMousePosition()}")
      pg.moveTo(pos[0] + mouse_click_offset , pos[1] + mouse_click_offset)
      time.sleep(1)
      
    except:
      print(f"DBG: image_path = {image_path}")
      print("Image not found on screen....")




while keyboard.is_pressed('q') == False:
  findMobStartFight()
