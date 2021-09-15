"""
    Author: Israel Dryer
    Modified: 2021-04-23
    Adapted for ttkbootstrap from: http://www.leo-backup.com/screenshots.shtml
"""
import tkinter
from datetime import datetime
from random import choices
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText

from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Back Me Up')
        self.style = Style()
        self.style.configure('bg.TFrame', background=self.style.colors.inputbg)
        self.style.configure('bg.TLabel', background=self.style.colors.inputbg)
        self.geometry("940x520")
        self.bmu = BackMeUp(self, padding=2, style='bg.TFrame')
        self.bmu.pack(fill='both', expand='yes')


class BackMeUp(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # images
        self.img_properties_d = tkinter.PhotoImage(name='properties-dark', file='assets/icons8_settings_24px.png')
        self.img_properties_l = tkinter.PhotoImage(name='properties-light', file='assets/icons8_settings_24px_2.png')
        self.img_addtobackup_d = tkinter.PhotoImage(name='add-to-backup-dark', file='assets/icons8_add_folder_24px.png')

        self.img_stopbackup_d = tkinter.PhotoImage(name='stop-backup-dark', file='assets/icons8_cancel_24px.png')
        self.img_stopbackup_l = tkinter.PhotoImage(name='stop-backup-light', file='assets/icons8_cancel_24px_1.png')

        self.img_refresh = tkinter.PhotoImage(name='refresh', file='assets/icons8_refresh_24px_1.png')
        self.img_stop_d = tkinter.PhotoImage(name='stop-dark', file='assets/icons8_stop_24px.png')
        self.img_stop_l = tkinter.PhotoImage(name='stop-light', file='assets/icons8_stop_24px_1.png')
        self.img_opened_folder = tkinter.PhotoImage(name='opened-folder', file='assets/icons8_opened_folder_24px.png')
        self.img_logo = tkinter.PhotoImage(name='logo', file='assets/backup.png')

        # ----- buttonbar
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill='x', pady=1, side='top')

        ## refresh
        bb_refresh_btn = ttk.Button(buttonbar, text='Refresh', image='refresh', compound='left')
        bb_refresh_btn.configure(command=lambda: showinfo(message='Refreshing...'))
        bb_refresh_btn.pack(side='left', ipadx=5, ipady=5, padx=0, pady=1)

        ## stop
        bb_stop_btn = ttk.Button(buttonbar, text='Stop', image='stop-light', compound='left')
        bb_stop_btn.configure(command=lambda: showinfo(message='Stopping backup.'))
        bb_stop_btn.pack(side='left', ipadx=5, ipady=5, padx=0, pady=1)

        ## settings
        bb_settings_btn = ttk.Button(buttonbar, text='Settings', image='properties-light', compound='left')
        bb_settings_btn.configure(command=lambda: showinfo(message='Changing settings'))
        bb_settings_btn.pack(side='left', ipadx=5, ipady=5, padx=0, pady=1)

        # ----- left panel
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side='left', fill='y')

        ## ----- backup summary (collapsible)
        bus_cf = CollapsingFrame(left_panel)
        bus_cf.pack(fill='x', pady=1)

        ## container
        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(bus_frm, title='Backup Summary', style='secondary.TButton')

        ## destination
        ttk.Label(bus_frm, text='Destination:').grid(row=0, column=0, sticky='w', pady=2)
        ttk.Label(bus_frm, textvariable='destination').grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.setvar('destination', 'd:/test/')

        ## last run
        ttk.Label(bus_frm, text='Last Run:').grid(row=1, column=0, sticky='w', pady=2)
        ttk.Label(bus_frm, textvariable='lastrun').grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        self.setvar('lastrun', '14.06.2021 19:34:43')

        ## files Identical
        ttk.Label(bus_frm, text='Files Identical:').grid(row=2, column=0, sticky='w', pady=2)
        ttk.Label(bus_frm, textvariable='filesidentical').grid(row=2, column=1, sticky='ew', padx=5, pady=2)
        self.setvar('filesidentical', '15%')

        ## section separator
        bus_sep = ttk.Separator(bus_frm, style='secondary.Horizontal.TSeparator')
        bus_sep.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')

        # ----- backup status (collapsible)
        status_cf = CollapsingFrame(left_panel)
        status_cf.pack(fill='x', pady=1)

        ## container
        status_frm = ttk.Frame(status_cf, padding=10)
        status_frm.columnconfigure(1, weight=1)
        status_cf.add(status_frm, title='Backup Status', style='secondary.TButton')

        ## progress message
        status_prog_lbl = ttk.Label(status_frm, textvariable='prog-message', font='Helvetica 10 bold')
        status_prog_lbl.grid(row=0, column=0, columnspan=2, sticky='w')
        self.setvar('prog-message', 'Backing up...')

        ## progress bar
        status_prog = ttk.Progressbar(status_frm, variable='prog-value', style='success.Horizontal.TProgressbar')
        status_prog.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 5))
        self.setvar('prog-value', 71)

        # ---- right panel
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side='right', fill='both', expand='yes')

        ## file input
        browse_frm = ttk.Frame(right_panel)
        browse_frm.pack(side='top', fill='x', padx=2, pady=1)
        file_entry = ttk.Entry(browse_frm, textvariable='folder-path')
        file_entry.pack(side='left', fill='x', expand='yes')
        open_btn = ttk.Button(browse_frm, image='opened-folder', style='secondary.Link.TButton',
                              command=self.get_directory)
        open_btn.pack(side='right')

        ## starting sample directory
        file_entry.insert('end', 'D:/text/myfiles/top-secret/samples/')

    def get_directory(self):
        """Open dialogue to get directory and update directory variable"""
        self.update_idletasks()
        d = askdirectory()
        if d:
            self.setvar('folder-path', d)


class CollapsingFrame(ttk.Frame):
    """
    A collapsible frame widget that opens and closes with a button click.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self.images = [tkinter.PhotoImage(name='open', file='assets/icons8_double_up_24px.png'),
                       tkinter.PhotoImage(name='closed', file='assets/icons8_double_right_24px.png')]

    def add(self, child, title="", style='primary.TButton', **kwargs):
        """Add a child to the collapsible frame

        :param ttk.Frame child: the child frame to add to the widget
        :param str title: the title appearing on the collapsible section header
        :param str style: the ttk style to apply to the collapsible section header
        """
        if child.winfo_class() != 'TFrame':  # must be a frame
            return
        style_color = style.split('.')[0]
        frm = ttk.Frame(self, style=f'{style_color}.TFrame')
        frm.grid(row=self.cumulative_rows, column=0, sticky='ew')

        # header title
        lbl = ttk.Label(frm, text=title, style=f'{style_color}.Inverse.TLabel')
        if kwargs.get('textvariable'):
            lbl.configure(textvariable=kwargs.get('textvariable'))
        lbl.pack(side='left', fill='both', padx=10)

        # header toggle button
        btn = ttk.Button(frm, image='open', style=style, command=lambda c=child: self._toggle_open_close(child))
        btn.pack(side='right')

        # assign toggle button to child so that it's accesible when toggling (need to change image)
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky='news')

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """
        Open or close the section and change the toggle button image accordingly

        :param ttk.Frame child: the child element to add or remove from grid manager
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image='closed')
        else:
            child.grid()
            child.btn.configure(image='open')


if __name__ == '__main__':
    Application().mainloop()
