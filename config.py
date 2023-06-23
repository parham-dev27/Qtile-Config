# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2023 Parhamdev-27


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import subprocess
from libqtile import layout, bar, hook
from libqtile.config import Drag, Group, Key, Match, Screen
from libqtile.command import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def muteVolume(qtile):
    subprocess.call(['amixer', '-D', 'pulse', 'set', "Master", "1+", "toggle"])

@lazy.function
def increaseVolume(qtile):
    output = subprocess.check_output(['amixer', 'sget', 'Master']).decode()
    current_volume = int(output.split('[')[1].split('%')[0])
    subprocess.call(['amixer', '-q', 'sset', 'Master', f"{min(current_volume + 5, 100)}%"])

@lazy.function
def decreaseVolume(qtile):
    output = subprocess.check_output(['amixer', 'sget', 'Master']).decode()
    current_volume = int(output.split('[')[1].split('%')[0])
    subprocess.call(['amixer', '-q', 'sset', 'Master', f"{max(current_volume - 5, 0)}%"])

@lazy.function
def gsimplecal(qtile):
    qtile.cmd_spawn("gsimplecal")
    
    
@lazy.function
def changeSoundOutput(qtile):
    active_device = subprocess.check_output(["pactl",  "get-default-sink"]).decode().strip()
    if active_device == "alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-stereo":
        subprocess.Popen(["pacmd", "set-default-sink", "alsa_output.pci-0000_00_1f.3.analog-stereo"])
    else:
        subprocess.Popen(["pacmd", "set-default-sink", "alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-stereo"])

@lazy.function
def switchLayout(qtile):
    p1 = subprocess.Popen(['setxkbmap', '-query'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'layout'], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['cut', '-d', ':', '-f2'], stdin=p2.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['tr', '-d', ' '], stdin=p3.stdout)

    output_str = output.decode('utf-8').strip()

    if output_str.lower() == "de":
        subprocess.Popen(['setxkbmap', '-layout', 'ir,de'])
    else:
        subprocess.Popen(['setxkbmap', '-layout', 'de'])

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [
# SOUND KEYS
    Key([mod], "F9", changeSoundOutput()),
    Key([mod], "F12", increaseVolume()),
    Key([mod], "F11", decreaseVolume()),
    Key([mod], "F10", muteVolume()), 

# CHANGE KEYBOARD LAYOUT
    Key([mod], "space", switchLayout()),

# SUPER + FUNCTION KEYS
    Key([mod], "q", lazy.window.kill()),

# SUPER + SHIFT KEYS
    Key([mod, "shift"], "r", lazy.restart()),

# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.reset()),
    Key([mod], "Tab", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "k", lazy.layout.grow().when(layout='monadtall'),),
    Key([mod, "control"], "Up", lazy.layout.grow().when(layout='monadtall'),),
    Key([mod, "control"], "j", lazy.layout.shrink().when(layout='monadtall'),),
    Key([mod, "control"], "Down", lazy.layout.shrink().when(layout='monadtall'),),
    Key([mod, "control"], "h", lazy.layout.grow().when(layout='monadwide'),),
    Key([mod, "control"], "Right", lazy.layout.grow().when(layout='monadwide'),),
    Key([mod, "control"], "l", lazy.layout.shrink().when(layout='monadwide'),),
    Key([mod, "control"], "Left", lazy.layout.shrink().when(layout='monadwide'),),

# MOVE WINDOWS UP OR DOWN MONADWIDE LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up().when(layout='monadwide')),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down().when(layout='monadwide')),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left().when(layout='monadwide')),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right().when(layout='monadwide')),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up().when(layout='monadwide')),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down().when(layout='monadwide')),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left().when(layout='monadwide')),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right().when(layout='monadwide')),

# MOVE WINDOWS UP OR DOWN MONADTALL LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up().when(layout='monadtall')),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down().when(layout='monadtall')),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left().when(layout='monadtall')),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right().when(layout='monadtall')),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up().when(layout='monadtall')),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down().when(layout='monadtall')),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left().when(layout='monadtall')),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right().when(layout='monadtall')),
]

# GROUPS
groups = []
group_names = ["a", "s", "f", "t", "z", "u", "i", "o", "p",]
group_labels = ["WWW", "FILE","DEV", "DOC", "VBOX", "CHAT", "MUS", "REC", "TMP",]
group_layouts = ["max", "monadtall", "max", "monadtall", "max", "monadtall", "monadtall", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Max(**layout_theme),
]

# COLORS 
# THEME NAME: ARCO LINUX
def init_colors():
    return [["#2F343F", "#2F343F"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fba922", "#fba922"], # color 3
            ["#3384d0", "#3384d0"], # color 4
            ["#f3f4f5", "#f3f4f5"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8
            ["#a9a9a9", "#a9a9a9"], # color 9
            ]



colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()


def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[1]),

        widget.GroupBox(
            font="Noto Sans",
            fontsize = 16,
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            disable_drag = True,
            active = '#46d9ff', 
            inactive = colors[2],
            rounded = False,
            highlight_method = "line",
            this_current_screen_border = colors[4],
            foreground = colors[2],
            background = colors[0]),

        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.CurrentLayoutIcon(
            foreground = colors[2],
            background = colors[0],
            padding = 0,
            scale = 0.7),

        widget.CurrentLayout(
            font = "Noto Sans Bold",
            foreground = colors[5],
            background = colors[1],),

        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.WindowName(
            font="Noto Sans",
            fontsize = 12,
            foreground = colors[9],
            background = colors[1],),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.Systray(
            font="Noto Sans",
            fontsize = 12,
            background = colors[1],
            icon_size = 20,
            padding = 6,),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.CheckUpdates(
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = " {updates}",
            foreground = "#ff6bc2",
            colour_have_updates = "#ff6bc2",
            colour_no_updates = "#ff6bc2",
            no_update_string = " 0",
            padding = 5,
            background = colors[0],
            fontsize=15,
            font= "Hack Nerd Font",
            decorations = [
                BorderDecoration(
                    colour = '#ff6bc2',
                    border_width = [0, 0, 2, 0],
                    padding_x = None,
                    padding_y = None,)],),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.CPU(
            foreground = '#b5eb6c',
            background = colors[0],
            padding = 5,
            format = " {load_percent}%",
            fmt = "{}",
            update_interval = 2,
            fontsize=15,
            font= "Hack Nerd Font",
            decorations = [
                BorderDecoration(
                    colour = '#b5eb6c',
                    border_width = [0, 0, 2, 0],
                    padding_x = None,
                    padding_y = None,)]),

        widget.ThermalSensor(
            foreground = '#b5eb6c',
            background = colors[0],
            threshold = 90,
            fontsize=15,
            padding = 5,
            fmt = ' {}',
            tag_sensor='Core 0',
            font= "Hack Nerd Font",
            decorations = [
                BorderDecoration(
                    colour = '#b5eb6c',
                    border_width = [0, 0, 2, 0],
                    padding_x = None,
                    padding_y = None,)]),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.Memory(
            fontsize=15,
            foreground = '#a9a1e1',
            background = colors[0],
            padding = 5,
            fmt = '{}',
            font= "Hack Nerd Font",
            measure_mem='G',
            decorations = [
                BorderDecoration(
                    colour = '#a9a1e1',
                    border_width = [0, 0, 2, 0],
                    padding_x = None,
                    padding_y = None,)],),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.KeyboardLayout(
            font= "Hack Nerd Font",
            foreground = colors[3],
            background = colors[0],
            fmt = ' {}',
            padding = 5,
            configured_keyboards = ["de", "ir,de"],
            fontsize=15,
            decorations = [
                BorderDecoration(
                    colour = colors[3],
                    border_width = [0, 0, 2, 0],
                    padding_x = 2,
                    padding_y = None,)],),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.Volume(
            font= "Hack Nerd Font",
            foreground = '#ff6c6b',
            background = colors[0],
            fmt = ' {}',
            padding = 5,
            fontsize=15,
            mouse_callbacks = {"Button1": changeSoundOutput()},
            decorations = [
                BorderDecoration(
                    colour = '#ff6c6b',
                    border_width = [0, 0, 2, 0],
                    padding_x = 2,
                    padding_y = None,)],),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),

        widget.Clock(
            foreground = '#51afef',
            background = colors[1],
            fontsize = 16,
            font = "Hack Nerd Font Bold",
            format=" %a %b %d, %Y  %H:%M",
            mouse_callbacks = {'Button1': gsimplecal()},
            decorations = [
                BorderDecoration(
                    colour = '#51afef',
                    border_width = [0, 0, 2, 0],
                    padding_x = 2,
                    padding_y = None,)],),

        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),
    ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


widgets_screen1 = init_widgets_screen1()



def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8),),]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []


# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser", "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", "Evolution", "Geary", "Mail", "Thunderbird", "evolution", "geary", "mail", "thunderbird", "Msgcompose", ]
    d[group_names[1]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt", "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
    d[group_names[2]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "atom", "subl", "geany", "brackets", "code-oss", "code", "Meld", "meld", "org.gnome.meld" "org.gnome.Meld", "Alacritty", "Xfce4-taskmanager", "xfce4-taskmanager", ]
    d[group_names[3]] = ["Okular", "okular", "libreoffice", "Libreoffice", "soffice","eog", "Eog", "DesktopEditors", "ONLYOFFICE Desktop Editors", "Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh", "inkscape", "nomacs", "ristretto", "nitrogen", "feh", "Gimp", "gimp", "libreoffice-writer", "libreoffice-calc", "libreoffice-impress", "libreoffice-draw", "libreoffice-base", "krita", ]
    d[group_names[4]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer", "virtualbox manager", "virtualbox machine", "vmplayer", "VirtualBox", "VirtualBoxVM", ]
    d[group_names[5]] = ["telegram-desktop", "TelegramDesktop", "Zoom", "zoom", "discord", "Discord", ]
    d[group_names[6]] = ["Spotify", "Pragha", "Alacritty", "Clementine", "Deadbeef", "Audacious", "spotify", "pragha", "clementine", "deadbeef", "audacious", "vlc", ]
    d[group_names[7]] = ["obs", "Obs", "guvcview", "Guvcview"]
    d[group_names[8]] = [ ]
    
    allowToBeInGroup = ["xfce4-terminal", "Xfce4-terminal", "gnome-calculator", "xfce4-notifyd", "Xfce4-notifyd", "gsimplecal", "spectacle", "polkit-gnome-authentication-agent-1", "Toolkit", "notification", "toolbar", "splash", "dialog"]


    wm_class = client.window.get_wm_class()
    if len(wm_class) >= 1:
        wm_class = wm_class[0]
        if wm_class not in allowToBeInGroup:
            for i in range(len(d)):
                if wm_class in list(d.values())[i]:
                    group = list(d.keys())[i]
                    client.togroup(group)
                    client.group.cmd_toscreen(toggle=False)
                    break
                else:
                    client.togroup("p")
                    client.group.cmd_toscreen(toggle=False)


main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='gnome-calculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),
    Match(wm_class="spectacle"),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
