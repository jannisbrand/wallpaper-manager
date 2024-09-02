##########################
# Author:	Jannis Brand #
# Date:		02.09.2024   #
##########################

import os
import ctypes

class wallpaper_manager:
	def __init__(self, resolution_x, resolution_y) -> None:
		self.desktop_resolution_x: int			= resolution_x
		self.desktop_resolution_y: int			= resolution_y

		self.wallpaper_change_interval: float 	= 0.0	# Interval in wich the next wallpaper gets shown
		self.working_directory: str				= ""	# Base directory where the different wallpaper folder are found
		self.wallpaper_directory: str			= ""
		self.wallpaper_frame_collection: list	= []	# Folder containing parts of frames of an animation. (Some sites only generate so many..)
		self.wallpaper_collection: list			= []	# All wallpapers in the wallpaper directory

		self.SPI_SETDESKWALLPAPER: int			= 0x14	# Flag to set Wallpaper in ctypes function
		self.SPIF_UPDATEINFILE: int				= 0x2	# Forces an instant update


	def set_working_directory(self, working_dir: str) -> bool:
		'''
		TODO: Write doc string
		'''
		if os.path.isdir(working_dir):
			self.working_directory = working_dir + "/"
			return True
		return False


	def set_wallpaper_directory(self, wallpaper_dir: str) -> bool:
		'''
		TODO: Write doc string
		'''
		if os.path.isdir(self.working_directory + wallpaper_dir + "/"):
			self.wallpaper_directory = wallpaper_dir + "/"
			if self._search_wallpaper_dir():
				return True
		return False


	def get_wallpapers(self) -> list:
		return self.wallpaper_collection


	def _search_wallpaper_dir(self) -> bool:
		'''
		Gets called after the wallpaper wallpaper directory gets set or changed.
		Lists and sorts files and folders accordingly

		TODO: Check if a file is an image and a supported file type!
		'''
		try:
			location = self.working_directory + self.wallpaper_directory
			for item in os.listdir(location):
				if os.path.isdir(location + item):
					self.wallpaper_frame_collection.append(item)
				elif os.path.isfile(location + item):
					self.wallpaper_collection.append(item)
			return 0
		except os.error as e:
			print(f"_search_for_wallpaper_collections: {e}")
			return 1


	def push_wallpaper_to_the_desktop(self, image: str = "") -> bool:
		'''
		TODO: Write doc string
		'''
		try:
			if image == "":
				image = self.wallpaper_collection[0]

			location = self.working_directory + self.wallpaper_directory
			return ctypes.windll.user32.SystemParametersInfoW(self.SPI_SETDESKWALLPAPER, 0, location + image, self.SPIF_UPDATEINFILE)
		except ctypes.WinError as e:
			print(f"push_wallpaper_to_the_desktop: {e}")
			return False