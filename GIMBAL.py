import asyncio
from mavsdk import System
from mavsdk.gimbal import GimbalMode, ControlMode

async def set_gimbal_mode(drone):
    await drone.gimbal.take_control(ControlMode.PRIMARY)
    # Set the gimbal to YAW_LOCK (= 1) mode (see docs for the difference)
    # Other valid values: YAW_FOLLOW (= 0)
    # YAW_LOCK will fix the gimbal pointing to an absolute direction,
    # whereas YAW_FOLLOW will point relative to vehicle heading.
    # error if Gimbal not attached.
    await drone.gimbal.set_mode(GimbalMode.YAW_FOLLOW)

async def gimbal_console(drone,cmd):
    if cmd==0:
        await drone.gimbal.set_pitch_and_yaw(0, 0)
        #look forward
    elif cmd==1:
        await drone.gimbal.set_pitch_and_yaw(-10, 0)
        #look down
    elif cmd==2:
        await drone.gimbal.set_pitch_and_yaw(10, 0)
        #look up
    elif cmd==3:
        await drone.gimbal.set_pitch_and_yaw(0,10)
        #look right
    elif cmd==4:
        await drone.gimbal.set_pitch_and_yaw(10,-10)
        #look left
        
async def release_control(drone):
    #Release control of gimbal again
    await drone.gimbal.release_control()
    
