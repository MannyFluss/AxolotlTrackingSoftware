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
        


if __name__ == "__main__":
    testDetector = AreaDetector(0,0,100,100)
    testDetector.myEventBus.listen("onEnterArea", lambda x: print("entered"))
    testDetector.myEventBus.listen("onExitArea", lambda x: print("exited"))
    testDetector.myEventBus.listen("onStayInArea", lambda x: print("stay in"))
    testDetector.myEventBus.listen("onStayOutArea", lambda x: print("stay in"))

    #stay out of area test
    testDetector.poll_position(150,150)
    testDetector.poll_position(150,150)
    #enter area test   
    testDetector.poll_position(50,50)
    #stay in area test
    testDetector.poll_position(50,50)
    testDetector.poll_position(50,50)
    #exit area test
    testDetector.poll_position(150,150)
    #stay out of area test
    testDetector.poll_position(150,150)
    testDetector.poll_position(150,150)
    