import kivy
from random import shuffle
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from os import path	
faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
suits = ['S', 'C', 'D', 'H']		

class Card(Button):
	def __init__(self, face, suit, **kwargs):
		super(Card, self).__init__(**kwargs)
		self.face = face
		self.suit = suit
		self.value = self.get_value(self.face, self.suit)
		
	def get_value(self, face, suit):
		return self.get_face_value()[face] + self.get_suit_value()[suit]
	
	def get_face_value(self):
		faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
		value = {}
		i = 0
		for item in faces:
			value[item] = i
			i+=1
		return value
			
	def get_suit_value(self):
		suits = ['S', 'C', 'D', 'H']
		value = {}
		k = 0
		for item in suits:
			value[item] = k
			k+=.1
		return value
		
class Deck():
	def __init__(self):
		self.deck = []
	
	def add_card(self, card):
		self.deck.append(card)
	
	def deal(self, number):	#takes a number and returns a list of number * cards
		hand = []
		for i in range(number):
			hand.append(self.deck.pop())
		return hand

class Player():
	def __init__(self, name):
		self.hand = []
		self.pos = None
		self.name = name
		self.turn = False
	
	def make_play(self, *cards):
		return Play(self.name, cards)		

class Field(RelativeLayout):
	current = ObjectProperty(None)
	def __init__(self, face, suit, card_facts, **kwargs):
		super(Field, self).__init__(**kwargs)	

class Play():
	def __init__(self, player, cards):
		self.t = Tests()
		self.player = player
		self.cards = cards
		self.type = None
		self.value = self.get_value(self.cards)
		
		
	def get_value(self, cards):
		total = 0
		if self.t.isSingle(self) == False:
			for card in cards:
				total += card.value
		else: total = cards[0].value
		return total

class Tests():
	
	def isSingle(self, play):
		return play.cards[0] == play.cards[len(play.cards)-1]
			
	def isChain(self, play):
		identity = True		#if true, it means its a chain and vice versa
		if len(play.cards)< 3:	
			identity = False
		
		else:
			value = {}		#these 10 lines find the card and return the index from faces and then uses that index as a key to unlock each card, the keys are added to a list and ordered
			for card in play.cards:
				c = 0
				for face in faces:
					if card.face == face:
						value[c] = card
						break
					c+=1
			
			
			order = []						
			for key in value:
				order.append(key)
			order.sort()
			for i in range(len(order)):
				if i == 0:
					if order[i] + 1 != order[i+1]:
						identity = False
				elif i == len(order) -1:
					if order[i] - 1 != order[i-1]:
						identity = False
						
		return identity
					
	def isDouble(self, play):
		identity = True
		if len(play.cards) != 2:
			identity  = False
		elif play.cards[0].face != play.cards[1].face:
			identity = False
		return identity
		
	def isTriple(self,play):
		identity = True
		trip = []
		if len(play.cards) != 3:
			identity  = False
		else:
			for card in play.cards:
				trip.append(card.face)
			identity = len(set(trip))== 1
			
		return identity
		
	def isChop(self,play):
		pass

d = Deck()
for face in faces:
	for suit in suits:
		d.add_card(Card(face, suit))
		
shuffle(d.deck)

p = Player("Trunks")
p.hand = d.deal(13)
p.hand[0].face = "4"
p.hand[3].face = "4"
p.hand[5].face = "4"
x = p.make_play(p.hand[0], p.hand[3],  p.hand[5])
print(x.t.isTriple(x))
