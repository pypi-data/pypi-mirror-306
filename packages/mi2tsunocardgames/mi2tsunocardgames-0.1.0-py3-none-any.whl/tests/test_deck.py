import pytest
from mi2tsunocardgames.deck import Deck

#デッキを生成したときの数を確認する
def test_deck_initialization():
  deck = Deck()
  assert len(deck.cards) == 52

#デッキを生成したとき既にシャッフルされているか確認する
def test_deck_shuffling():
  deck = Deck()
  unshuffled_cards = deck.cards[:]
  deck.__init__()
  assert deck.cards != unshuffled_cards

#デッキからカードを引いたときの数が51枚かを確認する
def test_deck_dealing_card():
  deck = Deck()
  card = deck.draw()
  assert card not in deck.cards
  assert len(deck.cards) == 51

#残り枚数の関数が正常か確認する
def test_deck_remaining_cards():
  deck = Deck()
  deck.draw()
  remaining_cards = deck.remaining_cards()
  assert remaining_cards == 51