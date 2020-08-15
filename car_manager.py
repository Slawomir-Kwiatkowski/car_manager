import tkinter as tk
from tkinter import messagebox, ttk
from sql_helper import Helper
from car import Car
from new_car import NewCarWindow
from repairs import RepairsWindow
from date_picker import DatePicker


class CarManager(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.helper = Helper()
        self.root = root
        root.attributes('-zoomed', True)
        root.title('Car manager')
        root.iconphoto(True, tk.PhotoImage(file='Resources/car_logo.png'))
        root.bind('<Control-x>', self.close_app)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        self.create_widgets()
        self.show_cars()

    def create_widgets(self):
        # create menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=exit, accelerator="Ctrl+x")
        menubar.add_cascade(label="File", menu=file_menu)

        # create toolbar
        tbar_frame = tk.Frame(root, height=10)
        tbar_frame.grid(row=0, column=0)

        self.add_car_img = tk.PhotoImage(file='Resources/add_car.gif')
        self.remove_car_img = tk.PhotoImage(file='Resources/remove_car.gif')
        self.repairs_img = tk.PhotoImage(file='Resources/repairs.gif')
        self.sold_img = tk.PhotoImage(file='Resources/sold.gif')

        add_car_button = tk.Button(tbar_frame, image=self.add_car_img,
                                   command=self.add_car).grid(row=0, column=0, sticky='W')
        del_car_button = tk.Button(tbar_frame, image=self.remove_car_img,
                                   command=self.del_car).grid(row=0, column=0, sticky='W', padx=30)
        repairs_button = tk.Button(tbar_frame, image=self.repairs_img,
                                   command=self.show_repairs).grid(row=0, column=0, sticky='W', padx=60)
        sold_button = tk.Button(tbar_frame, image=self.sold_img,
                                command=self.sell_car).grid(row=0, column=0, sticky='W', padx=90)

        # create search entry
        self.search_variable = tk.StringVar()
        self.search_entry = tk.Entry(
            root, textvariable=self.search_variable)
        self.search_entry.config(fg='grey')
        # search_variable.trace("w", callback)
        self.search_variable.set("Search car by VRN")
        self.search_entry.bind('<FocusIn>', self.on_entry_in)
        self.search_entry.bind('<FocusOut>', self.on_entry_out)
        self.search_entry.bind('<Return>', self.on_entry_return)
        self.search_entry.bind('<KP_Enter>', self.on_entry_return)
        self.search_entry.grid(row=0, column=1, sticky='E', ipadx=20)

        # create TreeView with Scrollbar
        col_headers = ('No', 'Make', 'Model', 'Year', 'VRN', 'VIN', 'Sold')
        self.car_tview = ttk.Treeview(self.root, columns=col_headers,
                                      show='headings', selectmode='browse')
        self.car_tview.columnconfigure(0, weight=1)
        self.car_tview.rowconfigure(0, weight=1)
        # set column headers
        for i, col in enumerate(col_headers):
            self.car_tview.heading(col, text=col)
            self.car_tview.column(col, anchor='center')
            if i == 0:
                self.car_tview.column(col, width=50, stretch='NO')
        self.car_tview.grid(row=2, column=0, columnspan=2, sticky='NSWE')

        scrollbar = tk.Scrollbar(self.root, command=self.car_tview.yview)
        scrollbar.grid(column=3, row=2, sticky='NS')

    def close_app(self, event):
        result = tk.messagebox.askyesno('Exit', 'Close application?')
        if result:
            self.root.destroy()

    def show_cars(self):
        all_cars = self.helper.show_all_cars()
        self.car_tview.delete(*self.car_tview.get_children())
        for i, car in enumerate(all_cars, start=1):
            car = list(car)
            car.insert(0, i)
            if i % 2:
                self.car_tview.insert('', 'end', values=car, tag='c2')
            else:
                self.car_tview.insert('', 'end', values=car, tag='c1')
            self.car_tview.tag_configure('c1', background='ivory3')
            self.car_tview.tag_configure('c2', background='ivory2')

    def __get_car_from_selection(self):
        selected_item = self.car_tview.focus()
        if selected_item == '':
            messagebox.showinfo('Information', 'No item selected')
        else:
            selection_dict = self.car_tview.item(selected_item)
            selection = selection_dict.get('values')
            i, *args = selection
            car = Car.from_list(args)
            return car

    def add_car(self):
        add_car = NewCarWindow(self.root, self)

    def del_car(self):
        car = self.__get_car_from_selection()
        if car and messagebox.askyesno('Delete', 'Delete selected car?'):
            self.helper.del_car(car)
            self.show_cars()

    def show_repairs(self):
        car = self.__get_car_from_selection()
        if car:
            repairs = RepairsWindow(self.root, car)

    def sell_car(self):
        car = self.__get_car_from_selection()
        if car and car.sold:
            messagebox.showinfo('Information', 'Already marked as sold')
        elif car and messagebox.askyesno('Sell', 'Mark car as sold?'):
            self.helper.set_sold(car)
            self.show_cars()

    def on_entry_return(self, event):
        vrn = self.search_variable.get()
        if vrn == '':
            self.show_cars()
        else:
            car = self.helper.search_by_vrn(vrn)
            self.car_tview.delete(*self.car_tview.get_children())
            if car:
                car = list(car)
                car.insert(0, 1)
                self.car_tview.insert('', 'end', values=car)

    def on_entry_in(self, event):
        self.search_entry.config(fg='black')
        self.search_variable.set('')

    def on_entry_out(self, event):
        self.search_entry.config(fg='grey')
        self.search_variable.set('Search car by VRN')


if __name__ == '__main__':
    root = tk.Tk()
    cm = CarManager(root)
    cm.mainloop()
