source ~/.aliases 
source /usr/share/git/completion/git-prompt.sh
source ~/.ps1_prompt
source ~/.envvars

shopt -s autocd
shopt -s dirspell
shopt -s direxpand
shopt -s histappend
shopt -s histverify

eval "`dircolors -b ~/.dircolors`"

export PATH=$PATH:~/storage/miniconda3/bin:~/storage/bin/
