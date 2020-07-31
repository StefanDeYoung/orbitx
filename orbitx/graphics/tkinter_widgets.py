import tkinter as tk
from orbitx.graphics.tkinter_style import Style
from orbitx.data_structures import PhysicsState, EngineeringState
from typing import Union, Optional
from PIL import Image, ImageColor, ImageTk

# Holder for images, to avoid garbage collection before rendering
images = {}


def set_im_style(im: Image, bg: tuple, fg: tuple) -> Image:
    pixels = im.load()

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pixels[i, j] == (0, 0, 0, 0):
                pixels[i, j] = bg
            else:
                pixels[i, j] = fg

    return im


class Label(tk.Label):
    """
    Use to display a physical characteristic of a component. e.g. Voltage
    E.g. rcon1_vdisplay = cw.ENGDisplayLabel(parent, RCON1, 'V')
    """

    def __init__(self, parent: tk.Widget, component: str, vartype: str):
        super().__init__(parent)
        self.name = component
        self.style = parent.style

        self.value = 999
        self.vartype = vartype

        self.display()

    def display(self):
        self.configure(text=self.text_format(),
                       anchor=tk.W,
                       justify=tk.LEFT,
                       bg=self.style.bg,
                       fg=self.style.text,
                       font=self.style.small
                       )

    def update_value(self, pstate: PhysicsState):
        if self.vartype == 'F':
            self.value = pstate[self.name].fuel
        else:
            component = pstate.engineering[self.name]
            if self.vartype == 'V':
                self.value = component.voltage
            elif self.vartype == 'A':
                self.value = component.current
            elif self.vartype == 'R':
                self.value = component.resistance
            elif self.vartype == 'P':
                self.value = component.voltage * component.current
            elif self.vartype == 'T':
                self.value = component.temperature
            elif self.vartype == 'L':
                self.value = component.get_coolant_loop()

        self.display()

    def text_format(self):
        if self.vartype == 'L':
            return 'LP-{}'.format(self.value)
        else:
            return str(self.value)


class UnitLabel(Label):
    """
    An UnitLabel, where the unit is also displayed
    """
    def __init__(self, parent: tk.Widget, component, vartype: str):
        assert vartype != 'L'

        units = {'V': 'V',
                 'A': 'A',
                 'R': 'Ω',  # U+2126
                 'P': 'W',
                 'T': '℃',  # U+2103
                 'F': 'kg'}

        self.unit = units[vartype]

        super().__init__(parent, component, vartype)

    def text_format(self):
        if self.vartype == 'F':
            return '{} kg'.format(self.value)
        elif self.value > 999:
            return '{} k{}'.format(self.value / 1000, self.unit)
        else:
            return '{} {}'.format(self.value, self.unit)


class LabelFrame(tk.LabelFrame):
    """A subdivision of the GUI using ENG styling.
    E.g. master = ENGLabelFrame(parent, text='Master Control')
    """

    def __init__(self, parent: tk.Widget, text: str):
        self.style = parent.style
        super().__init__(parent,
                         text=text,
                         font=self.style.normal,
                         fg=self.style.text,
                         bg=self.style.bg)


class EGridBox(tk.Frame):
    """A box of labels for the EGrid. Use this for Reactor, and Power Bus.
    E.g. master = ENGLabelFrame(parent, text='Master Control')
    """

    def __init__(self, parent: tk.Widget):
        self.style = parent.style
        super().__init__(parent, bg=self.style.bg, bd=2, relief=tk.RIDGE)


class Title(tk.Label):
    """A textbox with custom styling"""

    def __init__(self, parent: tk.Widget, *args, **kwargs):
        self.style = parent.style
        super().__init__(parent,
                         bg=self.style.bg,
                         fg=self.style.text,
                         font=self.style.normal,
                         *args, **kwargs)


class Button(tk.Button):
    """
    A master class for specialised buttons.
    Buttons have an off_state(), on_state() and are bound by default to
    the press() command.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = parent.style
        self.value = 0
        self.configure(bg=self.style.bg,
                       fg=self.style.text,
                       font=self.style.normal,
                       command=self.press)

        # Allows for button width, height to be specified in px
        if not ('blank_pixel') in images:
            images['blank_pixel'] = tk.PhotoImage(width=1, height=1)

    def off_state(self):
        self.value = 0

    def on_state(self):
        self.value = 1

    def press(self):
        if self.value:
            self.off_state()
        else:
            self.on_state()


class TextButton(Button):
    """
    Represents an flat button on the e-grid.
    E.g. ion1 = TextButton(parent, text='RCON1', block=True)

    Options:
        block:bool=False    Does the button appear in a block with other
                            buttons, so that the block will need to be
                            connected to a switch?
    """

    def __init__(self, parent, block: bool = False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(font=self.style.small,
                       relief=tk.FLAT)

        if isinstance(parent, EGridBox) or isinstance(parent, EGridComponent):
            self.configure(image=images['blank_pixel'],
                           compound='c',
                           height=5)

        if block:
            self.connection = self
            self.linked_buttons = [self]

    def change_connection(self, connection):
        self.connection = connection
        self.linked_buttons = [v for k, v in self.master.children.items()
                               if '!textbutton' in k]

    def off_state(self):
        self.value = 0
        self.configure(fg=self.style.text)

    def on_state(self):
        self.value = 1
        self.configure(fg=self.style.sw_on)

    def press(self):
        if self.value:
            self.off_state()
        else:
            self.on_state()
        if any([button.value for button in self.linked_buttons]):
            self.connection.on_state()
        else:
            self.connection.off_state()


class EGridComponent(tk.Frame):
    """
    Represents an flat button on the e-grid with associated temperature and
    coolant loop displays.
    E.g. ion1 = TextButton(parent, component='RCON1')

    Options:
        block:bool=False    Does the button appear in a block with other
                            buttons, so that the block will need to be
                            connected to a switch?
        switch:tuple   Whether a =+= style switch should appear
            length:str          The size of the =+= style switch e.g. '1h','3v'
            side:str            On which side of the text should the switch appear?
                                Use tk.N, tk.S, tk.E, tk.W
    """

    def __init__(self, parent, component, switch: Optional[tuple] = None,
                 block: bool = False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = parent.style
        self.configure(bg=self.style.bg)

        self.value = 0
        self.name = component

        self.textbutton = TextButton(self, text=self.name, block=block)
        self.temperature = Label(self, component, 'T')
        self.coolant = Label(self, component, 'L')

        # self.keyboard = Label

        if block:
            self.connection = self
            self.linked_buttons = [self]

        if switch is not None:
            length, side = switch
            self.switch = Switch(self, length)
            if side == tk.W:
                self.switch.grid(row=0, column=0)
                self.textbutton.grid(row=0, column=1)
                self.temperature.grid(row=0, column=2)
                self.coolant.grid(row=0, column=3)
            if side == tk.E:
                self.switch.grid(row=1, column=3)
            elif side == tk.N:
                self.switch.grid(row=0, column=1)
            elif side == tk.S:
                self.switch.grid(row=2, column=1)
        else:
            self.textbutton.grid(row=1, column=0)
            self.temperature.grid(row=1, column=1)
            self.coolant.grid(row=1, column=2)

    def update_labels(self, pstate: PhysicsState):
        self.temperature.update_value()
        self.coolant.update_value()


class Switch(Button):
    """
    A pipe that shows electrical connections between elements of the
    power grid.

    length='1h' shows '💢' for open and '=' for closed
    length='1v' shows '💢' for open and '||' for closed
    length='3h' shows '=💢=' for open and '===' for closed

    connection = a tk.Frame that contains multiple textbuttons that should
    all be toggled by this switch
    """

    def __init__(self, parent, length: str = '1h',
                 connection: Optional[tk.Widget] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        assert int(length[0]) % 2 == 1  # Length must be odd
        assert length[1] == 'h' or length[1] == 'v'
        self.length = length

        if not ('switch_open_{}'.format(self.length)) in images:
            self.generate_images()

        self.width = images['switch_open_{}'.format(self.length)].width()
        self.height = images['switch_open_{}'.format(self.length)].height()

        self.configure(width=self.width,
                       height=self.height,
                       relief=tk.FLAT,
                       bd=0,
                       highlightbackground=self.style.bg,
                       highlightthickness=0,
                       highlightcolor=self.style.bg
                       )
        self.off_state()

        if connection is None:
            self.connections = None
        else:
            self.connections = self.make_connections(connection)

    def off_state(self):
        self.value = 0
        self.configure(image=images['switch_open_{}'.format(self.length)])

    def on_state(self):
        self.value = 1
        self.configure(image=images['switch_closed_{}'.format(self.length)],
                       relief=tk.FLAT)

    def press(self):
        if self.value == 0:
            self.on_state()
            if self.connections is not None:
                for button in self.connections:
                    button.on_state()
        else:
            self.off_state()
            if self.connections is not None:
                for button in self.connections:
                    button.off_state()

    def make_connections(self, connection):
        if isinstance(connection, EGridBox):
            grid_components = [v for k, v in connection.children.items()
                               if '!egridcomponent' in k]
            textbuttons = []
            for c in grid_components:
                textbuttons.append(c.children['!textbutton'])
        else:
            textbuttons = [v for k, v in connection.children.items()
                           if '!textbutton' in k]
        for button in textbuttons:
            button.change_connection(self)
        return textbuttons

    def generate_images(self):
        try:
            mid_off = Image.open('../../data/textures/eng_switch_open.PNG')
            out_off = Image.open('../../data/textures/eng_switch_closed.PNG')
        except IOError:
            print('Unable to load images: Engineering Switches')

        assert mid_off.width == out_off.width
        assert mid_off.height == out_off.height
        width = mid_off.width
        height = mid_off.height

        color_on = ImageColor.getrgb(self.style.sw_on)
        color_off = ImageColor.getrgb(self.style.sw_off)
        color_bg = ImageColor.getrgb(self.style.bg)

        out_on = out_off.copy()

        mid_off = set_im_style(mid_off, color_bg, color_off)
        out_off = set_im_style(out_off, color_bg, color_off)
        out_on = set_im_style(out_on, color_bg, color_on)

        if self.length[1] == 'v':
            out_off = out_off.rotate(90)
            out_on = out_on.rotate(90)

        sw_size = int(self.length[0])

        if sw_size == 1:
            sw_off = mid_off
            sw_on = out_on
        else:
            if self.length[1] == 'h':
                sw_off = Image.new('RGB', (sw_size * width, height))
                sw_on = Image.new('RGB', (sw_size * width, height))
                for i in range(sw_size):
                    sw_on.paste(out_on, (i * width, 0))
                    if i == (sw_size - 1) / 2:
                        sw_off.paste(mid_off, (i * width, 0))
                    else:
                        sw_off.paste(out_off, (i * width, 0))
            else:
                sw_off = Image.new('RGB', (width, sw_size * height))
                sw_on = Image.new('RGB', (width, sw_size * height))
                for i in range(sw_size):
                    sw_on.paste(out_on, (0, i * height))
                    if i == (sw_size - 1) / 2:
                        sw_off.paste(mid_off, (0, i * height))
                    else:
                        sw_off.paste(out_off, (0, i * height))

        images['switch_open_{}'.format(self.length)] = \
            ImageTk.PhotoImage(sw_off)
        images['switch_closed_{}'.format(self.length)] = \
            ImageTk.PhotoImage(sw_on)


class Indicator(Button):
    """
    Represents an indicator light/toggle push-button switch.
    E.g. radar = Indicator(parent, text='RAD')
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(image=images['blank_pixel'],
                       compound='c',
                       width=40,
                       height=40,
                       fg=self.style.bg)

        self.off_state()

    def off_state(self):
        self.value = 0
        self.configure(relief=tk.SUNKEN, bg=self.style.ind_off)

    def on_state(self):
        self.value = 1
        self.configure(relief=tk.RAISED, bg=self.style.ind_on)


class OneTimeButton(Button):
    """
    A button, which can only be pressed once.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(image=images['blank_pixel'],
                       compound='c',
                       width=60,
                       height=30,
                       relief=tk.RIDGE,
                       bg=self.style.otb_unused,
                       fg=self.style.bg
                       )

    def on_state(self):
        self.value = 1
        self.configure(state=tk.DISABLED,
                       relief=tk.FLAT,
                       bg=self.style.otb_used,
                       fg=self.style.otb_unused
                       )


class Alert(Button):
    """
    Stays flat and gray until alerted. Then it flashes, until clicked.
    When clicked, the button should be flat, deactivated, and red, and
    stop flashing, but stay red until the issue causing the alert is cleared.

    Optional invisible tag sets the text to the same colour as the background.
    """

    def __init__(self, parent, invis: bool = False, counter: int = None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(image=images['blank_pixel'],
                       compound='c',
                       width=80,
                       height=20,
                       state=tk.DISABLED,
                       command=self.quiet
                       )
        self.normal_state()

        if invis:
            self.configure(disabledforeground=self.style.bg)

        if counter is not None:
            self.counter = counter

        # Duty Cycle = 0.8 means activated for 80% of the period
        self.flash_period = 450    # ms
        self.duty_cycle = 0.7

    def alert(self):
        self.value = 1
        self.alerted_state()

    def alerted_state(self):
        self.configure(relief=tk.RAISED,
                       bg=self.style.alert_bg,
                       fg=self.style.alert_text,
                       state=tk.NORMAL)
        if self.value:
            self.event = self.after(int(self.duty_cycle * self.flash_period),
                                    lambda: self.normal_state())

    def normal_state(self):
        self.configure(relief=tk.FLAT,
                       bg=self.style.bg,
                       fg=self.style.text
                       )
        if self.value:
            self.event = self.after(int((1-self.duty_cycle)*self.flash_period),
                                    lambda: self.alerted_state())

    def quiet(self):
        # Stop flashing, but stay alerted
        self.after_cancel(self.event)
        self.value = 0
        self.alerted_state()
        self.configure(state=tk.DISABLED, relief=tk.GROOVE)


class Enabler(Button):
    """
    A button that controls whether another button or component can be
    interacted with.

    e.g.
    widgets[SRB] = cw.OneTimeButton(frame, text=SRB, style=style)
    widgets['arm_SRB'] = cw.Enabler(frame, enables=widgets['SRB'], style=style)
    """

    def __init__(self, parent, enables: tk.Widget, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.enables = enables

        if not ('enabler_unarmed' in images):
            self.generate_images()

        self.width = images['enabler_unarmed'].width()
        self.height = images['enabler_unarmed'].height()

        self.configure(command=self.press,
                       width=self.width,
                       height=self.height,
                       relief=tk.RIDGE,
                       bd=0,
                       highlightbackground=self.style.bg,
                       highlightthickness=0,
                       highlightcolor=self.style.bg
                       )
        self.off_state()

    def off_state(self):
        self.value = 0
        self.configure(image=images['enabler_unarmed'])
        self.enables.configure(state=tk.DISABLED)

    def on_state(self):
        self.value = 1
        self.configure(image=images['enabler_armed'])
        self.enables.configure(state=tk.NORMAL)

    def generate_images(self):
        try:
            base_image = Image.open('../../data/textures/eng_enable_button.png')
        except IOError:
            print('Unable to load images: Engineering Switches')

        color_armed = ImageColor.getrgb(self.style.alert_bg)
        color_unarmed = ImageColor.getrgb(self.style.sw_off)
        color_bg = ImageColor.getrgb(self.style.bg)

        armed = base_image.copy()
        unarmed = base_image.copy()

        armed = set_im_style(armed, color_bg, color_armed)
        unarmed = set_im_style(unarmed, color_bg, color_unarmed)

        images['enabler_armed'] = ImageTk.PhotoImage(armed)
        images['enabler_unarmed'] = ImageTk.PhotoImage(unarmed)


class ENGScale(tk.Scale):
    """A slider."""

    def __init__(self, parent, label: Label):
        super().__init__(parent)
        self.style = parent.style
        self.label = label

        self.configure(from_=0,
                       to_=100,
                       resolution=5,
                       orient=tk.HORIZONTAL,
                       bg=self.style.bg,
                       fg=self.style.text,
                       troughcolor=self.style.bg,
                       showvalue=0,
                       command=self.update_slider_label
                       )

    def update_slider_label(self, val):
        self.label.value = val
        self.label.update()


class Spinbox(tk.Spinbox):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = parent.style
        self.configure(bg=self.style.bg,
                       fg=self.style.text,
                       font=self.style.normal)

        if 'values' in kwargs:
            self.views = {}

    def bind_view_selector(self, views):
        """views is a dict {'View1': tkinter.Widget_of_view1, ...}
        self.values must equal ['View1', 'View2']"""
        self.views = views
        self.bind('<Button-1>', lambda e: self.select_view(self.get()))

    def select_view(self, view: str):
        for k, v in self.views.items():
            if k == view:
                v.grid_remove()
            else:
                v.grid()