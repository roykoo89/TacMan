import threading
import time
from typing import Callable

#import cv2
# numpy as np
from collections import deque

from robot import HopeJuniorRobot
from leader import (
    Tac_Man,
)




def main():
    robot = HopeJuniorRobot()
    robot.connect_arm()
    robot.arm_bus.write("Lock", 0)
    robot.arm_bus.write("Maximum_Acceleration", 254)
    robot.arm_bus.write("Torque_Limit", 1000)
    encoder = Tac_Man("/dev/ttyACM1", 115200)#if encoder.read is between 2800 and 3000 do nothing, if encoder.read is above 3000 move clockwise until you reach 1000 (decrease goal position by 10) or if encoder.read is between 2800 and 3000, 

    import time

    # # Calculate the midpoint to target.#1 is positive (sensor0 motor1) center 3500, 3 is negative (sensor 1 motor3) center 3400, 2 is positive (sensor 2 motor2), center 3000
    # target = 3000
    # # Some gain value controlling how aggressively we move the motor
    # Kp = 0.7

    # while True:
    #     encoder_value = encoder.read()[2]


    #     current_position = robot.arm_bus.read("Present_Position", ["motor2"])[0]

    #     error = (encoder_value - target)
    #     # Adjust how big a step you take; negative error means move clockwise, positive means anticlockwise
    #     # The sign flips if your motor direction is reversed in your setup, so adjust as needed.
    #     step = Kp * error
        
    #     # For safety, clip step so it doesn’t become too large.
    #     max_step = 200  # define your comfort zone
    #     step = max(-max_step, min(step, max_step))
        
    #     new_position = current_position + step
        
    #     # Write to motor.
    #     robot.arm_bus.write("Goal_Position", new_position, ["motor2"])
    #     hall_angle = np.clip((np.array(encoder_value) - 3250)/400, 0,1)*20
        
    #     print(f"Hall_Angle: {int((360/4096)*current_position+hall_angle-20)}, Motor_Angle: {int((360/4096)*current_position - 10)}")
    #     time.sleep(0.001)

    
    #CONNECT TO HOST
    if False:

        import pygame
        import time
        import numpy as np


        import socket
        import time
        HOST = "172.20.10.2"   # Your machine's IP to bind to
        PORT = 65432    # Port you want to listen on

        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Motor Control Demo")

        # A flag to end the loop when the window is closed or ESC is pressed
        done = False

        # Track whether each motor should be stopped (True = not sending new positions)
        stop_motor1 = False
        stop_motor2 = False
        stop_motor3 = False

        # --- Your existing control parameters ---
        Kp = 0.7
        max_step = 200

        target1 = 3200  # sensor0 => motor1
        target2 = 3300  # sensor2 => motor2
        target3 = 3300  # sensor1 => motor3

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                # Bind the socket to the specified IP and port
                server_socket.bind((HOST, PORT))
                
                # Listen for incoming connections
                server_socket.listen(1)
                print(f"Server listening on {HOST}:{PORT}...")
                
                # Accept a connection
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connected by {addr}")

                    while not done:
                        # ------------------------------------------------------------------------
                        # 1) Handle Pygame events (user input)
                        # ------------------------------------------------------------------------
                        for event in pygame.event.get():
                            # If the user closed the window
                            if event.type == pygame.QUIT:
                                done = True
                            elif event.type == pygame.KEYDOWN:
                                # ESC key to quit
                                if event.key == pygame.K_ESCAPE:
                                    done = True

                                # Press A -> Stop motor1
                                elif event.key == pygame.K_a:
                                    stop_motor1 = True
                                    print(f"Motor1 stopped: {stop_motor1}")

                                # Press S -> Stop motor2
                                elif event.key == pygame.K_s:
                                    stop_motor2 = True
                                    print(f"Motor2 stopped: {stop_motor2}")

                                # Press D -> Stop motor3
                                elif event.key == pygame.K_d:
                                    stop_motor3 = True
                                    print(f"Motor3 stopped: {stop_motor3}")

                            elif event.type == pygame.KEYUP:
                                # Release A -> Resume motor1
                                if event.key == pygame.K_a:
                                    stop_motor1 = False
                                    print(f"Motor1 resumed: {not stop_motor1}")

                                # Release S -> Resume motor2
                                elif event.key == pygame.K_s:
                                    stop_motor2 = False
                                    print(f"Motor2 resumed: {not stop_motor2}")

                                # Release D -> Resume motor3
                                elif event.key == pygame.K_d:
                                    stop_motor3 = False
                                    print(f"Motor3 resumed: {not stop_motor3}")

                        if done:
                            break
                        
                        

                        # ------------------------------------------------------------------------
                        # 2) Read the current sensor values and motor positions
                        # ------------------------------------------------------------------------
                        sensor_values = encoder.read()  # e.g. [sensor0, sensor1, sensor2, ...]
                        encoder_val1 = sensor_values[0]  # sensor0 => motor1
                        encoder_val3 = sensor_values[1]  # sensor1 => motor3
                        encoder_val2 = sensor_values[2]  # sensor2 => motor2

                        current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                        current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                        current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]

                        # --------------------------- MOTOR 1 LOGIC ------------------------------
                        if not stop_motor1:
                            error1 = encoder_val1 - target1
                            step1 = -Kp * error1
                            step1 = max(-max_step, min(step1, max_step))  # clip
                            new_pos1 = current_pos1 + step1
                            robot.arm_bus.write("Goal_Position", new_pos1, ["motor1"])
                        # Even if stopped, you can still compute angles or do other non‐movement logic
                        hall_angle1 = np.clip((encoder_val1 - 3250) / 400, 0, 1) * 20
                        motor_angle1_degrees = (360.0 / 4096.0) * current_pos1 - 180

                        # --------------------------- MOTOR 2 LOGIC ------------------------------
                        if not stop_motor2:
                            error2 = encoder_val2 - target2
                            step2 = Kp * error2
                            step2 = max(-max_step, min(step2, max_step))  # clip
                            new_pos2 = current_pos2 + step2
                            robot.arm_bus.write("Goal_Position", new_pos2, ["motor2"])
                        hall_angle2 = np.clip((encoder_val2 - 2000) / 1300, 0, 1) * 20
                        motor_angle2_degrees = 360 - ((360.0 / 4096.0) * current_pos2) 

                        # --------------------------- MOTOR 3 LOGIC ------------------------------
                        if not stop_motor3:
                            error3 = encoder_val3 - target3
                            # Notice you used negative sign for motor3 in your snippet:
                            step3 = -Kp * error3
                            step3 = max(-max_step, min(step3, max_step))  # clip
                            new_pos3 = current_pos3 + step3
                            robot.arm_bus.write("Goal_Position", new_pos3, ["motor3"])
                        hall_angle3 = np.clip((encoder_val3 - 3150) / 300, 0, 1) * 20
                        motor_angle3_degrees = ((360.0 / 4096.0) * current_pos3)

                        # ------------------------------------------------------------------------
                        # 3) Print debugging info
                        # ------------------------------------------------------------------------
                        print(f"Motor1 -> Hall_Angle: {int(motor_angle1_degrees + hall_angle1 - 20)}, "
                            f"Motor_Angle: {int(motor_angle1_degrees - 10)}   "
                            f"[Stopped={stop_motor1}]")
                        print(f"Motor2 -> Hall_Angle: {int(motor_angle2_degrees + hall_angle2 - 20)}, "
                            f"Motor_Angle: {int(motor_angle2_degrees - 10)}   "
                            f"[Stopped={stop_motor2}]")
                        print(f"Motor3 -> Hall_Angle: {int(motor_angle3_degrees + hall_angle3 - 20)}, "
                            f"Motor_Angle: {int(motor_angle3_degrees - 10)}   "
                            f"[Stopped={stop_motor3}]\n")
                        
                        angle_to_send = f"S{motor_angle2_degrees},{motor_angle3_degrees},{motor_angle1_degrees}E"
                        conn.sendall(angle_to_send.encode("utf-8"))
                        # ------------------------------------------------------------------------
                        # 4) Short delay so we don't overload the bus (and allow Pygame to update)
                        # ------------------------------------------------------------------------
                        time.sleep(0.001)

            #check collision at angle 1 + hall/2 and angle 1 - hall/2, if it wants to move there then stop it
            #do this when doing pid so we dont apply the pid if the resulting pose hits a specific object
            #only need forward kinematics for this 

                # Done loop
                pygame.quit()

    #X Y Z COLLISION
    if False:
        import pygame
        import time
        import numpy as np

        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Motor Control Demo")

        done = False

        # --------------------------------------------------------------------
        # 1) Frame counters for overrides
        #    If > 0, that motor is overriding the normal PID with a fixed goal.
        # --------------------------------------------------------------------
        override_counter1 = 0
        override_counter2 = 0
        override_counter3 = 0

        # Store the specific override goal position (in Dynamixel steps, for example)
        override_goal1 = None
        override_goal2 = None
        override_goal3 = None

        # How many frames we hold the override position
        HOLD_FRAMES = 15

        # --- Your existing control parameters ---
        Kp = 0.7
        max_step = 200

        target1 = 3150  # sensor0 => motor1
        target2 = 3300  # sensor2 => motor2
        target3 = 3300  # sensor1 => motor3

        push_amount = 15  # degrees per nudge

        # For a typical Dynamixel-like system: 360 degrees -> 4096 steps
        STEPS_PER_DEG = 4096.0 / 360.0

        def deg_to_steps(deg):
            """
            Convert degrees -> (approx) motor steps
            """
            return int(deg * STEPS_PER_DEG)

        while not done:
            # ------------------------------------------------------------------------
            # 1) Handle Pygame events (user input)
            # ------------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

                    # ------------------------------------------------------------
                    # Key 4 -> Motor1 +10°
                    # ------------------------------------------------------------
                    elif event.key == pygame.K_4:
                        current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                        override_counter1 = HOLD_FRAMES
                        override_goal1 = current_pos1 + deg_to_steps(12)
                        print(f"Motor1 override: +{12} deg for {HOLD_FRAMES} frames.")

                    # ------------------------------------------------------------
                    # Key 5 -> Motor1 -10°
                    # ------------------------------------------------------------
                    elif event.key == pygame.K_5:
                        current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                        override_counter1 = HOLD_FRAMES
                        override_goal1 = current_pos1 - deg_to_steps(12)
                        print(f"Motor1 override: -{12} deg for {HOLD_FRAMES} frames.")

                    # ----------------------------------------------------------------
                    # Key 1 -> old "d + g" => Motor3 +10°, Motor2 -10°
                    # ----------------------------------------------------------------
                    elif event.key == pygame.K_1:
                        # Read current positions:
                        current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                        current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                        # Set override counters:
                        override_counter2 = HOLD_FRAMES
                        override_counter3 = HOLD_FRAMES
                        # Motor2 = -push_amount, Motor3 = +push_amount:
                        override_goal2 = current_pos2 - deg_to_steps(15)
                        override_goal3 = current_pos3 + deg_to_steps(15)
                        print(f"Motor2 override: -{push_amount} deg, Motor3 override: +{15} deg")

                    # ----------------------------------------------------------------
                    # Key 2 -> old "g + h" => Motor2 -10°, Motor3 -10°
                    # ----------------------------------------------------------------
                    elif event.key == pygame.K_2:
                        current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                        current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                        override_counter2 = HOLD_FRAMES
                        override_counter3 = HOLD_FRAMES
                        override_goal2 = current_pos2 - deg_to_steps(15)
                        override_goal3 = current_pos3 - deg_to_steps(15)
                        print(f"Motor2 override: -{push_amount} deg, Motor3 override: -{15} deg")

                    # ----------------------------------------------------------------
                    # Key 3 -> old "s + d" => Motor2 +10°, Motor3 +10°
                    # ----------------------------------------------------------------
                    elif event.key == pygame.K_3:
                        current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                        current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                        override_counter2 = HOLD_FRAMES
                        override_counter3 = HOLD_FRAMES
                        override_goal2 = current_pos2 + deg_to_steps(15)
                        override_goal3 = current_pos3 + deg_to_steps(15)
                        print(f"Motor2 override: +{push_amount} deg, Motor3 override: +{15} deg")

                    # ----------------------------------------------------------------
                    # Key 6 -> old "s + h" => Motor2 +10°, Motor3 -10°
                    # ----------------------------------------------------------------
                    elif event.key == pygame.K_6:
                        current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                        current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                        override_counter2 = HOLD_FRAMES
                        override_counter3 = HOLD_FRAMES
                        override_goal2 = current_pos2 + deg_to_steps(15)
                        override_goal3 = current_pos3 - deg_to_steps(15)
                        print(f"Motor2 override: +{push_amount} deg, Motor3 override: -{15} deg")

            if done:
                break

            # ------------------------------------------------------------------------
            # 2) Read the current sensor values and motor positions
            # ------------------------------------------------------------------------
            sensor_values = encoder.read()  # e.g. [sensor0, sensor1, sensor2, ...]
            encoder_val1 = sensor_values[0]  # sensor0 => motor1
            encoder_val3 = sensor_values[1]  # sensor1 => motor3
            encoder_val2 = sensor_values[2]  # sensor2 => motor2

            current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
            current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
            current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]

            # Decrement counters each frame if they're above 0
            if override_counter1 > 0:
                override_counter1 -= 1
            if override_counter2 > 0:
                override_counter2 -= 1
            if override_counter3 > 0:
                override_counter3 -= 1

            # ------------------------- MOTOR 1 LOGIC -------------------------
            if override_counter1 > 0:
                # If we're in override mode, keep sending that override_goal
                # and skip PID.
                robot.arm_bus.write("Goal_Position", override_goal1, ["motor1"])
            else:
                # Normal PID logic
                error1 = encoder_val1 - target1
                step1 = -Kp * error1
                step1 = max(-max_step, min(step1, max_step))  # clip
                new_pos1 = current_pos1 + step1
                robot.arm_bus.write("Goal_Position", new_pos1, ["motor1"])

            hall_angle1 = np.clip((encoder_val1 - 3250) / 400, 0, 1) * 20
            motor_angle1_degrees = (360.0 / 4096.0) * current_pos1

            # ------------------------- MOTOR 2 LOGIC -------------------------
            if override_counter2 > 0:
                robot.arm_bus.write("Goal_Position", override_goal2, ["motor2"])
            else:
                error2 = encoder_val2 - target2
                step2 = Kp * error2
                step2 = max(-max_step, min(step2, max_step))  # clip
                new_pos2 = current_pos2 + step2
                robot.arm_bus.write("Goal_Position", new_pos2, ["motor2"])

            hall_angle2 = np.clip((encoder_val2 - 1200) / 1600, 0, 1) * 20
            motor_angle2_degrees = (360.0 / 4096.0) * current_pos2

            # ------------------------- MOTOR 3 LOGIC -------------------------
            if override_counter3 > 0:
                robot.arm_bus.write("Goal_Position", override_goal3, ["motor3"])
            else:
                error3 = encoder_val3 - target3
                step3 = -Kp * error3
                step3 = max(-max_step, min(step3, max_step))  # clip
                new_pos3 = current_pos3 + step3
                robot.arm_bus.write("Goal_Position", new_pos3, ["motor3"])

            hall_angle3 = np.clip((encoder_val3 - 3150) / 300, 0, 1) * 20
            motor_angle3_degrees = (360.0 / 4096.0) * current_pos3

            # ------------------------------------------------------------------------
            # 3) Print debugging info
            # ------------------------------------------------------------------------
            print(f"Motor1 -> Hall_Angle: {int(motor_angle1_degrees + hall_angle1 - 20)}, "
                f"Motor_Angle: {int(motor_angle1_degrees - 10)}   "
                f"[Override={override_counter1 > 0} | {override_counter1} frames left]")

            print(f"Motor2 -> Hall_Angle: {int(motor_angle2_degrees + hall_angle2 - 20)}, "
                f"Motor_Angle: {int(motor_angle2_degrees - 10)}   "
                f"[Override={override_counter2 > 0} | {override_counter2} frames left]")

            print(f"Motor3 -> Hall_Angle: {int(motor_angle3_degrees + hall_angle3 - 20)}, "
                f"Motor_Angle: {int(motor_angle3_degrees - 10)}   "
                f"[Override={override_counter3 > 0} | {override_counter3} frames left]\n")

            # ------------------------------------------------------------------------
            # 4) Short delay so we don't overload the bus (and allow Pygame to update)
            # ------------------------------------------------------------------------
            time.sleep(0.001)

        pygame.quit()


    #SOCKET STUFF
    if False:
        import pygame
        import time
        import numpy as np
        import socket

        # ----------------- Socket Setup -----------------
        HOST = "172.20.10.2"   # Change to your server machine's IP
        PORT = 65432          # Port you want to listen on

        # Create the TCP socket and bind/listen
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}...")

        # Accept a single connection
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        # ----------------- Pygame Setup -----------------
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Motor Control Demo")

        # A flag to end the loop when the window is closed or ESC is pressed
        done = False

        # --------------------------------------------------------------------
        # 1) Frame counters for overrides
        #    If > 0, that motor is overriding the normal PID with a fixed goal.
        # --------------------------------------------------------------------
        override_counter1 = 0
        override_counter2 = 0
        override_counter3 = 0

        # Store the specific override goal position (in Dynamixel steps)
        override_goal1 = None
        override_goal2 = None
        override_goal3 = None

        # How many frames we hold the override position
        HOLD_FRAMES = 15

        # --- Your existing control parameters ---
        Kp = 0.7
        max_step = 200

        target1 = 3150  # sensor0 => motor1
        target2 = 3300  # sensor2 => motor2
        target3 = 3300  # sensor1 => motor3

        push_amount = 15  # degrees per nudge

        # For a typical Dynamixel-like system: 360 degrees -> 4096 steps
        STEPS_PER_DEG = 4096.0 / 360.0

        def deg_to_steps(deg):
            """
            Convert degrees -> (approx) motor steps
            """
            return int(deg * STEPS_PER_DEG)

        # ----------------- Main Loop (inside the socket connection) -----------------
        try:
            while not done:
                # ------------------------------------------------------------------------
                # 1) Handle Pygame events (user input)
                # ------------------------------------------------------------------------
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True

                        # ------------------------------------------------------------
                        # Key 4 -> Motor1 +12°
                        # ------------------------------------------------------------
                        elif event.key == pygame.K_4:
                            current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                            override_counter1 = HOLD_FRAMES
                            override_goal1 = current_pos1 + deg_to_steps(12)
                            print(f"Motor1 override: +12 deg for {HOLD_FRAMES} frames.")

                        # ------------------------------------------------------------
                        # Key 5 -> Motor1 -12°
                        # ------------------------------------------------------------
                        elif event.key == pygame.K_5:
                            current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                            override_counter1 = HOLD_FRAMES
                            override_goal1 = current_pos1 - deg_to_steps(12)
                            print(f"Motor1 override: -12 deg for {HOLD_FRAMES} frames.")

                        # ----------------------------------------------------------------
                        # Key 1 -> Motor2 -15°, Motor3 +15°
                        # ----------------------------------------------------------------
                        elif event.key == pygame.K_1:
                            current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                            current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                            override_counter2 = HOLD_FRAMES
                            override_counter3 = HOLD_FRAMES
                            override_goal2 = current_pos2 - deg_to_steps(15)
                            override_goal3 = current_pos3 + deg_to_steps(15)
                            print(f"Motor2 override: -{15} deg, Motor3 override: +{15} deg")

                        # ----------------------------------------------------------------
                        # Key 2 -> Motor2 -15°, Motor3 -15°
                        # ----------------------------------------------------------------
                        elif event.key == pygame.K_2:
                            current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                            current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                            override_counter2 = HOLD_FRAMES
                            override_counter3 = HOLD_FRAMES
                            override_goal2 = current_pos2 - deg_to_steps(15)
                            override_goal3 = current_pos3 - deg_to_steps(15)
                            print(f"Motor2 override: -{15} deg, Motor3 override: -{15} deg")

                        # ----------------------------------------------------------------
                        # Key 3 -> Motor2 +15°, Motor3 +15°
                        # ----------------------------------------------------------------
                        elif event.key == pygame.K_3:
                            current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                            current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                            override_counter2 = HOLD_FRAMES
                            override_counter3 = HOLD_FRAMES
                            override_goal2 = current_pos2 + deg_to_steps(15)
                            override_goal3 = current_pos3 + deg_to_steps(15)
                            print(f"Motor2 override: +{15} deg, Motor3 override: +{15} deg")

                        # ----------------------------------------------------------------
                        # Key 6 -> Motor2 +15°, Motor3 -15°
                        # ----------------------------------------------------------------
                        elif event.key == pygame.K_6:
                            current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                            current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                            override_counter2 = HOLD_FRAMES
                            override_counter3 = HOLD_FRAMES
                            override_goal2 = current_pos2 + deg_to_steps(15)
                            override_goal3 = current_pos3 - deg_to_steps(15)
                            print(f"Motor2 override: +{15} deg, Motor3 override: -{15} deg")

                # If ESC or window-quit triggered, exit loop
                if done:
                    break

                print(conn.recv(1024))
                # try:
                #     data = conn.recv(1024)  # This won't block
                #     if data:
                #         # Print raw bytes
                #         print("Raw data received:", data)
                #         # Decode text
                #         text = data.decode("utf-8", errors="replace")
                #         print("Decoded text:", text)
                # except BlockingIOError:
                #     pass

                # ------------------------------------------------------------------------
                # 2) Read the current sensor values and motor positions
                # ------------------------------------------------------------------------
                sensor_values = encoder.read()  # e.g. [sensor0, sensor1, sensor2, ...]
                encoder_val1 = sensor_values[0]  # sensor0 => motor1
                encoder_val3 = sensor_values[1]  # sensor1 => motor3
                encoder_val2 = sensor_values[2]  # sensor2 => motor2

                current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]

                # Decrement counters each frame if they're above 0
                if override_counter1 > 0:
                    override_counter1 -= 1
                if override_counter2 > 0:
                    override_counter2 -= 1
                if override_counter3 > 0:
                    override_counter3 -= 1

                # ------------------------- MOTOR 1 LOGIC -------------------------
                if override_counter1 > 0:
                    # If we're in override mode, keep sending that override_goal
                    # and skip PID.
                    robot.arm_bus.write("Goal_Position", override_goal1, ["motor1"])
                else:
                    # Normal PID logic
                    error1 = encoder_val1 - target1
                    step1 = -Kp * error1
                    step1 = max(-max_step, min(step1, max_step))  # clip
                    new_pos1 = current_pos1 + step1
                    robot.arm_bus.write("Goal_Position", new_pos1, ["motor1"])

                hall_angle1 = np.clip((encoder_val1 - 3250) / 400, 0, 1) * 20
                motor_angle1_degrees = (360.0 / 4096.0) * current_pos1

                # ------------------------- MOTOR 2 LOGIC -------------------------
                if override_counter2 > 0:
                    robot.arm_bus.write("Goal_Position", override_goal2, ["motor2"])
                else:
                    error2 = encoder_val2 - target2
                    step2 = Kp * error2
                    step2 = max(-max_step, min(step2, max_step))  # clip
                    new_pos2 = current_pos2 + step2
                    robot.arm_bus.write("Goal_Position", new_pos2, ["motor2"])

                hall_angle2 = np.clip((encoder_val2 - 1200) / 1600, 0, 1) * 20
                motor_angle2_degrees = (360.0 / 4096.0) * current_pos2

                # ------------------------- MOTOR 3 LOGIC -------------------------
                if override_counter3 > 0:
                    robot.arm_bus.write("Goal_Position", override_goal3, ["motor3"])
                else:
                    error3 = encoder_val3 - target3
                    step3 = -Kp * error3
                    step3 = max(-max_step, min(step3, max_step))  # clip
                    new_pos3 = current_pos3 + step3
                    robot.arm_bus.write("Goal_Position", new_pos3, ["motor3"])

                hall_angle3 = np.clip((encoder_val3 - 3150) / 300, 0, 1) * 20
                motor_angle3_degrees = (360.0 / 4096.0) * current_pos3

                # ------------------------------------------------------------------------
                # 3) Print debugging info
                # ------------------------------------------------------------------------
                # print(f"Motor1 -> Hall_Angle: {int(motor_angle1_degrees + hall_angle1 - 20)}, "
                #     f"Motor_Angle: {int(motor_angle1_degrees - 10)}   "
                #     f"[Override={override_counter1 > 0} | {override_counter1} frames left]")

                # print(f"Motor2 -> Hall_Angle: {int(motor_angle2_degrees + hall_angle2 - 20)}, "
                #     f"Motor_Angle: {int(motor_angle2_degrees - 10)}   "
                #     f"[Override={override_counter2 > 0} | {override_counter2} frames left]")

                # print(f"Motor3 -> Hall_Angle: {int(motor_angle3_degrees + hall_angle3 - 20)}, "
                #     f"Motor_Angle: {int(motor_angle3_degrees - 10)}   "
                #     f"[Override={override_counter3 > 0} | {override_counter3} frames left]\n")

                # ------------------------------------------------------------------------
                # 4) Send angles via socket + short delay
                # ------------------------------------------------------------------------
                angle_to_send = f"S{motor_angle2_degrees},{motor_angle3_degrees},{motor_angle1_degrees}E"
                conn.sendall(angle_to_send.encode("utf-8"))

                time.sleep(0.001)

        finally:
            # Close pygame and the connection on exit
            pygame.quit()
            conn.close()
            server_socket.close()


    #FINAL
    if True:
        import pygame
        import time
        import numpy as np
        import socket

        # ----------------- Socket Setup -----------------
        HOST = "172.20.10.2"   # Change to your server machine's IP
        PORT = 65431          # Port you want to listen on1
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}...")

        # Accept a single connection (blocking until client connects)
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        # Make the socket non-blocking so .recv() won't halt if no data is incoming
        conn.setblocking(False)

        # ----------------- Pygame Setup -----------------
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Motor Control Demo")

        done = False

        # --------------------------------------------------------------------
        # 1) Frame counters for overrides
        #    If > 0, that motor is overriding the normal PID with a fixed goal.
        # --------------------------------------------------------------------
        override_counter1 = 0
        override_counter2 = 0
        override_counter3 = 0

        # Store the specific override goal position (in Dynamixel steps)
        override_goal1 = None
        override_goal2 = None
        override_goal3 = None

        # How many frames we hold the override position
        HOLD_FRAMES = 5

        # --- Your existing control parameters ---
        Kp = 0.7
        max_step = 200

        target1 = 3150  # sensor0 => motor1
        target2 = 3300  # sensor2 => motor2
        target3 = 3300  # sensor1 => motor3

        # We'll nudge each motor by these amounts
        push_amount12 = 15  # degrees for "4"/"5"
        push_amount15 = 15  # degrees for commands "1","2","3","6"

        # For a typical Dynamixel-like system: 360 degrees -> 4096 steps
        STEPS_PER_DEG = 4096.0 / 360.0

        def deg_to_steps(deg):
            """
            Convert degrees -> (approx) motor steps
            """
            return int(deg * STEPS_PER_DEG)

        try:
            while not done:
                # ------------------------------------------------------------------------
                # 1) Handle minimal Pygame events: QUIT or ESC to exit
                # ------------------------------------------------------------------------
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True

                if done:
                    break

                # ------------------------------------------------------------------------
                # 2) Attempt to receive data from the socket (non-blocking)
                # ------------------------------------------------------------------------
                try:
                    data = conn.recv(1024)  # won't block, because setblocking(False)
                    if data:
                        # Print raw data
                        print("Raw data received:", data)
                        # Decode as UTF-8
                        text = data.decode("utf-8", errors="replace").strip()

                        # We might get multiple lines/commands in one chunk,
                        # so split them on newline or spaces if needed:
                        commands = text.split()
                        
                        for cmd in commands:
                            # If we only ever expect single-digit commands, you can check directly:
                            if cmd == '4':
                                # Motor1 +12 deg
                                current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                                override_counter1 = HOLD_FRAMES
                                override_goal1 = current_pos1 + deg_to_steps(push_amount12)
                                print(f"Motor1 override: +{push_amount12} deg")

                            elif cmd == '5':
                                # Motor1 -12 deg
                                current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                                override_counter1 = HOLD_FRAMES
                                override_goal1 = current_pos1 - deg_to_steps(push_amount12)
                                print(f"Motor1 override: -{push_amount12} deg")

                            elif cmd == '1':
                                # Motor2 -15°, Motor3 +15°
                                current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                                current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                                override_counter2 = HOLD_FRAMES
                                override_counter3 = HOLD_FRAMES
                                override_goal2 = current_pos2 - deg_to_steps(push_amount15)
                                override_goal3 = current_pos3 + deg_to_steps(push_amount15)
                                print(f"Motor2 override: -{push_amount15} deg, Motor3 override: +{push_amount15} deg")

                            elif cmd == '2':
                                # Motor2 -15°, Motor3 -15°
                                current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                                current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                                override_counter2 = HOLD_FRAMES
                                override_counter3 = HOLD_FRAMES
                                override_goal2 = current_pos2 - deg_to_steps(push_amount15)
                                override_goal3 = current_pos3 - deg_to_steps(push_amount15)
                                print(f"Motor2 override: -{push_amount15} deg, Motor3 override: -{push_amount15} deg")

                            elif cmd == '3':
                                # Motor2 +15°, Motor3 +15°
                                current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                                current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                                override_counter2 = HOLD_FRAMES
                                override_counter3 = HOLD_FRAMES
                                override_goal2 = current_pos2 + deg_to_steps(push_amount15)
                                override_goal3 = current_pos3 + deg_to_steps(push_amount15)
                                print(f"Motor2 override: +{push_amount15} deg, Motor3 override: +{push_amount15} deg")

                            elif cmd == '6':
                                # Motor2 +15°, Motor3 -15°
                                current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                                current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]
                                override_counter2 = HOLD_FRAMES
                                override_counter3 = HOLD_FRAMES
                                override_goal2 = current_pos2 + deg_to_steps(push_amount15)
                                override_goal3 = current_pos3 - deg_to_steps(push_amount15)
                                print(f"Motor2 override: +{push_amount15} deg, Motor3 override: -{push_amount15} deg")
                            
                            else:
                                # Unrecognized command or other text
                                print(f"Ignoring unknown cmd: {cmd}")

                    else:
                        # If data is empty, client likely disconnected
                        print("Client disconnected.")
                        done = True
                except BlockingIOError:
                    # No data arrived this loop; ignore and move on
                    pass

                # ------------------------------------------------------------------------
                # 3) Read sensor values and motor positions, apply override / PID logic
                # ------------------------------------------------------------------------
                sensor_values = encoder.read()  # e.g. [sensor0, sensor1, sensor2, ...]
                encoder_val1 = sensor_values[0]  # sensor0 => motor1
                encoder_val3 = sensor_values[1]  # sensor1 => motor3
                encoder_val2 = sensor_values[2]  # sensor2 => motor2

                current_pos1 = robot.arm_bus.read("Present_Position", ["motor1"])[0]
                current_pos2 = robot.arm_bus.read("Present_Position", ["motor2"])[0]
                current_pos3 = robot.arm_bus.read("Present_Position", ["motor3"])[0]

                # Decrement counters each frame if they're above 0
                if override_counter1 > 0:
                    override_counter1 -= 1
                if override_counter2 > 0:
                    override_counter2 -= 1
                if override_counter3 > 0:
                    override_counter3 -= 1

                # ------------------------- MOTOR 1 LOGIC -------------------------
                if override_counter1 > 0:
                    # If we're in override mode, keep sending that override_goal
                    # and skip PID.
                    robot.arm_bus.write("Goal_Position", override_goal1, ["motor1"])
                else:
                    # Normal PID logic
                    error1 = encoder_val1 - target1
                    step1 = -Kp * error1
                    step1 = max(-max_step, min(step1, max_step))  # clip
                    new_pos1 = current_pos1 + step1
                    robot.arm_bus.write("Goal_Position", new_pos1, ["motor1"])

                hall_angle1 = np.clip((encoder_val1 - 3250) / 400, 0, 1) * 20
                motor_angle1_degrees = (360.0 / 4096.0) * current_pos1-180

                # ------------------------- MOTOR 2 LOGIC -------------------------
                if override_counter2 > 0:
                    robot.arm_bus.write("Goal_Position", override_goal2, ["motor2"])
                else:
                    error2 = encoder_val2 - target2
                    step2 = Kp * error2
                    step2 = max(-max_step, min(step2, max_step))  # clip
                    new_pos2 = current_pos2 + step2
                    robot.arm_bus.write("Goal_Position", new_pos2, ["motor2"])

                hall_angle2 = np.clip((encoder_val2 - 1200) / 1600, 0, 1) * 20
                motor_angle2_degrees = 360-(360.0 / 4096.0) * current_pos2

                # ------------------------- MOTOR 3 LOGIC -------------------------
                if override_counter3 > 0:
                    robot.arm_bus.write("Goal_Position", override_goal3, ["motor3"])
                else:
                    error3 = encoder_val3 - target3
                    step3 = -Kp * error3
                    step3 = max(-max_step, min(step3, max_step))  # clip
                    new_pos3 = current_pos3 + step3
                    robot.arm_bus.write("Goal_Position", new_pos3, ["motor3"])

                hall_angle3 = np.clip((encoder_val3 - 3150) / 300, 0, 1) * 20
                motor_angle3_degrees = (360.0 / 4096.0) * current_pos3

                # ------------------------------------------------------------------------
                # 4) (Optional) Send angles back to client
                # ------------------------------------------------------------------------
                angle_to_send = f"S{motor_angle2_degrees},{motor_angle3_degrees},{motor_angle1_degrees}E"
                conn.sendall(angle_to_send.encode("utf-8"))

                # Short delay so we don't overload the bus (and allow Pygame to update)
                time.sleep(0.001)

        finally:
            # Cleanup on exit
            pygame.quit()
            conn.close()
            server_socket.close()
            print("Closed everything. Bye!")



if __name__ == "__main__":
    main()
