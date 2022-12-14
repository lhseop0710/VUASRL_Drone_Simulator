import asyncio, random
import threading
import mavsdk.telemetry
from mavsdk import System #if you get error here you will see a bulb like charcter press it and install the library.
from mavsdk.mission import (MissionItem, MissionPlan)
import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import second_window_Test
from second_window_Test import secondwindow
from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI, qfi_VSI, qfi_TC  #for Flight instruments



i = 0               #for sensing thread
class run():                    #Drone, UAM Start Loop Develop
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

    body = []

    async def run(self):        #start drone, loop
        global drone, position, absolute_altitude
        drone = System()
        await drone.connect(system_address="udp://:14540")  # Connects to the UAV
                                                            # Drone Status check

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

        # await mavsdk.telemetry.AngularVelocityBody
    async def angular(self):                            #Droen Angular rate check for Mission Plane
        async for body in drone.telemetry.attitude_angular_velocity_body():
            print(f"body info: {body}")

    async def speed_set(self, speed):                   #Drone Speed set
        await drone.action.set_current_speed(float(speed))


    async def takeoff(self, altitude):                  #Drone takeoff
        await drone.action.set_takeoff_altitude(float(altitude))
        await drone.action.takeoff()
        await asyncio.sleep(10)

    async def land(self):                               #Drone takeoff
        await drone.action.land()

    async def start_position_control(self):              #Drone position control for xbox360 controller
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

    async def upload_mission(self):                         #Drone Waypoints Mission Import to Misson Planer
        mission_plane = MissionPlan(second_window_Test.mission_items)
        await drone.mission.upload_mission(mission_plane)

    async def start_mission(self):                          #start Waypoints Flight Loop
        await drone.mission.start_mission()

    async def goto_location(self, lat, lon, altitude):      #start Point-to-Point Flight Loop
        flying_alt = absolute_altitude + altitude
        await drone.action.set_takeoff_altitude(altitude)
        await drone.action.goto_location(lat, lon, flying_alt, 0)



form_main = uic.loadUiType("untitled.ui")[0]                #Grapical User Interface Develope Using QtDesigner
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
        self.setFixedSize(1400, 850)
        self.setWindowTitle("VUASRL_UAV_Ground_Controll")
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        #Drawing_WayPoints_Background_Settings

        self.btn_trajectory.clicked.connect(self.show_trajectory)            #Button_Events_Function_deveop
        self.btn_arm.clicked.connect(self.arm)
        self.btn_takeoff.clicked.connect(self.takeoff)
        self.btn_land.clicked.connect(self.land)
        self.btn_position_control.clicked.connect(self.position_control)
        self.btn_erase_waypoints.clicked.connect(self.erase_waypoints)
        self.btn_upload_waypoints.clicked.connect(self.upload_waypoints)
        self.btn_start_waypoints.clicked.connect(self.start_waypoints)
        self.btn_goto.clicked.connect(self.goto_position)
        self.btn_set_landing_site_list.clicked.connect(self.set_landing_site_list)
        self.btn_set_landing_site_text.clicked.connect(self.set_landing_site_text)
        ###label_set



        ##instruments set
        self.mainLayout = QVBoxLayout()                                     #Flight Instrument Develop after this Olyimpiad
        self.mainLayout.addLayout(self.adi_gridLayout, 70)
        self.adi = qfi_ADI.qfi_ADI(self)
        self.adi.resize(300, 300)
        self.adi.reinit()
        self.adi_gridLayout.addWidget(self.adi, 0, 0)

        # self.timer=QTimer()                                               #for sensing thread
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.update1)
        self.show()

    # def update1(self):                                                    #for sensing thread
    #     global i
    #     self.loop.run_until_complete(run().angular())
    #     self.pitch_value.setText(str(data[1]))
    #     self.roll_value.setText(str(data[2]))
    #     self.adi.setRoll(float(data[1]))
    #     self.adi.setPitch(float(data[2]))
    #     self.adi.viewUpdate.emit()

    def show_trajectory(self):                               #Waypoint Mission Painter Show
        self.second = secondwindow()  # ???????????? ??????
        self.second.exec()  # ???????????? ??????????????? ?????????
            # self.show()  # ???????????? ????????? ?????? ???????????????


    def arm(self):                                             #Start Drone Armming
        # self.timer.start()
        self.loop.run_until_complete(run().run())
        self.gps_info_label.setText(str(run.gps_info_list[0]))


    def takeoff(self):                                          #Start Drone take-off
        print("Taking Off")
        alt = self.label_altitude.text()
        self.loop.run_until_complete(run().takeoff(float(alt)))

    def land(self):                                             #Landing
        print("LANDING")
        self.loop.run_until_complete(run().land())

    def position_control(self):                                   #start position control using controller
        self.loop.run_until_complete(run().start_position_control())
        print("Position Control")

    def erase_waypoints(self):                                   #Waypoint Painter a& Waypoints Mission item reset
        second_window_Test.chosen_points.clear()
        second_window_Test.mission_items.clear()
        print("Reset!!_Waypoint")

    def upload_waypoints(self):                                   #Waypoints Mission item upload
        self.loop.run_until_complete(run().upload_mission())

    def start_waypoints(self):                                     #start Waypoints flight
        print("start_waypoints_mission")
        self.loop.run_until_complete(run().start_mission())


    def goto_position(self):                                        #start point-to-point flight
        lat = self.label_lat.text()
        lon = self.label_lon.text()
        alt = self.label_altitude.text()
        speed = self.label_speed.text()
        print(lat, lon , alt, speed)

        self.loop.run_until_complete(run().takeoff(float(alt)))
        self.loop.run_until_complete(run().goto_location(float(lat), float(lon), float(alt)))
        self.loop.run_until_complete(run().speed_set(float(speed)))
    def set_landing_site_text(self):                                #set point-to-point flight position
        lat = self.textEdit_lat.toPlainText()
        lon = self.textEdit_lon.toPlainText()
        altitude = self.textEdit_altitude.toPlainText()
        speed = self.textEdit_speed.toPlainText()
        self.label_lat.setText(str(lat))
        self.label_lon.setText(str(lon))
        self.label_altitude.setText(str(altitude))
        self.label_speed.setText(str(speed))

    def set_landing_site_list(self):                                #set point-to-point flight destination
        item = self.listWidget.currentItem()
        value = self.listWidget.currentRow()
        if value == 0 :
            self.label_lat.setText("47.3961599")                #Osong-station Lat, Lon
            self.label_lon.setText("8.5402997")
            self.label_altitude.setText("50")
        elif value == 1 :
            self.label_lat.setText("47.397183399999996")        #Cheongju-station Lat, Lon
            self.label_lon.setText("8.552031999999999")
            self.label_altitude.setText("50")
        else:
            print("choice")

def VCS():
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # myWindow = WindowClass()
    # myWindow.show()
    # sys.exit(app.exec_())
    t1 = threading.Thread(target=VCS())
    t2 = threading.Thread(target=run.angular)           #Multithreading for Flight instrument Sensing
    t1.start()
    t2.start()

#     # dir_path="cd ~/Documents/"
#     # terminal_command = f"{dir_path}"
#     # os.system(terminal_command)
#     # os.system("./QGroundControl.AppImage")
#     # # Process(target=func2()).start()  Process(target=func1()).start()