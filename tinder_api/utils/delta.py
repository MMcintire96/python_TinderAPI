from datetime import datetime


class DeltaTimer:
    def __init__(self):
        self.marked = 0

    def mark(self):
        self.marked = datetime.now()
    
    def dt(self):
        print(self.marked - datetime.now())
