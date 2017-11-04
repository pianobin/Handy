from __future__ import division
import os, sys, inspect, thread, time, timeit
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
# arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

moveCounter = 0
xCounterSmall = 0
xCounterGood = 0
xCounterHigh = 0
yCounterSmall = 0
yCounterGood = 0
yCounterHigh = 0
zCounterSmall = 0
zCounterGood = 0
zCounterHigh = 0

def hand_placement(frame):
    count = 0
    for hand in frame.hands:
        handType = "Left hand" if hand.is_left else "Right hand"

        normal = hand.palm_normal
        direction = hand.direction

        real_roll = normal.yaw * Leap.RAD_TO_DEG
        real_yaw = direction.roll * Leap.RAD_TO_DEG
        real_pitch = direction.pitch * Leap.RAD_TO_DEG

        print "%s roll on the now y-axis: %f" % (handType, real_roll)
        print "%s yaw on the now z-axis: %f" % (handType, real_yaw)
        print "%s pitch on the now x-axis: %f" % (handType, real_pitch)

def handMovements(frame):
	for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, velocity: %s" % (handType, hand.id, hand.palm_velocity)

            global moveCounter, xCounterSmall, xCounterGood, xCounterHigh, yCounterSmall, yCounterGood, yCounterHigh, zCounterSmall, zCounterGood, zCounterHigh
            moveCounter += 1
            if abs(hand.palm_velocity.x) < 50:
            	xCounterSmall += 1
            elif abs(hand.palm_velocity.x) > 200:
            	xCounterHigh += 1
            else:
            	xCounterGood += 1

            if abs(hand.palm_velocity.y) < 50:
            	yCounterSmall += 1
            elif abs(hand.palm_velocity.y) > 200:
            	yCounterHigh += 1
            else:
            	yCounterGood += 1

            if abs(hand.palm_velocity.z) < 50:
            	zCounterSmall += 1
            elif abs(hand.palm_velocity.z) > 200:
            	zCounterHigh += 1
            else:
            	zCounterGood += 1

fingerCounter = 0
badFingerCounter = 0

def fingerPointing():
	global fingerCounter
	oneFinger = False
	multiFingers = False
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	for hand in frame.hands:
		for finger in hand.fingers:
			if finger.is_extended and not oneFinger:
				oneFinger = True 
			elif finger.is_extended and oneFinger:
				multiFingers = True 
			fingerCounter += 1
		if oneFinger and not multiFingers:
			badFingerCounter += 1
		oneFinger = False
		multiFingers = False



def displayResults():
	global moveCounter, xCounterSmall, xCounterGood, xCounterHigh, yCounterSmall, yCounterGood, yCounterHigh, zCounterSmall, zCounterGood, zCounterHigh
	print 'moveCounter is {}'.format(moveCounter)
	print 'xCounterSmall is {}'.format(xCounterSmall)
	print 'X-axis percentages are {} for small movement, {} for good movement, and {} for high movement'.format((xCounterSmall/moveCounter) * 100, (xCounterGood/moveCounter) * 100, (xCounterHigh/moveCounter) * 100)
	print 'Y-axis percentages are {} for small movement, {} for good movement, and {} for high movement'.format((yCounterSmall/moveCounter) * 100, (yCounterGood/moveCounter) * 100, (yCounterHigh/moveCounter) * 100)
	print 'Z-axis percentages are {} for small movement, {} for good movement, and {} for high movement'.format((zCounterSmall/moveCounter) * 100, (zCounterGood/moveCounter) * 100, (zCounterHigh/moveCounter) * 100)


startTime = 0
beforeTime = 0

class LeapEventListener(Leap.Listener):

    #global count = 0
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        #controller.enable_gesture(Leap.Gesture.Type.TYPE_SWIPE)
        #controller.config.set("Gesture.Swipe.MinLength", 200.0)
        #controller.config.save()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_frame(self, controller):
        frame = controller.frame()
        #Process frame data

        #Show time elapsed
        global startTime
        global beforeTime
        if startTime == 0:
        	startTime = timeit.default_timer()
        if int ((timeit.default_timer() - startTime) * 10) % 10 == 0:
        	if beforeTime != int(timeit.default_timer() - startTime):
        		print "Elapsed {}".format(int(timeit.default_timer() - startTime))
        		beforeTime = int(timeit.default_timer() - startTime)

        handMovements(frame)
        hand_placement(frame)

    def on_exit(self, controller):
        print "Exited"
        displayResults()
        #the method where we return our statistics

def main():
	listener = LeapEventListener()
	controller = Leap.Controller()
	controller.add_listener(listener)
	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)

if __name__ == "__main__":
    main()
