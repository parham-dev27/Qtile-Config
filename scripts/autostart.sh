#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

(conky -c $HOME/.config/qtile/scripts/EditedConky.conkyrc) &
run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &
numlockx on &
picom --config $HOME/.config/qtile/scripts/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
nitrogen --restore &
run /usr/lib/kdeconnectd &
run clipmenud &
xidlehook --not-when-audio --not-when-fullscreen --timer 600 'systemctl suspend' '' &
run dunst -conf $HOME/.config/qtile/scripts/dunstrc &
