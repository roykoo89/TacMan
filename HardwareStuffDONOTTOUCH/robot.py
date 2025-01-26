from lerobot.common.robot_devices.motors.feetech import (
    CalibrationMode,
    FeetechMotorsBus,
)

class HopeJuniorRobot:
    def __init__(self):
        self.arm_port = "/dev/ttyACM0"
        self.hand_port = "/dev/ttyACM1"
        self.shoulder_port = "/dev/ttyUSB0"
        self.arm_bus = FeetechMotorsBus(
            port = self.arm_port,
            motors={
                "motor1": (1, "sts3250"),
                "motor2": (2, "sts3250"),
                "motor3": (3, "sts3250"),
                
                #"shoulder_pitch": [1, "sts3215"],
                #"shoulder_yaw": [2, "sts3250"],  # TODO: sts3250
                # "shoulder_roll": [3, "sts3250"],  # TODO: sts3250
                # "elbow_flex": [4, "sts3250"],
                # "wrist_roll": [5, "sts3215"],
                # "wrist_yaw": [6, "sts3215"],
                # "wrist_pitch": [7, "sts3215"],
            },
            protocol_version=0,
        )
        self.shoulder_bus = FeetechMotorsBus(
            port = self.shoulder_port,
            motors={
                # "motor1": (2, "sts3250"),
                # "motor2": (1, "scs0009"),
                "shoulder_pitch": [1, "sm8512bl"],
            },
            protocol_version=0,
        )
        self.hand_bus = FeetechMotorsBus(
            port=self.hand_port,
            motors={
                "thumb_basel_rotation": [30, "scs0009"],
                "thumb_flexor": [27, "scs0009"],
                "thumb_pinky_side": [26, "scs0009"],
                "thumb_thumb_side": [28, "scs0009"],
                "index_flexor": [25, "scs0009"],
                "index_pinky_side": [31, "scs0009"],
                "index_thumb_side": [32, "scs0009"],
                "middle_flexor": [24, "scs0009"],
                "middle_pinky_side": [33, "scs0009"],
                "middle_thumb_side": [34, "scs0009"],
                "ring_flexor": [21, "scs0009"],
                "ring_pinky_side": [36, "scs0009"],
                "ring_thumb_side": [35, "scs0009"],
                "pinky_flexor": [23, "scs0009"],
                "pinky_pinky_side": [38, "scs0009"],
                "pinky_thumb_side": [37, "scs0009"],
            },
            protocol_version=1,#1
            group_sync_read=False,
        )

        self.arm_calib_dict = self.get_arm_calibration()
        self.hand_calib_dict = self.get_hand_calibration()

    def get_hand_calibration(self):
        homing_offset = [0] * len(self.hand_bus.motor_names)
        drive_mode = [0] * len(self.hand_bus.motor_names)

        start_pos = [
            450,  # thumb_basel_rotation
            900,  # thumb_flexor
            300,    # thumb_pinky_side
            400,  # thumb_thumb_side
            100,  # index_flexor
            250,   # index_pinky_side
            650,  # index_thumb_side
            100,  # middle_flexor
            200,  # middle_pinky_side
            50,   # middle_thumb_side
            100,  # ring_flexor
            500,  # ring_pinky_side
            980,  # ring_thumb_side
            100,  # pinky_flexor
            950,  # pinky_pinky_side
            750,  # pinky_thumb_side
        ]

        end_pos = [
            start_pos[0] - 400,  # thumb_basel_rotation
            start_pos[1] - 300,  # thumb_flexor
            start_pos[2] + 700,  # thumb_pinky_side
            start_pos[3] + 700,  # thumb_thumb_side
            start_pos[4] + 900,  # index_flexor
            start_pos[5] + 500,  # index_pinky_side
            start_pos[6] - 500,  # index_thumb_side
            start_pos[7] + 900,  # middle_flexor
            start_pos[8] + 700,  # middle_pinky_side
            start_pos[9] + 700,  # middle_thumb_side
            start_pos[10] + 900, # ring_flexor
            start_pos[11] + 700, # ring_pinky_side
            start_pos[12] - 600, # ring_thumb_side
            start_pos[13] + 900, # pinky_flexor
            start_pos[14] - 700, # pinky_pinky_side
            start_pos[15] - 700, # pinky_thumb_side
        ]

        

        calib_modes = [CalibrationMode.LINEAR.name] * len(self.hand_bus.motor_names)

        calib_dict = {
            "homing_offset": homing_offset,
            "drive_mode": drive_mode,
            "start_pos": start_pos,
            "end_pos": end_pos,
            "calib_mode": calib_modes,
            "motor_names": self.hand_bus.motor_names,
        }
        return calib_dict
    
    def get_arm_calibration(self):

        homing_offset = [0] * len(self.arm_bus.motor_names)
        drive_mode = [0] * len(self.arm_bus.motor_names)

        start_pos = [
            2800,  # shoulder_forward
            1800,  # shoulder_roll
            2200,  # bend_elbow
            700,  # wrist_roll
            1700,  # wrist_yaw
            800,  # wrist_pitch
        ]

        end_pos = [
            3200,  # shoulder_forward
            2900,  # shoulder_roll
            3500,  # bend_elbow
            2700,  # wrist_roll
            2200,  # wrist_yaw
            1300,  # wrist_pitch
        ]

        calib_modes = [CalibrationMode.LINEAR.name] * len(self.arm_bus.motor_names)

        calib_dict = {
            "homing_offset": homing_offset,
            "drive_mode": drive_mode,
            "start_pos": start_pos,
            "end_pos": end_pos,
            "calib_mode": calib_modes,
            "motor_names": self.arm_bus.motor_names,
        }
        return calib_dict


    def get_shoulder_calibration(self):

        homing_offset = [0] * len(self.shoulder_bus.motor_names)
        drive_mode = [0] * len(self.shoulder_bus.motor_names)

        start_pos = [
            1800,   # shoulder_up
        ]

        end_pos = [
            3300,  # shoulder_up
        ]

        calib_modes = [CalibrationMode.LINEAR.name] * len(self.shoulder_bus.motor_names)

        calib_dict = {
            "homing_offset": homing_offset,
            "drive_mode": drive_mode,
            "start_pos": start_pos,
            "end_pos": end_pos,
            "calib_mode": calib_modes,
            "motor_names": self.shoulder_bus.motor_names,
        }
        return calib_dict

    def connect_arm(self):
        self.arm_bus.connect()

    def connect_hand(self):
        self.hand_bus.connect()

    def connect_shoulder(self):
        self.shoulder_bus.connect()
