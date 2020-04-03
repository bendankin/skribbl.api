import pyautogui as pg
import time
import winsound as ws 

class SkribblAPI:

    def __init__(self):
        
        beepPause=3
        beepFreq=1000
        beepDur=300

        # ----------- Configure the colour palette -----------
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

        # ----------- Configure the canvas -----------
        print("Configure the colour palette:")
        print("Mouse over the top-left cornver of the canvas and wait",beepPause,"seconds for the beep...")

        time.sleep(beepPause)
        topleft_X, topleft_Y = pg.position()
        ws.Beep(beepFreq,beepDur)
        
        print("Mouse over the bottom-right of the canvas and wait",beepPause,"seconds for the beep...")
        
        time.sleep(beepPause)
        bottomright_X, bottomright_Y = pg.position()
        ws.Beep(beepFreq,beepDur)

        self.canvas={
            "topleft":        (topleft_X,topleft_Y),
            "bottomright":    (bottomright_X,bottomright_Y)
        }

    def selectColour(self, colour="black"):
        destination = self.coordinates[colour]
        pg.moveTo(destination[0],destination[1])
        pg.click()

    def drawLine(self, coor1, coor2, colour):
        self.selectColour(colour)
        pg.moveTo(coor1)
        pg.dragTo(coor2)

    def drawShape(self, vertices, colour):
        l = len(vertices)
        if l == 0:
            return
        for v in vertices:
            self.drawLine(v[0],v[1],'black')
    
    def moveTo(self, coor):
        pg.moveTo(coor[0],coor[1],0.1)

    def dragTo(self, coor):
        pg.dragTo(coor[0],coor[1])

api=SkribblAPI()
api.selectColour("blue")
#pg.displayMousePosition()
# 628 328
api.drawLine((638,328),(700,328),"pink")
api.drawLine((700,328),(700,428),"blue")
api.drawLine((700,428),(638,428),"red")
api.drawLine((638,428),(638,328),"green")

# for colour in api.coordinates.keys():
#     api.selectColour(colour)
#     time.sleep(2)
# 584 845 white
#     870 black
# 825     brown
# 825 870 dbrown
