import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer


class splash_screen:
    def __init__(self, splash):
        self.splash = splash
        self.splash.title("")
        self.splash.geometry("750x700")
        self.splash.resizable(width=False, height=False)
        self.splash.iconbitmap("icon.ico")
        self.bg_color = "#214447"

        self.bg_image = PhotoImage(file="splash.png")
        self.background_image = Label(splash, image=self.bg_image, bg=self.bg_color)
        self.background_image.pack()
        self.background_image.place(x=0, y=0)

        self.splash.attributes("-alpha", 1.0)
        self.splash.after(2500, self.fade_splash_screen)

    def fade_splash_screen(self):
        alpha = splash.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.01
            self.splash.attributes("-alpha", alpha)
            self.splash.after(10, self.fade_splash_screen)
        else:
            self.splash.destroy()


splash = tk.Tk()
spl = splash_screen(splash)
splash.mainloop()

mixer.init()
mixer.music.load("music.wav")
mixer.music.play(loops=-1)
mixer.music.set_volume(0.2)


class simulation(tk.Label):
    def __init__(self, master, frames, speed):
        self.frames = frames
        self.speed = speed
        self.index = 0
        self.photo_frames = [ImageTk.PhotoImage(frame) for frame in self.frames]
        first_frame = self.photo_frames[0]
        tk.Label.__init__(self, master, image=first_frame)
        self.image = first_frame
        self.after(speed, self.animate)

    def animate(self):
        self.index = (self.index + 1) % len(self.photo_frames)
        self.configure(image=self.photo_frames[self.index])
        self.after(self.speed, self.animate)


class main:
    def __init__(self):
        self.destination = os.getcwd()
        self.bg_color = "#5c8f90"
        self.root = root
        self.root.title("SnugFrame V1.0")
        self.root.geometry("750x700")
        self.root.configure(bg=self.bg_color)
        self.root.resizable(width=False, height=False)
        self.root.wm_attributes('-topmost', 1)
        self.root.iconbitmap("icon.ico")

        style = ttk.Style()
        style.configure("TButton", background=self.bg_color)

        self.bg_image = PhotoImage(file="bg.png")
        self.background_image = Label(root, image=self.bg_image, bg=self.bg_color)
        self.background_image.pack()
        self.background_image.place(x=0, y=0)

        simulate_button = ttk.Button(root, text="Simulate", style="TButton", command=self.simulate)
        simulate_button.pack()
        simulate_button.place(x=466, y=462, anchor="center")

        build_button = ttk.Button(root, text="Build", style="TButton", command=self.build)
        build_button.pack()
        build_button.place(x=658, y=661, anchor="center")

        up_button = ttk.Button(root, text="Up", style="TButton", command=self.up)
        up_button.pack()
        up_button.place(x=462, y=190, anchor="center")

        down_button = ttk.Button(root, text="Down", style="TButton", command=self.down)
        down_button.pack()
        down_button.place(x=462, y=220, anchor="center")

        delete_button = ttk.Button(root, text="Delete", style="TButton", command=self.delete)
        delete_button.pack()
        delete_button.place(x=462, y=250, anchor="center")

        reset_button = ttk.Button(root, text="Reset", style="TButton", command=self.reset)
        reset_button.pack()
        reset_button.place(x=462, y=280, anchor="center")

        manual_import_button = ttk.Button(root, text="Import", style="TButton", command=self.manual_import)
        manual_import_button.pack()
        manual_import_button.place(x=462, y=310, anchor="center")

        set_destination_button = ttk.Button(root, text="Set destination folder", style="TButton",
                                            command=self.set_destination)
        set_destination_button.pack()
        set_destination_button.place(x=548, y=661, anchor="center")

        self.destination_label = Label(root, text=self.destination, bg=self.bg_color)
        self.destination_label.pack()
        self.destination_label.place(x=68, y=610)

        self.log_value = tk.StringVar()
        self.log_value.set("Status will show here")
        self.log = Label(root, textvariable=self.log_value, bg='white')
        self.log.pack()
        self.log.place(x=165, y=460, anchor='center')

        self.options = ["Loop", "Back & Forth"]
        self.options_combo = ttk.Combobox(root, values=self.options)
        self.options_combo.set(self.options[0])
        self.options_combo.pack()
        self.options_combo.place(x=610, y=275, anchor="center")

        self.speed = Entry(root, width=10)
        self.speed.insert(0, "100")
        self.speed.pack()
        self.speed.place(x=610, y=215, anchor="center")

        self.name = Entry(root, width=10)
        self.name.insert(0, "File")
        self.name.pack()
        self.name.place(x=215, y=643)

        self.drag_and_drop_box()

    def drag_and_drop_box(self):
        self.image_list = []

        self.frame = tk.Frame(self.root, width=350, height=200)
        self.frame.pack_propagate(False)
        self.frame.pack()
        self.frame.place(x=63, y=250, anchor="w")

        self.file_list = tk.Listbox(self.frame, selectmode=tk.SINGLE, highlightthickness=0)
        self.file_list.pack(fill=tk.BOTH, expand=True)

        self.file_list.drop_target_register(DND_FILES)
        self.file_list.dnd_bind('<<Drop>>', self.drop)
        self.file_list.bind('<ButtonRelease-1>', self.on_list_click)

    def drop(self, event):
        files = event.data
        files_clean = files.replace('{', '').replace('}', '')
        paths = "\n".join(files_clean)
        self.image_list.append(files_clean)
        paths_cut = os.path.basename(paths)
        self.file_list.insert(tk.END, paths_cut)
        print(self.image_list)

    def on_list_click(self, event):
        self.selected_index = self.file_list.nearest(event.y)

    def update_log(self):
        try:
            check = self.simulation_window.winfo_exists()
            if not check:
                self.log_value.set("...")
            else:
                self.log_value.set("Simulation running...")
        except AttributeError:
            self.log_value.set("...")

    def up(self):
        try:
            check = self.simulation_window.winfo_exists()
            if check:
                self.update_log()
                return
            else:
                try:
                    if self.selected_index > 0:
                        self.up_module()
                except AttributeError:
                    self.log_value.set("No items selected !")
                    self.log.after(2000, lambda: self.update_log())

        except AttributeError:
            try:
                if self.selected_index > 0:
                    self.up_module()
            except AttributeError:
                self.log_value.set("No items selected !")
                self.log.after(2000, lambda: self.update_log())

    def up_module(self):
        self.log_value.set("Moved up")
        self.log.after(2000, lambda: self.update_log())
        # Update the ListBox
        temp = self.file_list.get(self.selected_index - 1)
        temp2 = self.file_list.get(self.selected_index)
        self.file_list.delete(self.selected_index - 1)
        self.file_list.insert(self.selected_index - 1, temp2)
        self.file_list.delete(self.selected_index)
        self.file_list.insert(self.selected_index, temp)

        # Update the paths list
        temp = self.image_list[self.selected_index - 1]
        self.image_list[self.selected_index - 1] = self.image_list[self.selected_index]
        self.image_list[self.selected_index] = temp

    def down(self):
        try:
            check = self.simulation_window.winfo_exists()
            if check:
                self.update_log()
                return
            else:
                try:
                    if self.selected_index < self.file_list.size() - 1:
                        self.down_module()
                except AttributeError:
                    self.log_value.set("No items selected !")
                    self.log.after(2000, lambda: self.update_log())
        except AttributeError:
            try:
                if self.selected_index < self.file_list.size() - 1:
                    self.down_module()
            except AttributeError:
                self.log_value.set("No items selected !")
                self.log.after(2000, lambda: self.update_log())

    def down_module(self):
        self.log_value.set("Moved down")
        self.log.after(2000, lambda: self.update_log())
        # Update the ListBox
        temp = self.file_list.get(self.selected_index + 1)
        temp2 = self.file_list.get(self.selected_index)
        self.file_list.delete(self.selected_index + 1)
        self.file_list.insert(self.selected_index + 1, temp2)
        self.file_list.delete(self.selected_index)
        self.file_list.insert(self.selected_index, temp)

        # Update the paths list
        temp = self.image_list[self.selected_index + 1]
        self.image_list[self.selected_index + 1] = self.image_list[self.selected_index]
        self.image_list[self.selected_index] = temp

    def delete(self):
        try:
            check = self.simulation_window.winfo_exists()
            if check:
                self.update_log()
                return
            else:
                self.delete_module()
        except AttributeError:
            self.delete_module()

    def delete_module(self):
        try:
            self.log_value.set("Item deleted")
            self.log.after(2000, lambda: self.update_log())
            self.file_list.delete(self.selected_index)
            self.image_list.pop(self.selected_index)
        except AttributeError:
            self.log_value.set("Select an item to delete !")
            self.log.after(2000, lambda: self.update_log())

    def reset(self):
        try:
            check = self.simulation_window.winfo_exists()
            if check:
                self.update_log()
                return
            else:
                self.reset_module()
        except AttributeError:
            self.reset_module()

    def reset_module(self):
        if self.image_list:
            self.log_value.set("Cleared !")
            self.log.after(2000, lambda: self.update_log())
            self.file_list.delete(0, tk.END)
            self.image_list.clear()
        else:
            self.log_value.set("The list is empty")
            self.log.after(2000, lambda: self.update_log())

    def manual_import(self):
        try:
            check = self.simulation_window.winfo_exists()
            if check:
                self.update_log()
                return
            else:
                self.import_module()
        except AttributeError:
            self.import_module()

    def import_module(self):
        selection = filedialog.askopenfilenames()
        for file in selection:
            self.image_list.append(file)
            name = os.path.basename(file)
            self.file_list.insert(tk.END, name)

    def set_destination(self):
        try:
            check = self.simulation_window.winfo_exists()
            if check:
                self.update_log()
                return
            else:
                self.destination = filedialog.askdirectory()
                self.destination_label.config(text=self.destination)
        except AttributeError:
            self.destination = filedialog.askdirectory()
            self.destination_label.config(text=self.destination)

    def simulate(self):
        self.log_value.set("Simulation running...")
        option = self.options_combo.get()
        speed = int(self.speed.get())
        if speed < 10:
            self.log_value.set("Minimum speed is 10 !")
            self.speed.delete(0, tk.END)
            self.speed.insert(0, "10")
            speed = 10
        if speed > 65535:
            self.log_value.set("Maximum speed is 65535 !")
            self.speed.delete(0, tk.END)
            self.speed.insert(0, "65532")
            speed = 65532
        for i in self.image_list:
            if not i.endswith(".png"):
                self.log_value.set("Only PNG's are accepted !")
                return

        frames = [Image.open(i) for i in self.image_list]

        if not frames:
            self.log_value.set("No images to simulate")
            self.log.after(2000, lambda: self.update_log())
            return

        if option == "Back & Forth":
            reversed_frames = frames[-2::-1]
            frames.extend(reversed_frames)

        self.simulation_window = tk.Toplevel(self.root)
        self.simulation_window.wm_attributes('-topmost', 1)
        self.simulation_window.title("SnugFrame Simulation")
        self.simulation_window.minsize(300, 300)
        self.simulation_window.configure(bg=self.bg_color)

        simulated_gif = simulation(self.simulation_window, frames, speed)
        simulated_gif.pack(expand=True, fill="both")

        self.simulation_window.update_idletasks()
        width = self.simulation_window.winfo_width()
        height = self.simulation_window.winfo_height()
        x = (self.simulation_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.simulation_window.winfo_screenheight() // 2) - (height // 2)
        self.simulation_window.geometry(f"{width}x{height}+{x}+{y}")

        self.simulation_window.protocol("WM_DELETE_WINDOW", self.simulation_log_update)

    def simulation_log_update(self):
        self.simulation_window.destroy()
        self.log_value.set("Simulation stopped")
        self.log.after(2000, lambda: self.update_log())

    def build(self):
        try:
            check = self.simulation_window.winfo_exists()
            if check:
                self.update_log()
                return
            else:
                self.build_engine()
        except AttributeError:
            self.build_engine()

    def build_engine(self):
        try:
            option = self.options_combo.get()
            speed = int(self.speed.get())
            final_destination = self.destination + "/" + self.name.get() + ".gif"

            if speed < 10:
                self.log_value.set("Minimum speed is 10")
                self.speed.delete(0, tk.END)
                self.speed.insert(0, "10")
                speed = 10
            if speed > 65535:
                self.log_value.set("Maximum speed is 65535")
                self.speed.delete(0, tk.END)
                self.speed.insert(0, "65532")
                speed = 65532
            frames = []
            for i in self.image_list:
                if not i.endswith(".png"):
                    self.log_value.set("Only PNG's are accepted !")
                    self.log.after(2000, lambda: self.update_log())
                    return
                new_frame = Image.open(i)
                frames.append(new_frame)
            if option == "Back & Forth":
                reversed_frames = frames[-2::-1]
                frames.extend(reversed_frames)
            frames[0].save(final_destination, format='GIF',
                           append_images=frames[1:],
                           save_all=True,
                           duration=speed,
                           optimize=False,
                           disposal=2,
                           loop=0)
            self.log_value.set("GIF made !")
            self.log.after(2000, lambda: self.update_log())
        except IndexError:
            self.log_value.set("No images to build !")
            self.log.after(2000, lambda: self.update_log())


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    main()
    root.mainloop()
