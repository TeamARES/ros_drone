import asyncio
import mavsdk

class telem():
    def __init__(self,drone):
        """information extractor"""
        self.t = drone.telemetry
        self.lat = None
        self.long = None
        self.alt = None
        self.battery = None
        self.uuid = None
        self.sf_11 = None
        self.speed = None
        self.fix_type = None
        self.sat_count = None
        self.health = None

    async def _lat(self):
        async for i in self.t.position():
            self.lat = i.latitude_deg
            self.long = i.longitude_deg
            self.alt =i.absolute_altitude_m

    async def _long(self):
        async for i in self.t.position():
             self.long = i.longitude_deg

    async def _alt(self):
        async for i in self.t.position():
             self.alt = i.absolute_altitude_m

    async def _battery(self):
        async for i in  self.t.battery():
              self.battery = i.voltage_v

    async def _health(self):
        async for i in self.t.health_all_ok():
            self.health = i

    async def _sf_11(self):
        async for i in self.t.distance_sensor():
            self.sf_11 = i.current_distance_m

    async def _speed(self):
        async for i in self.t.raw_gps():
            self.speed = i.velocity_m_s

    async def _fix_type(self):
        async for i in self.t.gps_info():
            self.fix_type = i.fix_type
            self.sat_count = i.num_satellites

    def _run(self):
        asyncio.ensure_future( self._lat() )
        asyncio.ensure_future( self._long() )
        asyncio.ensure_future( self._lat() )
        asyncio.ensure_future( self._battery() )
        asyncio.ensure_future( self._health() )
        asyncio.ensure_future( self._sf_11() )
        asyncio.ensure_future( self._speed() )
        asyncio.ensure_future( self._fix_type() )
