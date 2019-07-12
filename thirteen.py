import kivy
from random import shuffle, choice
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from os import path	
faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
suits = ['S', 'C', 'D', 'H']		
Builder.load_file("thirteen_.kv")

class WindowManager(ScreenManager):
	pass
	
class HowManyPlayers(Screen):
	humans = ObjectProperty(None)
	shape_shifter_o = ObjectProperty(None)
	def __init__(self, **kwargs):
		super(HowManyPlayers, self).__init__(**kwargs)
		self.shape_shifter = Label(text = "Play", size_hint = [.3,.1], pos_hint = {"right":1, "y":0 })
		self.add_widget(self.shape_shifter)
		self.hi = (Button(size_hint = [.1,.1]))
		self.add_widget(self.hi)
		self.players = []
		
	def on_humans(self, instance, value):#test method
		print("This is what humans changed to: " , value)

	def on_shape_shifter_o(self, instance, value):#removes button or label and replaces it
		self.remove_widget(self.shape_shifter)
		self.shape_shifter = value
		self.add_widget(self.shape_shifter)
		if isinstance(self.shape_shifter, Button):
			self.shape_shifter.bind(on_press = self.create_players) 
			self.shape_shifter.bind(on_release = self.change_screen)
		
	def create_players(self, instance):
		players = []
		for i in range(int(self.humans)):
			self.players.append(Player("Player " + str(i)))
			
	def change_screen(self, instance):
		sm.add_widget(Game(self.players))
		sm.current = "game"
		
class Human(ToggleButton):
	def on_state(self, instance, value):
		if value == "down":
			hmp.humans = self.text
			hmp.shape_shifter_o = Button(text = hmp.shape_shifter.text,size_hint = hmp.shape_shifter.size_hint,pos_hint = hmp.shape_shifter.pos_hint)

		elif value == "normal":
			hmp.humans = ""
			hmp.shape_shifter_o = Label(text = hmp.shape_shifter.text,size_hint = hmp.shape_shifter.size_hint,pos_hint = hmp.shape_shifter.pos_hint)

class Game(Screen):
	def __init__(self, players, **kwargs):
		super(Game, self).__init__(**kwargs)
		self.name = "game"
		self.players = players
		self.play_to_beat = None
		self.players_dict = self.set_players_dict(self.players)
		self.current_player = None
		self.deck = Deck()
		for player in self.players:
			self.add_widget(player)
		self.add_widget(Field())
		self.start()
		
	def set_players_dict(self, players):	#works
		new_dict = {}
		for player in players:
			new_dict[player.name] = player
		return new_dict
		
	def start(self):
		self.deal()
		self.current_player = self.find_lowest_card(self.players)
		
	def deal(self):	#works
		hands = []
		for i in range(4):
			hands.append(self.deck.deal(13))
		for player in self.players:
			player.hand = hands.pop()
	
	def find_lowest_card(self, players): #works, not yet being uitlized
		values = []
		for player in players:
			for card in player.hand:
				values.append(card.value)
		lowest_card = min(values)
		for player in players:
			for card in player.hand:
				if card.value == lowest_card:
					return player
		
class Grid(GridLayout):
	pass

class Card(ToggleButton):
	def __init__(self, face, suit, **kwargs):
		super(Card, self).__init__(**kwargs)
		self.face = face
		self.suit = suit
		self.value = self.get_value(self.face, self.suit)
		self.text = self.face + self.suit
		self.background_normal = "Pictures/JPEG/" + self.face + self.suit + ".jpg"
		
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
		
	def on_state(self, instance, value):#works
		tog = self.parent.current_play
		if isinstance(self.parent, Player): 
			if value == "down":
				tog.append(self)
			else:
				try:
					for i in range(len(tog)):
						if tog[i] == self:
							tog.pop(i)
				except:
					print("MMMM")
		
class Deck():
	def __init__(self):
		self.cards = self.initialize_deck()
		
	def deal(self, number):	#takes a number and returns a list of number * cards
		hand = []
		for i in range(number):
			hand.append(self.cards.pop())
		return hand
		
	def initialize_deck(self):
		cards = []
		faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
		suits = ['S', 'C', 'D', 'H']			
		for face in faces:
			for suit in suits:
				cards.append(Card(face, suit))		
		return cards
		
class Player(GridLayout):
	hand = ObjectProperty(None)
	def __init__(self, name, **kwargs):
		super(Player, self).__init__(**kwargs)
		#self.pos = None
		self.name = name
		print(self.name)
		if self.name == "Player 0":
			self.pos_hint = {"bottom": 1}
		else:
			self.pos_hint = {"top":1}
		self.turn = False
		self.current_play = []
	
	def make_play(self):
		p = Play(self.name, self.current_play)
		for card in p.cards:
			self.remove_widget(card)
		return p
			
	def on_hand(self, instance, value):
		self.display_cards(value)
				
	def display_cards(self, hand):	
		for card in hand:
			self.add_widget(card)
			
class Field(GridLayout):
	current_play = ObjectProperty(None)
	
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.current_play = self.parent.current_player.make_play()
			
	def on_current_play(self, instance, play):
		for card in play.cards:
			self.add_widget(card)
				
class Play():
	def __init__(self, player, cards):
		self.player = player
		self.cards = cards
		self.combo = self.run_tests()
		self.value = self.get_value(self.cards)
		
		
	def get_value(self, cards):
		total = 0
		if self.isSingle() == False:
			for card in cards:
				total += card.value
		else: total = cards[0].value
		return total
	
	def run_tests(self):
		if self.cards == "skip":
			combo = "skip"
		elif self.isSingle():
			combo = "single"
		elif self.isChop():
			combo = "chop"
		elif self.isDouble():
			combo = "double"
		elif self.isTriple():
			combo = "triple"
		elif self.isChain():
			combo = "chain"
		else:
			combo = False
		return combo
		
	def isSingle(self):
		return self.cards[0] == self.cards[len(self.cards)-1]
			
	def isChain(self): 
		identity = True		#if true, it means its a chain and vice versa
		if len(self.cards)< 3:	
			identity = False
		
		else:
			value = {}		#these 10 lines find the card and return the index from faces and then uses that index as a key to unlock each card, the keys are added to a list and ordered
			for card in self.cards:
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
				elif i > 0 and i < len(order) - 1: #doesnt work yet?
					if order[i] + 1 != order[i+1] and order[i] - 1 != order[i-1]:
						identity = False
						
		return identity
					
	def isDouble(self):
		identity = True
		dub = []
		if len(self.cards) != 2:
			identity  = False
		else:
			for card in self.cards:
				dub.append(card.face)
			identity = len(set(dub))== 1
		return identity
		
	def isTriple(self):
		identity = True
		trip = []
		if len(self.cards) != 3:
			identity  = False
		else:
			for card in self.cards:
				trip.append(card.face)
			identity = len(set(trip))== 1
			
		return identity
		
	def isChop(self):	#not complete
		chop = []
		new_list = []
		if len(self.cards) != 6:
			identity  = False
		else:
			for card in self.cards:
				chop.append(card.face)
			identity = len(set(chop)) == .5*len(chop)
	#	for i in range(len(faces)):
	#		val[faces[i]] = i
		
	#	for item in chop:
	#		new_list.append
		
		return identity		

sm = WindowManager()
hmp = HowManyPlayers()
sm.add_widget(hmp)

class ThirteenApp(App):
	
	def build(self):
		Window.clearcolor = [1, 0, 0, 1]
		Window.size = (560,940)
		Window.left = 0
		Window.top = 25
		return sm


if __name__ == '__main__':
	app = ThirteenApp()
	app.run()
