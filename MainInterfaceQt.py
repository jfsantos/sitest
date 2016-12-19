from PySide import QtGui, QtCore
from PySide.phonon import Phonon
from TestController import TestController

class MainInterfaceQt(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Speech Intelligibility Test')
        self.resize(800,100)
        self.media = Phonon.MediaObject(self)
        self.audio = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.media, self.audio)
        self.buttonStart = QtGui.QPushButton('Start', self)
        self.slider = Phonon.VolumeSlider(self)
        self.slider.setAudioOutput(self.audio)
        self.entry = QtGui.QLineEdit()
        self.entry.setEnabled(False)
        entryFont = QtGui.QFont("Times", 18)
        self.entry.setFont(entryFont)
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.entry, 0, 0, 1, 2)
        layout.addWidget(self.buttonStart, 1, 1)
        layout.addWidget(self.slider, 1, 0)
        layout.setRowStretch(0, 1)
        self.media.stateChanged.connect(self.handleStateChanged)
        self.media.finished.connect(self.handleSampleFinished)
        self.buttonStart.clicked.connect(self.handleButtonStart)
        self.entry.returnPressed.connect(self.handleSaveEntry)

    def getParticipantID(self):
        pid, ok = QtGui.QInputDialog.getInt(self, "Setup", "Participant ID", minValue=0)
        if ok:
            self.ctrl = TestController(participant_id = pid)
        return ok

    def updateAndPlayNext(self):
        try:
            path, n = self.ctrl.next_sample()
            self.media.setCurrentSource(Phonon.MediaSource(path))
            self.setWindowTitle('Sample %s' % n)
            if not self.ctrl.is_training_sample():
                self.slider.setEnabled(False)
            self.media.play()
        except IndexError:
            self.entry.setText("This was the last sample.")
            self.entry.setEnabled(False)
            self.buttonStart.setEnabled(False)

    def handleButtonStart(self):
        self.updateAndPlayNext()
        self.buttonStart.setText("Next")
        self.buttonStart.clicked.disconnect(self.handleButtonStart)
        self.buttonStart.clicked.connect(self.handleSaveEntry)

    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.entry.setText('')
            self.entry.setEnabled(False)
            self.buttonStart.setEnabled(False)
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print ('ERROR: could not play: %s' % source)
                print ('  %s' % self.media.errorString())

    def handleSampleFinished(self):
        self.entry.setEnabled(True)
        self.buttonStart.setEnabled(True)
        self.entry.setFocus()

    def handleSaveEntry(self):
        self.ctrl.save_result(self.entry.text())
        self.updateAndPlayNext()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Speech Intelligibility Test')
    window = MainInterfaceQt()
    ok = window.getParticipantID()
    if ok:
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(-1)
