from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher

###
# use this script to sniff for OSC messages if you're investigating stuff
# if using the same server as in the main app, unload it first:
# launchctl unload ~/Library/LaunchAgents/com.user.python.osc.totalmix.plist
###

# Use the same IP and PORT that TotalMix is sending TO
IP = "127.0.0.1"
PORT = 7002 

def print_handler(address, *args):
    print(f"Captured OSC -> Address: {address} | Data: {args}")

dispatcher = Dispatcher()
dispatcher.set_default_handler(print_handler)

server = BlockingOSCUDPServer((IP, PORT), dispatcher)
print(f"Listening for TotalMix messages on {PORT}...")
print("Go to TotalMix and click the 'Speaker B' button now.")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nStopping sniffer.")
