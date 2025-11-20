import sys
from arduino.app_utils import *

def main():
    print("=" * 60)
    print("LED Control - Arduino UNO R4")
    print("=" * 60)
    print("\n💡 LED TOGGLE:")
    print("\n🔴 LED3 (RGB):")
    print("  r - Toggle LED3_R (Red)")
    print("  g - Toggle LED3_G (Green)")
    print("  b - Toggle LED3_B (Blue)")
    print("\n🔵 LED4 (RGB):")
    print("  R - Toggle LED4_R (Red)")
    print("  G - Toggle LED4_G (Green)")
    print("  B - Toggle LED4_B (Blue)")
    print("\n✨ LED BLINK (1s ON, 1s OFF):")
    print("\n🔴 LED3 Blink:")
    print("  ir - Start blink LED3_R    sr - Stop blink LED3_R")
    print("  ig - Start blink LED3_G    sg - Stop blink LED3_G")
    print("  ib - Start blink LED3_B    sb - Stop blink LED3_B")
    print("\n🔵 LED4 Blink:")
    print("  iR - Start blink LED4_R    sR - Stop blink LED4_R")
    print("  iG - Start blink LED4_G    sG - Stop blink LED4_G")
    print("  iB - Start blink LED4_B    sB - Stop blink LED4_B")
    print("\n⚙️  Utilities:")
    print("  q - Quit")
    print("\n" + "=" * 60)
    print()
    
    # Track LED states
    led_states = {
        'led3_r': False,
        'led3_g': False,
        'led3_b': False,
        'led4_r': False,
        'led4_g': False,
        'led4_b': False,
    }
    
    try:
        while True:
            key = input("Choose LED to toggle (or 'q' to quit): ").strip()
            
            if key == 'q':
                print("Exiting...")
                break
            elif key == 'r':
                Bridge.call("toggle_led3_r")
                led_states['led3_r'] = not led_states['led3_r']
                status = "ON" if led_states['led3_r'] else "OFF"
                print(f"🔴 LED3_R is now {status}")
            elif key == 'g':
                Bridge.call("toggle_led3_g")
                led_states['led3_g'] = not led_states['led3_g']
                status = "ON" if led_states['led3_g'] else "OFF"
                print(f"🟢 LED3_G is now {status}")
            elif key == 'b':
                Bridge.call("toggle_led3_b")
                led_states['led3_b'] = not led_states['led3_b']
                status = "ON" if led_states['led3_b'] else "OFF"
                print(f"🔵 LED3_B is now {status}")
            elif key == 'R':
                Bridge.call("toggle_led4_r")
                led_states['led4_r'] = not led_states['led4_r']
                status = "ON" if led_states['led4_r'] else "OFF"
                print(f"🔴 LED4_R is now {status}")
            elif key == 'G':
                Bridge.call("toggle_led4_g")
                led_states['led4_g'] = not led_states['led4_g']
                status = "ON" if led_states['led4_g'] else "OFF"
                print(f"🟢 LED4_G is now {status}")
            elif key == 'B':
                Bridge.call("toggle_led4_b")
                led_states['led4_b'] = not led_states['led4_b']
                status = "ON" if led_states['led4_b'] else "OFF"
                print(f"🔵 LED4_B is now {status}")
            
            # Blink commands - LED3
            elif key == 'ir':
                Bridge.call("start_blink_led3_r")
                print("✨ LED3_R blink started")
            elif key == 'sr':
                Bridge.call("stop_blink_led3_r")
                print("⏹️  LED3_R blink stopped")
            elif key == 'ig':
                Bridge.call("start_blink_led3_g")
                print("✨ LED3_G blink started")
            elif key == 'sg':
                Bridge.call("stop_blink_led3_g")
                print("⏹️  LED3_G blink stopped")
            elif key == 'ib':
                Bridge.call("start_blink_led3_b")
                print("✨ LED3_B blink started")
            elif key == 'sb':
                Bridge.call("stop_blink_led3_b")
                print("⏹️  LED3_B blink stopped")
            
            # Blink commands - LED4
            elif key == 'iR':
                Bridge.call("start_blink_led4_r")
                print("✨ LED4_R blink started")
            elif key == 'sR':
                Bridge.call("stop_blink_led4_r")
                print("⏹️  LED4_R blink stopped")
            elif key == 'iG':
                Bridge.call("start_blink_led4_g")
                print("✨ LED4_G blink started")
            elif key == 'sG':
                Bridge.call("stop_blink_led4_g")
                print("⏹️  LED4_G blink stopped")
            elif key == 'iB':
                Bridge.call("start_blink_led4_b")
                print("✨ LED4_B blink started")
            elif key == 'sB':
                Bridge.call("stop_blink_led4_b")
                print("⏹️  LED4_B blink stopped")
            
            else:
                print("❌ Invalid option! Check the menu above.")
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)

if __name__ == '__main__':
    main()


