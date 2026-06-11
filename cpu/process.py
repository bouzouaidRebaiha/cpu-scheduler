

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid= pid
        self.arrival= arrival
        self.burst= burst
        self.priority=priority
        self.waiting=0
        self.turnaround=0
        self.completion = 0 
        self.remaining=burst
        self.response_time = -1


    
    