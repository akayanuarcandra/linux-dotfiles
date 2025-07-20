#!/usr/bin/env bash

echo "Hyprland startup script running as $(whoami)..." >> /tmp/hypr_startup.log

sudo adguardvpn-cli connect -l SG
echo "Privileged command executed." >> /tmp/hypr_startup.log

