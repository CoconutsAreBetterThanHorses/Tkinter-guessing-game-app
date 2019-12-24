from random import choice

import requests
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout
)


def convert(capital):
    """Help to handle right answer."""
    braces = ['[', '(']
    result_capital = []

    # Handle capitals with second name
    for num, let in enumerate(capital):
        if let in braces:
            capital = capital[:num - 1]
            continue

    # Handle double letter and lowercase input
    for num, let in enumerate(capital[:-1]):
        if let != capital[num + 1] and let.isalpha():
            result_capital.append(let.lower())
    return result_capital + [capital[-1]]


class Countries(QObject):
    """List of dictionaries with countries and it's capitals."""
    CBC = requests.get(
        'https://query.data.world/s/vfp6xp6lk3byc5mv4lawo3ojfwmmqz'
    ).json()
    CACHE = []

    def get(self):
        """Get dict with countries and it's capitals."""
        while 1:
            data = choice(self.CBC)
            # Exclude countries without capitals
            if data.get('city') is None:
                self.CACHE.append(data.get('country'))
            # Exclude countries that have been before (add it to cache)
            if data.get('country') not in self.CACHE:
                self.CACHE.append(data.get('country'))
                return data


class MainWindow(QMainWindow):
    """ Qt graphic interface."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initData()
        self.initUi()
        self.initSignals()
        self.initLayouts()
        self.initBlock()

    def initData(self):
        self.countries = Countries()
        self.country_data = self.countries.get()
        self.mistakes = 0

    def initUi(self):
        self.resize(300, 250)

        self.setMinimumSize(300, 200)
        self.setMaximumSize(600, 400)

        self.setWindowTitle('Guess the capital')

        self.countryLabel = QLabel(self.country_data.get('country'), )
        self.countryLabel.setStyleSheet("font: 18pt;")
        self.countryLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel = QLabel(self)
        self.resultLabel.setAlignment(Qt.AlignCenter)

        self.capitalEdit = QLineEdit(self)

        self.checkBtn = QPushButton('Check', self)
        self.newCountryBtn = QPushButton('New Country', self)
        self.quitBtn = QPushButton('Quit', self)

    def initSignals(self):
        self.checkBtn.clicked.connect(self.onClickCheck)
        self.newCountryBtn.clicked.connect(self.onClickNewCountry)
        self.quitBtn.clicked.connect(self.onClickQuit)

        self.capitalEdit.textChanged.connect(self.initBlock)

    def initLayouts(self):
        self.w = QWidget(self)

        self.mainLayout = QVBoxLayout(self.w)
        self.mainLayout.addWidget(self.countryLabel, Qt.AlignVCenter)
        self.mainLayout.addWidget(self.capitalEdit)
        self.mainLayout.addWidget(self.resultLabel, Qt.AlignVCenter)
        self.mainLayout.addWidget(self.checkBtn)
        self.mainLayout.addWidget(self.newCountryBtn)
        self.mainLayout.addWidget(self.quitBtn)

        self.setCentralWidget(self.w)

    def initBlock(self):
        self.checkBtn.setEnabled(True)
        if not self.getCapitalText():
            self.checkBtn.setEnabled(False)

    def getCapitalText(self):
        return self.capitalEdit.text()

    def onClickCheck(self):
        if self.mistakes == 10:  # attempt amount
            self.close()

        answer = convert(self.getCapitalText())
        city = convert(self.country_data.get('city'))

        if answer == city:  # mismatching handler
            self.resultLabel.setText("That's right!")
        else:
            self.mistakes += 1
            self.resultLabel.setText(f"You didn't guess! "
                                     f"The attempt №{self.mistakes}")

    def onClickNewCountry(self):
        # Quit from the app if all countries have been before
        if len(self.countries.CACHE) == len(self.countries.CBC):
            self.close()

        self.capitalEdit.setText('')
        self.resultLabel.setText('')

        # Set new country
        self.country_data = self.countries.get()
        self.countryLabel.setText(self.country_data.get('country'))

    def onClickQuit(self):
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.onClickCheck()
        if e.key() == Qt.Key_Space:
            self.onClickNewCountry()
