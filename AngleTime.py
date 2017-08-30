# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 21:45:05 2017

Angle Time - Compute the angle between the minute and hour hands on a clock given a time

@author: tom
"""

import math
import matplotlib.pyplot as plt
import numpy
import unittest

runTests = True
verbose = False

#constants
twoPi = 2.0*math.pi
maxDegree = 360.0
secondsInHour = 60
minutesInHour = secondsInHour
hoursInDay = 24
maxHour = math.ceil(hoursInDay/2)

def getStandardTimeFromMinuteTime(timeInMinutes):
    hours = str(math.floor(timeInMinutes/minutesInHour))
    mins = str(timeInMinutes % minutesInHour)
    
    if len(hours) == 1:
        hours = "0" + hours
            
    if len(mins) == 1:
        mins = "0" + mins
            
    return hours + ":" + mins
    
class Clock():
    def __init__(self, hour, minute, radians):
        self.hour = hour
        self.minute = minute
        self.radians = radians
        self.factor = twoPi
        if not radians:
            self.factor = maxDegree
        
        self.validateTime()
    
    def validateTime(self):
        if self.hour > hoursInDay - 1 or self.hour < 0:
            raise ValueError('Time must be valid - check hours')
        
        if self.minute > minutesInHour - 1 or self.minute < 0:
            raise ValueError('Time must be valid - check minutes')
                        
    def output(self):
        if verbose:
            print("Standard time is: ", self.getTimeStandardAsString(), ", Time in minutes : ", self.getTimeInMinutes(), ", Angle: ", self.computeAngle())            
    
    def getTimeStandardAsString(self):
        timeInMinutes = self.getTimeInMinutes()
        hours = str(math.floor(timeInMinutes/minutesInHour))
        mins = str(timeInMinutes % minutesInHour)
    
        if len(hours) == 1:
            hours = "0" + hours
            
        if len(mins) == 1:
            mins = "0" + mins
            
        return hours + ":" + mins
    
    def getTimeInMinutes(self):
        return self.hour*minutesInHour + self.minute
    
    # every minute moves the minute hand by 6 degrees
    def computeMinuteAngle(self):
        return self.minute*self.factor/minutesInHour
    
    # every hour moves the hour hand by 30 degrees and each minute moves the hour hand by 0.5 degrees
    def computeHourAngle(self):
        # convert to non 24 hour (between 0 and 12 only)
        simpleTimeHour = self.hour
        if simpleTimeHour > maxHour:
            simpleTimeHour = simpleTimeHour - maxHour
    
        return (simpleTimeHour*self.factor + self.computeMinuteAngle())/maxHour
        
    def computeSmallAngle(self):
        minuteAngle = self.computeMinuteAngle()
        hourAngle = self.computeHourAngle()
    
        angle = abs(hourAngle - minuteAngle)
        
        return min(angle, abs(self.factor - angle))
    
    def computeLargeAngle(self):
        return self.factor - self.computeSmallAngle()
    
    def computeAngle(self):
        return self.computeSmallAngle()
    
class ClockAnalyser():
    def __init__(self):
        self.times = []
        self.angles = []
        self.time_angle_pairs = []
        self.cross_over_times = []
    
    def computeAll(self):        
        hourRange = [0,hoursInDay-1]
        for i in range(hourRange[0], hourRange[1]):
            for j in range(0, minutesInHour):
                clock = Clock(i,j, False)
                self.times.append(clock.getTimeInMinutes())
                self.angles.append(clock.computeAngle())
            
                self.time_angle_pairs.append((self.times[-1], self.angles[-1]))
                
        #sort the tuple by the angles first
        self.time_angle_pairs.sort(key=lambda tup: tup[1])
        
        # cross over times - first 12 times from sorted list
        self.cross_over_times = self.time_angle_pairs[hourRange[0]:hourRange[1]-1]    
        self.cross_over_times.sort(key=lambda tup: tup[0])
        
    def output(self):
        print("Times at which crossover happens:")
        for i in self.cross_over_times:
            print(getStandardTimeFromMinuteTime(i[0]), " - ", i[1])   
            
    def plot(self):            
        # plot
        plt.plot(self.times, self.angles,'b-')
        plt.xlabel("Time [elapsed minutes from 00:00]")
        plt.ylabel("Angle [degrees]")
        plt.savefig("times_vs_angles.pdf")
        plt.show()  

# program start
def main():
    
    analyser = ClockAnalyser()
    analyser.computeAll()
    analyser.output()
    analyser.plot()                              
        
    # test
    clock = Clock(16,34, False)
    print(clock.computeAngle())
    
# Unit tests    
class TestTimeAngles12HourRad(unittest.TestCase):

    def test_1200_rad(self):
        clock = Clock(12,0, True)
        self.assertEqual(clock.computeAngle(),0.0 )
        
    def test_0600_rad(self):
        clock = Clock(6,0, True)
        self.assertEqual(clock.computeAngle(),math.pi )
        
    def test_0300_rad(self):
        clock = Clock(3,0, True)
        self.assertEqual(clock.computeAngle(),math.pi/2.0 )
        
    def test_0900_rad(self):
        clock = Clock(9,0, True)
        self.assertEqual(clock.computeAngle(),math.pi/2.0 )
        
    def test_0100_rad(self):
        clock = Clock(1,0, True)
        self.assertEqual(clock.computeAngle(),math.pi/6.0 )
        
class TestTimeAngles12HourDeg(unittest.TestCase):

    def test_1200_deg(self):
        clock = Clock(12,0, False)
        self.assertEqual(clock.computeAngle(),0.0 )

    def test_0600_deg(self):
        clock = Clock(6,0, False)
        self.assertEqual(clock.computeAngle(),180.0 )

    def test_0300_deg(self):
        clock = Clock(3,0, False)
        self.assertEqual(clock.computeAngle(),90.0 )
        
    def test_0900_deg(self):
        clock = Clock(9,0, False)
        self.assertEqual(clock.computeAngle(),90.0 )

    def test_0100_deg(self):
        clock = Clock(1,0, False)
        self.assertEqual(clock.computeAngle(),30.0 )
        
    def test_0105_deg(self):
        clock = Clock(1,5, False)
        self.assertEqual(clock.computeAngle(), 2.5)
        
    def test_1159_deg(self):
        clock = Clock(11,59, False)
        self.assertEqual(clock.computeAngle(), 5.5)
        
# Unit tests    
class TestTimeAngles24HourRad(unittest.TestCase):
        
    def test_2400_rad(self):
        clock = Clock(0,0, True)
        self.assertEqual(clock.computeAngle(),0.0 )
        
    def test_1800_rad(self):
        clock = Clock(18,0, True)
        self.assertEqual(clock.computeAngle(),math.pi )
        
    def test_1500_rad(self):
        clock = Clock(15,0, True)
        self.assertEqual(clock.computeAngle(),math.pi/2.0 )

    def test_2100_rad(self):
        clock = Clock(21,0, True)
        self.assertEqual(clock.computeAngle(),math.pi/2.0 )
        
    def test_1300_rad(self):
        clock = Clock(13,0, True)
        self.assertEqual(clock.computeAngle(),math.pi/6.0 )
        
class TestTimeAngles24HourDeg(unittest.TestCase):
                
    def test_2400_deg(self):
        clock = Clock(0,0, False)
        self.assertEqual(clock.computeAngle(),0.0 )

    def test_1800_deg(self):
        clock = Clock(18,0, False)
        self.assertEqual(clock.computeAngle(),180.0 )

    def test_1500_deg(self):
        clock = Clock(15,0, False)
        self.assertEqual(clock.computeAngle(),90.0 )

    def test_2100_deg(self):
        clock = Clock(21,0, False)
        self.assertEqual(clock.computeAngle(),90.0 )

    def test_1300_deg(self):
        clock = Clock(13,0, False)
        self.assertEqual(clock.computeAngle(),30.0 )
        
    def test_1305_deg(self):
        clock = Clock(13,5, False)
        self.assertEqual(clock.computeAngle(), 2.5)
        
    def test_2359_deg(self):
        clock = Clock(23,59, False)
        self.assertEqual(clock.computeAngle(), 5.5)
        
        
if __name__ == "__main__":
    main()
        
    # tests
    if runTests:
        unittest.main()
