import tkinter


class MainApp(tkinter.Tk):
    """
    Main tkinter app for the software (WIP)
    """
    def __init__(self):
        super().__init__()

        # Settings
        self.attributes('-alpha', 0.0)
        self.title("Geometrize to Logo")
        self.geometry("1280x720")
        self.center_window()
        self.resizable(False, False)
        self.iconphoto(True, tkinter.PhotoImage(file="./Assets/icon.png"))
        self.attributes('-alpha', 1.0)

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
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.deiconify()
