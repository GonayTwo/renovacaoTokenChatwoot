import pyautogui as pag
import time
import cv2 as cv
import mss
import numpy as np
from os import listdir
import yaml
from random import random
import pygetwindow as gw

cat = """
                                                _
                                                \`*-.
                                                 )  _`-.
                                                .  : `. .
                                                : _   '  \\
                                                ; *` _.   `*-._
                                                `-.-'          `-.
                                                  ;       `       `.
                                                  :.       .        \\
                                                  . \  .   :   .-'   .
                                                  '  `+.;  ;  '      :
                                                  :  '  |    ;       ;-.
                                                  ; '   : :`-:     _.`* ;
                                               .*' /  .*' ; .*`- +'  `*'
                                               `*-*   `*-*  `*-*'
=========================================================================
    Sript criado por: Gonay (Daniel Miranda)
    Linkedin:https://www.linkedin.com/in/daniel-miranda97/
    Tem como objetivo automatizar a renovação do token da API do Meta
    na plataforma de WhatsAPP ChatWoot
=========================================================================


"""

stream = open('config.yaml', 'r')
c = yaml.safe_load(stream)
cm = c['meta']

def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pag.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)

def remove_sufix(input_string, suffix):
  #Remove a extensão de arquivo passada nos parâmetros da função
  if suffix and input_string.endswith(suffix):
    return input_string[:-len(suffix)]
  return input_string

def load_images(dir_path='./images/'):
  #Carrega as imagens salvas na pasta e adiciona elas em um objeto chave e valor
  file_names = listdir(dir_path)
  targets = {}
  for file in file_names:
    path = 'images/'+ file
    targets[remove_sufix(file, '.png')] = cv.imread(path)
  return targets

def clickBtn(img, threshold = cm['default']):
  has_timed_out = False

  while(not has_timed_out):
    matches = positions(img, threshold=threshold)
    x,y,w,h = matches[0]
    pos_click_x = x+w/2
    pos_click_y = y+h/2
    moveToWithRandomness(pos_click_x,pos_click_y,1)
    pag.click()
    return True

  return False


def printScreen():
  with mss.mss() as sct:
    monitor = sct.monitors[0]
    sct_img = np.array(sct.grab(monitor))

    return sct_img[:,:,:3]

def positions(target, threshold=cm['default'], img = None):
  if img is None:
    img = printScreen()
  result = cv.matchTemplate(img, target, cv.TM_CCOEFF_NORMED)
  w = target.shape[1]
  h = target.shape[0]

  yloc, xloc = np.where(result >= threshold)
  rectangles = []
  for (x, y) in zip(xloc, yloc):
      rectangles.append([int(x), int(y), int(w), int(h)])
      rectangles.append([int(x), int(y), int(w), int(h)])

  rectangles, weights = cv.groupRectangles(rectangles, 1, 0.2)
  return rectangles

def list_all_windows():
    windows = gw.getAllWindows()
    print("=" * 40)
    print("Janelas Abertas:")
    print("=" * 40)
    for idx, window in enumerate(windows):
        print(f"{idx + 1}. Título: '{window.title}'")
    print("=" * 40)
def takeTokenMeta():
  """ Seleciona a aba e realiza as ações"""
  pag.hotkey('winleft','1')
  time.sleep(1)
  pag.hotkey('ctrlleft','1')
  time.sleep(1)
  pag.press('f5')
  time.sleep(15)
  clickBtn(images['generateTokenBTN'])
  time.sleep(5)

  list_all_windows()

  for window in gw.getAllWindows():
     if "Entrar com o Facebook" in window.title:
        window.maximize()
        time.sleep(2)
        break
     
  time.sleep(3)   
  clickBtn(images['reconnectBTN'])
  time.sleep(5)
  clickBtn(images['copyBTN'])
  time.sleep(1)

def putTokenOnChatWoot():
  """ Seleciona a aba e realiza as ações"""
  pag.hotkey('ctrlleft','2')
  time.sleep(1)
  pag.press('f5')
  time.sleep(15)
  clickBtn(images['configBTN'])
  time.sleep(2)
  clickBtn(images['emptyToken'])
  pag.hotkey('ctrlleft','v')
  time.sleep(2)
  clickBtn(images['updateBTN'])

def main():
  global images
  images = load_images()
  print(cat)
  time.sleep(3)
  takeTokenMeta()
  putTokenOnChatWoot()
  print('=' * 40)
  print('Token renovado com sucesso!')
  print('=' * 40)
main()