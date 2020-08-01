"""
Defines classes that make a tkinter GUI for Engineering
Main Application provides the root application window

The main lives inside hab_eng.py:
gui = MainApplication()
gui.mainloop()
"""

import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
from orbitx.strings import *

import tkinter as tk
import orbitx.graphics.tkinter_widgets as cw

widgets = {}


class MainApplication(tk.Tk):
    """The main application window in which lives the HabPage, and potentially
    other future pages.
    Creates the file menu
    """

    def __init__(self, style=cw.Style('default')):
        super().__init__()

        tk.Tk.wm_title(self, "OrbitX Engineering")
        # OCESS screens vary between 800x600 and 1024x768
        self.geometry("800x600")
        self.style = style
        self.configure(bg=self.style.bg)

        # Create menubar
        menubar = self._create_menu()
        tk.Tk.config(self, menu=menubar)

        # Create Application Window
        self.create_window()

    def _create_menu(self):
        menubar = tk.Menu(self)

        file = tk.Menu(menubar, tearoff=0)
        # file.add_command(label="Item1")
        file.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=file)

        return menubar

    def update_labels(self, new_value):
        self.label.value = new_value
        self.label.update()

    def create_window(self):
        master_ctrl = MasterControl(self)
        hab_fuel_ctrl = FuelControl(self, craft=HABITAT)
        ayse_fuel_ctrl = FuelControl(self, craft=AYSE)
        subsystem_ctrl = SubsystemControl(self)
        e_grid = EGridControl(self)
        hab_reactor_ctrl = ReactorControl(self, craft=HABITAT)
        ayse_reactor_ctrl = ReactorControl(self, craft=AYSE)
        coolant_lp1_ctrl = CoolantControl(self, loop=LP1)
        coolant_lp2_ctrl = CoolantControl(self, loop=LP2)
        coolant_lp3_ctrl = CoolantControl(self, loop=LP3)
        radiator_ctrl = RadiatorControl(self)

        master_ctrl.grid(row=0, column=0)
        hab_fuel_ctrl.grid(row=1, column=0)
        ayse_fuel_ctrl.grid(row=1, column=0)
        subsystem_ctrl.grid(row=2, column=0)
        e_grid.grid(row=0, column=1, rowspan=2, columnspan=3)
        hab_reactor_ctrl.grid(row=2, column=1)
        ayse_reactor_ctrl.grid(row=2, column=1)
        coolant_lp1_ctrl.grid(row=2, column=2)
        coolant_lp2_ctrl.grid(row=2, column=2)
        coolant_lp3_ctrl.grid(row=2, column=2)
        radiator_ctrl.grid(row=2, column=3)

        # Widgets to take up full space in their cell, with padding
        for k, v in self.children.items():
            if k != '!menu':
                v.grid(sticky=tk.NSEW, padx=2, pady=2)

        # Remove widgets that are conditionally displayed
        ayse_fuel_ctrl.grid_remove()
        ayse_reactor_ctrl.grid_remove()
        coolant_lp2_ctrl.grid_remove()
        coolant_lp3_ctrl.grid_remove()

        # Allow rows and columns to resize
        for i in range(3):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

        fuel_controls = {HABITAT: hab_fuel_ctrl, AYSE: ayse_fuel_ctrl}
        reactor_controls = {HABITAT: hab_reactor_ctrl, AYSE: ayse_reactor_ctrl}
        coolant_controls = {LP1: coolant_lp1_ctrl,
                            LP2: coolant_lp2_ctrl,
                            LP3: coolant_lp3_ctrl}

        master_ctrl.bind_view_selector(fuel_controls)
        master_ctrl.bind_view_selector(reactor_controls)
        # coolant_lp1_ctrl.bind_view_selector(coolant_controls)
        # coolant_lp2_ctrl.bind_view_selector(coolant_controls)
        # coolant_lp3_ctrl.bind_view_selector(coolant_controls)


class MasterControl(cw.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent, text='MASTER')

        widgets['master_freeze'] = cw.Indicator(self, text='Freeze\nConsole')
        widgets['CRAFT_SELECT'] = cw.Spinbox(self, width=7, wrap=True,
                                             values=(HABITAT, AYSE))
        widgets['a_master'] = cw.Alert(self, text='MASTER\nALARM')
        widgets['a_asteroid'] = cw.Alert(self, text='ASTEROID')
        widgets['a_radiation'] = cw.Alert(self, text='RADIATION')

        widgets['master_freeze'].grid(
            row=0, column=0, padx=(10, 5), pady=(5, 0))
        widgets['CRAFT_SELECT'].grid(row=0, column=1, padx=5)
        widgets['a_master'].grid(row=1, column=1, rowspan=2)
        widgets['a_asteroid'].grid(
            row=1, column=0, padx=5, sticky=tk.S, pady=(5, 0))
        widgets['a_radiation'].grid(row=2, column=0, padx=5, sticky=tk.N)

    def bind_view_selector(self, views):
        widgets['CRAFT_SELECT'].bind_view_selector(views)


class FuelControl(cw.LabelFrame):

    def __init__(self, parent, craft: str):
        super().__init__(parent, text='ENGINES - ' + craft)

        test = cw.Indicator(self, text='Hi')
        test.grid()

class SubsystemControl(cw.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent, text='SUBSYSTEMS')

        test = cw.Indicator(self, text='Hi')
        test.grid()


class EGridControl(cw.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent, text='POWER GRID')

        test = cw.Indicator(self, text='Hi')
        test.grid()


class ReactorControl(cw.LabelFrame):

    def __init__(self, parent, craft: str):
        super().__init__(parent, text='REACTOR - ' + craft)

        test = cw.Indicator(self, text='Hi')
        test.grid()


class CoolantControl(cw.LabelFrame):

    def __init__(self, parent, loop: str):
        super().__init__(parent, text='COOLANT - ' + loop)

        test = cw.Indicator(self, text='Hi')
        test.grid()


class RadiatorControl(cw.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent, text='RADIATORS')

        test = cw.Indicator(self, text='Hi')
        test.grid()


# MAIN
app = MainApplication(cw.Style('flat'))    # Essential. Do not remove.
#app.bind_all('<Key>', lambda e: app.keybinds(e))
#widgets['A_ASTEROID'].alert()
# app.after(1000, update_test())
app.mainloop()    # Essential. Do not remove.