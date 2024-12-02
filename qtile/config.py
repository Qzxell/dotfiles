import os
import re
import socket
import subprocess
from spotify import Spotify

from libqtile import hook
from libqtile import qtile
from typing import List  
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder
from pathlib import Path
from libqtile.log_utils import logger

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

mod = "mod4"
home = str(Path.home())
mod1 = "mod1"
MUSIC_PLAYER = 'spotify'
music_cmd = ('dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
             '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.')

def next_prev(action):
    def f(qtile):
        qtile.cmd_spawn(music_cmd + action)
    return f

keys = [

    # Focus
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window around"),
    
    # Move
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Swap
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),

    Key([mod], "Print", lazy.spawn(home + "/.config/qtile/scripts/screenshot.sh")),

    # Size
    Key([mod, "control"], "Down", lazy.layout.shrink(), desc="Grow window to the left"),
    Key([mod, "control"], "Up", lazy.layout.grow(), desc="Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Floating
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),
    
    # Split
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Toggle Layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    #System
    Key([mod1], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),

    Key([mod, "control"], "q", lazy.spawn(home + "/.config/qtile/scripts/powermenu.sh"), desc="Open Powermenu"), 
    # Apps
    Key([mod], "o", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn("qutebrowser"), desc="Launch terminal"),
    Key([mod], "e", lazy.spawn("nautilus"), desc="Launch terminal"),
    Key([mod1], "m", lazy.spawn("rofi -show drun"), desc="Launch terminal"),
    Key([mod1], "Tab", lazy.spawn("rofi -show window"), desc="Launch terminal"),
    Key([mod, "control"], "Return", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
    Key([mod, "shift"], "w", lazy.spawn(home + "/.config/qtile/scripts/wallpaper.sh"), desc="Update Theme and Wallpaper"),
    Key([mod, "control"], "w", lazy.spawn(home + "/.config/qtile/scripts/wallpaper.sh select"), desc="Select Theme and Wallpaper"),

    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl -q s +20%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl -q s 20%-"))        ,
    # Volume
    Key([mod1], "u", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([mod1], "d", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),
    Key([], 'XF86AudioNext', lazy.function(next_prev('Next'))),
    Key([], 'XF86AudioPrev', lazy.function(next_prev('Previous'))),
     # Redshift
    Key([mod], "r", lazy.spawn("redshift -O 2400")),
    Key([mod, "shift"], "h", lazy.spawn("redshift -x")),
    Key([mod], "q", lazy.shutdown()),
    Key([mod], "x", lazy.spawn("scrot 'screenshot_%Y-%m-%d-%T_$wx$h.png' -e 'mkdir -p ~/images/screenshots/ | mv $f ~/images/screenshots/'")),
    Key([mod, "shift"], "x", lazy.spawn("scrot -s")),
]



groups = [
    Group("1", layout='monadtall'),
    Group("2", layout='monadtall'),
    Group("3", layout='monadtall'),
    Group("4", layout='monadtall'),
    Group("5", layout='monadtall'),
]

dgroups_key_binder = simple_key_binder(mod)

# --------------------------------------------------------
# Scratchpads
# --------------------------------------------------------

groups.append(ScratchPad("6", [
    DropDown("chatgpt", "chromium --app=https://chat.openai.com", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
    DropDown("mousepad", "mousepad", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
    DropDown("terminal", "alacritty", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
    DropDown("scrcpy", "scrcpy -d", x=0.8, y=0.05, width=0.15, height=0.6, on_focus_lost_hide=False )
]))

keys.extend([
    Key([mod], 'F10', lazy.group["6"].dropdown_toggle("chatgpt")),
    Key([mod], 'F11', lazy.group["6"].dropdown_toggle("mousepad")),
    Key([mod], 'F12', lazy.group["6"].dropdown_toggle("terminal")),
    Key([mod], 'F9', lazy.group["6"].dropdown_toggle("scrcpy"))
])

layout_theme = { 
    "border_width": 3,
    "margin": 15,
    "border_focus": "F39132",
    "border_normal": "FFFFFF",
    "single_border_width": 3
}

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating()
]

widget_defaults = dict(
    font="DaddyTimeMono Nerd Font",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()
decor_left = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_left"
            # path="rounded_left"
            # path="forward_slash"
            # path="back_slash"
        )
    ],
}

decor_right = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_right"
            # path="rounded_right"
            # path="forward_slash"
            # path="back_slash"
        )
    ],
}

Color1 = "#FF6F61"  # Coral
Color2 = "#6B5B95"  # Gris perla
Color3 = "#88B04B"  # Verde pasto
Color4 = "#F7CAC9"  # Rosa suave
Color5 = "#92A8D1"  # Azul claro
Color6 = "#F0B27A"  # Naranja suave
Color7 = "#FFEB3B"  # Amarillo brillante
Color8 = "#E57373"  # Rojo suave
Color9 = "#64B5F6"  # Azul cielo
Color10 = "#81C784" # Verde menta
Color11 = "#81C784" # Verde menta
Color12 = "#81C784" # Verde menta
Color13 = "#81C784" # Verde menta
Color14 = "#81C784" # Verde menta
Color15 = "#81C784" # Verde menta

widget_list = [
    widget.TextBox(
        **decor_left,
        background=Color1+".4",
        text='Apps',
        foreground='ffffff',
        desc='',
        padding=10,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("rofi -show drun")},
    ),
    widget.TextBox(
        **decor_left,
        background="#ffffff.4",
        text="  ",
        foreground="000000.6",
        fontsize=18,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(home + "/.config/qtile/scripts/wallpaper.sh select")},
    ),
    widget.GroupBox(
        **decor_left,
        background="#ffffff.7",
        highlight_method='block',
        highlight='ffffff',
        block_border='ffffff',
        highlight_color=['ffffff','ffffff'],
        block_highlight_text_color='000000',
        foreground='ffffff',
        rounded=False,
        this_current_screen_border='ffffff',
        active='ffffff'
    ),
    widget.TextBox(
        **decor_left,
        background="#ffffff.4",
        text=" ",
        foreground="000000.6",
        fontsize=18,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("bash " + home + "/.config/.settings/filemanager.sh")}
    ),
    
    widget.WindowName(
        **decor_left,
        max_chars=50,
        background=Color2+".4",
        width=400,
        padding=10
    ),
    Spotify(),
    widget.Spacer(
        length=30
    ),
    widget.Spacer(),
    widget.TextBox(
        **decor_right,
        text="                ",
        background="#000000.3"      
    ),    
    widget.Volume(
        **decor_right,
        background=Color9+".4",
        padding=10, 
        fmt='Vol: {}',
    ),
    widget.Pomodoro(
        **decor_right,
        length_pomodori = 25,
        length_short_break = 5,
        length_long_break = 15,
        background=Color12+".4",
        padding=10, 
    ),
    widget.DF(
        **decor_right,
        padding=10, 
        background=Color8+".4",        
        visible_on_warn=False,
        format="{p} {uf}{m} ({r:.0f}%)"
    ),
    widget.Clock(
        **decor_right,
        background=Color4+".4",   
        padding=10,      
        format="%d-%m-%Y / %I:%M %p",
    ),
    widget.TextBox(
        **decor_right,
        background=Color2+".4",     
        padding=5,    
        text=" ",
        fontsize=20,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(home + "/.config/qtile/scripts/powermenu.sh")},
    ),
]


screens = [
    Screen(
        top=bar.Bar(
            widget_list,
            30,
            padding=20,
            opacity=0.7,
            border_width=[0, 0, 0, 0],
            margin=[0,0,0,0],
            background="#000000.3"
        ),
    ),
]
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"




@hook.subscribe.startup_once
def autostart():
    autostartscript = "~/.config/qtile/autostart.sh"
    home = os.path.expanduser(autostartscript)
    subprocess.Popen([home])
