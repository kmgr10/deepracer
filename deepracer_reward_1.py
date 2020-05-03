# Uses distance from center and waypoints

import math

DIRECTION_THRESHOLD = 10

def track_direction(next_point, prev_point):
	track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
	return math.degrees(track_direction)

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

	if distance_from_center < 0.1*track_width:
		reward = 1.0
	elif distance_from_center < 0.2*track_width:
		reward = 0.5
	elif distance_from_center < 0.5*track_width:
		reward = 0.1
	else:
		reward = 0.001

	direction_diff = abs(track_direction(next_point,prev_point)-heading)
	
	if direction_diff > DIRECTION_THRESHOLD:
		reward *= 0.8

	return reward