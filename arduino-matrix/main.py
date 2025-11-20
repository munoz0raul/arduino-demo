import sys
from arduino.app_utils import *
from arduino.app_bricks.keyword_spotting import KeywordSpotting

def main():
    print("=" * 60)
    print("Controle do Display LED - Arduino UNO Q")
    print("=" * 60)
    print("\n📋 MENU DE OPÇÕES:")
    print("\n🫀 Hearts:")
    print("  0 - LittleHeart    1 - Heart1    2 - Heart2    3 - Heart3")
    print("  4 - Heart4         5 - Heart5    6 - Heart6    7 - Heart7")
    print("  8 - Heart8")
    print("\n🎤 Microfones (Mic):")
    print("  m1 - Mic1    m2 - Mic2    m3 - Mic3    m4 - Mic4")
    print("\n📡 Sinais (Sig):")
    print("  s1 - Sig1    s2 - Sig2    s3 - Sig3    s4 - Sig4    s5 - Sig5")
    print("  s6 - Sig6    s7 - Sig7    s8 - Sig8    s9 - Sig9    s10 - Sig10")
    print("\n🎨 Logos:")
    print("  f - FoundriesLogo    a - ArduinoLogo")
    print("\n🎬 Animação:")
    print("  i - Iniciar animação Sig1-10    s - Parar animação")
    print("  mi - Iniciar animação Mic1-4    ms - Parar animação Mic")
    print("\n⚙️  Utilidades:")
    print("  z - Zero (limpar display)    q - Sair")
    print("\n" + "=" * 60)
    print()
    
    try:
        while True:
            key = input("Digite sua escolha: ").strip().lower()
            
            if key == 'q':
                print("Encerrando...")
                break
            elif key == '0':
                print("📤 Enviando LittleHeart...")
                Bridge.call("LittleHeart")
            elif key == '1':
                print("📤 Enviando Heart1...")
                Bridge.call("Heart1")
            elif key == '2':
                print("📤 Enviando Heart2...")
                Bridge.call("Heart2")
            elif key == '3':
                print("📤 Enviando Heart3...")
                Bridge.call("Heart3")
            elif key == '4':
                print("📤 Enviando Heart4...")
                Bridge.call("Heart4")
            elif key == '5':
                print("📤 Enviando Heart5...")
                Bridge.call("Heart5")
            elif key == '6':
                print("📤 Enviando Heart6...")
                Bridge.call("Heart6")
            elif key == '7':
                print("📤 Enviando Heart7...")
                Bridge.call("Heart7")
            elif key == '8':
                print("📤 Enviando Heart8...")
                Bridge.call("Heart8")
            elif key == 'm1':
                print("📤 Enviando Mic1...")
                Bridge.call("Mic1")
            elif key == 'm2':
                print("📤 Enviando Mic2...")
                Bridge.call("Mic2")
            elif key == 'm3':
                print("📤 Enviando Mic3...")
                Bridge.call("Mic3")
            elif key == 'm4':
                print("📤 Enviando Mic4...")
                Bridge.call("Mic4")
            elif key == 's1':
                print("📤 Enviando Sig1...")
                Bridge.call("Sig1")
            elif key == 's2':
                print("📤 Enviando Sig2...")
                Bridge.call("Sig2")
            elif key == 's3':
                print("📤 Enviando Sig3...")
                Bridge.call("Sig3")
            elif key == 's4':
                print("📤 Enviando Sig4...")
                Bridge.call("Sig4")
            elif key == 's5':
                print("📤 Enviando Sig5...")
                Bridge.call("Sig5")
            elif key == 's6':
                print("📤 Enviando Sig6...")
                Bridge.call("Sig6")
            elif key == 's7':
                print("📤 Enviando Sig7...")
                Bridge.call("Sig7")
            elif key == 's8':
                print("📤 Enviando Sig8...")
                Bridge.call("Sig8")
            elif key == 's9':
                print("📤 Enviando Sig9...")
                Bridge.call("Sig9")
            elif key == 's10':
                print("📤 Enviando Sig10...")
                Bridge.call("Sig10")
            elif key == 'f':
                print("📤 Enviando FoundriesLogo...")
                Bridge.call("FoundriesLogo")
            elif key == 'a':
                print("📤 Enviando ArduinoLogo...")
                Bridge.call("ArduinoLogo")
            elif key == 'z':
                print("📤 Limpando display (Zero)...")
                Bridge.call("Zero")
            elif key == 'i':
                print("🎬 Iniciando animação Sig1-10...")
                Bridge.call("StartAnimation")
            elif key == 's':
                print("⏹️  Parando animação...")
                Bridge.call("StopAnimation")
            elif key == 'mi':
                print("🎬 Iniciando animação Mic1-4...")
                Bridge.call("StartMicAnimation")
            elif key == 'ms':
                print("⏹️  Parando animação Mic...")
                Bridge.call("StopMicAnimation")
            else:
                print("❌ Opção inválida! Consulte o menu acima.")
                
    except KeyboardInterrupt:
        print("\nEncerrando...")
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
