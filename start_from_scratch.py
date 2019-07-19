import kivy
from card_functions import order_cards, isSingle, isChain, isDuplicate, isChop
from random import shuffle
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from os import path	
faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
suits = ['S', 'C', 'D', 'H']		
Builder.load_file("new_start.kv")
		
class Game():
	def __init__(self):
	self.players =	[Player("Player 0"), Player("Player 1")]	
	self.game_loop(self.players)

def game_setup(players):
	deck = Deck()
	deck.deal(players)
	current_player = self.find_lowest_card(players)
	current_play = Play()
	

class WindowManager(ScreenManager):
	pass
	
class HowManyPlayers(Screen):
	humans = ObjectProperty(None) #how many humans selected
	shape_shifter_o = ObjectProperty(None) #button info that changes from btn to label depending on if an option was selected
	def on_shape_shifter_o(self, instance, value):#removes button or label and replaces it
		self.remove_widget(self.ids.shape_shifter)
		self.ids.shape_shifter = value
		self.add_widget(self.ids.shape_shifter)
		if isinstance(self.ids.shape_shifter, Button):
			self.ids.shape_shifter.bind(on_release = self.change_screen)
		
	#def create_players(self, instance):
	#	players = []
		#for i in range(int(self.humans)):
		#	players.append(Player("Player " + str(i)))
	#	return players
		
	def change_screen(self, instance):
		#players = self.create_players(instance)
		sm.add_widget(GameScreen())
		sm.current = "game"
		
class Human(ToggleButton):
	def on_state(self, instance, value):
		if value == "down":
			hmp.humans = self.text
			hmp.shape_shifter_o = Button(text = hmp.ids.shape_shifter.text,size_hint = hmp.ids.shape_shifter.size_hint,pos_hint = hmp.ids.shape_shifter.pos_hint)

		elif value == "normal":
			hmp.humans = ""
			hmp.shape_shifter_o = Label(text = hmp.ids.shape_shifter.text,size_hint = hmp.ids.shape_shifter.size_hint,pos_hint = hmp.ids.shape_shifter.pos_hint)

class Grid(GridLayout):
	pass


class HUD(GridLayout):
	pass
	
class PlayerGrid(GridLayout):
	cards = ObjectProperty()
	def __init__(self, name, **kwargs):
		super(PlayerGrid, self).__init__(**kwargs)
		self.name = name
		self.pos_hint = {"bottom":1} if self.player.name == "Player 0" else {"top":1}	#dependent on player
		self.display_children(self.cards)
		self.hand = []
		
	#def on_cards(self, instance, value):
	#	self.clear_widgets()
	#	self.display_children(value)
			
#	def display_children(self, cards):
#		for card in cards:
#			self.add_widget(CardButton(self.cards))
#	play = ObjectProperty()
			
	
	#def return_cards(self, cards):
	#	for card in cards:
	#		self.hand.append(card)
		
	#def use_cards(self, hand):
	#	i = len(hand) - 1
	#	cards = []
	#	while i >=0:
	#		if hand[i].state == "down":
	#			cards += hand.pop(i)
	#		i-=1
	#	if Play(x).combo == False:
	#		self.return_cards(x)
	#	else:
	#		self.game.play(Play(x))
	#		
	#def order_hand(self, hand):	
	#	return order_cards(hand)
	
	def on_play(self, instance, value):
		self.use_cards(self.hand)
	
					
class Field(GridLayout):
	current_play = ObjectProperty(None)
	def __init__(self, game, **kwargs):
		super(Field, self).__init__(**kwargs)	
		self.game = game
		self.current_play = self.game.current_play
		
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.game.current_player.play(touch)
			
	def on_current_play(self, instance, play):
		self.clear_widgets()
		for card in play.cards:
			self.add_widget(card)

class CardButton(Button):
	def __init__(self, info, game, **kwargs):
		super(CardButton, self).__init__(**kwargs)
		self.background_normal = "Pictures/JPEG/" + self.face + self.suit + ".jpg"
		self.game = game
	
	def on_state(self, instance, value):
		self.game.current_player.hand[self.name].state = "selected"

class Game(Screen):
	def __init__(self):
		self.players = [Player("Player " + str(i), self) for i in range(4)]
		self.deck = Deck()
		self.current_play = Play(None)		
		self.current_player = None
		self.run()

		
	def run(self):
		hands_ = [player.hand for player in self.players]
		hands_ = self.deck.deal(deck = self.deck, hands = hands_ )	#1
		self.current_player = self.find_lowest_card(self.players)			#2
		
		
#algorithm to find the lowest card in the players' hands which decides who goes first	
	def find_lowest_card(self, players): 
		values = []
		for player in players:
			for card in player.hand:
				values.append(card.value)
		lowest_card = min(values)
		for player in players:
			for card in player.hand:
				if card.value == lowest_card:
					return player

#called by field to change turns
	def next_turn(self):	#doesn't work yet
		i = 0
		for player in self.players:
			if player == self.current_player: break
			i+=1
		i += 1 #adds turn kinda
		
		if i == len(self.players): i = 0
		self.current_player = self.players[i]	
	
	def play(self,play):
		combo = self.current_play.combo 
		if combo == "free" or (combo == play.combo and self.current_play.value < play.value):
			self.current_play = play
		else:
			print("Not a valid combo/value")
			self.current_player.return_cards(Play.cards)
		
class Play(GridLayout):
	def __init__(self, cards):
		self.cards = cards
		self.combo = "free" #self.run_tests(self.cards)
		self.value = 0 # self.get_value(self.cards)
		
		
#takes cards and returns the card combo
	def run_tests(self, cards):
		if cards == None:
			combo = "free"
		elif isSingle(cards):
			combo = "single"
		elif isChop(cards):
			combo = "chop"
		elif isDuplicate(cards, 2):
			combo = "double"
		elif isDuplicate(cards, 3):
			combo = "triple"
		elif isDuplicate(cards, 4):
			combo = "bomb"
		elif isChain(cards):
			combo = "chain"
		else:
			combo = False
		return combo
				
	def get_value(self, cards):
		if isSingle(cards):
			total = cards[0].value
		else:
			total = 0
			for card in cards:
				total += card.value
		return total

class Deck():
	def __init__(self):
		self.cards = []
		faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
		suits = ['S', 'C', 'D', 'H']			
		for face in faces:
			for suit in suits:
				self.cards.append(Card(face, suit))		
		shuffle(self.cards)
		
#takes hands (lists) and deals cards until there are no more		
	def deal(self, hands, cards):	
		while cards:
			for hand in hands:
				hand.append(cards.pop())
		return hands
		
class Card(ToggleButton):
	def __init__(self, face, suit, **kwargs):
		super(Card, self).__init__(**kwargs)
		self.face = face
		self.suit = suit
		self.value = self.get_value(self.face, self.suit)
		self.text = self.face + self.suit

		
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
	

class ThirteenApp(App):
	
	def build(self):
		Window.clearcolor = [1, 0, 0, 1]
		Window.size = (560,940)
		Window.left = 0
		Window.top = 25
		return Game()
			
if __name__ == '__main__':
	app = ThirteenApp()
	app.run()
