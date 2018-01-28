################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time, collections, numpy
import numpy as np

class SampleListener(Leap.Listener):
    def __init__(self, new_frame_cb=None, new_point_cb=None, send_message=None):
        super(SampleListener, self).__init__()
        self.new_frame_cb = new_frame_cb
        self.new_point_cb = new_point_cb
        self.send_message = send_message
        self.counter = 0
        self.max_big_buffer = 200
        self.max_small_buffer = 10
        self.big_buffer = collections.deque(maxlen=self.max_big_buffer)
        self.small_buffer = collections.deque(maxlen=self.max_small_buffer)
        self.writing = False


    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        if self.new_frame_cb is not None:
            self.new_frame_cb(self.counter)
        print(self.writing)
        self.counter += 1

        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:
            print(self.counter)
            velocity = hand.palm_velocity.y
            self.big_buffer.append(velocity)
            self.small_buffer.append(velocity)
            if self.counter % 10 == 0 and len(self.small_buffer) == self.max_small_buffer:
                ave1 = numpy.average(self.big_buffer)
                std = numpy.std(self.big_buffer)
                ave2 = numpy.average(self.small_buffer)
                # print("ay")
                # print(ave1)
                # print("yo")
                # print(ave2)
                if (abs(abs(ave1) - (ave2)) > 2*std):
                    self.writing = ave2 > 0
                    self.small_buffer.clear()

            thumb = hand.fingers[Leap.Finger.TYPE_THUMB]
            index_finger = hand.fingers[Leap.Finger.TYPE_INDEX]
            pinky = hand.fingers[Leap.Finger.TYPE_PINKY]

            #print(pinky.is_extended)
            #print(thumb.tip_position.distance_to(index_finger.tip_position))
        """
        if self.new_point_cb is not None:
            self.new_point_cb(point)
        """

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit...BOIIII"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
