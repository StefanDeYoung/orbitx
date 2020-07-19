# This is a small tkinter app that showcases all of the widgets
# from tkinter_widgets.py

import tkinter as tk
import orbitx.graphics.tkinter_widgets as cw

# Main widget dictionary holds all objects in the gui
widgets = {}

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

        self.e_grid = E_Grid(self)
        self.e_grid.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)


class E_Grid(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.bg)

        # LEFT Hab Power Bus
        widgets['e_hpb'] = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)

        hab_power_bus = tk.Label(widgets['e_hpb'], text='LEFT OBJECT',
                                 bg=style.bg, fg=style.text, font=style.normal)
        widgets['e_hpb_p'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=60, unit='kW',
                                         style=style)
        widgets['e_hpb_p'].configure(fg=style.ind_on, font=style.small)
        widgets['e_hpb_i'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=6.0, unit='A',
                                         style=style)
        widgets['e_hpb_i'].configure(fg=style.ind_on, font=style.small)
        widgets['e_hpb_v'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=10.0, unit='kV',
                                         style=style)
        widgets['e_hpb_v'].configure(fg=style.ind_on, font=style.small)

        widgets['e_hpb'].grid(row=1, column=0, padx=5, pady=5)
        hab_power_bus.grid(row=0, column=0, sticky=tk.W)
        widgets['e_hpb_p'].grid(row=1, column=0, sticky=tk.W)
        widgets['e_hpb_i'].grid(row=2, column=0, sticky=tk.W)
        widgets['e_hpb_v'].grid(row=3, column=0, sticky=tk.W)

        # MIDDLE Hab Power Bus
        widgets['e_hpb'] = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)

        hab_power_bus = tk.Label(widgets['e_hpb'], text='MIDDLE OBJECT',
                                 bg=style.bg, fg=style.text, font=style.normal)
        widgets['e_hpb_p'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=60, unit='kW',
                                         style=style)
        widgets['e_hpb_p'].configure(fg=style.ind_on, font=style.small)
        widgets['e_hpb_i'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=6.0, unit='A',
                                         style=style)
        widgets['e_hpb_i'].configure(fg=style.ind_on, font=style.small)
        widgets['e_hpb_v'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=10.0, unit='kV',
                                         style=style)
        widgets['e_hpb_v'].configure(fg=style.ind_on, font=style.small)

        widgets['e_hpb'].grid(row=1, column=2, pady=5)
        hab_power_bus.grid(row=0, column=0, sticky=tk.W)
        widgets['e_hpb_p'].grid(row=1, column=0, sticky=tk.W)
        widgets['e_hpb_i'].grid(row=2, column=0, sticky=tk.W)
        widgets['e_hpb_v'].grid(row=3, column=0, sticky=tk.W)

        # BOTTOM Hab Power Bus
        widgets['e_hpb'] = tk.Frame(self, bg=style.bg, bd=2, relief=tk.RIDGE)

        hab_power_bus = tk.Label(widgets['e_hpb'], text='BOTTOM OBJECT',
                                 bg=style.bg, fg=style.text, font=style.normal)
        widgets['e_hpb_p'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=60, unit='kW',
                                         style=style)
        widgets['e_hpb_p'].configure(fg=style.ind_on, font=style.small)
        widgets['e_hpb_i'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=6.0, unit='A',
                                         style=style)
        widgets['e_hpb_i'].configure(fg=style.ind_on, font=style.small)
        widgets['e_hpb_v'] = cw.ENGLabel(widgets['e_hpb'],
                                         text='', value=10.0, unit='kV',
                                         style=style)
        widgets['e_hpb_v'].configure(fg=style.ind_on, font=style.small)

        widgets['e_hpb'].grid(row=3, column=2, padx=5, pady=5)
        hab_power_bus.grid(row=0, column=0, sticky=tk.W)
        widgets['e_hpb_p'].grid(row=1, column=0, sticky=tk.W)
        widgets['e_hpb_i'].grid(row=2, column=0, sticky=tk.W)
        widgets['e_hpb_v'].grid(row=3, column=0, sticky=tk.W)

        # Switches
        # LEFT<->MIDDLE Connector
        widgets['sw_left_mid'] = cw.Switch(self, length='3h', style=style)
        widgets['sw_left_mid'].grid(row=1, column=1)

        widgets['sw_mid_bot'] = cw.Switch(self, length='1v', style=style)
        widgets['sw_mid_bot'].grid(row=2, column=2)


class Subsystems(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.bg)

        frame = cw.ENGLabelFrame(self, text="Frame", style=style)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # A couple of alarms
        widgets['a_asteroid'] = cw.Alert(frame, text='ASTEROID', style=style)
        widgets['a_radiation'] = cw.Alert(frame, text='RADIATION', style=style)

        # A couple of IndicatorButtons
        widgets['INS'] = cw.Indicator(frame, text='INS', style=style)
        widgets['LOS'] = cw.Indicator(frame, text='LOS', style=style)

        # A couple of OneTimeButtons
        widgets['SRB'] = cw.OneTimeButton(frame, text='SRB', style=style)
        widgets['CHUTE'] = cw.OneTimeButton(frame, text='CHUTE', style=style)

        # A couple of labels
        text_frame = tk.Frame(frame, bg=style.bg)
        widgets['habr_temp'] = cw.ENGLabel(text_frame, text='TEMP',
                                           value=0, unit='℃',    # U+2103
                                           style=style)
        widgets['cl1_pump'] = cw.ENGLabel(text_frame, text='PUMP',
                                           value=0, unit='%', style=style)

        # Display label
        widgets['event_display'] = tk.Label(frame, text='Waiting',
                                            bg=style.bg, fg=style.text,
                                            font=style.large)

        # Place widgets in the grid
        widgets['a_asteroid'].grid(row=0, column=0, padx=5, pady=5)
        widgets['a_radiation'].grid(row=1, column=0, padx=5, pady=5)
        widgets['INS'].grid(row=0, column=1, padx=5, pady=5)
        widgets['LOS'].grid(row=1, column=1, padx=5, pady=5)
        widgets['SRB'].grid(row=0, column=2, padx=5, pady=5)
        widgets['CHUTE'].grid(row=1, column=2, padx=5, pady=5)
        text_frame.grid(row=0, column=3, padx=5, pady=5)
        widgets['habr_temp'].grid(row=0, column=0, padx=5, pady=5)
        widgets['cl1_pump'].grid(row=1, column=0, padx=5, pady=5)
        widgets['event_display'].grid(row=3, column=0, padx=5, pady=40,
                                      columnspan=4)


# MAIN
app = MainApplication()    # Essential. Do not remove.
app.bind_all('<Key>', lambda e: keybinds(e))
widgets['a_asteroid'].alert()
app.mainloop()    # Essential. Do not remove.
