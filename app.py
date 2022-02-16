#! encoding = utf-8

""" Practice French conjugaison """

import sys
from os.path import isfile
from time import sleep
from sqlite3 import Error as dbError
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QTextOption, QKeySequence
from dictionary import TENSE_MOODS, PERSONS
from dictionary import conjug, conjug_all
from config import Config, from_json_, to_json
from lang import LANG_PKG
from db import AppDB


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        self.resize(QtCore.QSize(800, 750))

        self.config = Config()
        if isfile('config.json'):
            from_json_(self.config, 'config.json')
        self.config.nft = 0
        self.config.nfc = 0
        self.config.nbt = 0
        self.config.nbc = 0
        self.setWindowTitle(LANG_PKG[self.config.lang]['main_windowtitle'])
        self.setStyleSheet('font-size: {:d}pt'.format(self.config.font_size))

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

        self.box1.btnCheck.clicked.connect(self.box3.btnClear.click)
        self.box2.btnCheck.clicked.connect(self.box3.btnClear.click)
        self.box1.btnGen.clicked.connect(self.box3.btnClear.click)
        self.box2.btnGen.clicked.connect(self.box3.btnClear.click)
        self.box1.btnHelp.clicked.connect(self._slot_help_box1)
        self.box2.btnHelp.clicked.connect(self._slot_help_box2)

        self.dConfig = DialogConfig(self.config, parent=self)
        self.dPref = DialogPref(self.config, parent=self)
        self.dAddVoc = DialogAddVoc(self.db, self.config, parent=self)
        self.dBrowse = DialogBrowse(self.db, self.config, parent=self)
        # apply config to dialogs
        self.dConfig.set_tense_mood(self.config.enabled_tm_idx)
        self.dPref.accepted.connect(self.apply_pref)

        menubar = MenuBar(parent=self)
        self.setMenuBar(menubar)
        self.statusBar = StatusBar(self.config, parent=self)
        self.setStatusBar(self.statusBar)
        self.statusBar.refresh(*self.db.num_expired_entries(self.config.enabled_tm_idx))
        self.box1.sig_checked.connect(lambda: self.statusBar.refresh(
                *self.db.num_expired_entries(self.config.enabled_tm_idx)))
        self.box2.sig_checked.connect(lambda: self.statusBar.refresh(
                *self.db.num_expired_entries(self.config.enabled_tm_idx)))
        menubar.actionConfig.triggered.connect(self._config)
        menubar.actionPref.triggered.connect(self.dPref.exec)
        menubar.actionAddVoc.triggered.connect(self.dAddVoc.exec)
        menubar.actionBrowse.triggered.connect(self.dBrowse.exec)
        self.statusBar.showMessage(LANG_PKG[self.config.lang]['status_bar_msg'],
                                   1000)
        self.setDisabled(True)
        self.db.check_has_conjug()
        self.setDisabled(False)

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
                d = QtWidgets.QMessageBox(
                        QtWidgets.QMessageBox.Warning,
                        LANG_PKG[self.config.lang]['config_tm_warning_title'],
                        LANG_PKG[self.config.lang]['config_tm_warning_body'])
                d.exec_()
                # resume previous ones
                self.dConfig.set_tense_mood(self.config.enabled_tm_idx)
        else:
            # resume previous ones
            self.dConfig.set_tense_mood(self.config.enabled_tm_idx)

    @QtCore.pyqtSlot()
    def apply_pref(self):
        sleep(0.02)
        # apply font
        self.setStyleSheet('font-size: {:d}pt'.format(self.config.font_size))
        # apply language package
        self.setWindowTitle(LANG_PKG[self.config.lang]['main_windowtitle'])
        self.box1.apply_lang()
        self.box2.apply_lang()
        self.box3.apply_lang()
        self.dPref.apply_lang()
        self.dConfig.apply_lang()
        self.dAddVoc.apply_lang()
        self.dBrowse.apply_lang()
        self.menuBar().apply_lang(LANG_PKG[self.config.lang])
        self.statusBar.refresh(*self.db.num_expired_entries(self.config.enabled_tm_idx))

    @QtCore.pyqtSlot()
    def _slot_help_box1(self):
        verb, tense_mood = self.box1.ask_help()
        self.box3.editVerb.setText(verb)
        self.box3.comboTenseMood.setCurrentText(tense_mood)
        self.box1.btnCheck.setDisabled(True)

    @QtCore.pyqtSlot()
    def _slot_help_box2(self):
        verb, tense_mood = self.box2.ask_help()
        self.box3.editVerb.setText(verb)
        self.box3.comboTenseMood.setCurrentText(tense_mood)
        self.box2.btnCheck.setDisabled(True)

    def closeEvent(self, ev):
        self.db.update_stat(self.config.nft, self.config.nfc,
                            self.config.nbt, self.config.nbc)
        # close database
        self.db.close()
        # save setting to local file
        self.dPref.fetch_config()
        to_json(self.config, 'config.json')


class Box1(QtWidgets.QGroupBox):
    sig_checked = QtCore.pyqtSignal()

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config
        self.setTitle(LANG_PKG[config.lang]['box1_title'])
        self._timer = QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._gen)

        self.lblVerb = QtWidgets.QLabel()
        self.lblVerb.setStyleSheet('font-size: 14pt; color: #2c39cf; font: bold; ')
        self.lblTense = QtWidgets.QLabel()
        self.lblTense.setFixedWidth(120)
        self.lblMood = QtWidgets.QLabel()
        self.lblMood.setFixedWidth(100)
        self.lblPerson = QtWidgets.QLabel()
        self.lblPerson.setAligntment(QtCore.Qt.AlignLeft)
        self.editInput = QtWidgets.QLineEdit()
        self.btnGen = QtWidgets.QPushButton(LANG_PKG[config.lang]['box1_btnGen'])
        self.btnCheck = QtWidgets.QPushButton(LANG_PKG[config.lang]['box1_btnCheck'])
        self.btnCheck.setToolTip('Shift + Enter')
        self.btnCheck.setShortcut(QKeySequence(QtCore.Qt.SHIFT | QtCore.Qt.Key_Return))
        self.lblCk = QtWidgets.QLabel()
        self.lblCk.setFixedWidth(30)
        self.lblExp = QtWidgets.QLabel()
        self.lblExp.setWordWrap(True)
        self.lblExp.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Minimum)
        self.btnHelp = QtWidgets.QPushButton(LANG_PKG[config.lang]['box1_btnHelp'])
        self.btnHelp.setToolTip('Ctrl + Shift + Enter')
        self.btnHelp.setShortcut(QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.SHIFT | QtCore.Qt.Key_Return))

        self._answer = '*'  # to avoid matching empty input and give false correct
        self._entry_id = -1
        self._tm_idx = -1

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
        row3.addWidget(self.btnHelp)

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
                # every <retry_intvl> practices, retrieve the verb with
                # maximum incorrect number and try again
                if not (self.config.nft % self.config.retry_intvl):
                    entry_id, verb, explanation, tm_idx, pers_idx = self.db.choose_verb(
                            'practice_forward', self.config.enabled_tm_idx,
                            order='correct_num ASC')
                else:  # randomly select a verb
                    entry_id, verb, explanation, tm_idx, pers_idx = self.db.choose_verb(
                            'practice_forward', self.config.enabled_tm_idx)
                tense, mood = TENSE_MOODS[tm_idx]
                answer = conjug(verb, tense, mood, pers_idx)
                if answer:
                    self.lblVerb.setText(verb)
                    self.lblExp.setText(explanation)
                    self.lblPerson.setText(PERSONS[pers_idx])
                    if mood == 'impératif':
                        pass
                    else:
                        self.editInput.setText(PERSONS[pers_idx])
                    self.lblTense.setText(tense)
                    self.lblMood.setText(mood)
                    self.editInput.setFocus()
                    self._answer = answer
                    self._entry_id = entry_id
                    self._tm_idx = tm_idx
                    self.config.nft += 1  # add 1 to n total forward
                    self.btnCheck.setDisabled(False)
                    break
        except ValueError as err:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Critical,
                    LANG_PKG[self.config.lang]['msg_error_title'], str(err))
            d.exec_()
        except TypeError:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning,
                    LANG_PKG[self.config.lang]['msg_warning_title'],
                    LANG_PKG[self.config.lang]['msg_warning_no_entry'])
            d.exec_()
        except KeyError as err:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning,
                    LANG_PKG[self.config.lang]['msg_warning_title'],
                    LANG_PKG[self.config.lang]['msg_warning_no_config'].format(str(err))
            )
            d.exec_()

    def _ck(self):
        """ Check the answer """
        txt = self.editInput.text()
        # remove extra spaces and only put 1
        txt_striped = ' '.join(txt.split())
        if txt_striped == self._answer:
            self.lblCk.setText('✓')
            self.lblCk.setStyleSheet('font-size: 14pt; font: bold; color: #009933')
            self.config.nfc += 1
            self._timer.start()
        else:
            self.lblCk.setText('🞪')
            self.lblCk.setStyleSheet('font-size: 14pt; font: bold; color: #D63333')
        try:
            self.db.update_res('practice_forward', self._entry_id, txt_striped == self._answer)
            self.sig_checked.emit()
        except TypeError:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning,
                    LANG_PKG[self.config.lang]['msg_warning_title'],
                    LANG_PKG[self.config.lang]['msg_warning_no_entry']
            )
            d.exec_()

    def ask_help(self):
        return self.lblVerb.text(), ', '.join(TENSE_MOODS[self._tm_idx])

    def apply_lang(self):
        self.setTitle(LANG_PKG[self.config.lang]['box1_title'])
        self.btnGen.setText(LANG_PKG[self.config.lang]['box1_btnGen'])
        self.btnCheck.setText(LANG_PKG[self.config.lang]['box1_btnCheck'])
        self.btnHelp.setText(LANG_PKG[self.config.lang]['box1_btnHelp'])


class Box2(QtWidgets.QGroupBox):
    sig_checked = QtCore.pyqtSignal()

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config
        self.setTitle(LANG_PKG[config.lang]['box2_title'])
        self._timer = QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._gen)

        self.btnGen = QtWidgets.QPushButton(LANG_PKG[config.lang]['box2_btnGen'])
        self.btnCheck = QtWidgets.QPushButton(LANG_PKG[config.lang]['box2_btnCheck'])
        self.btnCheck.setToolTip('Alt + Enter')
        self.btnCheck.setShortcut(QKeySequence(QtCore.Qt.ALT | QtCore.Qt.Key_Return))
        self.btnHelp = QtWidgets.QPushButton(LANG_PKG[config.lang]['box2_btnHelp'])
        self.btnHelp.setToolTip('Shift + Alt + Enter')
        self.btnHelp.setShortcut(QKeySequence(QtCore.Qt.SHIFT | QtCore.Qt.ALT | QtCore.Qt.Key_Return))

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
        self.lblInf = QtWidgets.QLabel(LANG_PKG[config.lang]['box2_lblInf'])
        row2.addWidget(self.lblInf)
        row2.addWidget(self.editVerb)
        row2.addWidget(self.comboTenseMood)
        row2.addWidget(self.lblCk)

        row3 = QtWidgets.QHBoxLayout()
        row3.setAlignment(QtCore.Qt.AlignRight)
        row3.addWidget(self.btnGen)
        row3.addWidget(self.btnCheck)
        row3.addWidget(self.btnHelp)

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
                # every <retry_intvl> practices, retrieve the verb with
                # maximum incorrect number and try again
                if not (self.config.nbt % self.config.retry_intvl):
                    entry_id, verb, explanation, tm_idx, pers_idx = self.db.choose_verb(
                            'practice_backward', self.config.enabled_tm_idx,
                            order='correct_num ASC')
                else:  # randomly select a verb
                    entry_id, verb, explanation, tm_idx, pers_idx = self.db.choose_verb(
                            'practice_backward', self.config.enabled_tm_idx)
                tense, mood = TENSE_MOODS[tm_idx]
                conjug_str = conjug(verb, tense, mood, pers_idx)
                if conjug_str:
                    self.lblConjug.setText(conjug_str)
                    self.editVerb.setFocus()
                    self._answer = verb
                    self._entry_id = entry_id
                    self._tm_idx = tm_idx
                    self.config.nbt += 1  # add 1 to n total forward
                    self.btnCheck.setDisabled(False)
                    break
        except ValueError as err:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Critical,
                    LANG_PKG[self.config.lang]['msg_error_title'], str(err))
            d.exec_()
        except TypeError:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning,
                    LANG_PKG[self.config.lang]['msg_warning_title'],
                    LANG_PKG[self.config.lang]['msg_warning_no_entry'])
            d.exec_()
        except KeyError as err:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning,
                    LANG_PKG[self.config.lang]['msg_warning_title'],
                    LANG_PKG[self.config.lang]['msg_warning_no_config'].format(str(err))
            )
            d.exec_()

    def _ck(self):
        """ Check the answer """
        is_correct = self.editVerb.text().lower() == self._answer and \
                     self.comboTenseMood.currentText() == ', '.join(TENSE_MOODS[self._tm_idx])
        if is_correct:
            self.lblCk.setText('✓')
            self.lblCk.setStyleSheet('font-size: 14pt; color: #009933')
            self.config.nbc += 1
            self._timer.start()
        else:
            self.lblCk.setText('🞪')
            self.lblCk.setStyleSheet('font-size: 14pt; color: #D63333')
        try:
            self.db.update_res('practice_backward', self._entry_id, is_correct)
            self.sig_checked.emit()
        except TypeError:
            d = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning,
                    LANG_PKG[self.config.lang]['msg_warning_title'],
                    LANG_PKG[self.config.lang]['msg_warning_no_entry']
            )
            d.exec_()

    def ask_help(self):
        return self._answer, ', '.join(TENSE_MOODS[self._tm_idx])

    def apply_lang(self):
        self.setTitle(LANG_PKG[self.config.lang]['box2_title'])
        self.btnGen.setText(LANG_PKG[self.config.lang]['box2_btnGen'])
        self.btnCheck.setText(LANG_PKG[self.config.lang]['box2_btnCheck'])
        self.btnHelp.setText(LANG_PKG[self.config.lang]['box2_btnHelp'])
        self.lblInf.setText(LANG_PKG[self.config.lang]['box2_lblInf'])


class Box3(QtWidgets.QGroupBox):

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.db = db
        self.setTitle(LANG_PKG[config.lang]['box3_title'])

        self.editVerb = QtWidgets.QLineEdit()
        self.comboTenseMood = QtWidgets.QComboBox()
        self.comboTenseMood.setFixedWidth(300)
        self.comboTenseMood.addItems([', '.join(TENSE_MOODS[i]) for i in config.enabled_tm_idx])
        self.btnClear = QtWidgets.QPushButton(LANG_PKG[config.lang]['box3_btnClear'])
        self.lblExp = QtWidgets.QLabel()
        self.lblExp.setWordWrap(True)
        self.lblExp.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Minimum)
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
            self.lblExp.clear()
        except (ValueError, IndexError) as err:
            self.lblResult.setText(str(err))
            self.lblExp.clear()
        except dbError:
            self.lblResult.setText(LANG_PKG[self.config.lang]['box3_db_error'])
            self.lblExp.clear()

    def _clear(self):
        self.editVerb.clear()
        self.lblExp.clear()
        self.lblResult.clear()

    def apply_lang(self):
        self.setWindowTitle(LANG_PKG[self.config.lang]['box3_title'])
        self.btnClear.setText(LANG_PKG[self.config.lang]['box3_btnClear'])


class DialogConfig(QtWidgets.QDialog):

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        ckLayout = QtWidgets.QVBoxLayout()
        self._cklist = []
        for i, _tm in enumerate(TENSE_MOODS):
            ck = QtWidgets.QCheckBox(", ".join(_tm))
            self._cklist.append(ck)
            ckLayout.addWidget(ck)
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setAlignment(QtCore.Qt.AlignRight)
        self.btnOk = QtWidgets.QPushButton('Okay')
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        btnLayout.addWidget(self.btnCancel)
        btnLayout.addWidget(self.btnOk)
        self.apply_lang()

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

    def apply_lang(self):
        self.setWindowTitle(LANG_PKG[self.config.lang]['dialog_config_title'])
        self.btnOk.setText(LANG_PKG[self.config.lang]['btnOK'])
        self.btnCancel.setText(LANG_PKG[self.config.lang]['btnCancel'])


class DialogPref(QtWidgets.QDialog):

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle('Configure Preferences')

        self.lblIntvl = QtWidgets.QLabel()
        self.inpIntvl = QtWidgets.QSpinBox()
        self.inpIntvl.setMinimum(1)
        self.inpIntvl.setValue(config.retry_intvl)
        self.lblLang = QtWidgets.QLabel()
        self.lblFontSize = QtWidgets.QLabel()
        self.inpFontSize = QtWidgets.QSpinBox()
        self.inpFontSize.setMinimum(10)
        self.inpFontSize.setSuffix(' pt')
        self.comboLang = QtWidgets.QComboBox()
        self.comboLang.addItems(list(LANG_PKG.keys()))
        self.comboLang.setCurrentText(config.lang)
        prefLayout = QtWidgets.QFormLayout()
        prefLayout.addRow(self.lblIntvl, self.inpIntvl)
        prefLayout.addRow(self.lblLang, self.comboLang)
        prefLayout.addRow(self.lblFontSize, self.inpFontSize)

        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setAlignment(QtCore.Qt.AlignRight)
        self.btnOk = QtWidgets.QPushButton('Okay')
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        self.btnOk.setDefault(True)
        btnLayout.addWidget(self.btnCancel)
        btnLayout.addWidget(self.btnOk)

        self.apply_lang()

        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addLayout(prefLayout)
        thisLayout.addLayout(btnLayout)
        self.setLayout(thisLayout)

        self.btnCancel.clicked.connect(self.reject)
        self.btnOk.clicked.connect(self.accept)
        self.accepted.connect(self.fetch_config)

    def fetch_config(self):
        self.config.lang = list(LANG_PKG.keys())[self.comboLang.currentIndex()]
        self.config.retry_intvl = self.inpIntvl.value()
        self.config.font_size = self.inpFontSize.value()

    def apply_lang(self):
        self.setWindowTitle(LANG_PKG[self.config.lang]['dialog_pref_title'])
        self.lblIntvl.setText(LANG_PKG[self.config.lang]['dialog_pref_lblIntvl'])
        self.lblIntvl.setToolTip(LANG_PKG[self.config.lang]['dialog_pref_lblIntvl_tooltip'])
        self.lblLang.setText(LANG_PKG[self.config.lang]['dialog_pref_lblLang'])
        self.lblFontSize.setText(LANG_PKG[self.config.lang]['dialog_pref_lblFont'])
        current_idx = self.comboLang.currentIndex()
        self.comboLang.clear()
        self.comboLang.addItems(LANG_PKG[self.config.lang]['dialog_pref_comboLang'])
        self.comboLang.setCurrentIndex(current_idx)
        self.btnOk.setText(LANG_PKG[self.config.lang]['btnOK'])
        self.btnCancel.setText(LANG_PKG[self.config.lang]['btnCancel'])


class DialogAddVoc(QtWidgets.QDialog):

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config

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

        self.lblVerb = QtWidgets.QLabel('Verb')
        self.lblExp = QtWidgets.QLabel('Explanation')
        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addWidget(self.lblVerb)
        thisLayout.addWidget(self.editVerb)
        thisLayout.addWidget(self.lblExp)
        thisLayout.addWidget(self.editExp)
        thisLayout.addLayout(btnLayout)
        self.setLayout(thisLayout)
        self.apply_lang()

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

    def apply_lang(self):
        self.setWindowTitle(LANG_PKG[self.config.lang]['dialog_addvoc_title'])
        self.btnAdd.setText(LANG_PKG[self.config.lang]['dialog_addvoc_btnAdd'])
        self.btnCancel.setText(LANG_PKG[self.config.lang]['dialog_addvoc_btnCancel'])
        self.btnUpdate.setText(LANG_PKG[self.config.lang]['dialog_addvoc_btnUpdate'])
        self.lblVerb.setText(LANG_PKG[self.config.lang]['dialog_addvoc_lblVerb'])
        self.lblExp.setText(LANG_PKG[self.config.lang]['dialog_addvoc_lblExp'])


class DialogBrowse(QtWidgets.QDialog):

    def __init__(self, db, config, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config

        self.setWindowTitle(LANG_PKG[config.lang]['dialog_browse_title'])
        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumWidth(900)
        self.resize(QtCore.QSize(900, 600))
        self.setModal(False)

        self.btnRefresh = QtWidgets.QPushButton(LANG_PKG[config.lang]['dialog_browse_btnRefresh'])
        self.btnRefresh.clicked.connect(self._refresh)
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setAlignment(QtCore.Qt.AlignRight)
        btnLayout.addWidget(self.btnRefresh)

        self.dbTable = QtWidgets.QTableWidget()
        area = QtWidgets.QScrollArea()
        area.setWidget(self.dbTable)
        area.setWidgetResizable(True)
        area.setAlignment(QtCore.Qt.AlignTop)
        thisLayout = QtWidgets.QVBoxLayout()
        thisLayout.addWidget(area)
        thisLayout.addLayout(btnLayout)
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

    def apply_lang(self):
        self.setWindowTitle(LANG_PKG[self.config.lang]['dialog_browse_title'])
        self.btnRefresh.setText(LANG_PKG[self.config.lang]['dialog_browse_btnRefresh'])


class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.actionConfig = QtWidgets.QAction("Config Tense and Mood")
        self.actionPref = QtWidgets.QAction('Preference')
        self.actionAddVoc = QtWidgets.QAction("Add Vocabulary")
        self.actionAddVoc.setShortcut('Ctrl+N')
        self.actionBrowse = QtWidgets.QAction("Browse Glossary")
        self.actionStats = QtWidgets.QAction('Statistics')
        self.menuConfig = self.addMenu("&Config")
        self.menuConfig.addAction(self.actionConfig)
        self.menuConfig.addAction(self.actionPref)
        self.menuGloss = self.addMenu("&Glossary")
        self.menuGloss.addAction(self.actionAddVoc)
        self.menuGloss.addAction(self.actionBrowse)
        self.menuStats = self.addMenu("&Statistics")
        self.menuStats.addAction(self.actionStats)

    def apply_lang(self, lang_pkg):
        self.actionConfig.setText(lang_pkg['action_config'])
        self.actionPref.setText(lang_pkg['action_pref'])
        self.actionAddVoc.setText(lang_pkg['action_addvoc'])
        self.actionBrowse.setText(lang_pkg['action_browse'])
        self.actionStats.setText(lang_pkg['action_stats'])
        self.menuConfig.setTitle(lang_pkg['menu_config'])
        self.menuGloss.setTitle(lang_pkg['menu_glossary'])
        self.menuStats.setTitle(lang_pkg['menu_stats'])


class StatusBar(QtWidgets.QStatusBar):

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.labelN1 = QtWidgets.QLabel()
        self.labelN2 = QtWidgets.QLabel()
        self.addPermanentWidget(self.labelN1)
        self.addPermanentWidget(self.labelN2)

    def refresh(self, n1, n2):
        self.labelN1.setText(LANG_PKG[self.config.lang]['status_msg1'].format(n1))
        self.labelN2.setText(LANG_PKG[self.config.lang]['status_msg2'].format(n2))


def launch():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
