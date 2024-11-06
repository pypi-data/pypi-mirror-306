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

# Define background color codes
b_black = '\033[40m'
b_red = '\033[41m'
b_green = '\033[42m'
b_yellow = '\033[43m'
b_blue = '\033[44m'
b_purple = '\033[45m'
b_white = '\033[47m'

# Define light background color codes
b_light_black = '\033[100m'
b_light_red = '\033[101m'
b_light_green = '\033[102m'
b_light_yellow = '\033[103m'
b_light_blue = '\033[104m'
b_light_magenta = '\033[105m'
b_light_cyan = '\033[106m'
b_light_white = '\033[107m'

# Define the type of the text for bold, dim, and regular
bold = '\033[1m'
dim = '\033[2m'
regular = '\033[22m'

# Reset code to default color
reset = '\033[0m'

def console(content):
    """Replace custom tags with ANSI color codes and print the result."""
    # Foreground colors
    content = content.replace('[red]', red)
    content = content.replace('[light_red]', light_red)
    content = content.replace('[green]', green)
    content = content.replace('[light_green]', light_green)
    content = content.replace('[blue]', blue)
    content = content.replace('[light_blue]', light_blue)
    content = content.replace('[purple]', purple)
    content = content.replace('[light_magenta]', light_magenta)
    content = content.replace('[yellow]', yellow)
    content = content.replace('[light_yellow]', light_yellow)
    content = content.replace('[white]', white)
    content = content.replace('[light_white]', light_white)
    content = content.replace('[cyan]', light_cyan)
    content = content.replace('[black]', black)
    content = content.replace('[light_black]', light_black)
    
    # Background colors
    content = content.replace('[b_red]', b_red)
    content = content.replace('[b_light_red]', b_light_red)
    content = content.replace('[b_green]', b_green)
    content = content.replace('[b_light_green]', b_light_green)
    content = content.replace('[b_blue]', b_blue)
    content = content.replace('[b_light_blue]', b_light_blue)
    content = content.replace('[b_purple]', b_purple)
    content = content.replace('[b_light_magenta]', b_light_magenta)
    content = content.replace('[b_yellow]', b_yellow)
    content = content.replace('[b_light_yellow]', b_light_yellow)
    content = content.replace('[b_white]', b_white)
    content = content.replace('[b_light_white]', b_light_white)
    content = content.replace('[b_cyan]', b_light_cyan)
    content = content.replace('[b_black]', b_black)
    content = content.replace('[b_light_black]', b_light_black)

    # Text styles
    content = content.replace('[bold]', bold)
    content = content.replace('[dim]', dim)
    content = content.replace('[regular]', regular)

    # Reset
    content = content.replace('[reset]', reset)
    print(content)  

if __name__ == '__main__':
    # Test with both foreground and background colors
    console('[red]Red foreground text![reset]')
    console('[b_light_blue][black]Black text on light blue background![reset]')
    console('[bold][b_yellow]Bold text on yellow background![reset]')
    console('[dim][b_light_magenta]Dim text on light magenta background![reset]')