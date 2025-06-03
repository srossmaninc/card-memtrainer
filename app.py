from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout, QComboBox
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import copy
import random
import sys, os

class Card:
    def __init__(self, img_name):
        self.img_name = img_name

        # get numeric val. for ordering
        name_chars = list(img_name)
        val_unparsed = name_chars[0]
        self.val_raw = val_unparsed
        
        self.suit = name_chars[1]

        match val_unparsed:
            case "A":
                self.val = 14
            case "K":
                self.val = 13
            case "Q":
                self.val = 12
            case "J":
                self.val = 11
            case "T":
                self.val = 10
            case other:
                self.val = int(other)

        # whether or not this card has been flipped up
        self.seen = False
        pass

    def gen_path(self):
        return f"{CARD_DIR}{self.img_name}.png"
    
    def __str__(self):
        return f"{self.val_raw} of {self.suit}"

CARD_DIR = './assets/cards/'
CARD_BACK = './assets/card-backs/1B.png'
CARD_SIZE_W = 150
unicode_spades = "\u2660"
unicode_hearts = "\u2665"
unicode_diamonds = "\u2666"
unicode_clubs = "\u2663"

base_deck = []
for f in os.listdir(CARD_DIR):
    if f.endswith('.png'):
        cname = f.split('.')[0]
        base_deck.append(Card(cname))

class MainWindow(QMainWindow):
    display_cards = []
    deck = copy.deepcopy(base_deck)

    num_cards = 1

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Card MemTrainer")
        layout = QGridLayout()

        card_back = QLabel()
        print(card_back.size())
        cb_pixmap = QPixmap(CARD_BACK)
        # card_back.setScaledContents(True)
        cb_pixmap = cb_pixmap.scaledToWidth(CARD_SIZE_W, Qt.TransformationMode.SmoothTransformation)
        card_back.setPixmap(cb_pixmap)
        print(card_back.size())

        # w225xh315
        card_w = CARD_SIZE_W
        card_h = 5
        print(f"w{card_w}xh{card_h}")

        c1 = QLabel("1")
        c2 = QLabel("2")
        c3 = QLabel("3")
        c4 = QLabel("4")
        c5 = QLabel("5")
        # card_back.resize(card_w, card_h)
        # c1.resize(card_w, card_h)
        # c2.resize(card_w, card_h)
        # c3.resize(card_w, card_h)
        # c4.resize(card_w, card_h)
        # c5.resize(card_w, card_h)

        title_txt_font = QFont('Times', 30)
        title = QLabel("Card Memtrainer")
        title.setFont(title_txt_font)

        self.deck_count = QLabel(f"[ Deck Size: {len(self.deck)} ]")

        new_card_button = QPushButton("New Card(s)")
        new_card_button.setCheckable(False)
        new_card_button.clicked.connect(self.new_cards)

        reshuffle_button = QPushButton("Reshuffle")
        reshuffle_button.setCheckable(False)
        reshuffle_button.clicked.connect(self.reshuffle)

        layout.setColumnMinimumWidth(1, card_w)
        layout.setColumnMinimumWidth(2, card_w)
        layout.setColumnMinimumWidth(3, card_w)
        layout.setColumnMinimumWidth(4, card_w)
        layout.setColumnMinimumWidth(5, card_w)

        layout.addWidget(title, 0, 0)
        layout.addWidget(self.deck_count, 0, 1)
        layout.addWidget(new_card_button, 3, 0)
        layout.addWidget(reshuffle_button, 3, 1)
        layout.addWidget(card_back, 1, 0)
        layout.addWidget(c1, 1, 1)
        layout.addWidget(c2, 1, 2)
        layout.addWidget(c3, 1, 3)
        layout.addWidget(c4, 1, 4)
        layout.addWidget(c5, 1, 5)

        self.display_cards.append(c1)
        self.display_cards.append(c2)
        self.display_cards.append(c3)
        self.display_cards.append(c4)
        self.display_cards.append(c5)

        # layout.setSpacing(20)

        card_num_select = QComboBox()
        card_num_select.addItems(["1", "3", "5"])
        card_num_select.currentIndexChanged.connect( self.index_changed )
        layout.addWidget(card_num_select, 0, 5)

        # suit lists
        self.spades_left = QLabel(f"{unicode_spades}: {self.gen_remaining('S')}")
        self.hearts_left = QLabel(f"{unicode_hearts}: {self.gen_remaining('H')}")
        self.diamonds_left = QLabel(f"{unicode_diamonds}: {self.gen_remaining('D')}")
        self.clubs_left = QLabel(f"{unicode_clubs}: {self.gen_remaining('C')}")
        layout.addWidget(self.spades_left, 4, 0)
        layout.addWidget(self.hearts_left, 5, 0)
        layout.addWidget(self.diamonds_left, 6, 0)
        layout.addWidget(self.clubs_left, 7, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def reshuffle(self):
        self.deck = copy.deepcopy(base_deck)

        print(f"hit! {len(base_deck)} -> {len(list(filter(lambda x: not x.seen, base_deck)))}")

        sizeof_usable_deck = len(list(filter(lambda x: not x.seen, self.deck)))
        # print(f"new card from deck of size {sizeof_usable_deck}")
        self.deck_count.setText(f"[ Deck Size: {sizeof_usable_deck} ]")

    def new_cards(self):

        for idx, curr_card in enumerate(random.sample(list(filter(lambda x: not x.seen, self.deck)), self.num_cards)):
            curr_card.seen = True
            self.display_cards[idx].setPixmap(QPixmap(curr_card.gen_path()).scaledToWidth(CARD_SIZE_W, Qt.TransformationMode.SmoothTransformation))

        sizeof_usable_deck = len(list(filter(lambda x: not x.seen, self.deck)))
        # print(f"new card from deck of size {sizeof_usable_deck}")
        self.deck_count.setText(f"[ Deck Size: {sizeof_usable_deck} ]")

        self.spades_left.setText(f"{unicode_spades}: {self.gen_remaining('S')}")
        self.hearts_left.setText(f"{unicode_hearts}: {self.gen_remaining('H')}")
        self.diamonds_left.setText(f"{unicode_diamonds}: {self.gen_remaining('D')}")
        self.clubs_left.setText(f"{unicode_clubs}: {self.gen_remaining('C')}")

        # filter by "has been flipped up", sample 1,3,5

    def index_changed(self, idx):
        match idx:
            case 0:
                self.num_cards = 1
            case 1:
                self.num_cards = 3
            case 2:
                self.num_cards = 5

    # there is 100% a better way to do this that isn't O(n^2)
    def gen_remaining(self, suit):
        ret_string = ""
        filtered_deck = list(filter(lambda x: x.suit == suit, self.deck))
        # for elem in filtered_deck:
        #     print(elem)
        # filtered_deck_seen = filter(lambda y: not y.seen, filtered_deck)
        for i in range(14, 1, -1):
            for c in filtered_deck:
                if c.val == i:
                    if c.seen:
                        ret_string += " "
                    else:
                        ret_string += c.val_raw
                    break
        return ret_string

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()