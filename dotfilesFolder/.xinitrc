export DESKTOP_SESSION=plasma
export QT_QPA_PLATFORMTHEME="qt5ct"
nitrogen --restore
while :; do
	pgrep picom || picom -b
	pgrep nm-applet || nm-applet &
	pgrep slstatus || slstatus &
	dwm
done
