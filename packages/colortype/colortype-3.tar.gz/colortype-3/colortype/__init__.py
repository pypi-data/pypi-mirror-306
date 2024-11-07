class ANSIFore:
    # Define standard color codes
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    white = '\033[37m'

    # Define light color codes
    light_black = '\033[90m'
    light_red = '\033[91m'
    light_green = '\033[92m'
    light_yellow = '\033[93m'
    light_blue = '\033[94m'
    light_magenta = '\033[95m'
    light_cyan = '\033[96m'
    light_white = '\033[97m'
class ANSIBack:
    # Define background color codes
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    yellow = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    white = '\033[47m'

    # Define light background color codes
    light_black = '\033[100m'
    light_red = '\033[101m'
    light_green = '\033[102m'
    light_yellow = '\033[103m'
    light_blue = '\033[104m'
    light_magenta = '\033[105m'
    light_cyan = '\033[106m'
    light_white = '\033[107m'
class ANSIStyle:
    # Define the type of the text for bold, dim, and regular
    bold = '\033[1m'
    dim = '\033[2m'
    regular = '\033[22m'
    reset = '\033[0m'

def console(content):
    """Replace custom tags with ANSI color codes and print the result."""
    # Foreground colors
    content = content.replace('[red]', ANSIFore.red)
    content = content.replace('[light_red]', ANSIFore.light_red)
    content = content.replace('[green]', ANSIFore.green)
    content = content.replace('[light_green]', ANSIFore.light_green)
    content = content.replace('[blue]', ANSIFore.blue)
    content = content.replace('[light_blue]', ANSIFore.light_blue)
    content = content.replace('[purple]', ANSIFore.purple)
    content = content.replace('[light_magenta]', ANSIFore.light_magenta)
    content = content.replace('[yellow]', ANSIFore.yellow)
    content = content.replace('[light_yellow]', ANSIFore.light_yellow)
    content = content.replace('[white]', ANSIFore.white)
    content = content.replace('[light_white]', ANSIFore.light_white)
    content = content.replace('[cyan]', ANSIFore.light_cyan)
    content = content.replace('[black]', ANSIFore.black)
    content = content.replace('[light_black]', ANSIFore.light_black)
    
    # Background colors
    content = content.replace('[b_red]', ANSIBack.red)
    content = content.replace('[b_light_red]', ANSIBack.light_red)
    content = content.replace('[b_green]', ANSIBack.green)
    content = content.replace('[b_light_green]', ANSIBack.light_green)
    content = content.replace('[b_blue]', ANSIBack.blue)
    content = content.replace('[b_light_blue]', ANSIBack.light_blue)
    content = content.replace('[b_purple]', ANSIBack.purple)
    content = content.replace('[b_light_magenta]', ANSIBack.light_magenta)
    content = content.replace('[b_yellow]', ANSIBack.yellow)
    content = content.replace('[b_light_yellow]', ANSIBack.light_yellow)
    content = content.replace('[b_white]', ANSIBack.white)
    content = content.replace('[b_light_white]', ANSIBack.light_white)
    content = content.replace('[b_cyan]', ANSIBack.light_cyan)
    content = content.replace('[b_black]', ANSIBack.black)
    content = content.replace('[b_light_black]', ANSIBack.light_black)

    # Text styles
    content = content.replace('[bold]', ANSIStyle.bold)
    content = content.replace('[dim]', ANSIStyle.dim)
    content = content.replace('[regular]', ANSIStyle.regular)

    # Reset
    content = content.replace('[reset]', ANSIStyle.reset)
    print(content)

fore  =    ANSIFore()
back  =    ANSIBack()
style =    ANSIStyle()