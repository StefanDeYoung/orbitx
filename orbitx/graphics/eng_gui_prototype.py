import tkinter as tk
import orbitx.graphics.tkinter_widgets as cw
from orbitx.graphics.eng_keybinds import keybinding
from orbitx.strings import *
from PIL import Image, ImageTk


def keybinds(event):
    try:
        widgets[keybinding[event.char]].invoke()
    except KeyError:
        print('key does not correspond to a widget')


class ENGComponent:
    """
    self.widgets is a dict that contains pointers to each label that displays
    the values of the ENGComponent.

    Instantiate all of the ENGComponents at the top of the script, then
    after creating widget, add a pointer to it in components[ENGComponent.name]

    eg.
    voltage_label = cw.ENGLabel(parent, text = 'V', value=999, unit='kV')
    components[ENGComponent.name]['V'].append(voltage_label)
    """
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
        # Voltage, Resistance, Current, Power, Temperature, Coolant Loop
        self.widgets = {'V': [], 'R': [], 'I': [], 'P': [], 'T': [], 'CL': []}

    def update_widgets(self):
        for k, v in self.widgets.items():
            for w in v:
                w.update_value(self.values[k])


# Main widget dictionary holds all buttons
widgets = {}

components = {}
for c in COMPONENT_NAMES:
    components[c] = ENGComponent(name=c)

# Python garbage collection deletes ImageTk images, unless you save them
images = {}

style = cw.Style('flat')


class MainApplication(tk.Tk):
    """The main application window in which lives the HabPage, and potentially
    other future pages.
    Creates the file menu
    """

    def __init__(self):
        super().__init__()

        tk.Tk.wm_title(self, "OrbitX Engineering")
        self.geometry("800x600")
        #self.geometry("1920x1080")

        # Create menubar
        menubar = self._create_menu()
        tk.Tk.config(self, menu=menubar)

        # Initialise main page
        self.page = HabPage(self)
        self.page.grid()

    def _create_menu(self):
        menubar = tk.Menu(self)

        file = tk.Menu(menubar, tearoff=0)
        file.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=file)

        return menubar


class HabPage(tk.Frame):
    """1. Create a page in which lives all of the HabPage GUI
    2. Divide the page into a left and right pane. The right
    pane is divided into top, middle, bottom
    3. Create and render everything in each of the panes.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.configure(bg=style.bg)

        # ----------------  Overall Page Organisation ----------------
        master_ctrl = cw.ENGLabelFrame(self, text='MASTER', style=style)
        fuel_ctrl = cw.ENGLabelFrame(self, text='ENGINE', style=style)
        subsystem_ctrl = cw.ENGLabelFrame(self, text='SUBSYSTEM', style=style)
        e_grid = cw.ENGLabelFrame(self, text='EGRID', style=style)
        coolant_ctrl = cw.ENGLabelFrame(self, text='COOLANT', style=style)
        reactor_ctrl = cw.ENGLabelFrame(self, text='REACTOR', style=style)
        radiator_ctrl = cw.ENGLabelFrame(self, text='RADIATOR', style=style)

        master_ctrl.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        fuel_ctrl.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        subsystem_ctrl.grid(row=2, column=0, sticky=tk.NSEW, padx=5)
        e_grid.grid(row=0, column=1, rowspan=2, columnspan=3, sticky=tk.NSEW)
        reactor_ctrl.grid(row=2, column=1,sticky=tk.NSEW, padx=2)
        coolant_ctrl.grid(row=2, column=2, sticky=tk.NSEW, padx=2)
        radiator_ctrl.grid(row=2, column=3, sticky=tk.NSEW, padx=2)

        # ---------------- Master ctrl ----------------
        top_frame = tk.Frame(master_ctrl, bg=style.bg)
        bot_frame = tk.Frame(master_ctrl, bg=style.bg)
        top_frame.grid(row=0, column=0)
        bot_frame.grid(row=2, column=0)

        widgets['master_freeze'] = cw.Indicator(top_frame,
                                                text='Freeze\nConsole',
                                                style=style)
        widgets['master_freeze'].configure(width=55, height=50)
        widgets['CRAFT_SELECT'] = tk.Spinbox(
            top_frame, width=7, bg=style.bg, fg=style.text, font=style.large,
            values=(HABITAT, AYSE), wrap=True)

        widgets['master_freeze'].grid(row=0, column=0, padx=(25, 5),
                                      pady=(5, 0))
        widgets['CRAFT_SELECT'].grid(row=0, column=1, padx=5)

        widgets['a_master'] = cw.Alert(bot_frame, text='MASTER\nALARM',
                                       font=style.large, style=style)
        widgets['a_master'].configure(height=40)
        widgets['a_asteroid'] = cw.Alert(bot_frame, text='ASTEROID',
                                         style=style)
        widgets['a_radiation'] = cw.Alert(bot_frame, text='RADIATION',
                                          style=style)

        widgets['a_asteroid'].grid(row=0, column=0, padx=5, sticky=tk.S,
                                   pady=(5, 0))
        widgets['a_radiation'].grid(row=1, column=0, padx=5, sticky=tk.N)

        widgets['a_master'].grid(row=0, column=1, rowspan=2)

        # ---------------- Fuel ctrl ----------------
        widgets[INJ1] = cw.Indicator(fuel_ctrl, text=INJ1, style=style)
        widgets[INJ2] = cw.Indicator(fuel_ctrl, text=INJ2, style=style)

        fuel = tk.Frame(fuel_ctrl, bg=style.bg)
        fuel_label = tk.Label(fuel, text='FUEL',
                              bg=style.bg, fg=style.text, font=style.normal)
        widgets['HAB_FUEL'] = cw.ENGLabel(fuel, text='HAB', value=999,
                                          unit='kg', style=style)
        widgets['HAB_FUEL'].configure(font=style.small)
        widgets['AYSE_FUEL'] = cw.ENGLabel(fuel, text='AYSE', value=999,
                                          unit='kg', style=style)
        widgets['AYSE_FUEL'].configure(font=style.small)

        burn = tk.Frame(fuel_ctrl, bg=style.bg)
        burn_label = tk.Label(burn, text='BURN\nRATE',
                              bg=style.bg, fg=style.text, font=style.normal)
        widgets['HAB_BURN'] = cw.ENGLabel(burn, text='HAB', value=999,
                                          unit='kg/h', style=style)
        widgets['HAB_BURN'].configure(font=style.small)
        widgets['AYSE_BURN'] = cw.ENGLabel(burn, text='AYSE', value=999,
                                           unit='kg/h', style=style)
        widgets['AYSE_BURN'].configure(font=style.small)

        fuel_management = tk.Frame(fuel_ctrl, bg=style.bg)
        widgets[A_DOCKED] = cw.Alert(fuel_management, text=A_DOCKED,
                                       style=style)
        widgets[LOAD] = cw.Indicator(fuel_management, text=LOAD,
                                     style=style)
        widgets[DUMP] = cw.Indicator(fuel_management, text=DUMP,
                                     style=style)

        # columnwise
        widgets[INJ1].grid(row=0, column=0, padx=(5, 0), pady=(5, 0))
        fuel.grid(row=0, column=1)
        widgets[INJ2].grid(row=1, column=0, padx=(5, 0))
        burn.grid(row=1, column=1)
        fuel_management.grid(row=2, column=0, columnspan=2)

        fuel_label.grid(row=0, column=0, rowspan=2)
        widgets['HAB_FUEL'].grid(row=0, column=1, sticky=tk.W)
        widgets['AYSE_FUEL'].grid(row=1, column=1, sticky=tk.W)

        burn_label.grid(row=0, column=0, rowspan=2)
        widgets['HAB_BURN'].grid(row=0, column=1, sticky=tk.W)
        widgets['AYSE_BURN'].grid(row=1, column=1, sticky=tk.W)

        widgets[A_DOCKED].grid(row=0, column=0)
        widgets[LOAD].grid(row=0, column=1)
        widgets[DUMP].grid(row=0, column=2)

        # ---------------- Subsystems ----------------
        widgets[INS] = cw.Indicator(subsystem_ctrl, text=INS, style=style)
        widgets[RADAR] = cw.Indicator(subsystem_ctrl, text=RADAR, style=style)
        widgets[LOS] = cw.Indicator(subsystem_ctrl, text=LOS, style=style)
        widgets[GNC] = cw.Indicator(subsystem_ctrl, text=GNC, style=style)
        widgets[A_ATMO] = cw.Alert(subsystem_ctrl, text=A_ATMO, style=style)
        widgets[CHUTE] = cw.OneTimeButton(subsystem_ctrl, text=CHUTE,
                                          style=style)
        widgets[SRB] = cw.OneTimeButton(subsystem_ctrl, text=SRB, style=style)
        widgets['arm_SRB'] = cw.Enabler(subsystem_ctrl, enables=widgets['SRB'],
                                        style=style)
        widgets['a_SRBTIME'] = cw.Alert(subsystem_ctrl, text='120s',
                                        invis=False, style=style)
        widgets['a_SRBTIME'].configure(width=30)
        widgets['DOCK'] = cw.OneTimeButton(subsystem_ctrl, text='LATCH',
                                           style=style)
        widgets['arm_DOCK'] = cw.Enabler(subsystem_ctrl,
                                         enables=widgets['DOCK'], style=style)

        widgets[INS].grid(row=0, column=0, padx=(5, 0), pady=(5, 0))
        widgets[RADAR].grid(row=1, column=0, padx=(5, 0))
        widgets[LOS].grid(row=2, column=0, padx=(5, 0))
        widgets[GNC].grid(row=3, column=0, padx=(5, 0))
        widgets[A_ATMO].grid(row=0, column=1)
        widgets[CHUTE].grid(row=1, column=1)
        widgets['SRB'].grid(row=2, column=1)
        widgets['DOCK'].grid(row=3, column=1)
        widgets['a_SRBTIME'].grid(row=0, column=2)
        widgets['arm_SRB'].grid(row=2, column=2, sticky=tk.W)
        widgets['arm_DOCK'].grid(row=3, column=2, sticky=tk.W)

        # ---------------- EGrid ----------------
        # First instantiate widgets, and grid them relative to their containers
        # Then instantiate one-of widgets
        # Then instantiate switches
        # Then grid everything
        # Engines + Power Lines
        engines = {}
        for e in ['ION', 'ACC', 'GPD']:
            engines[e] = tk.Frame(e_grid, bg=style.bg, bd=2, relief=tk.RIDGE)
            for i in range(4):
                name = '{}{}'.format(e, i+1)
                widgets[name] = cw.TextButton(engines[e], text=name,
                                              connected=True, style=style)
                temperature = cw.ENGLabel(engines[e], text='T', value=60,
                                          style=style, small=True)
                coolant_loop = cw.ENGLabel(engines[e], text='L', value=1,
                                           style=style, small=True)

                # Render relative to container; container rendered later
                widgets[name].grid(row=i, column=0, sticky=tk.W)
                temperature.grid(row=i, column=1)
                coolant_loop.grid(row=i, column=2)

                # Store pointer to representation
                components[name].widgets['T'].append(temperature)
                components[name].widgets['CL'].append(coolant_loop)

                # Render relative to container; container rendered later
                widgets[name].grid(row=i, column=0, sticky=tk.W)
                temperature.grid(row=i, column=1)
                coolant_loop.grid(row=i, column=2)

                # Store pointer to representation
                components[name].widgets['T'].append(temperature)
                components[name].widgets['CL'].append(coolant_loop)

        # Power Busses
        busses = {}
        for b in [BUS1, BUS2, BUS3, BUSA]:
            busses[b] = tk.Frame(e_grid, bg=style.bg, bd=2, relief=tk.RIDGE)
            label = tk.Label(busses[b], text=b,
                             bg=style.bg, fg=style.text, font=style.normal)
            power = cw.ENGLabel(busses[b], text='', value=60, unit='kW',
                                style=style)
            power.configure(fg=style.ind_on, font=style.small)
            current = cw.ENGLabel(busses[b], text='', value=6.0, unit='A',
                                  style=style)
            current.configure(fg=style.ind_on, font=style.small)
            voltage = cw.ENGLabel(busses[b], text='', value=10.0, unit='kV',
                                  style=style)
            voltage.configure(fg=style.ind_on, font=style.small)

            # Render labels relative to container; container rendered with switches
            label.grid(row=0, column=0, sticky=tk.W)
            power.grid(row=1, column=0, sticky=tk.W)
            current.grid(row=2, column=0, sticky=tk.W)
            voltage.grid(row=3, column=0, sticky=tk.W)

            # Store pointer to representation
            components[b].widgets['P'].append(power)
            components[b].widgets['I'].append(current)
            components[b].widgets['V'].append(voltage)

        # Reactors
        reactors = {}
        for r in [HAB_REACT, AYSE_REACT]:
            reactors[r] = tk.Frame(e_grid, bg=style.bg, bd=2, relief=tk.RIDGE)
            label = tk.Label(reactors[r], text=r,
                             bg=style.bg, fg=style.text, font=style.normal)
            current = cw.ENGLabel(reactors[r], text='', value=99, unit='A',
                                style=style)
            temperature = cw.ENGLabel(reactors[r], text='', value=99, unit='*C',
                                  style=style)

            label.grid(row=0, column=0, sticky=tk.W)
            current.grid(row=1, column=0, sticky=tk.W)
            temperature.grid(row=2, column=0, sticky=tk.W)

            components[r].widgets['I'].append(current)
            components[r].widgets['T'].append(temperature)

        # One-of Widgets
        widgets[RADS_BATT] = tk.Label(e_grid, text='100%', font=style.small,
                                      bg=style.bg, fg=style.text)
        widgets[RADS1] = cw.TextButton(e_grid, text=RADS1, style=style)
        widgets[RADS2] = cw.TextButton(e_grid, text=RADS2, style=style)
        widgets[RCON_BATT] = tk.Label(e_grid, text='2000 As', font=style.small,
                                      bg=style.bg, fg=style.text)
        widgets[RCON1] = cw.TextButton(e_grid, text=RCON1, style=style)
        widgets[RCON2] = cw.TextButton(e_grid, text=RCON2, style=style)

        # Create Switches
        widgets['sw_RADS1'] = cw.Switch(e_grid, length='1h', style=style)
        widgets['sw_RADS2'] = cw.Switch(e_grid, length='1h', style=style)
        widgets['sw_RCON1'] = cw.Switch(e_grid, length='1h', style=style)
        widgets['sw_RCON2'] = cw.Switch(e_grid, length='1h', style=style)
        widgets['sw_ions'] = cw.Switch(
            e_grid, length='3v', style=style, connection=engines['ION'])
        widgets['sw_acc'] = cw.Switch(
            e_grid, length='3v', style=style, connection=engines['ACC'])
        widgets['sw_gpd'] = cw.Switch(
            e_grid, length='3v', style=style, connection=engines['GPD'])
        widgets['sw_habr'] = cw.Switch(e_grid, length='1v', style=style)

        # Render EGrid
        engines['ION'].grid(row=0, column=3)
        engines['ACC'].grid(row=0, column=5)
        engines['GPD'].grid(row=0, column=14)

        widgets['sw_ions'].grid(row=1, column=3, rowspan=2)
        widgets['sw_acc'].grid(row=1, column=5, rowspan=2)
        widgets['sw_gpd'].grid(row=1, column=14, rowspan=2)

        widgets[RADS_BATT].grid(row=3, column=0, rowspan=2)
        widgets[RADS1].grid(row=3, column=1)
        widgets['sw_RADS1'].grid(row=3, column=2)
        widgets[RADS2].grid(row=4, column=1)
        widgets['sw_RADS2'].grid(row=4, column=2)
        busses[BUS1].grid(row=3, column=3, rowspan=4, columnspan=3)
        busses[BUSA].grid(row=3, column=14, rowspan=4, columnspan=3)

        widgets[RCON_BATT].grid(row=5, column=0, rowspan=2)
        widgets[RCON1].grid(row=5, column=1)
        widgets['sw_RCON1'].grid(row=5, column=2)
        widgets[RCON2].grid(row=6, column=1)
        widgets['sw_RCON2'].grid(row=6, column=2)

        widgets['sw_habr'].grid(row=7, column=3)
        reactors[HAB_REACT].grid(row=8, column=3, rowspan=3, columnspan=2)
        busses[BUS2].grid(row=8, column=7, rowspan=3, columnspan=2)
        busses[BUS3].grid(row=8, column=11, rowspan=3, columnspan=2)
        reactors[AYSE_REACT].grid(row=8, column=14, rowspan=3, columnspan=2)

        # ---------------- Coolant Loops ----------------
        loop1 = tk.Label(coolant_ctrl, text=LP1, font=style.normal,
                         bg=style.bg, fg=style.text)
        loop2 = tk.Label(coolant_ctrl, text=LP2, font=style.normal,
                         bg=style.bg, fg=style.text)
        pump = tk.Label(coolant_ctrl, text='PUMP', font=style.normal,
                        bg=style.bg, fg=style.text)
        temp = tk.Label(coolant_ctrl, text='TEMP', font=style.normal,
                        bg=style.bg, fg=style.text)
        widgets['PUMP1'] = tk.Spinbox(
            coolant_ctrl, width=2, from_=0, to=100, increment=5,
            bg=style.bg, fg=style.text, font=style.normal)
        widgets['PUMP2'] = tk.Spinbox(
            coolant_ctrl, width=2, from_=0, to=100, increment=5,
            bg=style.bg, fg=style.text, font=style.normal)
        temp1 = tk.Label(coolant_ctrl, text='99', font=style.normal,
                         bg=style.bg, fg=style.text)
        temp2 = tk.Label(coolant_ctrl, text='99', font=style.normal,
                         bg=style.bg, fg=style.text)
        widgets['CL_SELECT'] = tk.Spinbox(
            coolant_ctrl, width=6, bg=style.bg, fg=style.text,
            font=style.normal, values=(LP1, LP2), wrap=True)

        radiators = tk.Frame(coolant_ctrl, bg=style.bg)
        for i in range(2):
            for j in range(3):
                rad = 'R{}'.format(i * 3 + j + 1)
                widgets[rad] = cw.Indicator(radiators, text=rad, style=style)
                widgets[rad].grid(row=i+4, column=j, sticky=tk.E)

        loop1.grid(row=1, column=0)
        loop2.grid(row=2, column=0)
        pump.grid(row=0, column=1)
        widgets['PUMP1'].grid(row=1, column=1)
        widgets['PUMP2'].grid(row=2, column=1)
        temp.grid(row=0, column=2)
        temp1.grid(row=1, column=2)
        temp2.grid(row=2, column=2)
        widgets['CL_SELECT'].grid(row=3, column=0, columnspan=3, pady=10)
        radiators.grid(row=4, column=0, columnspan=3, pady=10)

        components[LP1].widgets['T'].append(temp1)
        components[LP2].widgets['T'].append(temp2)

        # ---------------- Reactor Control ----------------
        controls = tk.Frame(reactor_ctrl, bg=style.bg)
        table = tk.Frame(reactor_ctrl, bg=style.bg)
        graph_section = tk.Frame(reactor_ctrl, bg=style.bg)
        controls.grid(row=0, column=0)
        table.grid(row=0, column=1)
        # graph_section.grid(row=1, column=0, columnspan=2)

        widgets[REACT_INJ1] = cw.Indicator(controls, text=REACT_INJ1,
                                           style=style)
        widgets[REACT_INJ2] = cw.Indicator(controls, text=REACT_INJ2,
                                           style=style)
        widgets['hr_heater'] = cw.Indicator(controls, text="HEAT",
                                            style=style)
        widgets[RCON1] = cw.Indicator(controls, text=RCON1, style=style)
        widgets[RCON2] = cw.Indicator(controls, text=RCON2, style=style)
        widgets[A_OVERTEMP] = cw.Alert(controls, text='TEMP', style=style)

        widgets[REACT_INJ1].grid(row=0, column=0, sticky=tk.E,
                                 padx=(5, 0), pady=(5, 0))
        widgets[REACT_INJ2].grid(row=1, column=0, sticky=tk.E)
        widgets['hr_heater'].grid(row=2, column=0, sticky=tk.E)
        widgets[RCON1].grid(row=0, column=1, sticky=tk.W, pady=(5, 0))
        widgets[RCON2].grid(row=1, column=1, sticky=tk.W)
        widgets[A_OVERTEMP].grid(row=2, column=1, sticky=tk.W)
        # widgets[BAT].grid(row=2, column=2, columnspan=2)
        # widgets[A_LOWBATT].grid(row=3, column=2, columnspan=2)

        hab_label = tk.Label(table, text='HAB_R')
        ayse_label = tk.Label(table, text='AYSE_R')
        rcon1_label = tk.Label(table, text='RCON1')
        rcon2_label = tk.Label(table, text='RCON2')
        temp_label = tk.Label(table, text='TEMP')
        curr_label = tk.Label(table, text='CURR')
        habr_temp = tk.Label(table, text='99')
        ayser_temp = tk.Label(table, text='99')
        rcon1_temp = tk.Label(table, text='99')
        rcon2_temp = tk.Label(table, text='99')
        habr_curr = tk.Label(table, text='99')
        ayser_curr = tk.Label(table, text='99')

        for w in table.children.values():
            w.configure(bg=style.bg, fg=style.text, font=style.small)

        hab_label.grid(row=1, column=0)
        ayse_label.grid(row=2, column=0)
        rcon1_label.grid(row=3, column=0)
        rcon2_label.grid(row=4, column=0)
        temp_label.grid(row=0, column=1)
        curr_label.grid(row=0, column=2)
        habr_temp.grid(row=1, column=1)
        ayser_temp.grid(row=2, column=1)
        rcon1_temp.grid(row=3, column=1)
        rcon2_temp.grid(row=4, column=1)
        habr_curr.grid(row=1, column=2)
        ayser_curr.grid(row=2, column=2)

        components[HAB_REACT].widgets['I'].append(habr_curr)
        components[HAB_REACT].widgets['T'].append(habr_temp)
        components[AYSE_REACT].widgets['I'].append(ayser_curr)
        components[AYSE_REACT].widgets['T'].append(ayser_temp)
        components[RCON1].widgets['T'].append(rcon1_temp)
        components[RCON2].widgets['T'].append(rcon2_temp)

        graph = tk.Canvas(graph_section,width=100, height=100)
        graph.grid() # Why can't I use pack?

        # ---------------- Radiator Control ----------------
        for i in range(8):
            rad = 'R{}'.format(i+1)

            label = tk.Label(radiator_ctrl, text=rad,
                             bg=style.bg, fg=style.text, font=style.normal)

            if i < 3:
                widgets['r_' + rad] = tk.Spinbox(
                    radiator_ctrl, width=6, bg=style.bg, fg=style.text,
                    font=style.normal,
                    values=(STOWED, ISOLATED, LP1, LP2), wrap=True)
            elif i < 6:
                widgets['r_' + rad] = tk.Spinbox(
                    radiator_ctrl, width=6, bg=style.bg, fg=style.text,
                    font=style.normal,
                    values=(ISOLATED, LP1, LP2), wrap=True)
            else:
                widgets['r_' + rad] = tk.Spinbox(
                    radiator_ctrl, width=6, bg=style.bg, fg=style.text,
                    font=style.normal,
                    values=(ISOLATED, LP3), wrap=True)

            label.grid(row=i, column=0)
            widgets['r_' + rad].grid(row=i, column=1, padx=15)


# MAIN LOOP
app = MainApplication()    # Essential. Do not remove.
app.bind_all('<Key>', lambda e: keybinds(e))
widgets['a_asteroid'].alert()
app.mainloop()    # Essential. Do not remove.
