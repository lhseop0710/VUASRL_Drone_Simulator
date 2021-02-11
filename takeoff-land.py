import asyncio
from mavsdk import System #if you get error here you will see a bulb like charcter press it and install the library.

async def run():
    uav = System()
    await uav.connect(system_address="udp://:14540") #Connects to the UAV

    print("Establishing Connection...")
    #Check CONNECTION & if there is a positive connection Feedback = CONNECTED
    async for  state in uav.core.connection_state():
        if state.is_connected:
            print("UAV target UUID: {state.uuid}") #Prints the UUID of the UAV to which the system connected
            break


    print("Establishing GPS lock on UAV..")
    #Checks the gps Connection via telemetry health command
    async for health in uav.telemetry.health():
        if health.is_global_position_ok:
            print("Established GPS lock...")#GPS health approved
            break

    print("Arming UAV")
    await uav.action.arm()

    print("Taking Off")
    await uav.action.takeoff()

    await asyncio.sleep(10)

    print("LANDING")
    await uav.action.land()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
