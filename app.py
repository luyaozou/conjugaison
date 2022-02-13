#! encoding = utf-8

""" Practice French conjugaison """

import sys
from os.path import isfile
from sqlite3 import Error as dbError
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QTextOption, QKeySequence
from dictionary import TENSE_MOODS, AVAILABLE_TENSE_MOODS, PERSONS
from dictionary import conjug, conjug_all
from config import Config, from_json_, to_json
from db import AppDB


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Practice French Conjugaison')
        self.setStyleSheet('font-size: 12pt')
        self.setMinimumWidth(600)
        self.setMinimumHeight(650)
        self.resize(QtCore.QSize(800, 650))

        self.config = Config()
        if isfile('config.json'):
            from_json_(self.config, 'config.json')

        self.db = AppDB('app.db')

        centerWidget = QtWidgets.QWidget()
        self.box1 = Box1(self.db, self.config, parent=self)
        self.box2 = Box2(self.db, self.config, parent=self)
        self.box3 = Box3(self.db, self.config, parent=self)
        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.setAlignment(QtCore.Qt.AlignHCenter)
        thisLayout.setSpacing(10)
        thisLayout.addWidget(self.box1)
        thisLayout.addWidget(self.box2)
        thisLayout.addWidget(self.box3)
        centerWidget.setLayout(thisLayout)

        # set central widget
        self.setCentralWidget(centerWidget)

        self.dConfig = DialogConfig(parent=self)
        self.dAddVoc = DialogAddVoc(self.db, parent=self)
        self.dBrowse = DialogBrowse(self.db, parent=self)
        # apply config to dialogs
        self.dConfig.set_tense_mood(self.config.enabled_tm_idx)

        menubar = MenuBar(parent=self)
        self.setMenuBar(menubar)
        self.statusBar = StatusBar(parent=self)
        self.setStatusBar(self.statusBar)
        self.statusBar.refresh(*self.db.num_expired_entries(self.config.enabled_tm_idx))
        self.box1.sig_checked.connect(lambda: self.statusBar.refresh(
                *self.db.num_expired_entries(self.config.enabled_tm_idx)))
        self.box2.sig_checked.connect(lambda: self.statusBar.refresh(
                *self.db.num_expired_entries(self.config.enabled_tm_idx)))
        menubar.actionConfig.triggered.connect(self._config)
        menubar.actionAddVoc.triggered.connect(self.dAddVoc.exec)
        menubar.actionBrowse.triggered.connect(self.dBrowse.exec)

    def _config(self):
        # retrieve current checked tense mood pairs
        self.dConfig.exec()
        if self.dConfig.result() == QtWidgets.QDialog.Accepted:
            tm_idx = self.dConfig.get_tense_mood()
            if tm_idx:
                # apply the new checked tms
                self.config.enabled_tm_idx = tm_idx
                self.box2.set_tm(self.config.enabled_tm_idx)
                self.box3.set_tm(self.config.enabled_tm_idx)
                self.statusBar.refresh(*self.db.num_expired_entries(tm_idx))
            else:
                d = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                'Empty', 'At least one tense mood should be selected. Resume previous configuration')
                d.exec_()
                # resume previous ones
                self.dConfig.set_tense_mood(self.config.enabled_tm_idx)
        else:
            # resume previous ones
            self.dConfig.set_tense_mood(self.config.enabled_tm_idx)

    def closeEvent(self, ev):
        # close database
        self.db.close()
        # save setting to local file
        to_json(self.config, 'config.json')


class Box1(QtWidgets.QGroupBox):

    sig_checked = QtCore.pyqtSignal()

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config
        self.setTitle('Forward Practice: Conjugate Verb')
        self._timer = QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._gen)

        self.lblVerb = QtWidgets.QLabel()
        self.lblVerb.setStyleSheet('font-size: 14pt; color: #2c39cf; font: bold; ')
        self.lblTense = QtWidgets.QLabel()
        self.lblTense.setFixedWidth(120)
        self.lblMood = QtWidgets.QLabel()
        self.lblMood.setFixedWidth(80)
        self.lblPerson = QtWidgets.QLabel()
        self.editInput = QtWidgets.QLineEdit()
        self.btnGen = QtWidgets.QPushButton('Next')
        self.btnGen.setFixedWidth(100)
        self.btnCheck = QtWidgets.QPushButton('Check Answer (Shift+Enter)')
        self.btnCheck.setFixedWidth(225)
        self.btnCheck.setShortcut(QKeySequence(QtCore.Qt.SHIFT | QtCore.Qt.Key_Return))
        self.lblCk = QtWidgets.QLabel()
        self.lblCk.setFixedWidth(30)
        self.lblExp = QtWidgets.QLabel()
        self.lblExp.setWordWrap(True)

        self._answer = '*'  # to avoid matching empty input and give false correct
        self._entry_id = -1

        row1 = QtWidgets.QHBoxLayout()
        row1.setAlignment(QtCore.Qt.AlignLeft)
        row1.addWidget(self.lblVerb)
        row1.addWidget(self.lblExp)

        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(self.lblTense)
        row2.addWidget(self.lblMood)
        row2.addWidget(self.lblPerson)
        row2.addWidget(self.editInput)
        row2.addWidget(self.lblCk)

        row3 = QtWidgets.QHBoxLayout()
        row3.setAlignment(QtCore.Qt.AlignRight)
        row3.addWidget(self.btnGen)
        row3.addWidget(self.btnCheck)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.setSpacing(10)
        thisLayout.setAlignment(QtCore.Qt.AlignHCenter)
        thisLayout.addLayout(row1)
        thisLayout.addLayout(row2)
        thisLayout.addLayout(row3)
        self.setLayout(thisLayout)

        self.btnGen.clicked.connect(self._gen)
        self.btnCheck.clicked.connect(self._ck)

    def _gen(self):
        """ Generate a verb & a conjugaison """
        # clear previous result
        self.lblCk.clear()
        self.editInput.clear()

        # draw random verb until there is a valid conjugation
        # this is to avoid those few special verbs that do not have full conjug.
        try:
            while True:
                # randomly select a verb
                entry_id, verb, explanation, tm_idx, pers_idx = self.db.choose_verb(
                        'practice_forward', self.config.enabled_tm_idx)
                tense, mood = TENSE_MOODS[tm_idx]
                answer = conjug(verb, tense, mood, pers_idx)
                if answer:
                    self.lblVerb.setText(verb)
                    self.lblExp.setText(explanation)
                    self.lblPerson.setText(PERSONS[pers_idx])
                    self.editInput.setText(PERSONS[pers_idx])
                    self.lblTense.setText(tense)
                    self.lblMood.setText(mood)
                    self.editInput.setFocus()
                    self._answer = answer
                    self._entry_id = entry_id
                    break
        except ValueError as err:
            d = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                      'Error', str(err))
            d.exec_()
        except TypeError:
            d = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                      'Warning', 'No entry found')
            d.exec_()

    def _ck(self):
        """ Check the answer """
        txt = self.editInput.text()
        # remove extra spaces and only put 1
        txt_striped = ' '.join(txt.split())
        if txt_striped == self._answer:
            self.lblCk.setText('✓')
            self.lblCk.setStyleSheet('font-size: 14pt; font: bold; color: #009933')
            self._timer.start()
        else:
            self.lblCk.setText('🞪')
            self.lblCk.setStyleSheet('font-size: 14pt; font: bold; color: #D63333')
        try:
            self.db.update_res('practice_forward', self._entry_id, txt_striped == self._answer)
            self.sig_checked.emit()
        except TypeError:
            d = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                      'Warning', 'No entry found')
            d.exec_()


class Box2(QtWidgets.QGroupBox):

    sig_checked = QtCore.pyqtSignal()

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config
        self.setTitle('Reverse Practice: Guess infinitive, tense and mood')
        self._timer = QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._gen)

        self.btnGen = QtWidgets.QPushButton('Next')
        self.btnGen.setFixedWidth(100)
        self.btnCheck = QtWidgets.QPushButton('Check Answer (Alt+Enter)')
        self.btnCheck.setFixedWidth(225)
        self.btnCheck.setShortcut(QKeySequence(QtCore.Qt.ALT | QtCore.Qt.Key_Return))

        self.editVerb = QtWidgets.QLineEdit()
        self.comboTenseMood = QtWidgets.QComboBox()
        self.comboTenseMood.setFixedWidth(300)
        self.set_tm(self.config.enabled_tm_idx)
        self.lblCk = QtWidgets.QLabel()
        self.lblCk.setFixedWidth(30)
        self.lblConjug = QtWidgets.QLabel()
        self.lblConjug.setStyleSheet('font-size: 14pt; color: #2c39cf; font: bold; ')

        self.btnGen.clicked.connect(self._gen)
        self.btnCheck.clicked.connect(self._ck)

        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(QtWidgets.QLabel('Infinitive: '))
        row2.addWidget(self.editVerb)
        row2.addWidget(self.comboTenseMood)
        row2.addWidget(self.lblCk)

        row3 = QtWidgets.QHBoxLayout()
        row3.setAlignment(QtCore.Qt.AlignRight)
        row3.addWidget(self.btnGen)
        row3.addWidget(self.btnCheck)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.setAlignment(QtCore.Qt.AlignHCenter)
        thisLayout.setSpacing(10)
        thisLayout.addWidget(self.lblConjug)
        thisLayout.addLayout(row2)
        thisLayout.addLayout(row3)
        self.setLayout(thisLayout)

        self.editVerb.editingFinished.connect(self.comboTenseMood.setFocus)
        self._answer = '*'  # to avoid matching empty string and give false correct
        self._entry_id = -1
        self._tm_idx = -1

    def set_tm(self, checked_tm_idx):
        """ set tense mood options """
        self.comboTenseMood.clear()
        self.comboTenseMood.addItems([', '.join(TENSE_MOODS[i]) for i in checked_tm_idx])
        self.comboTenseMood.adjustSize()

    def _gen(self):
        """ Generate a conjugaison """
        # clear previous result
        self.lblCk.clear()
        self.editVerb.clear()

        # draw random verb until there is a valid conjugation
        # this is to avoid those few special verbs that do not have full conjug.
        try:
            while True:
                # randomly select a verb
                entry_id, verb, _, tm_idx, pers_idx = self.db.choose_verb(
                        'practice_backward', self.config.enabled_tm_idx)
                tense, mood = TENSE_MOODS[tm_idx]
                conjug_str = conjug(verb, tense, mood, pers_idx)
                if conjug_str:
                    self.lblConjug.setText(conjug_str)
                    self.editVerb.setFocus()
                    self._answer = verb
                    self._entry_id = entry_id
                    self._tm_idx = tm_idx
                    break
        except ValueError as err:
            d = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                      'Error', str(err))
            d.exec_()
        except TypeError:
            d = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                      'Warning', 'No entry to practice today')
            d.exec_()

    def _ck(self):
        """ Check the answer """
        is_correct = self.editVerb.text().lower() == self._answer and \
                     self.comboTenseMood.currentText() == ', '.join(TENSE_MOODS[self._tm_idx])
        if is_correct:
            self.lblCk.setText('✓')
            self.lblCk.setStyleSheet('font-size: 14pt; color: #009933')
            self._timer.start()
        else:
            self.lblCk.setText('🞪')
            self.lblCk.setStyleSheet('font-size: 14pt; color: #D63333')
        try:
            self.db.update_res('practice_backward', self._entry_id, is_correct)
            self.sig_checked.emit()
        except TypeError:
            d = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                      'Warning', 'No entry to practice today')
            d.exec_()


class Box3(QtWidgets.QGroupBox):

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.db = db
        self.setTitle('Look up')

        self.editVerb = QtWidgets.QLineEdit()
        self.comboTenseMood = QtWidgets.QComboBox()
        self.comboTenseMood.setFixedWidth(300)
        self.comboTenseMood.addItems([', '.join(TENSE_MOODS[i]) for i in config.enabled_tm_idx])
        self.btnClear = QtWidgets.QPushButton('Clear')
        self.lblExp = QtWidgets.QLabel()
        self.lblExp.setWordWrap(True)
        self.lblResult = QtWidgets.QTextEdit()
        self.lblResult.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.lblResult.setReadOnly(True)
        self.btnClear.clicked.connect(self._clear)
        self.editVerb.editingFinished.connect(self._search)
        self.comboTenseMood.currentIndexChanged.connect(self._search)

        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self.editVerb)
        row1.addWidget(self.comboTenseMood)
        row1.addWidget(self.btnClear)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addLayout(row1)
        thisLayout.addWidget(self.lblExp)
        thisLayout.addWidget(self.lblResult)
        self.setLayout(thisLayout)

    def set_tm(self, checked_tm_idx):
        """ set tense mood options """
        self.comboTenseMood.clear()
        self.comboTenseMood.addItems([', '.join(TENSE_MOODS[i]) for i in checked_tm_idx])

    def _search(self):
        try:
            verb = self.editVerb.text().strip()
            tense, mood = self.comboTenseMood.currentText().split(', ')
            self.lblResult.clear()
            self.lblResult.setText('\n'.join(conjug_all(verb, tense, mood)))
            self.lblExp.setText(self.db.get_explanation(verb))
        except (KeyError, TypeError):
            self.lblResult.clear()
        except (ValueError, IndexError) as err:
            self.lblResult.setText(str(err))
        except dbError:
            self.lblResult.setText("Cannot find verb in glossary")

    def _clear(self):
        self.editVerb.clear()
        self.lblResult.clear()


class DialogConfig(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Configure tense and mood for practice')
        ckLayout = QtWidgets.QVBoxLayout()
        self._cklist = []
        for i, _tm in enumerate(TENSE_MOODS):
            ck = QtWidgets.QCheckBox(", ".join(_tm))
            self._cklist.append(ck)
            ckLayout.addWidget(ck)
            if i not in AVAILABLE_TENSE_MOODS:
                ck.setChecked(False)
                ck.setDisabled(True)
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setAlignment(QtCore.Qt.AlignRight)
        self.btnOk = QtWidgets.QPushButton('Okay')
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        btnLayout.addWidget(self.btnCancel)
        btnLayout.addWidget(self.btnOk)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addLayout(ckLayout)
        thisLayout.addLayout(btnLayout)
        self.setLayout(thisLayout)

        self.btnCancel.clicked.connect(self.reject)
        self.btnOk.clicked.connect(self.accept)

    def get_tense_mood(self):
        checked_tense_moods = []
        for i, ck in enumerate(self._cklist):
            if ck.isChecked():
                checked_tense_moods.append(i)
        return checked_tense_moods

    def set_tense_mood(self, tm_idx):
        for i, ck in enumerate(self._cklist):
            if ck.isEnabled():
                ck.setChecked(i in tm_idx)


class DialogAddVoc(QtWidgets.QDialog):

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db

        self.btnAdd = QtWidgets.QPushButton('Add')
        self.btnCancel = QtWidgets.QPushButton('Cancel')
        self.btnUpdate = QtWidgets.QPushButton('Update')
        self.editVerb = QtWidgets.QLineEdit()
        self.editExp = QtWidgets.QTextEdit()
        self.editExp.setWordWrapMode(QTextOption.WordWrap)
        self.editExp.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.btnAdd.setDefault(True)
        self.btnUpdate.setAutoDefault(True)

        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setAlignment(QtCore.Qt.AlignRight)
        btnLayout.addWidget(self.btnCancel)
        btnLayout.addWidget(self.btnUpdate)
        btnLayout.addWidget(self.btnAdd)

        self.btnAdd.clicked.connect(self._add)
        self.btnCancel.clicked.connect(self.reject)
        self.btnUpdate.clicked.connect(self._update)
        self.editVerb.editingFinished.connect(self._check_exist)

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addWidget(QtWidgets.QLabel('Verb'))
        thisLayout.addWidget(self.editVerb)
        thisLayout.addWidget(QtWidgets.QLabel('Explanation'))
        thisLayout.addWidget(self.editExp)
        thisLayout.addLayout(btnLayout)
        self.setLayout(thisLayout)

    def _add(self):
        verb = self.editVerb.text().strip()
        explanation = self.editExp.toPlainText().strip()
        self.db.add_voc(verb, explanation)
        self.editVerb.clear()
        self.editExp.clear()

    def _update(self):
        verb = self.editVerb.text().strip()
        explanation = self.editExp.toPlainText().strip()
        self.db.update_voc(verb, explanation)
        self.editVerb.clear()
        self.editExp.clear()

    def _check_exist(self):
        verb = self.editVerb.text().strip()
        is_exist = self.db.check_exist(verb)
        if is_exist:
            self.btnAdd.setDisabled(True)
            self.btnUpdate.setDisabled(False)
            self.editExp.setText(self.db.get_explanation(verb))
        else:
            self.btnAdd.setDisabled(False)
            self.btnUpdate.setDisabled(True)
            self.editExp.clear()


class DialogBrowse(QtWidgets.QDialog):

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db

        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumWidth(900)
        self.resize(QtCore.QSize(900, 600))
        self.setModal(False)

        btn = QtWidgets.QPushButton('Refresh')
        btn.clicked.connect(self._refresh)
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setAlignment(QtCore.Qt.AlignHCenter)
        btnLayout.addWidget(btn)

        self.dbTable = QtWidgets.QTableWidget()
        area = QtWidgets.QScrollArea()
        area.setWidget(self.dbTable)
        area.setWidgetResizable(True)
        area.setAlignment(QtCore.Qt.AlignTop)
        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addLayout(btnLayout)
        thisLayout.addWidget(area)
        self.setLayout(thisLayout)
        self._refresh()

    def _refresh(self):
        self.dbTable.clearContents()
        records = self.db.get_glossary()
        rows = len(records)
        self.dbTable.setRowCount(rows)
        self.dbTable.setColumnCount(2)
        for row, rec in enumerate(records):
            for col, x in enumerate(rec):
                item = QtWidgets.QTableWidgetItem(str(x))
                self.dbTable.setItem(row, col, item)
        self.dbTable.resizeRowsToContents()
        self.dbTable.resizeColumnsToContents()


class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.actionConfig = QtWidgets.QAction("Config Tense and Mood")
        self.actionAddVoc = QtWidgets.QAction("Add Vocabulary")
        self.actionAddVoc.setShortcut('Ctrl+N')
        self.actionBrowse = QtWidgets.QAction("Browse Glossary")
        menuConfig = self.addMenu("&Config")
        menuConfig.addAction(self.actionConfig)
        menuGloss = self.addMenu("&Glossary")
        menuGloss.addAction(self.actionAddVoc)
        menuGloss.addAction(self.actionBrowse)


class StatusBar(QtWidgets.QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.labelN1 = QtWidgets.QLabel()
        self.labelN2 = QtWidgets.QLabel()
        self.addPermanentWidget(self.labelN1)
        self.addPermanentWidget(self.labelN2)

    def refresh(self, n1, n2):
        self.labelN1.setText(' {:d} entries to practice in exercise 1 '.format(n1))
        self.labelN2.setText(' {:d} entries to practice in exercise 2'.format(n2))


def launch():
   
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
    
    
if __name__ == '__main__':

    launch()
