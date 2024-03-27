count = 0

def prompt():
    global count
    _count = count
    count = count + 1
    return '{SLOWBLINK_PURPLE}str(_count) + ' $ {RESET}'

$PROMPT = prompt

$UPDATE_PROMPT_ON_KEYPRESS = True
$PROMPT_REFRESH_INTERVAL = 1



from xontrib import prompt_vi_mode
def prompt():
    return prompt_vi_mode.vi_mode() + ' $ '


$PROMPT = prompt

