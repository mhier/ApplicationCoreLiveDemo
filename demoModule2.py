#!/usr/bin/python3

import PyApplicationCore as ac

class Automation(ac.ApplicationModule):
  def __init__(self, owner):
    super().__init__(owner, "Automation", "Just a simple example")

    self.trigger = ac.ScalarPushInput(ac.DataType.uint64, self, "/msTimer/tick", "", "Trigger")

    self.amplitudeIn = ac.ScalarPollInput(ac.DataType.float64, self, "amplitude", "V", "Amplitude")

    self.amplitudeOut = ac.ScalarOutput(ac.DataType.float64, self, "/DacTable/amplitude", "V", "Amplitude")

  def mainLoop(self):
    while True:
      # first read all push input(s), then all poll input(s)
      self.readAll()

      # maximum +- 0.1V per trigger
      delta = max(min(self.amplitudeIn - self.amplitudeOut, 0.1), -0.1)

      self.amplitudeOut.writeIfDifferent(self.amplitudeOut + delta)


ac.app.automation = Automation(ac.app)
