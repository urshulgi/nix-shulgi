# Add autostart script
import os
from libqtile import hook

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

from typing import Optional
from libqtile.widget import base
from libqtile.widget.textbox import TextBox

mod = "mod4"
terminal = "alacritty"

from libqtile.widget import base
from libqtile import hook

import subprocess


class Output(base.ThreadPoolText):
    """ ... """

    defaults = [
        ("update_interval", 
         60,
         "update time in seconds"),

        ("cmd",
         "date",
         "command line as a string or list of arguments to execute"),

        ("shell",
         True,
         "run command through a shell to enable piping and shell expansion"),

        ("text_before",
         "",
         "additional text to display before command output"),

        ("text_after",
         "",
         "additional text to display after command output"),
    ]


    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Output.defaults)


    def _configure(self, qtile, bar):
        base.ThreadPoolText._configure(self, qtile, bar)

        self.text_before = str(self.text_before)
        self.text_after = str(self.text_after)

        self.add_callbacks({
            "Button1": self.cmd_force_update,
        })


    def poll(self):
        """ Run command and update from output. """

        self.run_process()
        return self.get_output()


    def run_process(self):
        """ Run command. """

        self.completed_process = subprocess.run(
            self.cmd,
            capture_output=True,
            text=True,
            shell=self.shell,
        )

        return self.completed_process


    def get_output(self):
        """ Extract output and format for bar. """

        output = self.completed_process.stdout.strip()
        output = self.text_before + output + self.text_after
        return str(output)

# Arrow functions for nice separation of widgets
def left_half_circle(fg_color, bg_color):
    return TextBox(
        text='\uE0B6',
        fontsize=10,
        foreground=fg_color,
        background=bg_color,
        padding=0)


def right_half_circle(fg_color, bg_color: Optional['str'] = None):
    return TextBox(
        text='\uE0B4',
        fontsize=35,
        background=bg_color,
        foreground=fg_color,
        padding=0)


def lower_left_triangle(bg_color, fg_color):
    return TextBox(
        text='\u25e2',
        padding=0,
        fontsize=50,
        background=bg_color,
        foreground=fg_color)


def left_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B2',
        padding=-1,
        fontsize=25,
        background=bg_color,
        foreground=fg_color)


def right_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B0',
        padding=0,
        fontsize=25,
        background=bg_color,
        foreground=fg_color)

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "p", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    # Toggle Keyboard layout
    Key([mod, "control"], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next Keyboard Layout"),
    Key([mod], "print", lazy.spawn("gnome-screenshot -i"), desc="Deepin Screenshot"),

    # Spawn i3lock. Check this post for more customization:
    # https://www.reddit.com/r/unixporn/comments/7df2wz/i3lock_minimal_lockscreen_pretty_indicator/
    Key([mod], "l", lazy.spawn('i3lock -B --inside-color=373445ff --ring-color=ffffffff --line-uses-inside --keyhl-color=d23c3dff --bshl-color=d23c3dff --separator-color=00000000 --insidever-color=fecf4dff --insidewrong-color=d23c3dff --ringver-color=ffffffff --ringwrong-color=ffffffff --ind-pos="x+86:y+1003" --radius=15 --verif-text="" --wrong-text=""'), desc="i3lock Lock Screen"),

    # Media keys
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 2%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 2%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
]

#groups = [Group(i) for i in "123456789"]
groups = [Group("", layout='monadtall'),
          Group("󰖟", layout='max'),
          Group("󰊴", layout='max'),
          Group("󰚢", layout='monadtall'),
          Group("", layout='monadtall'),
          Group("", layout='max'),
         ]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(groups.index(i) + 1),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(groups.index(i) + 1),
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(border_focus_stack=["#d75f5f", "#8f3d3d"], margin=8),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Floating(),
]

colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    #font="Ubuntu Bold",
    font="Caskaydia Cove Nerd Font Bold",
    #font="Noto Sans Mono Bold",
    fontsize=14,
    padding_x=5,
    padding_y=0,
    background=colors[0],
    foreground=colors[2],
)
extension_defaults = widget_defaults.copy()

# Icons for widgets: https://fontawesome.com/v5/cheatsheet
screens = [
    Screen(
        wallpaper='~/Pictures/wallpapers/nix-wallpaper-simple-red.png',
        top=bar.Bar(
            [
                widget.QuickExit(
                    default_text = '\uf011',
                    countdown_format = '{}',
                    background = colors[4],
                    foreground = colors[1],
                    ),
                widget.CurrentLayout(
                    background = colors[5],
                    foreground = colors[1],
                    ),
                right_arrow(colors[6], colors[5]),
                widget.GroupBox(
                    background = colors[6],
                    foreground = colors[1],
                    padding_x = 5,
                    padding_y = -10,
                    fontsize = 30,
                    highlight_method = "line",
                    this_current_screen_border = colors[7],
                    this_screen_border = colors[4],
                    other_current_screen_border = colors[7],
                    other_screen_border = colors[4],
                    ),
                right_arrow(colors[0], colors[6]),
                widget.Prompt(
                    ),
                widget.WindowName(
                    ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                widget.StatusNotifier(),
                widget.Systray(
                    ),
                left_arrow(colors[0], colors[5]),
                widget.TextBox(
                    background = colors[5],
                    foreground = colors[1],
                    text = "󰋎",
                    fontsize = 22,
                    padding = 5,
                    ),
                Output(
                    background = colors[5],
                    foreground = colors[1],
                    cmd="headsetcontrol -b | sed -n -e 's/^.*Battery: //p'", 
                    shell=True
                    ),
                left_arrow(colors[5], colors[7]),
                widget.Memory(
                    background = colors[7],
                    foreground = colors[1],
                    format = " {MemUsed: .0f}{mm} /{MemTotal: .0f}{mm}",
                    update_interval = 10.0,
                    measure_mem = "G",
                    ),
                left_arrow(colors[7], colors[6]),
                widget.TextBox(
                    background = colors[6],
                    foreground = colors[1],
                    text = "󰻠",
                    fontsize = 22,
                    padding = 5,
                    ),
                widget.CPU(
                    background = colors[6],
                    foreground = colors[1],
                    format = "{load_percent}%",
                    update_interval = 10.0,
                    ),
                left_arrow(colors[6], colors[4]),
                widget.Clock(
                    format="%I:%M%p \uf073 %a %d/%m/%y",
                    foreground = colors[0],
                    background = colors[4],
                    ),
                left_arrow(colors[4], colors[8]),
                widget.KeyboardLayout(
                    configured_keyboards = ['us', 'es'],
                    foreground = colors[0],
                    background = colors[8],
                    fmt = '\uf11c  {}',
                    padding = 5,
                    decorations = [
                            BorderDecoration(
                                colour = colors[8],
                                border_width = [0, 0, 2, 0],
                                padding_x = 5,
                                padding_y = None,
                            )
                        ],
                    ),
                left_arrow(colors[8], colors[7]),
                widget.Volume(
                    foreground = colors[0],
                    background = colors[7],
                    fmt = '\uf028  {}',
                    padding = 5,
                    ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    Screen(
        wallpaper='~/Pictures/wallpapers/wallpaper-paisaje.png',
        top=bar.Bar(
            [
                widget.CurrentLayout(
                    background = colors[5],
                    foreground = colors[1],
                    ),
                right_arrow(colors[6], colors[5]),
                widget.GroupBox(
                    background = colors[6],
                    foreground = colors[1],
                    padding_x = 5,
                    padding_y = 5,
                    fontsize = 30,
                    highlight_method = "line",
                    this_current_screen_border = colors[7],
                    this_screen_border = colors[4],
                    other_current_screen_border = colors[7],
                    other_screen_border = colors[4],
                    ),
                right_arrow(colors[0], colors[6]),
                widget.Prompt(
                    ),
                widget.WindowName(
                    ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("&lt;Win-p&gt; to drun", foreground="#d75f5f"),
                left_arrow(colors[0], colors[4]),
                widget.Clock(
                    format="%I:%M%p \uf073 %a %d/%m/%y",
                    foreground = colors[0],
                    background = colors[4],
                    ),

            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
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
auto_minimize = False 

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"



