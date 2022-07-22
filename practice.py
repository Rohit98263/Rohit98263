class Car:
    def __init__(self):
        self.colour = "blue"
        self.body = "steel"
        self.steering = "powersteering"
        self.drive()
    
    def start(self):
        print( f"{self.colour} press the start button then turn the steering")
        
    
    def drive(self):
        return self.start()
        
        
a=Car()




