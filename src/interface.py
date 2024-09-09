##########################
# Author:	Jannis Brand #
# Date:		02.09.2024   #
##########################

from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from wallpaper_manager import wallpaper_manager
import os

class GUI():
	BUTTON_WIDTH_NORMAL = 110
	BUTTON_HEIGHT_NORMAL = 30
	FONT = "Comic Sans"
	HEADER_WEIGHT = 18
	CONTROL_WEIGHT = 11
	HINT_WEIGHT = 8
	PREVIEW_COL_DISTANCE = 10
	PREVIEW_ROW_DISTANCE = 10
	PREVIEW_ROW_AMOUNT = 4
	PREVIEW_COL_AMOUNT = 3
	PREVIEW_FIELD_SIZE_X = 75
	PREVIEW_FIELD_SIZE_Y = 45

	def __init__(self, wp_mngr: wallpaper_manager, title: str, size_x: int = None, size_y: int = None) -> None:
		self.wp_mngr = wp_mngr

		self.window = Tk()
		self.window.title(title)
		self.window.config(width=size_x, height=size_y)
		self.window_size = (size_x, size_y)

		self.frame = ttk.Frame(self.window)

		self.labels: list = []
		self.preview_labels: list = []
		self.buttons: list = []

		self.preview_page: int = 1
		self.max_shown_previews: int = 12
		self.preview_start_pos: tuple = (485, ((self.BUTTON_HEIGHT_NORMAL*2) + 20 + 100))	# 2 Buttons + 4 spaces (5px) + 1 listbox
		self.preview_start_index = 0

		self.create_widgets()


	def create_widgets(self) -> bool:
		lbl_control_header = ttk.Label(self.window, text="Controls", font=(self.FONT, self.HEADER_WEIGHT), compound=CENTER)
		lbl_preview_header = ttk.Label(self.window, text="Preview", font=(self.FONT, self.HEADER_WEIGHT), compound=CENTER)
		self.lbl_current_directory = ttk.Label(self.window, text="Select directory...", font=(self.FONT, self.CONTROL_WEIGHT), compound=CENTER)
		btn_select_work_dir = ttk.Button(self.window, text="Select Working Dir.", command=self.open_file_dialog_work_dir)
		btn_select_wallpaper_dir = ttk.Button(self.window, text="Select Wallpaper Dir.", command=self.open_file_dialog_wp_dir)
		#btn_select_wallpaper = ttk.Button(self.window, text="Select Wallpaper", width=20, command=self.open_file_dialog_wp_dir)
		btn_get_wallpapers = ttk.Button(self.window, text="Find Wallpapers", command=self.get_wallpapers)
		btn_increment_preview_page = ttk.Button(self.window, name="inc", text=">")
		btn_increment_preview_page.bind("<Button>", self._change_preview_page)
		btn_decrement_preview_page = ttk.Button(self.window, name="dec", text="<")
		btn_decrement_preview_page.bind("<Button>", self._change_preview_page)
		self.lst_available_wallpaper_dirs = Listbox(self.window, font=self.CONTROL_WEIGHT)
		self.lst_available_wallpaper_dirs.bind("<<ListboxSelect>>", self._wallpaper_dir_selected)
		
		self.labels.append(lbl_control_header)
		self.labels.append(lbl_preview_header)
		self.labels.append(self.lbl_current_directory)

		self.buttons.append(btn_select_wallpaper_dir)
		self.buttons.append(btn_select_work_dir)
		self.buttons.append(btn_increment_preview_page)
		self.buttons.append(btn_decrement_preview_page)

		# lbl_control_header.place(x=0, y=0)	
		# lbl_preview_header.place(x=self.WIDTH*0.15, y=40)
		self.lbl_current_directory.place(x=0, y=0)
		btn_select_work_dir.place(x=485, y=5, width=self.BUTTON_WIDTH_NORMAL, height=self.BUTTON_HEIGHT_NORMAL)
		btn_select_wallpaper_dir.place(x=600, y=5, width=self.BUTTON_WIDTH_NORMAL, height=self.BUTTON_HEIGHT_NORMAL)
		btn_get_wallpapers.place(x=485, y=0 + (self.BUTTON_HEIGHT_NORMAL + 15 + 100), width=self.BUTTON_WIDTH_NORMAL, height=self.BUTTON_HEIGHT_NORMAL)
		self.lst_available_wallpaper_dirs.place(x=485, y=0 + (self.BUTTON_HEIGHT_NORMAL + 10), width=230, height=100)
		
		btn_decrement_preview_page.place(x=485, y=((self.BUTTON_HEIGHT_NORMAL*2) + (4 * 5) + 100 + (self.PREVIEW_ROW_AMOUNT * self.PREVIEW_FIELD_SIZE_Y + 5)), width=80, height=25)
		btn_increment_preview_page.place(x=635, y=((self.BUTTON_HEIGHT_NORMAL*2) + (4 * 5) + 100 + (self.PREVIEW_ROW_AMOUNT * self.PREVIEW_FIELD_SIZE_Y + 5)), width=80, height=25)

	def open_file_dialog_work_dir(self) -> bool:
		try:
			path = filedialog.askdirectory(mustexist=True)
			self.lbl_current_directory.config(text=path)
			self.wp_mngr.set_working_directory(path)
			#self.cbo_available_wallpaper_dirs["values"] = self.wp_mngr.get_items_of_wallpaper()
			self._populate_listbox_items(self.lst_available_wallpaper_dirs, self.wp_mngr.get_items_of_wallpaper())
			return True
		except FileExistsError as e:
			print(f"open_file_dialog_dir: {e}")
			return False


	def open_file_dialog_wp_dir(self) -> bool:
		try:
			path = filedialog.askdirectory(initialdir=self.wp_mngr.get_work_dir(), mustexist=True)
			if self.wp_mngr.get_work_dir() not in path:
				return False
			path = path.removeprefix(self.wp_mngr.get_work_dir())
			self.wp_mngr.set_wallpaper_directory(path)
			return True
		except FileExistsError as e:
			print(f"open_file_dialog_dir: {e}")
			return False


	def select_wallpaper(self, event) -> bool:
		try:
			try:
				wallpaper_index: int = int(event.widget.winfo_name())
			except TypeError as e:
				print(f"Select_wallpaper: {e}")
				return 0
			
			self.wp_mngr.push_wallpaper_to_the_desktop(self.wp_mngr.wallpaper_collection[wallpaper_index])
			return 1
		except Exception as e:
			print(f"Select_wallpaper: {e}")


	def _populate_listbox_items(self, widget: ttk.Widget, items: list):
		try:
			print(widget.size())
			for i in range(items.__len__()):
				widget.insert(i, items[i])
		except IndexError as e:
			print(f"_populate_listbox_items {e}")


	def _wallpaper_dir_selected(self, event) -> bool:
		try:
			wallpaper_dir: str = event.widget.get(event.widget.curselection())
			if os.path.isdir(self.wp_mngr.get_work_dir() + wallpaper_dir + "/"):
				self.wp_mngr.set_wallpaper_directory(wallpaper_dir)
		except:
			pass


	def get_wallpapers(self) -> bool:
		try:
			self._show_preview_images()
		except:
			pass


	def _change_preview_page(self, event):
		try:
			widget_name: str = str(event.widget.winfo_name())
			got_changed: bool = False

			if widget_name == "inc":
				if self.preview_page + 1 < 11:
					self.preview_page += 1
					got_changed = True
			elif widget_name == "dec":
				if self.preview_page - 1 > 0:
					self.preview_page -= 1
					got_changed = True

			if got_changed:
				preview_images_max: int = self.PREVIEW_COL_AMOUNT * self.PREVIEW_ROW_AMOUNT
				self.preview_start_index = preview_images_max * (self.preview_page -1)
				self._show_preview_images()
			print(f"Page: {self.preview_page} Start index: {self.preview_start_index}")
		except:
			pass


	def _clear_preview_raster(self) -> bool:
		try:
			count: int = 0
			for item in range(self.preview_labels.__len__()):
				self.preview_labels[item].destroy()
				del self.preview_labels[item]
				self.window.update()
				count += 1

			print(f"Elements destroyed: {count}")
			return 1
		except:
			return 0


	def _show_preview_images(self) -> bool:
		try:
			self._clear_preview_raster()

			amount: int = self.wp_mngr.get_wallpapers().__len__()
			try:
				path: str = self.wp_mngr.get_work_dir() + self.wp_mngr.get_wallpaper_dir()	# Missing method
			except Exception as e:
				path: str = "C:/Users/wm00964/Documents/Wallpaper/Animated/WormHole/"

			if amount <= 0:
				return 0

			image_counter = 0
			image_index = self.preview_start_index
			start_pos_x = self.preview_start_pos[0]
			start_pos_y = self.preview_start_pos[1]
			for row in range(self.PREVIEW_ROW_AMOUNT):
				for column in range(self.PREVIEW_COL_AMOUNT):
					if image_counter == self.max_shown_previews or image_index >= amount:
						return 1
					
					image = Image.open(path + self.wp_mngr.get_wallpapers()[image_index]).resize((self.PREVIEW_FIELD_SIZE_X, self.PREVIEW_FIELD_SIZE_Y))
					photo = ImageTk.PhotoImage(image)
					lbl_preview = ttk.Label(self.window, name=f"{image_counter}", image=photo, borderwidth=0)
					lbl_preview.image = photo
					lbl_preview.bind("<Button>", self.select_wallpaper)
					self.preview_labels.append(lbl_preview)
					lbl_preview.place(x=start_pos_x + (self.PREVIEW_FIELD_SIZE_X * column), y=start_pos_y + (self.PREVIEW_FIELD_SIZE_Y * row), width=self.PREVIEW_FIELD_SIZE_X, height=self.PREVIEW_FIELD_SIZE_Y)

					image_counter += 1
					image_index += 1
			return 1
		except Exception as e:
			print(e)


if __name__ == "__main__":
	wp = wallpaper_manager(resolution_x=600, resolution_y=400)
	test = GUI(wp, "HIIII")