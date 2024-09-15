fish_add_path /home/storage/julia/bin
fish_add_path -aP /home/storage/miniconda3/bin
fish_add_path /home/storage/texlive/2024/bin/x86_64-linux/
export JULIA_DEPOT_PATH="/home/storage/.julia"

if status is-interactive
    # Commands to run in interactive sessions can go here
end

if status --is-login
	if test -z "$DISPLAY" -a "$XDG_VTNR" = 1
		exec startx -- -keeptty
	end
end

set fish_greeting
