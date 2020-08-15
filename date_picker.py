import tkinter as tk
import calendar
from datetime import datetime
from functools import partial


class DatePicker():
    """Date picker module for tkinter.

	Arguments:
	root - parent window
	date_entry - parent class tk.Entry
	date_strf - date format string
	"""

    def __init__(self, root, date_entry, date_strf):
        self.root = root
        self.date_entry = date_entry
        self.date_strf = date_strf
        self.top_level = tk.Toplevel(self.root)
        self.top_level.grab_set()
        self.top_level.title('Date picker')
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.top_level.geometry(
            '+{}+{}'.format(x + int(width / 2), y + int(height / 2)))
        self.c = calendar
        self.cal = self.c.Calendar(self.c.firstweekday())
        self.dp_frame = None
        self.create_cal_ui()

    def create_cal_ui(self, year=datetime.today().year, month=datetime.today().month):
        """Create date picker UI.

		Arguments:
		year - selected year
		month - selected month

		Returns:
		None
		"""

        mc = self.cal.monthdayscalendar(year, month)
        self.month = month
        self.year = year
        month_txt = self.c.month_name[month]
        self.date_str = f'{month_txt} {year}'

        if self.dp_frame is not None:
            self.dp_frame.destroy()

        self.dp_frame = tk. Frame(self.top_level)
        self.dp_frame.grid(column=0, row=0)

        self.prev_img = tk.PhotoImage(file='Resources/prev.gif')
        self.next_img = tk.PhotoImage(file='Resources/next.gif')
        prev_btn = tk.Button(self.dp_frame, image=self.prev_img, relief='flat')
        prev_btn.bind(
            '<Button-1>', lambda event: self.set_date(event, 'prev_btn'))
        prev_btn.grid(row=0, column=0)
        next_btn = tk.Button(self.dp_frame, image=self.next_img, relief='flat')
        next_btn.bind(
            '<Button-1>', lambda event: self.set_date(event, 'next_btn'))
        next_btn.grid(row=0, column=6)
        self.date_lbl = tk.Label(self.dp_frame, text=self.date_str,
                                 font=12)
        self.date_lbl.grid(row=0, column=1, columnspan=5, sticky='WE')

        week_names = self.c.day_abbr
        for i, name in enumerate(week_names):
            label = tk.Label(self.dp_frame, text=name).grid(column=i, row=1)

        col = 0
        row = 2
        for week in mc:
            for day in week:
                state = 'normal'
                if day == 0:
                    state = 'disabled'
                    day = ''
                day = str(day)
                button = tk.Button(self.dp_frame, text=day,
                                   relief='flat', state=state, command=partial(self.get_date, day))
                button.grid(column=col, row=row)
                col += 1
            row += 1
            col = 0

    def set_date(self, arg, sender):
        if sender == 'prev_btn':
            self.month -= 1
            if self.month < 1:
                self.month = 12
                self.year -= 1
        if sender == 'next_btn':
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        self.create_cal_ui(self.year, self.month)

    def get_date(self, day):
        day = int(day)
        self.date_entry.delete(0, tk.END)
        d = datetime(self.year, self.month, day)
        self.date_entry.insert(0, d.strftime(self.date_strf))
        self.top_level.destroy()
