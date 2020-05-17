## Strategy: basic model to keep close to centerline
## Includes waypoint for direction
## Incentive to speed up when on straights, based on waypoints further ahead

import math

DIRECTION_THRESHOLD = 15 # Tolerance for heading difference
TRACK_TURN_THRESHOLD = 3 # Tolerance for determining whether track is turning
MAX_SPEED_1 = 2.7 # Threshold for highest speed reward when on straights
MAX_SPEED_0 = 1.4 # Threshold for second speed reward when on straights
NEUTRAL_STEER = 2 # Tolerance for what is considered no steering NOT USED

def track_direction(next_point, prev_point):
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    return math.degrees(track_direction)

def get_wp(idx,waypoints):
    if idx > len(waypoints) -1:
        return waypoints[idx - len(waypoints)]
    elif idx < 0:
        return waypoints[len(waypoints) + idx]
    else:
        return waypoints[idx]

def get_turnangle(idx,waypoints):
    # idx +- X, where X can be chosen based on how far ahead we want to see
    angle_fwd = track_direction(get_wp(idx,waypoints),get_wp(idx+4,waypoints))
    angle_bk = track_direction(get_wp(idx-1,waypoints),get_wp(idx,waypoints))

    diff = angle_fwd - angle_bk
    if angle_fwd < -90 and angle_bk > 90:
        return 360 + diff
    elif diff > 180:
        return -180 + (diff -180)
    elif diff <-180:
        return 180 - (diff + 180)
    else:
        return diff

def reward_function(params):
    x = params['x']
    y = params['y']
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    steering_angle = params['steering_angle']
    heading = params['heading']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']
    
    # Centerline penalty
    if distance_from_center < 0.1*track_width:
        reward = 1.0
    elif distance_from_center < 0.2*track_width:
        reward = 0.5
    elif distance_from_center < 0.5*track_width:
        reward = 0.1
    else:
        reward = 0.001

    # Encourage speed on the straights
    track_is_turning = False
    if get_turnangle(closest_waypoints[0],waypoints) >= TRACK_TURN_THRESHOLD:
        track_is_turning = True

    if not track_is_turning and speed > MAX_SPEED_1:
        reward += 0.5
    elif not track_is_turning and speed > MAX_SPEED_0:
        reward += 0.25
    else:
        reward += 0.001

    # Penalty based on not tracking the direction of the circuit
    direction_diff = abs(track_direction(next_point,prev_point)-heading)
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.8
    
    return reward