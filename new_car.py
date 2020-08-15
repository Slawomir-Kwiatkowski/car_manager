import tkinter as tk
from sql_helper import Helper


class NewCarWindow():
    def __init__(self, root, parent):
        self.top_level = tk.Toplevel(root)
        self.helper = Helper()
        self.parent = parent
        x = self.top_level.winfo_screenwidth()
        y = self.top_level.winfo_screenheight()
        geometry = '+{}+{}'.format(int((x / 2) - 100),
                                   int((y / 2) - 100))
        size = self.top_level.geometry(geometry)
        self.top_level.title('Add car')
        self.top_level.grab_set()
        label_make = tk.Label(self.top_level, text='Make: ',
                              font=12, padx=20, pady=10).grid(row=0, column=0)
        label_model = tk.Label(self.top_level, text='Model: ',
                               font=12, padx=20, pady=10).grid(row=1, column=0)
        label_year = tk.Label(self.top_level, text='Year: ',
                              font=12, padx=20, pady=10).grid(row=2, column=0)
        label_vrn = tk.Label(self.top_level, text='VRN: ',
                             font=12, padx=20, pady=10).grid(row=3, column=0)
        label_vin = tk.Label(self.top_level, text='VIN: ',
                             font=12, padx=20, pady=10).grid(row=4, column=0)
        self.make_sv = tk.StringVar()
        self.model_sv = tk.StringVar()
        self.year_sv = tk.StringVar()
        self.vrn_sv = tk.StringVar()
        self.vin_sv = tk.StringVar()
        self.info_sv = tk.StringVar()

        entry_make = tk.Entry(
            self.top_level, text=self.make_sv)
        entry_make.focus_set()
        entry_make.grid(row=0, column=1)
        entry_model = tk.Entry(
            self.top_level, text=self.model_sv).grid(row=1, column=1)
        entry_year = tk.Entry(
            self.top_level, text=self.year_sv).grid(row=2, column=1)
        entry_vrn = tk.Entry(
            self.top_level, text=self.vrn_sv).grid(row=3, column=1)
        entry_vin = tk.Entry(
            self.top_level, text=self.vin_sv).grid(row=4, column=1)

        info_label = tk.Label(self.top_level, textvariable=self.info_sv,
                              font=12, padx=10, pady=10, fg='red').grid(row=5, column=0, columnspan=2)
        save_button = tk.Button(self.top_level, text='Save',
                                command=self.save_new_car)
        save_button.bind('<Return>', self.save_new_car)
        save_button.grid(row=6, column=1, sticky='W', padx=10)
        cancel_button = tk.Button(self.top_level, text='Cancel',
                                  command=self.top_level.destroy)
        cancel_button.grid(row=6, column=1, sticky='W', padx=70)
        cancel_button.bind('<Return>', self.top_level.destroy)

    def save_new_car(self, event=None):
        if self.make_sv.get() and self.model_sv.get() and self.year_sv.get() and self.vrn_sv.get() and self.vin_sv.get():
            self.helper.add_car(self.make_sv.get(),
                                self.model_sv.get(),
                                self.year_sv.get(),
                                self.vrn_sv.get(),
                                self.vin_sv.get())
            self.top_level.destroy()
            self.parent.show_cars()
        else:
            self.info_sv.set('Please fill in all entry fields')
