from random import choice, shuffle

import requests
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout
)


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

    def get_capital_choices(self, chosen_data):
        """Get capital names for buttons."""
        capitals = [chosen_data.get('city')]

        while len(capitals) < 4:
            data = choice(self.CBC)
            # Exclude repeats and empty capitals
            if data.get('city') not in capitals and data.get('city'):
                capitals.append(data.get('city'))

        # Mix the list
        shuffle(capitals)
        return capitals


class MainWindow(QMainWindow):
    """ Qt graphic interface."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()
        self.initSingltoneData()
        self.initNewCountryData()
        self.initSignals()
        self.initLayouts()

    def initUi(self):
        self.resize(400, 350)

        self.setMinimumSize(300, 250)
        self.setMaximumSize(600, 400)

        self.setWindowTitle('Guess the capital')

        self.countryLabel = QLabel(self)
        self.countryLabel.setStyleSheet("font: 18pt;")
        self.countryLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel = QLabel(self)
        self.resultLabel.setAlignment(Qt.AlignCenter)

        self.firstCapitalBtn = QPushButton(self)
        self.secondCapitalBtn = QPushButton(self)
        self.thirdCapitalBtn = QPushButton(self)
        self.fourthCapitalBtn = QPushButton(self)
        self.emptyLabel = QLabel(self)
        self.newCountryBtn = QPushButton('Set New Country', self)
        self.quitBtn = QPushButton('Quit', self)

    def initSingltoneData(self):
        self.countries = Countries()
        self.mistakes = 0

    def initNewCountryData(self):
        self.country_data = self.countries.get()
        self.countryLabel.setText(self.country_data.get('country'))
        self.capital_choices = self.countries.get_capital_choices(
            self.country_data
        )

        self.firstCapitalBtn.setText(self.capital_choices[0])
        self.secondCapitalBtn.setText(self.capital_choices[1])
        self.thirdCapitalBtn.setText(self.capital_choices[2])
        self.fourthCapitalBtn.setText(self.capital_choices[3])

        self.newCountryBtn.setEnabled(False)

    def initSignals(self):
        self.firstCapitalBtn.clicked.connect(
            lambda: self.onClickCheckCountryCapital(0)
        )
        self.secondCapitalBtn.clicked.connect(
            lambda: self.onClickCheckCountryCapital(1)
        )
        self.thirdCapitalBtn.clicked.connect(
            lambda: self.onClickCheckCountryCapital(2)
        )
        self.fourthCapitalBtn.clicked.connect(
            lambda: self.onClickCheckCountryCapital(3)
        )
        self.newCountryBtn.clicked.connect(self.onClickNewCountry)
        self.quitBtn.clicked.connect(self.onClickQuit)

    def initLayouts(self):
        self.w = QWidget(self)

        self.mainLayout = QVBoxLayout(self.w)
        self.mainLayout.addWidget(self.countryLabel, Qt.AlignVCenter)
        self.mainLayout.addWidget(self.resultLabel, Qt.AlignVCenter)
        self.mainLayout.addWidget(self.firstCapitalBtn)
        self.mainLayout.addWidget(self.secondCapitalBtn)
        self.mainLayout.addWidget(self.thirdCapitalBtn)
        self.mainLayout.addWidget(self.fourthCapitalBtn)
        self.mainLayout.addWidget(self.emptyLabel)
        self.mainLayout.addWidget(self.newCountryBtn)
        self.mainLayout.addWidget(self.quitBtn)

        self.setCentralWidget(self.w)

    def onClickCheckCountryCapital(self, number):
        answer = self.capital_choices[number]
        city = self.country_data.get('city')

        if answer == city:  # mismatching handler
            self.resultLabel.setText("That's right!")
            # Unlock the button if answer is right
            self.newCountryBtn.setEnabled(True)
        else:
            self.mistakes += 1
            if self.mistakes == 10:  # attempt amount
                self.close()

            self.resultLabel.setText(f"You didn't guess! "
                                     f"The attempt №{self.mistakes + 1}")


    def onClickNewCountry(self):
        # Quit from the app if all countries have been before
        if len(self.countries.CACHE) == len(self.countries.CBC):
            self.close()

        self.resultLabel.setText('')

        # Set new country parameters
        self.initNewCountryData()

    def onClickQuit(self):
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.onClickNewCountry()
        if e.key() == Qt.Key_Escape:
            self.onClickQuit()
