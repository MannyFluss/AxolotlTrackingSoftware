import keyboard
import asyncio
import time
#write a line to import a file called inputModule.py

#signal system, chatGPT thank you
#all this code is running under the assumption of one entity, the axolotl.
class EventBus:
    def __init__(self):
        self.listeners = {}

    def listen(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def emit(self, event_type, *args, **kwargs):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(*args, **kwargs)
    

class AreaDetector:
    def __init__(self,_x = 0, _y=0, _width = 0, _height = 0):
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        #might be useful?
        self.entered = False
        self.myEventBus = EventBus()
    #this will take in the position of axolotl, then determine if just entered,exited, stay in/ out of area
    
    def poll_position(self , _x, _y):


        if self.x <= _x <= self.x + self.width and self.y <= _y <= self.y + self.height:
            if not self.entered:
                self.entered = True
                self.myEventBus.emit("onEnterArea", self)
                return
        else:
            if self.entered:
                self.entered = False
                self.myEventBus.emit("onExitArea", self)
                return
        if self.x <= _x <= self.x + self.width and self.y <= _y <= self.y + self.height and self.entered:
            self.myEventBus.emit("onStayInArea", self)
            return
        else:
            self.myEventBus.emit("onStayOutArea", self)
            return
        
#ok now I am going to create a thing that emits keystroke inputs, it also wants an areaDetector to listen to
class InputEmitter:
    def __init__(self, key = "a") -> None:
        self.myKeyToPress = key
        self.currentlyPressed = False
        self.myAreaDetector = None
    
    def registerAreaDetector(self, _areaDetector):
        self.myAreaDetector = _areaDetector
        self.myAreaDetector.myEventBus.listen("onEnterArea", self.onEnterArea)
        self.myAreaDetector.myEventBus.listen("onExitArea", self.onExitArea)
        self.myAreaDetector.myEventBus.listen("onStayInArea", self.onStayInArea)
        self.myAreaDetector.myEventBus.listen("onStayOutArea", self.onStayOutArea)
    
    def onEnterArea(self, _areaDetector):
        if not self.currentlyPressed:
            keyboard.press(self.myKeyToPress)
            self.currentlyPressed = True

        pass
    def onExitArea(self, _areaDetector):
        if self.currentlyPressed:
            keyboard.release(self.myKeyToPress)
            self.currentlyPressed = False

        pass

    def onStayInArea(self, _areaDetector):
        pass
    def onStayOutArea(self, _areaDetector): 
        pass

class AreaInputController:
    def __init__(self, areaDetector : AreaDetector(), inputEmitter : InputEmitter) -> None:
        self.areaDetector = areaDetector
        self.inputEmitter = inputEmitter
        self.inputEmitter.registerAreaDetector(self.areaDetector)

    def poll_position(self, _x, _y):
        self.areaDetector.poll_position(_x, _y)
        




    
def main():
    # testEmitter = InputEmitter()
    # testDetector = AreaDetector(0,0,100,100)
    time.sleep(1.0)
    # testEmitter.registerAreaDetector(testDetector)
    testAreaInputer = AreaInputController(AreaDetector(0,0,100,100),InputEmitter("a"))
    # testDetector.myEventBus.listen("onEnterArea", lambda x: print("entered"))
    # testDetector.myEventBus.listen("onExitArea", lambda x: print("exited"))
    # testDetector.myEventBus.listen("onStayInArea", lambda x: print("stay in"))
    # testDetector.myEventBus.listen("onStayOutArea", lambda x: print("stay out"))

    #stay out of area test
    testAreaInputer.poll_position(150,150)
    testAreaInputer.poll_position(150,150)
    #enter area test   
    testAreaInputer.poll_position(50,50)
    #stay in area test
    testAreaInputer.poll_position(50,50)
    testAreaInputer.poll_position(50,50)
    #exit area test
    testAreaInputer.poll_position(150,150)
    #stay out of area test
    testAreaInputer.poll_position(150,150)
    testAreaInputer.poll_position(150,150)
    
if __name__ == "__main__":
    main()