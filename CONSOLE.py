import mavsdk as m
import asyncio
import MANUAL as man
import GIMBAL as gim
import TELEMETRY as telem
from mavsdk.mission import (MissionItem, MissionPlan)

class Console():
    """ call functions by using the key word await inside a async coroutine intialised to run"""
    def __init__(self, connection = "udp://:14540"):
        self.telemetry=None
        self.drone=m.System()
        self.TELEM=None
        self.curr=None
        self.data=None
        self.loop= asyncio.get_event_loop()
        
           
    def start_telem(self,drone):
        self.TELEM = telem.telem(drone)
        self.TELEM._run()
            
    async def initialize(self):
        """Run before every flight"""
        await self.drone.connect()
        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                break

        armed = await self.drone.action.arm()
        takeoff = await self.drone.action.takeoff()

        self.start_telem(self.drone)
        #self.home = telem.latitude_deg,telem.longitude_deg
        return
            
    async def plc1_plc2(self,drone,lat,long,alt,deg):
        """Displaces from point A(curr) to point B(given).CAUTION CANNOT BE INTRUPTED"""
        async for state in drone.core.connection_state():
            if state.is_connected:
                break
            
        self.curr = await drone.action.goto_location(lat,long,alt,deg)
        
    async def plan_mission(self,drone,lat,long,alt,speed):
        """Displaces from point A(curr) to point B(given). All params in SI units"""
        mission_items = []
        mission_items.append(MissionItem(lat,
                                         long,
                                         alt,
                                         speed,
                                         True,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan')))
        mission_plan = MissionPlan(mission_items)
        await drone.mission.upload_mission(mission_plan)
        await drone.action.arm()
        #await drone.action.takeoff()
        
        self.curr=await drone.mission.start_mission()
            
    async def terminate_curr(self,drone):
        
        """Terminates an on going mission"""
        async for state in drone.core.connection_state():
            if state.is_connected:
                break
        
        self.curr = await drone.mission.pause_mission()
    
    async def rth(self,drone):
        
        """returns to its take off location"""
        
        async for state in drone.core.connection_state():
            if state.is_connected:
                break
        
        await self.terminate_curr(drone)
        self.curr = await drone.action.return_to_launch()
        
    
    async def orbit(self,drone,radius,velocity,lat,long,alt):
        from mavsdk.action import OrbitYawBehavior
        """orbits around
            method
            
            lat long alt correspond to the configuration of the
            
            centre around which the motion is going to occur
            
            HOLD_FRONT_TANGENT_TO_CIRCLE = 3
            HOLD_FRONT_TO_CIRCLE_CENTER = 0
            HOLD_INITIAL_HEADING = 1
            RC_CONTROLLED = 4
            UNCONTROLLED = 2

        """
        position = await drone.telemetry.position().__aiter__().__anext__()
        orbit_height = position.absolute_altitude_m + 10
        await drone.action.do_orbit(radius,velocity,OrbitYawBehavior.HOLD_FRONT_TO_CIRCLE_CENTER,lat,long,orbit_height)
        
    
    async def main(self,call,data):
        """calls int based
            (give data for the required targets)
            data->dict{key:value} keys=[lat,long,alt,speed,deg,method,radius]
            0. intialize
            1. goto*
            2. mission*
            3. terminate mission
            4. rth
            5. orbit*
            6. return telem value
	    7. manual
	    8. switch to offboard 
	    9. land 
	    10.set gimbal mode
            11.gimbal control
            12.release gimbal control
        """
        if call==0:
            await self.initialize()
        elif call==1:
            await self.plc1_plc2(self.drone,
                                 data["lat"],
                                 data["long"],
                                 data["alt"],
                                 data["deg"])
        elif call==2:
            await self.plan_mission(self.drone,
                                    data["lat"],
                                    data["long"],
                                    data["alt"],
                                    data["speed"])
        elif call==3:
            await self.terminate_curr(self.drone)
        elif call==4:
            await self.rth(self.drone)
        elif call==5:
            await self.orbit(self.drone,
                             data["radius"],
                             data["speed"],
                             data["lat"],
                             data["long"],
                             data["alt"],)
        elif call==6:
            #self.start_telem(self.drone)
            T=self.TELEM
            self.data={"lat":T.lat,
                       "long":T.long,
                       "alt":T.alt,
                       "battery":T.battery,
                       "sf_11":T.sf_11,
                       "fix_type":T.fix_type,
                       "sat_count":T.sat_count,}
            print(self.data)
        elif call==7: 
            # kafka function-> i(variable)
            i = int(input("give_int_"))
            await man.manual(i, self.drone)
        elif call==8:
            # change mode to off board for manual control
            await man.change_2_offboard(self.drone)
        elif call==9:
            await  self.drone.action.land()
        elif call==10:
            await gim.set_gimbal_mode(self.drone)
        elif call==11:
            cmd = int(input("give_int_"))
            await gim.gimbal_console(self.drone,cmd)
        elif call==12:
            await gim.release_control(self.drone)
            
    def run(self,a,data):
        #a=int(input("give num"))
        #data=eval(input("give data"))
        self.loop.run_until_complete(self.main(a,data))
            
#a=Console()
#a.run()
