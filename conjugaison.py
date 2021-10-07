#! encoding = utf-8

""" Practice French conjugaison """

import sys
from PyQt5 import QtWidgets, QtCore
from random import choice, randint
from time import sleep
from dictionary import VERB_DICT, TENSES, MOODS, PERSONS, conjug

VERBS = tuple(VERB_DICT.keys())


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Practice French Conjugaison')
        self.setStyleSheet('font-size: 12pt')
        self.setMinimumWidth(600)
        self.setMinimumHeight(650)
        self.resize(QtCore.QSize(800, 650))

        centerWidget = QtWidgets.QWidget()
        box1 = Box1(parent=self)
        box2 = Box2(parent=self)
        box3 = Box3(parent=self)
        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.setAlignment(QtCore.Qt.AlignHCenter)
        thisLayout.setSpacing(10)
        thisLayout.addWidget(box1)
        thisLayout.addWidget(box2)
        thisLayout.addWidget(box3)
        centerWidget.setLayout(thisLayout)

        # set central widget
        self.setCentralWidget(centerWidget)


class Box1(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Conjugate')
        self.lblVerb = QtWidgets.QLabel()
        self.lblVerb.setStyleSheet('font-size: 14pt; color: #2c39cf; font: bold; ')
        self.lblTense = QtWidgets.QLabel()
        self.lblTense.setFixedWidth(120)
        self.lblMood = QtWidgets.QLabel()
        self.lblMood.setFixedWidth(80)
        self.lblPerson = QtWidgets.QLabel()
        self.editInput = QtWidgets.QLineEdit()
        self.btnGen = QtWidgets.QPushButton('Generate (Ctrl+D)')
        self.btnGen.setFixedWidth(175)
        self.btnGen.setShortcut('Ctrl+D')
        self.btnCheck = QtWidgets.QPushButton('Check')
        self.btnCheck.setFixedWidth(175)
        self.lblCk = QtWidgets.QLabel()
        self.lblCk.setFixedWidth(30)
        self._answer = ''

        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(self.lblTense)
        row2.addWidget(self.lblMood)
        row2.addWidget(self.lblPerson)
        row2.addWidget(self.editInput)
        row2.addWidget(self.lblCk)

        row3 = QtWidgets.QHBoxLayout()
        row3.addWidget(self.btnGen)
        row3.addWidget(self.btnCheck)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.setSpacing(10)
        thisLayout.setAlignment(QtCore.Qt.AlignHCenter)
        thisLayout.addWidget(self.lblVerb)
        thisLayout.addLayout(row2)
        thisLayout.addLayout(row3)
        self.setLayout(thisLayout)

        self.btnGen.clicked.connect(self._gen)
        self.btnCheck.clicked.connect(self._ck)
        self.editInput.editingFinished.connect(self._ck)

    def _gen(self):
        """ Generate a verb & a conjugaison """
        # clear previous result
        self.lblCk.clear()
        self.editInput.clear()

        # randomly select a verb,
        verb = choice(VERBS)
        self.lblVerb.setText(verb)
        while True:
            # randomly select tense and mood
            tense = choice(TENSES)
            mood = choice(MOODS)
            # randomly select a person
            idx = randint(0, 5)
            try:
                answer = conjug(verb, tense, mood, idx)
                if answer:
                    pers = PERSONS[idx]
                    self.lblPerson.setText(pers)
                    self.editInput.setText(pers)
                    self.lblTense.setText(tense)
                    self.lblMood.setText(mood)
                    self._answer = answer
                    break
            except (KeyError, TypeError):
                # make another draw
                pass

    def _ck(self):
        """ Check the answer """
        txt = self.editInput.text()
        # remove extra spaces and only put 1
        txt_striped = ' '.join(txt.split())
        if txt_striped == self._answer:
            self.lblCk.setText('✓')
            self.lblCk.setStyleSheet('font-size: 14pt; font: bold; color: #009933')
        else:
            self.lblCk.setText('🞪')
            self.lblCk.setStyleSheet('font-size: 14pt; font: bold; color: #D63333')


class Box2(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Guess infinitive')

        self.btnGen = QtWidgets.QPushButton('Generate (Ctrl+F)')
        self.btnGen.setFixedWidth(175)
        self.btnGen.setShortcut('Ctrl+F')
        self.btnCheck = QtWidgets.QPushButton('Check')
        self.btnCheck.setFixedWidth(175)

        self.editVerb = QtWidgets.QLineEdit()
        self.comboTense = QtWidgets.QComboBox()
        self.comboMood = QtWidgets.QComboBox()
        self.lblCk = QtWidgets.QLabel()
        self.lblCk.setFixedWidth(30)
        self.lblConjug = QtWidgets.QLabel()
        self.lblConjug.setStyleSheet('font-size: 14pt; color: #2c39cf; font: bold; ')
        self.comboTense.addItems(TENSES)
        self.comboMood.addItems(MOODS)

        self.btnGen.clicked.connect(self._gen)
        self.btnCheck.clicked.connect(self._ck)
        self.editVerb.editingFinished.connect(self._ck)
        self.comboTense.currentIndexChanged.connect(self._ck)
        self.comboMood.currentIndexChanged.connect(self._ck)

        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(QtWidgets.QLabel('Infinitive: '))
        row2.addWidget(self.editVerb)
        row2.addWidget(self.comboTense)
        row2.addWidget(self.comboMood)
        row2.addWidget(self.lblCk)

        row3 = QtWidgets.QHBoxLayout()
        row3.addWidget(self.btnGen)
        row3.addWidget(self.btnCheck)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.setAlignment(QtCore.Qt.AlignHCenter)
        thisLayout.setSpacing(10)
        thisLayout.addWidget(self.lblConjug)
        thisLayout.addLayout(row2)
        thisLayout.addLayout(row3)
        self.setLayout(thisLayout)

        self._answer = ''
        self._tense = ''
        self._mood = ''

    def _gen(self):
        """ Generate a conjugaison """
        # clear previous result
        self.lblCk.clear()
        self.editVerb.clear()

        # randomly select a verb
        verb = choice(VERBS)
        self._answer = verb
        # randomly select a person and form the conjugaison
        while True:
            self._tense = choice(TENSES)
            self._mood = choice(MOODS)
            idx = randint(0, 5)
            try:
                answer = conjug(verb, self._tense, self._mood, idx)
                if answer:
                    self.lblConjug.setText(answer)
                    break
            except (KeyError, TypeError):
                pass

    def _ck(self):
        """ Check the answer """
        if self.editVerb.text().lower() == self._answer and \
                self.comboTense.currentText() == self._tense and \
                self.comboMood.currentText() == self._mood:
            self.lblCk.setText('✓')
            self.lblCk.setStyleSheet('font-size: 14pt; color: #009933')
        else:
            self.lblCk.setText('🞪')
            self.lblCk.setStyleSheet('font-size: 14pt; color: #D63333')


class Box3(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Look up')

        self.editVerb = QtWidgets.QLineEdit()
        self.comboTense = QtWidgets.QComboBox()
        self.comboMood = QtWidgets.QComboBox()
        self.comboTense.addItems(TENSES)
        self.comboMood.addItems(MOODS)
        self.btnClear = QtWidgets.QPushButton('Clear')
        self.lblResult = QtWidgets.QTextEdit()
        self.lblResult.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.lblResult.setReadOnly(True)
        self.btnClear.clicked.connect(self._clear)
        self.editVerb.editingFinished.connect(self._search)
        self.comboMood.currentIndexChanged.connect(self._search)
        self.comboTense.currentIndexChanged.connect(self._search)

        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self.editVerb)
        row1.addWidget(self.comboTense)
        row1.addWidget(self.comboMood)
        row1.addWidget(self.btnClear)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addLayout(row1)
        thisLayout.addWidget(self.lblResult)
        self.setLayout(thisLayout)

    def _search(self):
        verb = self.editVerb.text().strip()
        tense = self.comboTense.currentText()
        mood = self.comboMood.currentText()
        try:
            self.lblResult.clear()
            self.lblResult.setText(conjug(verb, tense, mood, None))
        except (KeyError, TypeError):
            self.lblResult.clear()
        except (ValueError, IndexError) as err:
            self.lblResult.setText(str(err))

    def _clear(self):
        self.editVerb.clear()
        self.lblResult.clear()


def launch():
   
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
    
    
if __name__ == '__main__':

    launch()
