#
# based on a similar java class in cyberaide, and java cog kit
# however the java class is still mor fancy as we can suspend and resume
#
import time


class StopWatch(object):

    # Timer start dict
    timer_start = {}
    # Timer end dict
    timer_end = {}

    def __init__(self):
        self.clear()

    def start(self, name):
        '''
        starts a timer with the given name
        '''
        self.timer_start[name] = time.time()

    def stop(self, name):
        '''
        stops the timer with a given name
        '''
        self.timer_end[name] = time.time()

    def get(self, name):
        '''
        returns the time of the timer
        '''
        time_elapsed = self.timer_end[name] - \
            self.timer_start[name]
        return time_elapsed

    def clear(self):
        '''
        clear start and end timer_start
        '''
        self.timer_start.clear()
        self.timer_end.clear()
