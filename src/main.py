##########################
# Author:	Jannis Brand #
# Date:		02.09.2024   #
##########################

from wallpaper_manager import wallpaper_manager
from interface import GUI

def main() -> int:
	try:
		wp_mngr = wallpaper_manager(resolution_x=1920, resolution_y=1080)
		if isinstance(wp_mngr, wallpaper_manager):
			gui = GUI(wp_mngr, "Wallpaper Manager V0.1 by Jannis Brand")
		if isinstance(gui, GUI):
			gui.window.mainloop()
	except Exception as e:
		print(f"main() {e}")
		return 1
	return 0


if __name__ == "__main__":
	main()