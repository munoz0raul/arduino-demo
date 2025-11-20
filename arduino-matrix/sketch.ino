// SPDX-FileCopyrightText: Copyright (C) 2025 ARDUINO SA <http://www.arduino.cc>
//
// SPDX-License-Identifier: MPL-2.0

#include <Arduino_RouterBridge.h>
#include "frames.h"

// TODO: those will go into an header file.
extern "C" void matrixWrite(const uint32_t* buf);
extern "C" void matrixBegin();

bool animating = false;
bool animatingMic = false;
const uint8_t* SigAnim[] = { Sig1, Sig2, Sig3, Sig4, Sig5, Sig6, Sig7, Sig8, Sig9, Sig10 };
const uint8_t* MicAnim[] = { Mic1, Mic2, Mic3, Mic4 };

void setup() {
  matrixBegin();
  convertAndDisplay(LittleHeart, 2000);
  Bridge.begin();
  Bridge.provide("LittleHeart", play_LittleHeart);
  Bridge.provide("Heart1", play_Heart1);
  Bridge.provide("Heart2", play_Heart2);
  Bridge.provide("Heart3", play_Heart3);
  Bridge.provide("Heart4", play_Heart4);
  Bridge.provide("Heart5", play_Heart5);
  Bridge.provide("Heart6", play_Heart6);
  Bridge.provide("Heart7", play_Heart7);
  Bridge.provide("Heart8", play_Heart8);
  Bridge.provide("FoundriesLogo", play_FoundriesLogo);
  Bridge.provide("ArduinoLogo", play_ArduinoLogo);
  Bridge.provide("Mic1", play_Mic1);
  Bridge.provide("Mic2", play_Mic2);
  Bridge.provide("Mic3", play_Mic3);
  Bridge.provide("Mic4", play_Mic4);
  Bridge.provide("Sig1", play_Sig1);
  Bridge.provide("Sig2", play_Sig2);
  Bridge.provide("Sig3", play_Sig3);
  Bridge.provide("Sig4", play_Sig4);
  Bridge.provide("Sig5", play_Sig5);
  Bridge.provide("Sig6", play_Sig6);
  Bridge.provide("Sig7", play_Sig7);
  Bridge.provide("Sig8", play_Sig8);
  Bridge.provide("Sig9", play_Sig9);
  Bridge.provide("Sig10", play_Sig10);
  Bridge.provide("Zero", play_Zero);
  Bridge.provide("StartAnimation", start_animation);
  Bridge.provide("StopAnimation", stop_animation);
  Bridge.provide("StartMicAnimation", start_mic_animation);
  Bridge.provide("StopMicAnimation", stop_mic_animation);
}

void loop() {
  if (animating) {
    playAnimation(SigAnim, 10, 1, 200);
  } else if (animatingMic) {
    playAnimation(MicAnim, 4, 1, 200);
  } else {
    delay(100);  // Pequeno delay para não consumir CPU desnecessariamente
  }
}

void playAnimation(const uint8_t* frames[], int frameCount, int repeat, int frameDelay) {
  for (int r = 0; r < repeat; r++) {
    for (int i = 0; i < frameCount; i++) {
      if (!animating && !animatingMic) return;  // Para a animação se os flags mudarem
      convertAndDisplay(frames[i], frameDelay);
    }
  }
}

void convertAndDisplay(const uint8_t* matrix, int delayMs) {
  // Converte uint8_t[104] para uint32_t[4] (formato LSB-first)
  uint32_t buffer[4] = {0, 0, 0, 0};
  
  for (int i = 0; i < 104; i++) {
    if (matrix[i]) {
      int uint32_index = i / 32;        // Qual uint32_t (0-3)
      int bit_position = i % 32;        // Posição do bit (0-31)
      buffer[uint32_index] |= (1UL << bit_position);
    }
  }
  
  matrixWrite(buffer);
  delay(delayMs);
}

void play_LittleHeart() {
  convertAndDisplay(LittleHeart, 2000);
}

void play_Heart1() {
  convertAndDisplay(Heart1, 2000);
}

void play_Heart2() {
  convertAndDisplay(Heart2, 2000);
}

void play_Heart3() {
  convertAndDisplay(Heart3, 2000);
}

void play_Heart4() {
  convertAndDisplay(Heart4, 2000);
}

void play_Heart5() {
  convertAndDisplay(Heart5, 2000);
}

void play_Heart6() {
  convertAndDisplay(Heart6, 2000);
}

void play_Heart7() {
  convertAndDisplay(Heart7, 2000);
}

void play_Heart8() {
  convertAndDisplay(Heart8, 2000);
}

void play_FoundriesLogo() {
  convertAndDisplay(FoundriesLogo, 2000);
}

void play_ArduinoLogo() {
  convertAndDisplay(ArduinoLogo, 2000);
}

void play_Mic1() {
  convertAndDisplay(Mic1, 2000);
}

void play_Mic2() {
  convertAndDisplay(Mic2, 2000);
}

void play_Mic3() {
  convertAndDisplay(Mic3, 2000);
}

void play_Mic4() {
  convertAndDisplay(Mic4, 2000);
}

void play_Sig1() {
  convertAndDisplay(Sig1, 2000);
}

void play_Sig2() {
  convertAndDisplay(Sig2, 2000);
}

void play_Sig3() {
  convertAndDisplay(Sig3, 2000);
}

void play_Sig4() {
  convertAndDisplay(Sig4, 2000);
}

void play_Sig5() {
  convertAndDisplay(Sig5, 2000);
}

void play_Sig6() {
  convertAndDisplay(Sig6, 2000);
}

void play_Sig7() {
  convertAndDisplay(Sig7, 2000);
}

void play_Sig8() {
  convertAndDisplay(Sig8, 2000);
}

void play_Sig9() {
  convertAndDisplay(Sig9, 2000);
}

void play_Sig10() {
  convertAndDisplay(Sig10, 2000);
}

void play_Zero() {
  convertAndDisplay(Zero, 2000);
}

void start_animation() {
  animating = true;
}

void stop_animation() {
  animating = false;
  convertAndDisplay(Zero, 100);  // Limpa o display ao parar
}

void start_mic_animation() {
  animatingMic = true;
}

void stop_mic_animation() {
  animatingMic = false;
  convertAndDisplay(Zero, 100);  // Limpa o display ao parar
}

