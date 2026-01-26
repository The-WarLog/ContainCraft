import pyfiglet 

def print_ascii_banner():
    #generate the ascii text
    ascii_banner=pyfiglet.figlet_format(text="ContainCraft",font="slant")
    return ascii_banner