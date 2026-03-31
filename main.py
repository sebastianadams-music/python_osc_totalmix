import threading
from pynput import mouse, keyboard
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher

# --- Configuration ---
IP = "127.0.0.1"
IN_PORT = 7001  
OUT_PORT = 7002 
OSC_ADDR = "/1/mastervolume"
OSC_ADDR_SPK_B = "/1/mainSpeakerB"
STEP_SENSITIVITY = 0.005  
REF_LEVEL_20DB = 0.4      

client = SimpleUDPClient(IP, IN_PORT)
current_volume = 0.0
ctrl_pressed = False
s_key_pressed = False 

# --- OSC Server (Keeping Volume Sync Alive) ---
def volume_handler(address, *args):
    global current_volume
    if args:
        current_volume = float(args[0])

def speaker_handler(address, *args):
    if args:
        val = float(args[0])
        print(f"TotalMix Status -> Speaker B is {'ON' if val > 0.5 else 'OFF'}")

def start_server():
    dispatcher = Dispatcher()
    dispatcher.map(OSC_ADDR, volume_handler)
    dispatcher.map(OSC_ADDR_SPK_B, speaker_handler)
    server = BlockingOSCUDPServer((IP, OUT_PORT), dispatcher)
    server.serve_forever()

# --- Input Handlers ---
def on_scroll(x, y, dx, dy):
    global current_volume, ctrl_pressed
    if ctrl_pressed:
        current_volume += (dy * STEP_SENSITIVITY)
        current_volume = max(0.0, min(1.0, current_volume))
        client.send_message(OSC_ADDR, current_volume)

def on_click(x, y, button, pressed):
    global current_volume, ctrl_pressed
    if pressed and ctrl_pressed and button == mouse.Button.middle:
        current_volume = REF_LEVEL_20DB
        client.send_message(OSC_ADDR, current_volume)

def on_press(key):
    global ctrl_pressed, s_key_pressed
    
    if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_pressed = True

    try:
        # Detect 's' key
        if ctrl_pressed and hasattr(key, 'char') and key.char.lower() == 's':
            if not s_key_pressed:
                s_key_pressed = True
                
                # TotalMix should toggle the state internally.
                client.send_message(OSC_ADDR_SPK_B, 1.0)
                print("HOTKEY -> Sent Trigger (1.0)")
                
    except Exception:
        pass 

def on_release(key):
    global ctrl_pressed, s_key_pressed
    if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_pressed = False
    if hasattr(key, 'char') and key.char.lower() == 's':
        s_key_pressed = False

# --- Main ---
if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    m_listener = mouse.Listener(on_scroll=on_scroll, on_click=on_click)
    k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    m_listener.start()
    k_listener.start()
    
    print("--- Bridge Active (Trigger Mode) ---")
    m_listener.join()
    k_listener.join()