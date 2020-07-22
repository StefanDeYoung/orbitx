import tkinter as tk
from orbitx.graphics.tkinter_style import Style
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


class ENGLabel(tk.Label):
    """
    Use to display a label that also has a value, which may take a unit.
    E.g. ENGLabel(parent, text='FUEL', value=1000, unit='kg'
    """

    def __init__(self, parent: tk.Widget, text: str = '',
                 value: Union[int, str]= 'n/a', unit: Optional[str] = None,
                 style=Style('default'), small: Optional[bool] = False):
        super().__init__(parent)
        self.text = text
        self.value = value
        self.unit = unit

        self.configure(anchor=tk.W, justify=tk.LEFT,
                       bg=style.bg, fg=style.text)

        if small:
            self.configure(font=style.small)
        else:
            self.configure(font=style.normal)

        self.update_value(self.value)

    def text_decorator(self) -> str:
        if self.unit is not None:
            return self.text + ' ' + str(self.value) + ' ' + self.unit
        else:
            return self.text + ' ' + str(self.value)

    def update_value(self, value):
        self.value = value
        self.configure(text=self.text_decorator())


class ENGLabelFrame(tk.LabelFrame):
    """A subdivision of the GUI using ENG styling.
    E.g. master = ENGLabelFrame(parent, text='Master Control')
    """

    def __init__(self, parent: tk.Widget, text: str, style=Style('default')):
        font = style.normal
        super().__init__(parent, text=text, font=font, fg=style.text, bg=style.bg)


class TextButton(tk.Button):
    """
    Represents an flat button on the e-grid.
    E.g. ion1 = TextButton(parent, text='RAD')
    """

    def __init__(self, parent, style=Style('default'), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(command=self.press,
                       font=style.small,
                       relief=tk.FLAT,
                       bg=style.bg,
                       fg=style.text)

        self.style = style
        self.value = 0

    def press(self):
        if self.value == 0:
            self.value = 1
            self.configure(fg=self.style.sw_on)
        else:
            self.value = 0
            self.configure(fg=self.style.text)


class Indicator(tk.Button):
    """
    Represents an indicator light/toggle push-button switch.
    E.g. radar = Indicator(parent, text='RAD')
    """

    def __init__(self, parent, style=Style('default'), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Allows for button width, height to be specified in px
        self.px_img = tk.PhotoImage(width=1, height=1)

        self.configure(image=self.px_img,
                       compound='c',
                       width=50,
                       height=50,
                       command=self.press,
                       font=style.normal
                       )

        self.style = style
        self.value = 1    # Will be set to 0, on next line
        self.invoke()

    def press(self):
        if self.value == 0:
            self.value = 1
            self.configure(relief=tk.RAISED, bg=self.style.ind_on)
        else:
            self.value = 0
            self.configure(relief=tk.SUNKEN, bg=self.style.ind_off)


class OneTimeButton(tk.Button):
    """
    A button, which can only be pressed once.
    """

    def __init__(self, parent, style=Style('default'), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Allows for button width, height to be specified in px
        self.px_img = tk.PhotoImage(width=1, height=1)

        self.configure(image=self.px_img,
                       compound='c',
                       width=100,
                       height=40,
                       font=style.normal,
                       relief=tk.RIDGE,
                       bg=style.otb_unused,
                       command=self.press
                       )

        self.value = 0
        self.style = style

    def press(self):
        self.value = 1
        self.configure(state=tk.DISABLED,
                       relief=tk.FLAT,
                       bg=self.style.otb_used,
                       fg=self.style.otb_unused
                       )


class Alert(tk.Button):
    """
    Stays flat and gray until alerted. Then it flashes, until clicked.
    When clicked, the button should be flat, deactivated, and red, and
    stop flashing, but stay red until the issue causing the alert is cleared.

    Optional invisible tag sets the text to the same colour as the background.
    """

    def __init__(self, parent, invis: bool = False, counter: int = None,
                 style=Style('default'), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.style = style

        # Allows for button width, height to be specified in px
        self.px_img = tk.PhotoImage(width=1, height=1)
        self.configure(image=self.px_img,
                       compound='c',
                       width=80,
                       height=35,
                       font=style.normal,
                       state=tk.DISABLED,
                       command=self.quiet
                       )
        self.alerted = 0
        self.normal_state()

        # Invis doesn't seem to work?
        if invis:
            self.configure(disabledforeground=self.style.bg)

        if counter is not None:
            self.counter = counter

        # Duty Cycle = 0.8 means activated for 80% of the period
        self.flash_period = 450    # ms
        self.duty_cycle = 0.7

    def alert(self):
        self.alerted = 1
        # print('ALERT')
        self.alerted_state()

    def alerted_state(self):
        # print('Alerted State')
        self.configure(relief=tk.RAISED,
                       bg=self.style.alert_bg,
                       fg=self.style.alert_text,
                       state=tk.NORMAL)
        if self.alerted:
            self.event = self.after(int(self.duty_cycle * self.flash_period),
                                    lambda: self.normal_state())

    def normal_state(self):
        # print('Normal State', self.value==True)
        self.configure(relief=tk.FLAT,
                       bg=self.style.bg,
                       fg=self.style.text
                       )
        if self.alerted:
            self.event = self.after(int((1-self.duty_cycle)*self.flash_period),
                                    lambda: self.alerted_state())

    def quiet(self):
        # Stop flashing, but stay alerted
        self.after_cancel(self.event)
        self.alerted = False
        self.alerted_state()
        self.configure(state=tk.DISABLED, relief=tk.GROOVE)


class ENGScale(tk.Scale):
    """A slider."""

    def __init__(self, parent, label: ENGLabel, style=Style('default')):
        super().__init__(parent)

        self.label = label

        self.configure(from_=0,
                       to_=100,
                       resolution=5,
                       orient=tk.HORIZONTAL,
                       bg=style.bg,
                       fg=style.text,
                       troughcolor=style.bg,
                       showvalue=0,
                       command=self.update_slider_label
                       )

    def update_slider_label(self, val):
        self.label.value = val
        self.label.update()


class Switch(tk.Button):
    """
    A pipe that shows electrical connections between elements of the
    power grid.

    length='1h' shows '💢' for open and '=' for closed
    length='1v' shows '💢' for open and '||' for closed
    length='3h' shows '=💢=' for open and '===' for closed
    """

    def __init__(self, parent, length: str = '1h', style=Style('default'),
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.style = style

        assert int(length[0]) % 2 == 1  # Length must be odd
        assert length[1] == 'h' or length[1] == 'v'
        self.length = length

        if not ('switch_open_{}'.format(self.length)) in images:
            self.generate_images()

        self.width = images['switch_open_{}'.format(self.length)].width()
        self.height = images['switch_open_{}'.format(self.length)].height()

        self.configure(command=self.press,
                       width=self.width,
                       height=self.height,
                       relief=tk.FLAT,
                       bd=0,
                       highlightbackground=style.bg,
                       highlightthickness=0,
                       highlightcolor=style.bg
                       )

        self.value = 0
        self.off_state()

        # # TODO Add a char to the button to show its keybinding
        # # As far as I can tell, compound=tk.CENTER is the only choice
        # # to be able to superimpose the text on the button's image
        # # Using this method puts a border around the button, which, for some
        # # reason isn't disabled by setting the bd, highlightbackground, and
        # # highlightthickness. Keep reading
        # # https://effbot.org/tkinterbook/button.htm
        #
        # self.configure(fg=style.text,
        #                text='a',
        #                compound=tk.CENTER)

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
        else:
            self.off_state()

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


class Enabler(tk.Button):
    """
    A button that controls whether another button or component can be
    interacted with.

    e.g.
    widgets[SRB] = cw.OneTimeButton(frame, text=SRB, style=style)
    widgets['arm_SRB'] = cw.Enabler(frame, enables=widgets['SRB'], style=style)
    """

    def __init__(self, parent, enables: tk.Widget, style=Style('default'),
                 *args, **kwargs):
        super().__init__(parent)

        self.enables = enables
        self.style = style

        if not ('enabler_unarmed' in images):
            self.generate_images()

        self.width = images['enabler_unarmed'].width()
        self.height = images['enabler_unarmed'].height()

        self.configure(command=self.press,
                       width=self.width,
                       height=self.height,
                       relief=tk.RIDGE,
                       bd=0,
                       highlightbackground=style.bg,
                       highlightthickness=0,
                       highlightcolor=style.bg
                       )

        self.value = 0
        self.off_state()

        # # TODO Add a char to the button to show its keybinding
        # # As far as I can tell, compound=tk.CENTER is the only choice
        # # to be able to superimpose the text on the button's image
        # # Using this method puts a border around the button, which, for some
        # # reason isn't disabled by setting the bd, highlightbackground, and
        # # highlightthickness. Keep reading
        # # https://effbot.org/tkinterbook/button.htm
        #
        # self.configure(fg=style.text,
        #                text='a',
        #                compound=tk.CENTER)

    def off_state(self):
        self.value = 0
        self.configure(image=images['enabler_unarmed'])
        self.enables.configure(state=tk.DISABLED)

    def on_state(self):
        self.value = 1
        self.configure(image=images['enabler_armed'])
        self.enables.configure(state=tk.NORMAL)

    def press(self):
        if self.value == 0:
            self.on_state()
        else:
            self.off_state()

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
