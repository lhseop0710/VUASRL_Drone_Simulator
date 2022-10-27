import asyncio, random
from mavsdk import System #if you get error here you will see a bulb like charcter press it and install the library.
from mavsdk.mission import (MissionItem, MissionPlan)
import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

# import second_window
# from second_window import secondwind
import second_window_Test
from second_window_Test import secondwindow
from PyQt5 import QtCore
import draw

class run():
    manual_inputs = [
        [0, 0, 0.5, 0],  # no movement
        [-1, 0, 0.5, 0],  # minimum roll
        [1, 0, 0.5, 0],  # maximum roll
        [0, -1, 0.5, 0],  # minimum pitch
        [0, 1, 0.5, 0],  # maximum pitch
        [0, 0, 0.5, -1],  # minimum yaw
        [0, 0, 0.5, 1],  # maximum yaw
        [0, 0, 1, 0],  # max throttle
        [0, 0, 0, 0],  # minimum throttle
    ]

    gps_info_list = [["",""]]
    print(gps_info_list)
    mission_items = []

    async def run(self):
        global drone, position, absolute_altitude
        drone = System()
        await drone.connect(system_address="udp://:14540")  # Connects to the UAV

        print("Establishing Connection...")
        # Check CONNECTION & if there is a positive connection Feedback = CONNECTED
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("UAV target UUID: {state.uuid}")  # Prints the UUID of the UAV to which the system connected
                async for position in drone.telemetry.position():
                    print(position)
                    async for gpsinfo in drone.telemetry.gps_info():
                        self.gps_info_list.clear()
                        self.gps_info_list.append(gpsinfo)
                        print(self.gps_info_list[0])
                        break
                    break
                break

        print("Establishing GPS lock on UAV..")
        # Checks the gps Connection via telemetry health command
        async for health in drone.telemetry.health():
            if health.is_global_position_ok:
                print("Established GPS lock...")  # GPS health approved
                break

        print("Fetching amsl altitude at home location....")
        async for terrain_info in drone.telemetry.home():
            absolute_altitude = terrain_info.absolute_altitude_m
            break


        # set the manual control input after arming
        await drone.manual_control.set_manual_control_input(
            float(0), float(0), float(0.5), float(0)
        )

        print("Arming UAV")
        await drone.action.arm()


    async def takeoff(self):
        await drone.action.set_takeoff_altitude(10)
        await drone.action.takeoff()
        # await asyncio.sleep(10)

    async def land(self):
        await drone.action.land()

    async def start_position_control(self):
        print("-- Starting manual control")
        while True:
            if drone.telemetry.armed():
                await drone.manual_control.start_position_control()
                # start manual control
                # grabs a random input from the test list
                # WARNING - your simulation vehicle may crash if its unlucky enough
                input_index = random.randint(0, len(self.manual_inputs) - 1)
                input_list = self.manual_inputs[input_index]

                # get current state of roll axis (between -1 and 1)
                roll = float(input_list[0])
                # get current state of pitch axis (between -1 and 1)
                pitch = float(input_list[1])
                # get current state of throttle axis (between -1 and 1, but between 0 and 1 is expected)
                throttle = float(input_list[2])
                # get current state of yaw axis (between -1 and 1)
                yaw = float(input_list[3])

                await drone.manual_control.set_manual_control_input(roll, pitch, throttle, yaw)
                if not drone.telemetry.armed():
                    break
                break
            break

    async def start_mission(self):
        WindowClass.goto_position()

        mission_plane = MissionPlan(WindowClass.mission_items)
        await drone.mission.upload_mission(mission_plane)
        await drone.mission.start_mission()

    async def goto_location(self, lat, lon, altitude):
        flying_alt = absolute_altitude + altitude
        await drone.action.set_takeoff_altitude(altitude)
        await drone.action.goto_location(lat, lon, flying_alt, 0)



form_main = uic.loadUiType("untitled.ui")[0]
class WindowClass(QMainWindow, form_main):
    loop = asyncio.get_event_loop()
    back_ground = "pablo.png"

    def initUI(self) :
        self.show()

    def __init__(self, parent = None) :
        super(WindowClass, self).__init__(parent)

        self.mission_items = []        #append_Mission_Waypoints
        #Main_Window_Size_setting
        self.setupUi(self)
        self.setFixedSize(1400, 825)
        self.setWindowTitle("VUASRL_UAV_Ground_Controll")
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        #Drawing_WayPoints_Background_Settings

        # self.label.setPixmap(self.qPixmapFileVar)
        # self.label.resize(self.label.width(), self.label.height())
        self.btn_trajectory.clicked.connect(self.show_trajectory)
        self.btn_arm.clicked.connect(self.arm)
        self.btn_takeoff.clicked.connect(self.takeoff)
        self.btn_land.clicked.connect(self.land)
        self.btn_position_control.clicked.connect(self.position_control)
        self.btn_erase_waypoints.clicked.connect(self.erase_waypoints)
        self.btn_start_waypoints.clicked.connect(self.start_waypoints)
        self.btn_goto.clicked.connect(self.goto_position)
        ###label_set

    def show_trajectory(self):
        self.second = secondwindow()  # 두번째창 생성
        self.second.exec()  # 두번째창 닫을때까지 기다림
            # self.show()  # 두번쨰창 닫으면 다시 메인윈도우


    def arm(self):
        self.loop.run_until_complete(run().run())
        self.gps_info_label.setText(str(run.gps_info_list[0]))

    def takeoff(self):
        print("Taking Off")
        self.loop.run_until_complete(run().takeoff())

    def land(self):
        print("LANDING")
        self.loop.run_until_complete(run().land())

    def position_control(self):
        self.loop.run_until_complete(run().start_position_control())
        print("Position Control")

    def erase_waypoints(self):
        second_window_Test.chosen_points.clear()
        print("Reset!!_Waypoint")

    def start_waypoints(self):
        print("start_waypoints_mission")

    def goto_position(self):
        lat = self.textEdit_lat.toPlainText()
        lon = self.textEdit_lon.toPlainText()
        altitude = self.textEdit_altitude.toPlainText()
        if lat == None or lon == None or altitude == None:
            self.label_lat.setText("47.3967339")
            self.lable_lon.setText("8.539988")
            self.label_altitude.setText("50")
        else:
            self.label_lat.setText(lat)
            self.label_lon.setText(lon)
            self.label_altitude.setText(altitude)
            self.loop.run_until_complete(run().takeoff())
            self.loop.run_until_complete(run().goto_location(float(lat), float(lon), float(altitude)))
            # self.loop.run_until_complete(run().land())



# class mavsdk.mission.MissionItem(latitude_deg, longitude_deg, relative_altitude_m, speed_m_s, is_fly_through,
#                                   imbal_pitch_deg, gimbal_yaw_deg, camera_action, loiter_time_s, camera_photo_interval_s, acceptance_radius_m, yaw_deg, camera_photo_distance_m)
# Bases: object
#
# Type representing a mission item.
#
# A MissionItem can contain a position and/or actions. Mission items are building blocks to assemble a mission,
# which can be sent to (or received from) a system. They cannot be used independently.
#
    # Parameters:
        # latitude_deg (double) – Latitude in degrees (range: -90 to +90)
        # longitude_deg (double) – Longitude in degrees (range: -180 to +180)
        # relative_altitude_m (float) – Altitude relative to takeoff altitude in metres
        # speed_m_s (float) – Speed to use after this mission item (in metres/second)
        # is_fly_through (bool) – True will make the drone fly through without stopping, while false will make the drone stop on the waypoint
        # gimbal_pitch_deg (float) – Gimbal pitch (in degrees)
        # gimbal_yaw_deg (float) – Gimbal yaw (in degrees)
        # camera_action (CameraAction) – Camera action to trigger at this mission item
        # loiter_time_s (float) – Loiter time (in seconds)
        # camera_photo_interval_s (double) – Camera photo interval to use after this mission item (in seconds)
        # acceptance_radius_m (float) – Radius for completing a mission item (in metres)
        # yaw_deg (float) – Absolute yaw angle (in degrees)
        # camera_photo_distance_m (float) – Camera photo distance to use after this mission item (in meters)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
    # dir_path="cd ~/Documents/"
    # terminal_command = f"{dir_path}"
    # os.system(terminal_command)
    # os.system("./QGroundControl.AppImage")
    # # Process(target=func2()).start()  Process(target=func1()).start()