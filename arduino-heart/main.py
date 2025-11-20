import time
import sys
from arduino.app_utils import *
from arduino.app_bricks.keyword_spotting import KeywordSpotting

def on_keyword_detected():
    """Executes the expected action when the keyword is detected or simulated."""
    print("[debug] on_keyword_detected() called")
    try:
        Bridge.call("keyword_detected")
        print("[debug] Bridge.call succeeded")
    except Exception as e:
        print(f"[error] Bridge.call failed: {e}", file=sys.stderr)

def main():
    print("Sending 'keyword_detected' automatically every 10 seconds...")
    try:
        while True:
            print(f"[{time.strftime('%H:%M:%S')}] Trigger...")
            on_keyword_detected()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == '__main__':
    main()