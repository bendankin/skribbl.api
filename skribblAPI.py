import pyautogui as pg
import time
import winsound as ws 

class SkribblAPI:

    def __init__(self):
        
        beepPause=3
        beepFreq=1000
        beepDur=300

        print("Configure colour palette:")
        print("Mouse over the middle of white and wait",beepPause,"seconds for the beep...")

        time.sleep(beepPause)
        topleft_X, topleft_Y = pg.position()
        ws.Beep(beepFreq,beepDur)

        print("Mouse over the middle of dark brown and wait",beepPause,"seconds for the beep...")
        
        time.sleep(beepPause)
        bottomright_X, bottomright_Y = pg.position()
        ws.Beep(beepFreq,beepDur)

        delta_X = (bottomright_X - topleft_X)/10
    
        self.coordinates = {
            "white":    (topleft_X,topleft_Y),
            "gray":     (topleft_X+delta_X, topleft_Y),
            "red":      (2*delta_X+topleft_X, topleft_Y),
            "orange":   (3*delta_X+topleft_X, topleft_Y),
            "yellow":   (4*delta_X+topleft_X, topleft_Y),
            "green":    (5*delta_X+topleft_X, topleft_Y),
            "skyblue":  (6*delta_X+topleft_X, topleft_Y),
            "blue":     (7*delta_X+topleft_X, topleft_Y),
            "magenta":  (8*delta_X+topleft_X, topleft_Y),
            "pink":     (9*delta_X+topleft_X, topleft_Y),
            "brown":    (bottomright_X, topleft_Y),
            "black":    (topleft_X,bottomright_Y),
            "dgray":    (topleft_X+delta_X, bottomright_Y),
            "dred":     (2*delta_X+topleft_X, bottomright_Y),
            "dorange":  (3*delta_X+topleft_X, bottomright_Y),
            "dyellow":  (4*delta_X+topleft_X, bottomright_Y),
            "dgreen":   (5*delta_X+topleft_X, bottomright_Y),
            "dskyblue": (6*delta_X+topleft_X, bottomright_Y),
            "navy":     (8*delta_X+topleft_X, bottomright_Y),
            "purple":   (7*delta_X+topleft_X, bottomright_Y),
            "dpink ":   (9*delta_X+topleft_X, bottomright_Y),
            "dbrown":   (bottomright_X, bottomright_Y)
        }
    
    def selectColour(self, colour="black"):
        destination = self.coordinates[colour]
        pg.moveTo(destination[0],destination[1])
        pg.click()
       


api=SkribblAPI()
api.selectColour("blue")
for colour in api.coordinates.keys():
    api.selectColour(colour)
    time.sleep(2)
# 584 845 white
#     870 black
# 825     brown
# 825 870 dbrown
