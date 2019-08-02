import kivy
from random import shuffle
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from os import path	
import copy

faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
suits = ['S', 'C', 'D', 'H']		
Builder.load_file("thirteen2_.kv")

class WindowManager(ScreenManager):
	pass
	
class HowManyPlayers(Screen):	#NOT IMPLEMENTED FULLY
	humans = ObjectProperty(None) #how many humans selected
	shape_shifter_o = ObjectProperty(None) #button info that changes from btn to label depending on if an option was selected
	def on_shape_shifter_o(self, instance, value):#removes button or label and replaces it
		self.remove_widget(self.ids.shape_shifter)
		self.ids.shape_shifter = value
		self.add_widget(self.ids.shape_shifter)
		if isinstance(self.ids.shape_shifter, Button):
			self.ids.shape_shifter.bind(on_release = self.change_screen)
		
	def create_players(self, instance):
		players = []
		for i in range(int(self.humans)):
			players.append(Player("Player " + str(i)))
		return players
		
	def change_screen(self, instance):
		#players = self.create_players(instance)
		#sm.add_widget(Game(players))
		sm.current = "game"
		
class Human(ToggleButton):	#NOT IMPLEMENTED FULLY
	def on_state(self, instance, value):
		if value == "down":
			hmp.humans = self.text
			hmp.shape_shifter_o = Button(text = hmp.ids.shape_shifter.text,size_hint = hmp.ids.shape_shifter.size_hint,pos_hint = hmp.ids.shape_shifter.pos_hint)

		elif value == "normal":
			hmp.humans = ""
			hmp.shape_shifter_o = Label(text = hmp.ids.shape_shifter.text,size_hint = hmp.ids.shape_shifter.size_hint,pos_hint = hmp.ids.shape_shifter.pos_hint)

class FieldGrid(GridLayout):
	game = ObjectProperty()
	current_play = ObjectProperty()
	def __init__(self, game, **kwargs):
		super(FieldGrid, self).__init__(**kwargs)
		self.started = False
		self.game = game
		self.current_play = self.game.get_current("play")
		self.started = True
		
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			game = self.game.new_play()
			if game:
				gs.change_game()					
	
	def cards_changed(self, current_cards, new_cards):
		return current_cards != new_cards
		
	def on_game(self, instance, value):
		if self.started:
			new_play = self.game.get_current("play")
			if isinstance(new_play, Play):
				self.update_current_play(new_play)
				
	def update_current_play(self, new_play):
		if self.cards_changed(self.game.get_actual_current_play(), new_play.cards):
			self.current_play = new_play
	
	def on_current_play(self, instance, value):
		if self.children: self.clear_widgets()
		if value.cards:
			for card in value.cards: self.add_widget(CardButton(card))
		else: self.add_widget(Label(text = "Tap here to make play"))	
	
class CardButton(ToggleButton):
	def __init__(self, card, **kwargs):
		super(CardButton, self).__init__(**kwargs)		
		self.card = card
		self.background_normal = "Pictures/JPEG/" + self.card.face + self.card.suit + ".jpg"
	
	def on_state(self, instance, value):
		self.card.selected = True if value == "down" else False

class PlayerGrid(GridLayout):

#A. Takes Game() and Player()
#A. Hand is ObjectProperty(), points to PLayer().hand

#1. When self.hand is set in the init, on_hand is called
#2. When Game() gets changed,on_game gets called
#3a. If the hand changed, hand will update.
#term - 3b. If hand is the same, nothing gets updated
#term - 4a. on_hand is called, which updates screen	"""
	game = ObjectProperty()
	hand = ListProperty([])
	def __init__(self, game, player, **kwargs):
		super(PlayerGrid, self).__init__(**kwargs)	
		self.player = player
		self.hand = self.player.hand
		self.game = game
		self.pos_hint = {"bottom": 1} if self.player.name == "Player 0" else {"top": 1}
		
	def hand_changed(self, current_hand, new_hand):
		return current_hand != new_hand
				
	def on_game(self, instance, value):
		if self.hand_changed(self.hand, self.player.hand):
			self.hand = self.player.hand
			
	def on_hand(self, instance, value):
		if self.children: self.clear_widgets()
		for item in value:
			self.add_widget(CardButton(item))
			
class GameScreen(Screen):
	game = ObjectProperty()
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.game = Game()
		self.display_grids(self.game)
		
	def display_grids(self, game):
		for player in game.players : 
			p = PlayerGrid(self.game, player)
			self.ids.layout.add_widget(p)
		self.ids.layout.add_widget(FieldGrid(self.game))
		self.ids.layout.add_widget(CurrentPlayer(self.game))
		
	def change_game(self):
		self.game = copy.copy(self.game)
			
		
	def on_game(self, instance, value):
		for child in self.children[0].children:
			child.game = value
			try:
				child.game = value
			except:
				continue
				
		print("New Game: ", value)
		
class CurrentPlayer(Label):
	current_player = ObjectProperty()
	game = ObjectProperty()
	def __init__(self, game, **kwargs):
		super(CurrentPlayer, self).__init__(**kwargs) 
		self.game = game
		self.current_player = self.game.get_current("player")
	
	def on_game(self, instance, value):
		self.current_player = value.get_current("player")
		print("current player game changed")
		
	def on_current_player(self, instance, value):
		self.text = value.name
			
class Game():
	def __init__(self):
		self.players = [Player("Player 0", self), Player("Player 1", self)]
		self.start_game()
		self.field = Field(self)
		
	def start_game(self):
		self.deal_cards(self.players)

	def deal_cards(self, players):	#1
		hands = [players[0].hand, players[1].hand, [], []]
		cards = []
		faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
		suits = ['S', 'C', 'D', 'H']			
		for face in faces:
			for suit in suits:
				cards.append(Card(face, suit))		
		shuffle(cards)
		while cards:
			for hand in hands:
				hand += [cards.pop()]
	
	def get_current(self, x):
		return self.field.get_current(x)
		
	def get_plays(self):
		return self.field.get_plays()
	
	def get_actual_current_play(self):
		return self.field.get_actual_current_play()
		
	def new_play(self):
		current_player = self.get_current("player")
		play = current_player.play()
		verdict = self.field.play(play, self.players)
		if verdict == False and play.cards: current_player.addCards(play.cards)
		return verdict
				
class Field():
#mainly deals with current gamestate affairs
	def __init__(self, game, **kwargs):
		super(Field, self).__init__(**kwargs)	
		self.game = game
		self.lowest_value = self.get_lowest_value(self.game.players)
		self.plays = [Play()]
		self.player = self.first_to_go(self.lowest_value, self.game.players)
		self.first_turn = True
		self.free_pass = False
		
	def get_lowest_value(self, players):
		values = []
		for player in players:
			for card in player.hand:
				values.append(card.value)
		return min(values)

	def first_to_go(self, lowest_value, players):
		for player in players:
			for card in player.hand:
				if card.value == lowest_value:
					return player

	def play(self, play, players):	#called by Player()'s play() method
		current_play = self.get_current("play")
		if self.isValid(current_play, play):
			self.player = self.nextTurn(self.player, players)
			self.addPlay(play)
			return True
		else:
			return False
				
	def nextTurn(self, current_player, players):
		for i in range(len(players)):
			if current_player == players[i]:
				break
		if i == len(players) - 1:
			print("It is now , " , players[0].name, "'s turn")
			return players[0]
		else:
			print("It is now , " , players[i+1].name, "'s turn")
			return players[i+1]
		
	def isValid(self, current_play, new_play):
		if self.first_turn:
			if new_play.get_combo() == "pass":
				print("Player with lowest card goes first!")
				return False
			else:
				verdict = False
				for card in new_play.cards:
					if card.value == self.lowest_value:
						self.first_turn = False
						verdict = True
						return verdict
						break
				if verdict == False: 
					print("You must use your lowest card first")
					
		elif new_play.get_combo() == "pass":
			return True
		else:
			if new_play.value <= current_play.value:
				print("That card(s) value too low. Try again...")
				return False
			elif new_play.get_combo() != current_play.get_combo():
				print("What you put was not a " + current_play.get_combo())
				return False
			else:
				return True	
				
	def addPlay(self, play):
		self.plays.insert(0, play)
		print("these are all the plays: " , self.plays)
		
	def get_current(self, x):
		if x == "player":
			return self.player
		elif x == "play":
			return self.plays[0]
	
	def get_plays(self):
		return self.plays

	def get_actual_current_play(self):
		for play in self.plays:
			if play.combo != "pass":
				return play
				break
	
	def free_play(self):
		i = 0
		for play in self.plays:
			if play.combo == "pass":
				i+= 1
		if i == len(self.game.players) - 1:
			self.plays.addPlay(Play(combo = None))
				
class Player():
	def __init__(self, name, game):
		self.name = name
		self.game = game
		self.hand = []

	def play(self): 
		hand_copy = self.hand[:]
		i = 0
		selected = []
		while i < len(hand_copy):
			if hand_copy[i].selected:
				selected.append(hand_copy.pop(i))
				continue
			i+=1
		if selected:
			print("Old hand len: ", len(self.hand), "new_hand length", len(hand_copy))
			play = Play(selected)
			if play.combo:
				print("play gets returned")
				self.hand = hand_copy
				return play
			else:
				self.hand += selected
				print("This is not a valid combo")
				return False

		else:
			return Play()
			
	def order_hand(self, hand):
		value = dict()
		for card in hand:	#makes each card's value a key for the card
			value[card.value] = card
		list_value = sorted(list(value))	#converts all the keys to an ordered list
		new_list = list()
		for item in list_value:
			new_list.append(value[item])
		return new_list

	def addCards(self, cards):	
		self.hand += cards

	def getHand(self):	
		return self.hand
	
	def getName(self):
		return self.name
	
class Play():
	def __init__(self, cards = None, combo = self.get_combo(), **kwargs):
		self.cards = cards
		self.combo = self.get_combo()
		self.value = self.get_value(self.cards)
		
		
	def get_value(self, cards):
		if cards:
			total = 0
			for card in cards:
				total += card.value
			return total
		else:
			return None
	
	def run_tests(self, cards):
		if cards == None:
			return "pass"
		elif self.isSingle():
			return "single"
		elif self.isChop():
			return "chop"
		elif self.isDouble():
			return "double"
		elif self.isTriple():
			return "triple"
		elif self.isChop():
			return "bomb"
		elif self.isChain():
			return "chain"
		else:
			return False
		
	def isSingle(self):
		return self.cards[0] == self.cards[len(self.cards)-1]
			
	def isChain(self): 
		identity = True		#if true, it means its a chain and vice versa
		if len(self.cards)< 3:	
			identity = False
		else:
			order = Player("Test").order_cards(self.cards)
			for i in range(len(order)):
				if i == 0:
					identity = int(order[i].value + 1) != int(order[i+1].value)
				elif i == len(order) -1:
					identity = int(order[i].value - 1) != int(order[i-1].value)
				elif i > 0 and i < len(order) - 1: #doesnt work yet?
					identity = (int(order[i].value + 1) != int(order[i+1].value)) and (int(order[i].value - 1) != int(order[i-1].value))
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
		
	def isBomb(self):
		identity = True
		trip = []
		if len(self.cards) != 4:
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
	
	def get_combo(self):
		return self.run_tests(self.cards)
		
class Card():	#perfect
	def __init__(self, face, suit):
		self.face = face
		self.suit = suit
		self.value = self.get_value(self.face, self.suit)
		self.text = self.face + self.suit
		self.selected = False
		
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
		

sm = WindowManager()
hmp = HowManyPlayers()
sm.add_widget(hmp)
gs = GameScreen()
sm.add_widget(gs)


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
