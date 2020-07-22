# This is a small tkinter app that showcases all of the widgets
# from tkinter_widgets.py

import tkinter as tk
import orbitx.graphics.tkinter_widgets as cw
from orbitx.strings import A_ASTEROID, A_RADIATION, INS, LOS, SRB, CHUTE, \
    HAB_REACT, LP1, SMALL_COMPONENTS_NAMES


class ENGComponent:

    def __init__(self, name):
        self.name = name

        # Electrical
        self.V = 'V'
        self.R = 'R'
        self.I = 'I'

        # Thermal
        self.T = 'T'

        # Characteristics
        # V/I curve
        # R/T curve

        # Representations
        # Voltage, Resistance, Current, Power, Temperature
        self.widgets = {'V': [], 'R': [], 'I': [], 'P': [], 'T': []}


# Main widget dictionary holds all objects in the gui
widgets = {}
components = {}
for c in SMALL_COMPONENTS_NAMES:
    components[c] = ENGComponent(name=c)

# Python garbage collection deletes ImageTk images, unless you save them
images = {}

style = cw.Style('flat')

keybinding = {'i': 'INS',
              'c': 'CHUTE',
              's': 'SRB'}


def keybinds(event):
    widgets['event_display'].configure(text=event.char)
    try:
        widgets[keybinding[event.char]].invoke()
    except KeyError:
        print('key does not correspond to a widget')


class MainApplication(tk.Tk):

    def __init__(self):
        super().__init__()

        tk.Tk.wm_title(self, "tkinter widget demo")
        self.geometry("800x300")

        # Initialise main page
        self.subsystems = Subsystems(self)
        self.subsystems.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.e_grid = EGrid(self)
        self.e_grid.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)


class EGrid(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.bg)

        # LEFT Hab Power Bus
        # Define
        left_object = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)
        label = tk.Label(left_object, text='LEFT OBJECT',
                                 bg=style.bg, fg=style.text, font=style.normal)
        power = cw.ENGLabel(left_object, text='', value=60, unit='kW', style=style)
        power.configure(fg=style.ind_on, font=style.small)
        current = cw.ENGLabel(left_object, text='', value=6.0, unit='A',
                              style=style)
        current.configure(fg=style.ind_on, font=style.small)
        voltage = cw.ENGLabel(left_object, text='', value=10.0, unit='kV',
                              style=style)
        voltage.configure(fg=style.ind_on, font=style.small)

        # Render labels relative to container; container rendered with switches
        label.grid(row=0, column=0, sticky=tk.W)
        power.grid(row=1, column=0, sticky=tk.W)
        current.grid(row=2, column=0, sticky=tk.W)
        voltage.grid(row=3, column=0, sticky=tk.W)

        # Store pointer to representation
        components[HAB_REACT].widgets['P'].append(power)
        components[HAB_REACT].widgets['I'].append(current)
        components[HAB_REACT].widgets['V'].append(voltage)

        # MIDDLE Hab Power Bus
        mid_object = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)
        label = tk.Label(mid_object, text='Middle OBJECT',
                         bg=style.bg, fg=style.text, font=style.normal)
        power = cw.ENGLabel(mid_object, text='', value=60, unit='kW', style=style)
        power.configure(fg=style.ind_on, font=style.small)
        current = cw.ENGLabel(mid_object, text='', value=6.0, unit='A',
                              style=style)
        current.configure(fg=style.ind_on, font=style.small)
        voltage = cw.ENGLabel(mid_object, text='', value=10.0, unit='kV',
                              style=style)
        voltage.configure(fg=style.ind_on, font=style.small)

        # Render labels relative to container; container rendered with switches
        label.grid(row=0, column=0, sticky=tk.W)
        power.grid(row=1, column=0, sticky=tk.W)
        current.grid(row=2, column=0, sticky=tk.W)
        voltage.grid(row=3, column=0, sticky=tk.W)

        # Store pointer to representation
        components[HAB_REACT].widgets['P'].append(power)
        components[HAB_REACT].widgets['I'].append(current)
        components[HAB_REACT].widgets['V'].append(voltage)

        # BOTTOM Hab Power Bus
        bot_object = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)
        label = tk.Label(bot_object, text='LEFT OBJECT',
                         bg=style.bg, fg=style.text, font=style.normal)
        power = cw.ENGLabel(bot_object, text='', value=60, unit='kW', style=style)
        power.configure(fg=style.ind_on, font=style.small)
        current = cw.ENGLabel(bot_object, text='', value=6.0, unit='A',
                              style=style)
        current.configure(fg=style.ind_on, font=style.small)
        voltage = cw.ENGLabel(bot_object, text='', value=10.0, unit='kV',
                              style=style)
        voltage.configure(fg=style.ind_on, font=style.small)

        # Render labels relative to container; container rendered with switches
        label.grid(row=0, column=0, sticky=tk.W)
        power.grid(row=1, column=0, sticky=tk.W)
        current.grid(row=2, column=0, sticky=tk.W)
        voltage.grid(row=3, column=0, sticky=tk.W)

        # Store pointer to representation
        components[HAB_REACT].widgets['P'].append(power)
        components[HAB_REACT].widgets['I'].append(current)
        components[HAB_REACT].widgets['V'].append(voltage)

        # Create Switches
        widgets['sw_left_mid'] = cw.Switch(self, length='3h', style=style)
        widgets['sw_mid_bot'] = cw.Switch(self, length='1v', style=style)

        # Render EGrid
        left_object.grid(row=1, column=0, padx=5, pady=5)
        widgets['sw_left_mid'].grid(row=1, column=1)
        mid_object.grid(row=1, column=2, padx=5, pady=5)
        widgets['sw_mid_bot'].grid(row=2, column=2)
        bot_object.grid(row=3, column=2, padx=5, pady=5)


class Subsystems(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.bg)

        frame = cw.ENGLabelFrame(self, text="Frame", style=style)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # A couple of alarms
        widgets[A_ASTEROID] = cw.Alert(frame, text=A_ASTEROID, style=style)
        widgets[A_RADIATION] = cw.Alert(frame, text=A_RADIATION, style=style)

        # A couple of IndicatorButtons
        widgets[INS] = cw.Indicator(frame, text=INS, style=style)
        widgets[LOS] = cw.Indicator(frame, text=LOS, style=style)

        # A couple of OneTimeButtons
        widgets[SRB] = cw.OneTimeButton(frame, text=SRB, style=style)
        widgets[CHUTE] = cw.OneTimeButton(frame, text=CHUTE, style=style)

        # A couple of labels
        text_frame = tk.Frame(frame, bg=style.bg)
        hab_reactor_temp = cw.ENGLabel(text_frame, text='TEMP',
                                           value=0, unit='℃',    # U+2103
                                           style=style)
        widgets[LP1] = cw.ENGLabel(text_frame, text='PUMP',
                                           value=0, unit='%', style=style)

        # Display label
        widgets['event_display'] = tk.Label(frame, text='Waiting',
                                            bg=style.bg, fg=style.text,
                                            font=style.large)

        # Place widgets in the grid
        widgets[A_ASTEROID].grid(row=0, column=0, padx=5, pady=5)
        widgets[A_RADIATION].grid(row=1, column=0, padx=5, pady=5)
        widgets[INS].grid(row=0, column=1, padx=5, pady=5)
        widgets[LOS].grid(row=1, column=1, padx=5, pady=5)
        widgets[SRB].grid(row=0, column=2, padx=5, pady=5)
        widgets[CHUTE].grid(row=1, column=2, padx=5, pady=5)
        text_frame.grid(row=0, column=3, padx=5, pady=5)
        hab_reactor_temp.grid(row=0, column=0, padx=5, pady=5)
        widgets[LP1].grid(row=1, column=0, padx=5, pady=5)
        widgets['event_display'].grid(row=3, column=0, padx=5, pady=40,
                                      columnspan=4)

        # Add component representation to components[c].widgets
        components[HAB_REACT].widgets['T'].append(hab_reactor_temp)


# MAIN
app = MainApplication()    # Essential. Do not remove.
app.bind_all('<Key>', lambda e: keybinds(e))
widgets[A_ASTEROID].alert()
app.mainloop()    # Essential. Do not remove.
