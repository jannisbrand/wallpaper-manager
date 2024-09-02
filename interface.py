from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from wallpaper_manager import wallpaper_manager

class GUI():
	WIDTH = 600
	HEIGHT = 400
	BUTTON_WIDTH = 20
	FONT = "Comic Sans"
	HEADER_WEIGHT = 18
	CONTROL_WEIGHT = 14

	def __init__(self, wp_mngr: wallpaper_manager, title: str, size_x: int = None, size_y: int = None) -> None:
		self.wp_mngr = wp_mngr

		self.window = Tk()
		self.window.title(title)
		self.window.config(width=self.WIDTH, height=self.HEIGHT)

		self.frame = ttk.Frame(self.window)

		self.labels = []
		self.buttons = []

		self.create_widgets()

		self.window.mainloop()

	def create_widgets(self) -> bool:
		lbl_control_header = ttk.Label(self.window, text="Controls", width=self.WIDTH/2, font=(self.FONT, self.HEADER_WEIGHT), compound=CENTER)
		lbl_preview_header = ttk.Label(self.window, text="Preview", width=self.WIDTH/2, font=(self.FONT, self.HEADER_WEIGHT), compound=CENTER)
		btn_select_work_dir = ttk.Button(self.window, text="Select Working Dir.", width=20, command=self.open_file_dialog_work_dir)
		btn_select_wallpaper_dir = ttk.Button(self.window, text="Select Wallpaper Dir.", width=20, command=self.open_file_dialog_wp_dir)
		
		self.labels.append(lbl_control_header)
		self.labels.append(lbl_preview_header)

		self.buttons.append(btn_select_wallpaper_dir)
		self.buttons.append(btn_select_work_dir)

		lbl_control_header.place(x=self.WIDTH*0.65)
		lbl_preview_header.place(x=self.WIDTH*0.15)
		btn_select_work_dir.place(x=(self.WIDTH) - (btn_select_work_dir["width"] * 6) - 20, y=40)
		btn_select_wallpaper_dir.place(x=(self.WIDTH) - (btn_select_wallpaper_dir["width"] * 6) - 20, y=100)


	def open_file_dialog_work_dir(self) -> bool:
		try:
			path = filedialog.askdirectory(mustexist=True)
			self.wp_mngr.set_working_directory(path)
			return True
		except FileExistsError as e:
			print(f"open_file_dialog_dir: {e}")
			return False


	def open_file_dialog_wp_dir(self) -> bool:
		try:
			path = filedialog.askdirectory(initialdir=self.wp_mngr.get_work_dir(), mustexist=True)	# TODO: Missing method get_work_dir()
			if self.wp_mngr.get_work_dir() not in path:
				return False
			self.wp_mngr.set_working_directory(path)
			return True
		except FileExistsError as e:
			print(f"open_file_dialog_dir: {e}")
			return False
		

if __name__ == "__main__":
	wp = wallpaper_manager(resolution_x=600, resolution_y=400)
	test = GUI(wp, "HIIII")