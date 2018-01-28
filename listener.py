################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, collections
import statistics as stats

class Listener(Leap.Listener):
    def __init__(self, send = None):
        super(Listener, self).__init__()
        self.send = send
        self.is_writing = False
        self.is_hand = False
        self.counter = 0

        self.max_big_buffer = 200
        self.max_small_buffer = 10
        self.big_buffer = collections.deque(maxlen=self.max_big_buffer)
        self.small_buffer = collections.deque(maxlen=self.max_small_buffer)


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
        was_writing = False
        # Send diagnostic information to the front end
        print(self.is_hand)
        self.send("log," + str(self.is_writing))
        self.counter += 1

        # Get the most recent frame and report some basic information
        frame = controller.frame()

        if len(frame.hands) == 1:
            if not self.is_hand:
                self.is_hand = True

            hand = frame.hands[0]
            velocity = int(hand.palm_velocity.y)
            self.big_buffer.append(velocity)
            self.small_buffer.append(velocity)
            if self.counter % 10 == 0 and len(self.small_buffer) == self.max_small_buffer:
                big_ave = stats.mean(self.big_buffer)
                std = stats.stdev(self.big_buffer)
                small_ave = stats.mean(self.small_buffer)
                if (abs(abs(big_ave) - (small_ave)) > 2*std):
                    was_writing = self.is_writing
                    self.is_writing = small_ave > 0
                    self.small_buffer.clear()

            if self.is_writing:
                x = int(hand.palm_position.x)
                y = int(hand.palm_position.y)
                msg = "point," + str(x) + "," + str(y)
                if not was_writing:
                    msg += str(True)
                self.send(msg)
        else:
            if self.is_writing:
                self.is_writing = False
            if self.is_hand:
                self.is_hand = False

def main():
    # Create a sample listener and controller
    listener = Listener()
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
