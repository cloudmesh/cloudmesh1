'''
Module to introduce s Stop wacth.

This class is based on a similar java class in cyberaide, and java cog kit.
However the java class is still mor fancy as we can suspend and resume. At a
later time we may want o also introduce these features.
'''

import time


class StopWatch(object):

    '''
    A class to measure times between events.
    '''

    # Timer start dict
    timer_start = {}
    # Timer end dict
    timer_end = {}

    def __init__(self):
        '''
        Set up the stopwatch.
        '''
        self.clear()

    def keys(self):
        '''returns the names of the timers'''
        return self.timer_end.keys()

    def start(self, name):
        '''
        starts a timer with the given name.

        :param name: the name of the timer
        :type name: string
        '''
        self.timer_start[name] = time.time()

    def stop(self, name):
        '''
        stops the timer with a given name.

        :param name: the name of the timer
        :type name: string
        '''
        self.timer_end[name] = time.time()

    def get(self, name):
        '''
        returns the time of the timer.

        :param name: the name of the timer
        :type name: string
        :rtype: the elapsed time
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
