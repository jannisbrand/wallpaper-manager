##########################
# Author:	Jannis Brand #
# Date:		02.09.2024   #
##########################

from wallpaper_manager import wallpaper_manager

def main() -> int:
	try:
		manager = wallpaper_manager(resolution_x=1920, resolution_y=1080)
		if isinstance(manager, wallpaper_manager):
			# Pass it to the GUI

			manager.set_working_directory("C:/Users/wm00964/Documents/Wallpaper/Animated")
			manager.set_wallpaper_directory("WormHole")
			image = manager.get_wallpapers()
			manager.push_wallpaper_to_the_desktop(image[0])

	except Exception as e:
		print(f"main() {e}")
		return 1
	return 0


if __name__ == "__main__":
	main()