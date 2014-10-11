# ZSH Theme - Yuka version
# Thanks to gallifrey, upon whose theme this is based

local return_code="%(?..%{$fg_bold[red]%}%? ↵%{$reset_color%})"

function my_git_prompt_info() {
  ref=$(git tag 2> /dev/null) || return
  GIT_STATUS=$(git_prompt_status)
  [[ -n $GIT_STATUS ]] && GIT_STATUS=" $GIT_STATUS"
  BB=$(current_branch)
 echo "$ZSH_THEME_GIT_PROMPT_PREFIX${BB}$GIT_STATUS$ZSH_THEME_GIT_PROMPT_SUFFIX"
}

function jobs_running() {
  j_run=$(jobs | wc -l)
  [[ j_run -ne 0 ]] || return
 echo "%{$fg[yellow]%}(jobs: %B${j_run}%b%{$fg[yellow]%})%{$reset_color%}"
}

RPS2="%{$fg_bold[red]%}[%{$fg_bold[cyan]%}%*%{$fg_bold[red]%}]%{$reset_color%}"

#PROMPT='╭─%{$fg_bold[green]%}%n@%m%{$reset_color%} %{$fg_bold[blue]%}%~%{$reset_color%} $(#my_git_prompt_info)%{$reset_color%}$(jobs_running) $RPS2
#╰─%B»%b '

PROMPT='╭─%{$fg_bold[red]%}<%{$fg_bold[yellow]%}%n%{$fg_bold[red]%}@%{$reset_color%}%{$fg_bold[yellow]%}%m%{$reset_color%}:%{$fg_bold[blue]%}%~%{$reset_color%}%{$fg_bold[red]%}>%{$reset_color%} $(my_git_prompt_info)%{$reset_color%}$(jobs_running) $RPS2
╰─%B»%b '

RPS1="${return_code}"

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg[yellow]%}("
ZSH_THEME_GIT_PROMPT_SUFFIX=") %{$reset_color%}"
ZSH_THEME_GIT_PROMPT_UNTRACKED="%%"
ZSH_THEME_GIT_PROMPT_ADDED="+"
ZSH_THEME_GIT_PROMPT_MODIFIED="*"
ZSH_THEME_GIT_PROMPT_RENAMED="~"
ZSH_THEME_GIT_PROMPT_DELETED="!"
ZSH_THEME_GIT_PROMPT_UNMERGED="?"
