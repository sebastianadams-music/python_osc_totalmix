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
STEP_SENSITIVITY = 0.005  # Adjust this for your Mac mouse speed
REF_LEVEL_20DB = 0.4      # Default value to return to on CTRL + click; adjust if needed

client = SimpleUDPClient(IP, IN_PORT)
current_volume = 0.0
ctrl_pressed = False

# --- OSC Server Functions ---
def volume_handler(address, *args):
    global current_volume
    if args:
        current_volume = args[0]

def start_server():
    dispatcher = Dispatcher()
    dispatcher.map(OSC_ADDR, volume_handler)
    server = BlockingOSCUDPServer((IP, OUT_PORT), dispatcher)
    server.serve_forever()

# --- Input Handlers ---
def on_scroll(x, y, dx, dy):
    global current_volume
    if ctrl_pressed:
        current_volume += (dy * STEP_SENSITIVITY)
        current_volume = max(0.0, min(1.0, current_volume))
        client.send_message(OSC_ADDR, current_volume)
        print(f"Master Volume: {int(current_volume * 100)}% (Val: {current_volume:.3f})")

def on_click(x, y, button, pressed):
    global current_volume
    # Button.middle is the scroll wheel click
    if pressed and ctrl_pressed and button == mouse.Button.middle:
        current_volume = REF_LEVEL_20DB
        client.send_message(OSC_ADDR, current_volume)
        print(f"Reset to -20dB ({REF_LEVEL_20DB})")

def on_press(key):
    global ctrl_pressed
    if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_pressed = True

def on_release(key):
    global ctrl_pressed
    if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_pressed = False

# --- Main ---
if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Added on_click to the mouse listener
    m_listener = mouse.Listener(on_scroll=on_scroll, on_click=on_click)
    k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    m_listener.start()
    k_listener.start()
    
    print("TotalMix OSC Bridge Active. Ctrl+Scroll = Vol, Ctrl+MiddleClick = -20dB")
    m_listener.join()
    k_listener.join()
