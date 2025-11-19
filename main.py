import time
import sys
from arduino.app_utils import *
from arduino.app_bricks.keyword_spotting import KeywordSpotting

def on_keyword_detected():
    """Executa a ação esperada quando a 'palavra' é detectada ou simulada."""
    print("[debug] on_keyword_detected() called")
    try:
        Bridge.call("keyword_detected")
        print("[debug] Bridge.call succeeded")
    except Exception as e:
        print(f"[error] Bridge.call failed: {e}", file=sys.stderr)

def main():
    print("Enviando 'keyword_detected' automaticamente a cada 10 segundos...")
    try:
        while True:
            print(f"[{time.strftime('%H:%M:%S')}] Trigger...")
            on_keyword_detected()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Encerrando...")

if __name__ == '__main__':
    main()

