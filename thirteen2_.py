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
faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
suits = ['S', 'C', 'D', 'H']		
Builder.load_file("thirteen2_.kv")

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
		
	def create_players(self, instance):
		players = []
		for i in range(int(self.humans)):
			players.append(Player("Player " + str(i)))
		return players
		
	def change_screen(self, instance):
		#players = self.create_players(instance)
		#sm.add_widget(Game(players))
		sm.current = "game"
		
class Human(ToggleButton):
	def on_state(self, instance, value):
		if value == "down":
			hmp.humans = self.text
			hmp.shape_shifter_o = Button(text = hmp.ids.shape_shifter.text,size_hint = hmp.ids.shape_shifter.size_hint,pos_hint = hmp.ids.shape_shifter.pos_hint)

		elif value == "normal":
			hmp.humans = ""
			hmp.shape_shifter_o = Label(text = hmp.ids.shape_shifter.text,size_hint = hmp.ids.shape_shifter.size_hint,pos_hint = hmp.ids.shape_shifter.pos_hint)

class FieldGrid(GridLayout):
	def __init__(self, field, **kwargs):
		super(FieldGrid, self).__init__(**kwargs)
		self.field = field
	
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			#self.field.current["player"].play()
			#self.game.play()
			self.field.play()
		
class CardButton(ToggleButton):
	def __init__(self, card, **kwargs):
		super(CardButton, self).__init__(**kwargs)		
		self.card = card
		self.background_normal = "Pictures/JPEG/" + self.card.face + self.card.suit + ".jpg"
	
	def on_state(self, instance, value):
		self.card.selected = True if value == "down" else False
		
class PlayerGrid(GridLayout):
	hand = ListProperty([])
	def __init__(self, player, **kwargs):
		super(PlayerGrid, self).__init__(**kwargs)	
		self.player = player
		self.player.hand = self.hand
		self.pos_hint = self._setPosition(self.player.name)
		
	def _setPosition(self, name):
		if name == "Player 0":
			return {"bottom": 1}
		else:
			return {"top":1}	
	
	def on_hand(self, instance, value):
		self.clear_widgets()
		for item in value:
			self.add_widget(CardButton(item))
	
class GameScreen(Screen):
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.game = Game()	
		self.dic = {}
		self.display_grids(self.game)
		self.game.start_game()

		
	def display_grids(self, game):
		for player in game.players : 
			p = PlayerGrid(player)
			self.dic[player.name] = p
			self.ids.layout.add_widget(p)
		self.ids.layout.add_widget(FieldGrid(self.game.field))
		self.ids.layout.add_widget(CurrentPlayer(self.game.field.current))
		#self.ids.layout.add_widget(CurrentPlayer(game.field))
class CurrentPlayer(Label):
	my_current = ObjectProperty({})
	def __init__(self, current, **kwargs):
		super(CurrentPlayer, self).__init__(**kwargs) 
#class CurrentPlayer(Label):
#	currentplayer = ObjectProperty()
#	def __init__(self, field, **kwargs):
#		super(CurrentPlayer, self).__init__(**kwargs)
#		self.field = field
#		self.current_player = self.field.current["player"]
#		self.text = self.current_player.name
			
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
	
	def next_turn(self, player):
		print("Next Turn runs")
		for i in range(len(self.players)):
			if player == self.players[i]:
				break
		print(i)
		if i == len(self.players) - 1:
			print("It is now , " , self.players[0].name, "'s turn")
			return self.players[0]
		else:
			print("It is now , " , self.players[i+1].name, "'s turn")
			return self.players[i+1]
				
class Field(EventDispatcher):
	current_player = ObjectProperty()
	def __init__(self, game, **kwargs):
		super(Field, self).__init__(**kwargs)	
		self.game = game
		self.current = {"play": None, "player": self._find_lowest_card(self.game.players)}
		self.turns = 0
		
	def _find_lowest_card(self, players): #2
		values = []
		for player in players:
			for card in player.hand:
				values.append(card.value)
		lowest_card = min(values)
		for player in players:
			for card in player.hand:
				if card.value == lowest_card:
					return player

	def play(self):	#called by Player()'s play() method
		player = self.current["player"]
		play = player.play()
		if play == "pass":
			self.current["play"] = play
			self.current["player"] = self.game.next_turn(player)
		elif play == False:
			print("Try again but with a valid combo this time")
		else:
			if isValid(x, self.current["play"]):
				self.current["play"] = play
				self.current["player"] = self.game.next_turn(player)
				
			

		#if play == "pass":
		#	self.game.next_turn()
		#elif self.is_Valid(play, self.current["play"]):
		#	self.current["play"] = play
		#else:
		#	self.returnCards(self.current["player"], play.cards)
		
	def returnCards(self, player, cards):
		for card in cards: player.hand.append(card)
		
	def is_Valid(self, new_play, current_play):
		if current_play == None:
			count = False
			for card in new_play.cards:
				if card.face == "3":
					count = True
			return count
		else:
			if new_play.value <= current_play.value:
				print("That card(s) value too low. Try again...")
				return False
			elif new_play.combo != current_play.combo:
				print("What you put was not a " + current_play.combo)
				return False
			else:
				return True	
				
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
			if play == False:
				self.hand += selected
				return False
			else:
				self.hand = hand_copy
				return play
		else:
			return "pass"
			

	def order_hand(self, hand):
		value = dict()
		for card in hand:	#makes each card's value a key for the card
			value[card.value] = card
		list_value = sorted(list(value))	#converts all the keys to an ordered list
		new_list = list()
		for item in list_value:
			new_list.append(value[item])
		return new_list

class Play():
	def __init__(self, cards):
		self.cards = cards
		#self.combo = self.run_tests()
		self.value = self.get_value(self.cards)
		
		
	def get_value(self, cards):
		if cards:
			total = 0
			for card in cards:
				total += card.value
			return total
		else:
			return None
	
	def run_tests(self):
		if self.cards == None:
			combo = "pass"
		elif self.isSingle():
			combo = "single"
		elif self.isChop():
			combo = "chop"
		elif self.isDouble():
			combo = "double"
		elif self.isTriple():
			combo = "triple"
		elif self.isChop():
			combo = "bomb"
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
