import tkinter as tk
from tkinter import ttk
from sql_helper import Helper
from date_picker import DatePicker


class RepairsWindow():
    def __init__(self, root, car):
        self.top_level = tk.Toplevel(root)
        self.root = root
        self.top_level.title('Repairs')
        self.top_level.grab_set()
        self.car = car
        self.helper = Helper()

        x = self.top_level.winfo_screenwidth()
        y = self.top_level.winfo_screenheight()
        geometry = '+{}+{}'.format(int((x / 2) - 150),
                                   int((y / 2) - 150))
        size = self.top_level.geometry(geometry)

        toolbox_frame = tk.Frame(self.top_level)
        toolbox_frame.grid(column=0, row=0, sticky='W')
        self.add_repair_img = tk.PhotoImage(file='Resources/add_repair.gif')
        add_repair_button = tk.Button(
            toolbox_frame, image=self.add_repair_img, command=self.add_repair)
        add_repair_button.grid(column=0, row=0, sticky='W')
        add_repair_button.bind('<Return>', self.add_repair)
        add_repair_button.bind('<KP_Enter>', self.add_repair)
        if car.sold:
            add_repair_button.config(state='disabled')

        col_headers = ('No', 'Date', 'Description')
        self.repairs_tv = ttk.Treeview(self.top_level, columns=col_headers,
                                       show='headings', selectmode='none')
        self.repairs_tv.tag_configure('c1', background='ivory2')
        self.repairs_tv.tag_configure('c2', background='ivory3')
        for i, col in enumerate(col_headers):
            self.repairs_tv.heading(col, text=col)
            self.repairs_tv.column(col, anchor='center')
            if i == 0:
                self.repairs_tv.column(col, width=50, stretch='NO')
        self.repairs_tv.grid(column=0, row=2,  sticky='NSWE')

        scrollbar = tk.Scrollbar(self.top_level, command=self.repairs_tv.yview)
        scrollbar.grid(column=1, row=2, sticky='NS')

        self.show_repairs()

    def add_repair(self, event=None):
        self.add_repair_frame = tk.Frame(self.top_level)
        self.add_repair_frame.grid(
            column=0, row=1, pady=20, sticky='WE')

        date_label = tk.Label(self.add_repair_frame,
                              text='Date:').grid(column=0, row=2)
        self.date_sv = tk.StringVar()
        self.date_entry = tk.Entry(self.add_repair_frame,
                                   text=self.date_sv)
        self.date_entry.focus_set()
        self.date_entry.grid(column=1, row=2, sticky='W')

        self.cal_img = tk.PhotoImage(file='Resources/calendar.gif')
        show_cal_btn = tk.Button(self.add_repair_frame, image=self.cal_img,
                                 command=self.show_cal, relief='flat').grid(column=1, row=2, sticky='W', padx=170)

        description_label = tk.Label(self.add_repair_frame,
                                     text='Description:').grid(column=0, row=3)
        self.description_sv = tk.StringVar()
        self.description_entry = tk.Entry(self.add_repair_frame,
                                          text=self.description_sv)
        self.description_entry.grid(column=1, row=3, ipadx=200)
        save_button = tk.Button(self.add_repair_frame, text='Save',
                                command=self.save_repair)
        save_button.grid(column=1, row=4, pady=10, sticky='E')
        save_button.bind('<Return>', self.save_repair)
        save_button.bind('<KP_Enter>', self.save_repair)
        cancel_button = tk.Button(self.add_repair_frame, text='Cancel',
                                  command=self.cancel_repair)
        cancel_button.grid(column=1, row=4, sticky='E', padx=60)
        cancel_button.bind('<Return>', self.cancel_repair)
        cancel_button.bind('<KP_Enter>', self.cancel_repair)

    def cancel_repair(self, event=None):
        self.add_repair_frame.grid_remove()

    def save_repair(self, event=None):
        if self.date_sv.get() and self.description_sv.get():
            self.helper.add_repair(self.car, self.date_sv.get(),
                                   self.description_sv.get())
            self.show_repairs()

            self.add_repair_frame.grid_remove()

    def show_repairs(self):
        repairs = self.helper.show_repairs(self.car)
        self.repairs_tv.delete(*self.repairs_tv.get_children())
        for i, repair in enumerate(repairs, start=1):
            repair = (i, repair[0], repair[2])
            if i % 2:
                self.repairs_tv.insert('', 'end', values=repair, tag='c1')
            else:
                self.repairs_tv.insert('', 'end', values=repair, tag='c2')

    def show_cal(self, event=None):
        date_picker = DatePicker(self.top_level, self.date_entry, '%d-%m-%Y')
        self.description_entry.focus_set()
