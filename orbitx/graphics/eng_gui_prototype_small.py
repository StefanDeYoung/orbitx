# This is a small tkinter app that showcases all of the widgets
# from tkinter_widgets.py

import tkinter as tk
import orbitx.graphics.tkinter_widgets as cw
from orbitx.strings import A_ASTEROID, A_RADIATION, INS, LOS, SRB, CHUTE, \
    HAB_REACT, LP1, SMALL_COMPONENTS_NAMES, ION1, ACC1


class ENGComponent:

    def __init__(self, name):
        self.name = name

        self.values = {'V': 'V',
                       'R': 'R',
                       'I': 'I',
                       'P': 'P',
                       'T': 'T',
                       'CL': 'CL'
                       }

        # Characteristics
        # V/I curve
        # R/T curve

        # Representations
        # Voltage, Resistance, Current, Power, Temperature
        self.widgets = {'V': [], 'R': [], 'I': [], 'P': [], 'T': [], 'CL': []}

    def update_widgets(self):
        for k, v in self.widgets.items():
            for w in v:
                w.update_value(self.values[k])


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
        engines = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)
        widgets[ION1] = cw.TextButton(engines, text=ION1, style=style)
        ion_temp = cw.ENGLabel(engines, text='T', value=60,
                               style=style, small=True)
        ion_loop = cw.ENGLabel(engines, text='L', value=1,
                               style=style, small=True)
        widgets[ACC1] = cw.TextButton(engines, text=ACC1, style=style)
        acc_temp = cw.ENGLabel(engines, text='T', value=60,
                               style=style, small=True)
        acc_loop = cw.ENGLabel(engines, text='L', value=1,
                               style=style, small=True)

        # Render labels relative to container; container rendered with switches
        widgets[ION1].grid(row=0, column=0, sticky=tk.W)
        ion_temp.grid(row=0, column=1)
        ion_loop.grid(row=0, column=2)

        widgets[ACC1].grid(row=1, column=0, sticky=tk.W)
        acc_temp.grid(row=1, column=1)
        acc_loop.grid(row=1, column=2)

        # Store pointer to representation
        components[ION1].widgets['T'].append(ion_temp)
        components[ION1].widgets['CL'].append(ion_loop)
        components[ACC1].widgets['T'].append(acc_temp)
        components[ACC1].widgets['CL'].append(acc_loop)

        # MIDDLE Hab Power Bus
        hab_power_bus = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)
        label = tk.Label(hab_power_bus, text='Middle OBJECT',
                         bg=style.bg, fg=style.text, font=style.normal)
        power = cw.ENGLabel(hab_power_bus, text='', value=60, unit='kW', style=style)
        power.configure(fg=style.ind_on, font=style.small)
        current = cw.ENGLabel(hab_power_bus, text='', value=6.0, unit='A',
                              style=style)
        current.configure(fg=style.ind_on, font=style.small)
        voltage = cw.ENGLabel(hab_power_bus, text='', value=10.0, unit='kV',
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
        label = tk.Label(bot_object, text='Bottom OBJECT',
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
        widgets['sw_engines'] = cw.Switch(self, length='3h', style=style)
        widgets['sw_mid_bot'] = cw.Switch(self, length='1v', style=style)

        # Render EGrid
        engines.grid(row=1, column=0, padx=5, pady=5)
        widgets['sw_engines'].grid(row=1, column=1)
        hab_power_bus.grid(row=1, column=2, padx=5, pady=5)
        widgets['sw_mid_bot'].grid(row=2, column=2)
        bot_object.grid(row=3, column=2, padx=5, pady=5)

        # Switch interconnections
        # TODO fix this and put it in the Switch class
        def connect_switches(event):
            if not(widgets[ION1].value and widgets[ACC1].value):
                widgets['sw_engines'].on_state()
            else:
                widgets['sw_engines'].off_state()
        widgets[ION1].bind('<Button-1>', lambda e: connect_switches(e))
        widgets[ACC1].bind('<Button-1>', lambda e: connect_switches(e))


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
        cl1_pump_power = cw.ENGLabel(text_frame, text='PUMP',
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
        cl1_pump_power.grid(row=1, column=0, padx=5, pady=5)
        widgets['event_display'].grid(row=3, column=0, padx=5, pady=40,
                                      columnspan=4)

        # Add component representation to components[c].widgets
        components[HAB_REACT].widgets['T'].append(hab_reactor_temp)
        components[LP1].widgets['P'].append(cl1_pump_power)


def update_test():
    components[HAB_REACT].values['P'] = 5000
    components[HAB_REACT].update_widgets()


# MAIN
app = MainApplication()    # Essential. Do not remove.
app.bind_all('<Key>', lambda e: keybinds(e))
widgets[A_ASTEROID].alert()
app.after(1000, update_test())
app.mainloop()    # Essential. Do not remove.
