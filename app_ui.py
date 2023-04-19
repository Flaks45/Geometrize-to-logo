import tkinter
import tkinter.filedialog
import tkinter.messagebox
import webbrowser

from render_images import preview_image
from file_management import get_file_path_json, copy_text, dict_to_json_file
from logo_logic import generate_image


def geometrize_link_button():
    tkinter.messagebox.showwarning(message="Only generate rotated rectangles, rectangles, circles and lines with the "
                                           "following settings: shape_opacity=255, initial_background_opacity=255 ("
                                           "Accept to go to link)")
    webbrowser.open("https://www.samcodes.co.uk/project/geometrize-haxe-web/", new=1)


class MainApp(tkinter.Tk):
    """
    Main tkinter app for the software.
    """
    def __init__(self):
        super().__init__()

        # Settings
        self.attributes("-alpha", 0.0)
        self.title("Geometrize to Logo")
        self.geometry("1280x720")
        self.center_window()
        self.resizable(False, False)
        self.iconbitmap("./Assets/icon.ico")
        self.attributes("-alpha", 1.0)
        self.configure(bg="white")

        # Initializing variables
        self.image_data = None
        self.displace = None
        self.scale_factor = None
        self.color_variation = None
        self.slider_precision = False

        self.scale_slider_clicking = False
        self.xdisplace_slider_clicking = False
        self.ydisplace_slider_clicking = False
        self.is_bg_on = False

        # Bind key events to actions
        self.bind("<KeyPress-Shift_L>", self.slider_precision_change)
        self.bind("<KeyRelease-Shift_L>", self.slider_unprecision_change)

        # Geometrize website button
        self.geometrize_website_frame = tkinter.Frame(bg="#FFFFFF")
        self.geometrize_website_frame.pack(side=tkinter.BOTTOM, fill="x", padx=100, pady=40)

        self.geometrize_website_button = tkinter.Button(self.geometrize_website_frame,
                                                        text="Geometrize website (image generator)",
                                                        command=geometrize_link_button)
        self.geometrize_website_button.pack(expand=True, fill="both")

        # Preview container
        self.preview_image_frame = tkinter.Frame(bg="#FFFFFF")
        self.preview_image_frame.pack(side=tkinter.LEFT, padx=100)

        # Image label
        self.preview_image_dir = None
        self.preview_image = None
        self.preview_image_label = tkinter.Label(self.preview_image_frame, width=500, height=500)
        self.update_preview_image()
        self.preview_image_label.pack()

        # Image buttons widget
        self.preview_image_widget = tkinter.Frame(self.preview_image_frame)
        self.preview_image_widget.pack(fill="x", pady=10)

        self.preview_image_widget_left = tkinter.Frame(self.preview_image_widget)
        self.preview_image_widget_left.pack(side=tkinter.LEFT, fill="x", expand=True)

        self.preview_image_widget_right = tkinter.Frame(self.preview_image_widget)
        self.preview_image_widget_right.pack(side=tkinter.RIGHT, fill="x", expand=True)

        # Get JSON file button
        self.get_image_data_button = tkinter.Button(self.preview_image_widget_left, text="Upload image",
                                                    command=self.get_json_data_button)
        self.get_image_data_button.pack(side=tkinter.LEFT, fill="both", expand=True)

        # Copy code button
        self.get_code_button = tkinter.Button(self.preview_image_widget_left, text="Copy code to clipboard",
                                              command=self.get_code_button)
        self.get_code_button.pack(side=tkinter.RIGHT, fill="both", expand=True)

        # Save settings button
        self.save_options_button = tkinter.Button(self.preview_image_widget_right, text="Save current settings",
                                                  command=self.save_options_button)
        self.save_options_button.pack(side=tkinter.LEFT, fill="both", expand=True)

        # Load settings button
        self.load_options_button = tkinter.Button(self.preview_image_widget_right, text="Load settings",
                                                  command=self.load_options_button)
        self.load_options_button.pack(side=tkinter.RIGHT, fill="both", expand=True)

        # Options frame
        self.configuration_frame = tkinter.Frame(bg="#FFFFFF")
        self.configuration_frame.pack(side=tkinter.RIGHT, padx=100)

        # Toggle background button
        self.toggle_background = tkinter.Button(self.configuration_frame, text="Activate background",
                                                command=self.toggle_background_button, height=1)
        self.toggle_background.pack(expand=True, fill="both")

        # Displace sliders
        self.displace_x_slider = tkinter.Scale(self.configuration_frame, from_=0, to=500, orient=tkinter.HORIZONTAL,
                                               tickinterval=50, length=500, resolution=10, label="X displace")
        self.displace_y_slider = tkinter.Scale(self.configuration_frame, from_=0, to=500, orient=tkinter.HORIZONTAL,
                                               tickinterval=50, length=500, resolution=10, label="Y displace")

        self.displace_x_slider.pack()
        self.displace_y_slider.pack()

        self.displace_x_slider.bind("<ButtonPress>", self.xdisplace_slider_precision)
        self.displace_y_slider.bind("<ButtonPress>", self.ydisplace_slider_precision)

        self.displace_x_slider.bind("<ButtonRelease>", self.update_preview_image_func)
        self.displace_y_slider.bind("<ButtonRelease>", self.update_preview_image_func)

        # Color sliders
        self.red_modifier_slider = tkinter.Scale(self.configuration_frame, from_=0, to=255, orient=tkinter.HORIZONTAL,
                                                 tickinterval=51, length=500, label="Red modifier")
        self.green_modifier_slider = tkinter.Scale(self.configuration_frame, from_=0, to=255, orient=tkinter.HORIZONTAL,
                                                   tickinterval=51, length=500, label="Green modifier")
        self.blue_modifier_slider = tkinter.Scale(self.configuration_frame, from_=0, to=255, orient=tkinter.HORIZONTAL,
                                                  tickinterval=51, length=500, label="Blue modifier")

        self.red_modifier_slider.set(255)
        self.green_modifier_slider.set(255)
        self.blue_modifier_slider.set(255)

        self.red_modifier_slider.pack()
        self.green_modifier_slider.pack()
        self.blue_modifier_slider.pack()

        self.red_modifier_slider.bind("<ButtonRelease>", self.update_preview_image_func)
        self.green_modifier_slider.bind("<ButtonRelease>", self.update_preview_image_func)
        self.blue_modifier_slider.bind("<ButtonRelease>", self.update_preview_image_func)

        # Scale slider
        self.scale_factor_slider = tkinter.Scale(self.configuration_frame, from_=0, to=10, orient=tkinter.HORIZONTAL,
                                                 tickinterval=1, length=500, resolution=0.5, digits=4,
                                                 label="Scale factor")
        self.scale_factor_slider.set(1)
        self.scale_factor_slider.pack()
        self.scale_factor_slider.bind("<ButtonPress>", self.scale_slider_precision)
        self.scale_factor_slider.bind("<ButtonRelease>", self.update_preview_image_func)

        # Information label of shift precision
        self.precision_label = tkinter.Label(self.configuration_frame,
                                             text="* Press left shift for more slider accuracy")
        self.precision_label.pack(fill="x")

    def center_window(self):
        """
        Centers a tkinter window.
        :param self: Window
        """
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry("{}x{}+{}+{}".format(width, height, x, y))
        self.deiconify()

    def update_preview_image(self):
        """
        Function to update the preview image.
        :return:
        """
        self.preview_image_dir = preview_image(self.image_data, self.displace, self.scale_factor, self.color_variation,
                                               self.is_bg_on)
        self.preview_image = tkinter.PhotoImage(file=self.preview_image_dir)
        self.preview_image_label.config(image=self.preview_image)
        self.preview_image_label.pack()

    def get_json_data_button(self, *args):
        try:
            file = tkinter.filedialog.askopenfilename()
            self.image_data = get_file_path_json(file)
            self.update_preview_image()
        except UnicodeDecodeError:
            tkinter.messagebox.showerror(message="Couldn't load file")
        except TypeError:
            tkinter.messagebox.showerror(message="Couldn't load file")
        except PermissionError:
            return

    def get_code_button(self, *args):
        generated_code = generate_image(self.image_data, self.displace, self.scale_factor, self.color_variation,
                                        self.is_bg_on)
        copy_text(generated_code)
        tkinter.messagebox.showinfo(message="Logo code has been successfully copied")

    def update_preview_image_func(self, *args):
        self.scale_slider_clicking = False
        self.xdisplace_slider_clicking = False
        self.ydisplace_slider_clicking = False

        self.displace = (self.displace_x_slider.get(), self.displace_y_slider.get())
        self.color_variation = (self.red_modifier_slider.get(), self.green_modifier_slider.get(),
                                self.blue_modifier_slider.get())
        self.scale_factor = self.scale_factor_slider.get()
        self.update_preview_image()

    def save_options_button(self):
        saved_data = {"image_data": self.image_data, "displace": self.displace,
                      "color_variation": self.color_variation, "scale_factor": self.scale_factor,
                      "bg_active": self.is_bg_on}
        try:
            file_path = tkinter.filedialog.asksaveasfilename(initialfile="config", defaultextension=".json")
            dict_to_json_file(saved_data, file_path)
            tkinter.messagebox.showinfo(message=f"Settings have been saved at {file_path}")

        except PermissionError:
            return

        except FileNotFoundError:
            return

    def load_options_button(self):
        try:
            file = tkinter.filedialog.askopenfilename()
            loaded_settings = get_file_path_json(file)
            copy_image = tkinter.messagebox.askyesno(message="Do you want to import the associated image?")
            if copy_image:
                self.image_data = loaded_settings["image_data"]
            self.displace = loaded_settings["displace"]
            self.color_variation = loaded_settings["color_variation"]
            self.scale_factor = loaded_settings["scale_factor"]
            self.is_bg_on = not loaded_settings["bg_active"]  # Reversed to toggle flip down in function

            # Set widgets to settings
            self.displace_x_slider.set(self.displace[0])
            self.displace_y_slider.set(self.displace[1])
            self.red_modifier_slider.set(self.color_variation[0])
            self.green_modifier_slider.set(self.color_variation[1])
            self.blue_modifier_slider.set(self.color_variation[2])
            self.scale_factor_slider.set(self.scale_factor)
            self.toggle_background_button()

            self.update_preview_image()

        except KeyError:
            return

        except FileNotFoundError:
            return

        except UnicodeDecodeError:
            tkinter.messagebox.showerror(message="Couldn't load file")

        except TypeError:
            tkinter.messagebox.showerror(message="Couldn't process file")

    def slider_precision_change(self, *args):
        self.slider_precision = True

        if self.scale_slider_clicking is True:
            self.scale_factor_slider.configure(resolution=0.01)
        if self.xdisplace_slider_clicking is True:
            self.displace_x_slider.configure(resolution=1)
        if self.ydisplace_slider_clicking is True:
            self.displace_y_slider.configure(resolution=1)

    def slider_unprecision_change(self, *args):
        self.slider_precision = False

        if self.scale_slider_clicking is True:
            self.scale_factor_slider.configure(resolution=0.5)
        if self.xdisplace_slider_clicking is True:
            self.displace_x_slider.configure(resolution=10)
        if self.ydisplace_slider_clicking is True:
            self.displace_y_slider.configure(resolution=10)

    def scale_slider_precision(self, *args):
        self.scale_slider_clicking = True
        if self.slider_precision is True:
            self.scale_factor_slider.configure(resolution=0.01)
        else:
            self.scale_factor_slider.configure(resolution=0.5)

    def xdisplace_slider_precision(self, *args):
        self.xdisplace_slider_clicking = True
        if self.slider_precision is True:
            self.displace_x_slider.configure(resolution=1)
        else:
            self.displace_x_slider.configure(resolution=10)

    def ydisplace_slider_precision(self, *args):
        self.ydisplace_slider_clicking = True
        if self.slider_precision is True:
            self.displace_y_slider.configure(resolution=1)
        else:
            self.displace_y_slider.configure(resolution=10)

    def toggle_background_button(self, *args):
        if self.is_bg_on:
            self.toggle_background.configure(text="Activate background")
            self.is_bg_on = False

        else:
            self.toggle_background.configure(text="Deactivate background")
            self.is_bg_on = True

        self.update_preview_image()
