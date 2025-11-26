#!/usr/bin/python3

import math
import numpy as np
import PyApplicationCore as ac

class DacTable(ac.ApplicationModule):
  def __init__(self, owner):
    super().__init__(owner, "DacTable", "DAC table generation")
    self.fs = 100  # 100 kHz sampling frequency

    self.amplitude = ac.ScalarPushInput(ac.DataType.float64, self, "amplitude", "V", "Amplitude")
    self.phase = ac.ScalarPushInput(ac.DataType.float64, self, "phase", "deg", "Phase")
    self.delay = ac.ScalarPushInput(ac.DataType.float64, self, "delay", "ms", "Pulse start delay")
    self.length = ac.ScalarPushInput(ac.DataType.float64, self, "pulseLength", "ms", "Pulse length")

    self.I = ac.ArrayOutput(ac.DataType.int32, self, "I", "bits", 1024, "Table with I component")
    self.Q = ac.ArrayOutput(ac.DataType.int32, self, "Q", "bits", 1024, "Table with Q component")

  def mainLoop(self):
    rag = self.readAnyGroup()
    while True:
      # Initial values are there at start of mainLoop, so compute and write first, then wait for changes

      # erase output arrays
      self.I.set(np.zeros(dtype=np.float64, shape=(1024)))
      self.Q.set(np.zeros(dtype=np.float64, shape=(1024)))

      print(f'I = {self.amplitude * math.cos(self.phase * math.pi / 180)}')

      # compute pulse
      nDelay = int(self.delay * self.fs)
      nLength = int(self.length * self.fs)
      self.I[nDelay:nDelay+nLength] = self.amplitude * \
          math.cos(self.phase * math.pi / 180)
      self.Q[nDelay:nDelay+nLength] = self.amplitude * \
          math.sin(self.phase * math.pi / 180)

      # write outputs
      self.writeAll()
      # or: self.I.write() and self.Q.write()

      # Blocks until any of the push inputs is written to
      rag.readAny()


ac.app.dacTable = DacTable(ac.app)
