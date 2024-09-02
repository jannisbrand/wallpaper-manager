import os
import time
import ctypes


run_animation : bool = False
total_amount_of_frames : int = 0

work_dir : str = "C:/Users/wm00964/Documents/Wallpaper/Animated/"
wallpaper_dir : str = "WormHole/"

collections : list = os.listdir(work_dir + wallpaper_dir + "/")
frame_paths : list = []
frames_per_collection : list

for collection in collections:
	for frame in os.listdir(work_dir + wallpaper_dir + collection + "/"):
		frame_path = work_dir + wallpaper_dir + collection + "/" + frame
		frame_paths.append(frame_path)
		print(frame_path)
total_amount_of_frames = frame_paths.__len__()
print(f"Total Frames: {total_amount_of_frames}")

run_animation = True

current_frame : int = 1
current_collection : int = 0

while run_animation:
	print(f"Current Frame: {current_frame}")
	print(f"Current Image: {frame_paths[current_frame-1]}")

	if current_frame + 1 < total_amount_of_frames:
		ctypes.windll.user32.SystemParametersInfoW(20, 0, frame_paths[current_frame-1], 0)
		current_frame += 1
	else:
		current_frame = 0

	time.sleep(0.2)