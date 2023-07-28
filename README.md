# ros_drone
A simple console based on mavsdk and asyncio capabilities. Currently supported for PX4 firmware only.

REQUIREMENTS python3.10+, MAVSDK, ASYNCIO, GAZEBO9( gimbal support for model <gazebo-classic_typhoon_h480>), Jmavsim(no gimbal support), PX4_sitl
OPTIONAL QGC, INAV

# HOW TO USE THE CONSOLE
>>>import CONSOLE
>>>drone=CONSOLE.Console()
>>>data=data={"lat":47.397,"long":8.5455,"alt":10,"speed":1,"deg":3,"radius":10}
>>>drone.run(0,data) # 0 intialises the drone and takes-off
>>>drone.run( command_number , associated_data )



 
