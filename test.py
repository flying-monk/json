from dronekit import connect, LocationGlobalRelative, LocationGlobal
import math

# vehicle = connect('127.0.0.1:14550', wait_ready=True)
vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=115200)

mode = vehicle.mode.name
global_location = vehicle.location.global_frame
global_location_relative_altitude = vehicle.location.global_relative_frame
local_location = vehicle.location.local_frame
vehicle_altitude = vehicle.attitude
vehicle_velocity = vehicle.velocity
vehicle_gps_0 = vehicle.gps_0
ground_speed = vehicle.groundspeed
air_speed = vehicle.airspeed
battery = vehicle.battery
heart_beat = vehicle.last_heartbeat
range_finder = vehicle.rangefinder
range_finder_distance = vehicle.rangefinder.distance
range_finder_voltage = vehicle.rangefinder.voltage
heading = vehicle.heading
arm_status = vehicle.is_armable
system_status = vehicle.system_status.state

print ("========================")
print ("Mode: %s" % vehicle.mode.name)
print ("========================")
print ("Global Location:")
print ("Latitude %s" % vehicle.location.global_frame.lat)
print ("Longitude %s" % vehicle.location.global_frame.lon)
print ("Sea Level Altitude %s" % vehicle.location.global_frame.alt)
print ("========================")
print ("Global Location (relative altitude):")
print ("Latitude: %s" % vehicle.location.global_relative_frame.lat)
print ("Longitude: %s" % vehicle.location.global_relative_frame.lon)
print ("Altitude: %s" % vehicle.location.global_relative_frame.alt)
print ("========================")
print ("Local Location:")
print ("North: %s" % vehicle.location.local_frame.north)
print ("East: %s" % vehicle.location.local_frame.east) 
print ("Down: %s" % vehicle.location.local_frame.down)
print ("========================")
print ("Attitude: %s" % vehicle.attitude)
print ("========================")
print ("Velocity: %s" % vehicle.velocity)
print ("========================")
print ("GPS:")
print ("GPS fix: %s" % vehicle.gps_0.fix_type)
print ("GPS Sat: %s" % vehicle.gps_0.satellites_visible)
print ("========================")
print ("Groundspeed: %s" % vehicle.groundspeed)
print ("========================")
print ("Airspeed: %s" % vehicle.airspeed)
print ("========================")
print ("Battery: %s" % vehicle.battery)
print ("========================")
print ("Last Heartbeat: %s" % vehicle.last_heartbeat)
print ("========================")
print ("Rangefinder distance: %s" % vehicle.rangefinder.distance)
print ("========================")
print ("Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
print ("========================")
print ("Heading: %s" % vehicle.heading)
print ("========================")
print ("Is Armable?: %s" % vehicle.is_armable)
print ("========================")
print ("System status: %s" % vehicle.system_status.state)
print ("========================")
print ("========================")
print ("Channel values from RC Tx:", vehicle.channels)
print ("========================")
print ("Read channels individually:")
print ("========================")
print (" Ch1: %s" % vehicle.channels['1'])
print (" Ch2: %s" % vehicle.channels['2'])
print (" Ch3: %s" % vehicle.channels['3'])
print (" Ch4: %s" % vehicle.channels['4'])
print (" Ch5: %s" % vehicle.channels['5'])
print (" Ch6: %s" % vehicle.channels['6'])
print (" Ch7: %s" % vehicle.channels['7'])
print (" Ch8: %s" % vehicle.channels['8'])
print ("========================")


def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def distance_to_current_waypoint():
    nextwaypoint=vehicle.commands.next
    if nextwaypoint ==0:
        return None
    missionitem=vehicle.commands[nextwaypoint-1] 
    lat=missionitem.x
    lon=missionitem.y
    alt=missionitem.z
    targetWaypointLocation=LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint

def get_location_metres(original_location, dNorth, dEast):
    earth_radius=6378137.0
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
    return targetlocation

