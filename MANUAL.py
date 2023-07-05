import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityNedYaw,VelocityBodyYawspeed)
""" 
    make sure the drone is already in AIR

"""

TIME=5 #sec 

async def map_exec(i,drone):

    if(i<0):
        await drone.offboard.stop()

    elif(i==0):
        PACK=[0,0,0,0]

    elif(i==1):
        PACK=[2,0,0,0]
    
    elif(i==2):
        PACK=[0,2.0,0,0]
    
    elif(i==3):
        PACK=[0,0,2,0]
    
    elif(i==4):
        PACK=[0,0,0,10]
    
    elif(i==5):
        PACK=[-2,0,0,0]
    
    elif(i==6):
        PACK=[0,-2,0,0]
    
    elif(i==7):
        PACK=[0,0,-2,0]
    
    elif(i==8):
        PACK=[0,0,0,-10]
    
    pack=PACK
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(float(pack[0]), float(pack[1]), float(pack[2]), float(pack[3]))) 
    
async def change_2_offboard(drone):

    await drone.connect()
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            # print("-- Global position estimate OK")
            break

    await drone.action.arm()
    # make sure its already in air
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
    await drone.offboard.start()
    #mark your mode
    
    return

async def manual(i, drone):
    # i=int(input("input_for _manual"))
    await map_exec(i,drone)
    # print("lol")
    # asyncio.run(c())
    # asyncio.run(a())
