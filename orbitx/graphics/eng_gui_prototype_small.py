# This is a small tkinter app that showcases all of the widgets
# from tkinter_widgets.py

import tkinter as tk
import orbitx.graphics.tkinter_widgets as cw
from orbitx import strings


# Main widget dictionary holds all objects in the gui
widgets = {}

# Python garbage collection deletes ImageTk images, unless you save them
images = {}

keybinding = {'i': 'INS',
              'c': 'CHUTE',
              's': 'SRB'}


class MainApplication(tk.Tk):

    def __init__(self, style=cw.Style('default')):
        super().__init__()

        tk.Tk.wm_title(self, "tkinter widget demo")
        self.geometry("800x300")
        self.style = style

        # Initialise main page
        self.subsystems = Subsystems(self)
        self.subsystems.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.e_grid = EGrid(self)
        self.e_grid.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def keybinds(self, event):
        widgets['event_display'].configure(text=event.char)
        try:
            widgets[keybinding[event.char]].invoke()
        except KeyError:
            print('key does not correspond to a widget')


class EGrid(cw.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent, text='EGrid')

        # IONS
        ions = cw.EGridBox(self)
        names = [strings.ION1, strings.ION2, strings.ION3, strings.ION4]
        for i in range(len(names)):
            widgets[names[i]] = cw.EGridComponent(ions, names[i], block=True)
            widgets[names[i]].grid(row=i, column=0, sticky=tk.W)

        # Hab Power Bus
        hab_power_bus = cw.EGridBox(self)
        title = cw.Title(hab_power_bus, text='Habitat Main Bus')
        power = cw.UnitLabel(hab_power_bus, strings.BUS1, 'P')
        current = cw.UnitLabel(hab_power_bus, strings.BUS1, 'A')
        voltage = cw.UnitLabel(hab_power_bus, strings.BUS1, 'V')

        # Render labels relative to container; container rendered with switches
        title.grid(row=0, column=0, sticky=tk.W)
        power.grid(row=1, column=0, sticky=tk.W)
        current.grid(row=2, column=0, sticky=tk.W)
        voltage.grid(row=3, column=0, sticky=tk.W)

        # BOTTOM Object - (a duplicate of Habitat Main Bus for show)
        bus2 = cw.EGridBox(self)
        title = cw.Title(bus2, text=strings.BUS2)
        power = cw.UnitLabel(bus2, strings.BUS2, 'P')
        current = cw.UnitLabel(bus2, strings.BUS2, 'A')
        voltage = cw.UnitLabel(bus2, strings.BUS2, 'V')

        # Render labels relative to container; container rendered with switches
        title.grid(row=0, column=0, sticky=tk.W)
        power.grid(row=1, column=0, sticky=tk.W)
        current.grid(row=2, column=0, sticky=tk.W)
        voltage.grid(row=3, column=0, sticky=tk.W)

        # Create Switches
        widgets['sw_engines'] = cw.Switch(self, length='3h', connection=ions)
        widgets['sw_mid_bot'] = cw.Switch(self, length='1v')

        # Render EGrid
        ions.grid(row=1, column=0, padx=5, pady=5)
        widgets['sw_engines'].grid(row=1, column=1)
        hab_power_bus.grid(row=1, column=2, padx=5, pady=2)
        widgets['sw_mid_bot'].grid(row=2, column=2)
        bus2.grid(row=3, column=2, padx=5, pady=2)


class Subsystems(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.style = parent.style
        self.configure(bg=self.style.bg)

        frame = cw.LabelFrame(self, text="Subsystems")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # A couple of alarms
        widgets['A_ASTEROID'] = cw.Alert(frame, text='A_ASTEROID')
        widgets['A_RADIATION'] = cw.Alert(frame, text='A_RADIATION')

        # A couple of IndicatorButtons
        widgets[strings.INS] = cw.Indicator(frame, text=strings.INS)
        widgets[strings.LOS] = cw.Indicator(frame, text=strings.LOS)

        # A couple of OneTimeButtons
        widgets[strings.SRB] = cw.OneTimeButton(frame, text=strings.SRB)
        widgets['arm_SRB'] = cw.Enabler(frame, enables=widgets['SRB'])
        widgets['CHUTE'] = cw.OneTimeButton(frame, text='CHUTE')

        # Views
        views = {}

        # View1
        VIEW1 = 'View1'
        views[VIEW1] = cw.LabelFrame(frame, VIEW1)
        hab_reactor_temp = cw.UnitLabel(views[VIEW1], strings.HAB_REACT, 'T')
        cl1_pump_power = cw.Label(views[VIEW1], strings.LP1, 'P')
        values = cw.Spinbox(views[VIEW1], width=2, from_=0, to=100, increment=5)

        hab_reactor_temp.grid(row=0, column=0)
        cl1_pump_power.grid(row=1, column=0)
        values.grid(row=2, column=0)

        # View2
        VIEW2 = 'View2'
        views[VIEW2] = cw.LabelFrame(frame, VIEW2)
        hello_world = cw.Title(views[VIEW2], text='Hello World')
        hello_world.grid(row=0, column=0)

        # A spinbox
        select = cw.Spinbox(frame, values=(VIEW1, VIEW2), wrap=True, width=5)
        select.bind_view_selector(views)

        # Display label
        widgets['event_display'] = tk.Label(
            frame, text='Waiting for keyboard',
            bg=self.style.bg, fg=self.style.text, font=self.style.large)

        # Place widgets in the grid
        widgets['A_ASTEROID'].grid(row=0, column=0, padx=5, pady=5)
        widgets['A_RADIATION'].grid(row=1, column=0, padx=5, pady=5)
        widgets[strings.INS].grid(row=0, column=1, padx=5, pady=5)
        widgets[strings.LOS].grid(row=1, column=1, padx=5, pady=5)
        widgets[strings.SRB].grid(row=0, column=2, padx=5, pady=5)
        widgets['CHUTE'].grid(row=1, column=2, padx=5, pady=5)
        widgets['arm_SRB'].grid(row=0, column=3, padx=5, pady=5)
        select.grid(row=1, column=3)
        # Note that VIEW1, VIEW2 are gridded on top of each other
        views[VIEW1].grid(row=0, column=4, rowspan=3, padx=5, pady=5)
        views[VIEW2].grid(row=0, column=4, rowspan=3, padx=5, pady=5)
        views[VIEW2].grid_remove()
        widgets['event_display'].grid(
            row=4, column=0, padx=5, pady=20, columnspan=4)


# MAIN
app = MainApplication(cw.Style('flat'))    # Essential. Do not remove.
app.bind_all('<Key>', lambda e: app.keybinds(e))
widgets['A_ASTEROID'].alert()
# app.after(1000, update_test())
app.mainloop()    # Essential. Do not remove.
