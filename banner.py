import pyfiglet
from termcolor import colored

def show_banner():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Create ASCII art text
    banner_text = pyfiglet.figlet_format("GHOST FLOOD", font="slant")
    
    # Print banner with colors
    print(colored(banner_text, 'green', attrs=['bold']))
    print(colored("╔══════════════════════════════════════════════════════════════╗", 'green', attrs=['bold']))
    print(colored("║                  [EDUCATIONAL PURPOSE ONLY]                 ║", 'green', attrs=['bold']))
    print(colored("╠══════════════════════════════════════════════════════════════╣", 'green', attrs=['bold']))
    print(colored("║  WARNING: Use only on websites you OWN or have permission   ║", 'yellow', attrs=['bold']))
    print(colored("║  Unauthorized use is illegal and punishable by law.        ║", 'red', attrs=['bold']))
    print(colored("╚══════════════════════════════════════════════════════════════╝", 'green', attrs=['bold']))
    print(colored("\n[+] Tool Loaded Successfully", 'cyan', attrs=['bold']))
    print(colored("[+] Enter Target IP to Start Testing", 'cyan', attrs=['bold']))
    print(colored("[+] Press Ctrl+C to Stop Attack\n", 'cyan', attrs=['bold']))
