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
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from os import path	
import copy

faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
suits = ['S', 'C', 'D', 'H']		
Builder.load_file("thirteen.kv")

def set_color(name):
	#takes player name and returns a color if yadayada
	return [1,.5,.5,1] if name == "Player 0" else [.5, .5, 1, 1]

class WindowManager(ScreenManager):
	pass
	
class CardImage(Image):
	state = StringProperty("")
	def __init__(self, card, **kwargs):
		super(CardImage, self).__init__(**kwargs)
		self.card = card
		self.states = {"normal": "Pictures/Cards/" + self.card.face + self.card.suit + ".png", "down": "Pictures/Cards/back.png"}
		self.state = "normal"
		self.allow_stretch = True
		self.keep_ratio = False
		
	def change_state(self):
		self.state = "down" if self.state == "normal" else "normal" 

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.change_state()

	def on_state(self, instance, value):
		self.source = self.states[value]
		self.card.selected = True if value == "down" else False
	
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
		self.current_play = self.game.get_actual_current_play()
		self.started = True
		
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			game = self.game.new_play()
			if game:
				gs.change_game(copy.copy(self.game))					
	
	def cards_changed(self, current_cards, new_cards):
		return current_cards != new_cards
		
	def on_game(self, instance, value):
		if self.started:
			new_play = self.game.get_actual_current_play()
			if isinstance(new_play, Play):
				self.update_current_play(new_play)
				
	def update_current_play(self, new_play):
		if self.cards_changed(self.game.get_actual_current_play(), new_play.cards):
			self.current_play = new_play
	
	def on_current_play(self, instance, value):
		if self.children: self.clear_widgets()
		if value.cards:
			for card in value.cards: self.add_widget(CardImage(card))
		else: self.add_widget(Label(text = "Tap here to make play"))	
	
class CardButton(ToggleButton):
	def __init__(self, card, **kwargs):
		super(CardButton, self).__init__(**kwargs)		
		self.card = card
		self.background_normal = "Pictures/Cards/" + self.card.face + self.card.suit + ".png"
		
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
		self.pos_hint = {"y": .05} if self.player.name == "Player 0" else {"top": .95}
		
	def hand_changed(self, current_hand, new_hand):
		return current_hand != new_hand
				
	def on_game(self, instance, value):
		if self.hand_changed(self.hand, self.player.hand):
			self.hand = self.player.hand
			
	def on_hand(self, instance, value):
		if self.children: self.clear_widgets()
		for item in value:
			self.add_widget(CardImage(item))
		self.size_hint[0] = 1 - ((13-len(self.children))/13)
		self.pos_hint = {"x" : .5 - (self.size_hint[0]/2)}	
			
class GameScreen(Screen):
	game = ObjectProperty()
	win_player = ObjectProperty()
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.newGame()
			
	def newGame(self):
		layout = self.children[0]
		if layout.children: layout.clear_widgets()
		self.setupEverything()
				
	def setupEverything(self):
		self.game = Game()
		self.display_grids(self.game)
		
	def display_grids(self, game):
		for player in game.players : 
			p = PlayerGrid(self.game, player)
			self.ids.layout.add_widget(p)
			self.ids.layout.add_widget(OrderButton(self.game, player))
		self.ids.layout.add_widget(FieldGrid(self.game))
		self.ids.layout.add_widget(CurrentPlayer(self.game))
		l = Label(text = "PLAYER 1", size_hint = [.1, .05]) 
		l.pos_hint = {"x" : .5 - (l.size_hint[0]/2), "top" : 1}
		self.ids.layout.add_widget(l)
		l = Label(text = "PLAYER 0", size_hint = [.1, .05]) 
		l.pos_hint = {"x" : .5 - (l.size_hint[0]/2)}
		self.ids.layout.add_widget(l)
		self.ids.layout.add_widget(FreePlay(self.game))
		self.ids.layout.add_widget(CombosGrid(self.game))

		
	def change_game(self, game_copy):
		self.game = game_copy
	
	def get_win_player(self):
		return self.win_player
		
	def on_game(self, instance, value):
		try:
			self.win_player = value.win_player
		except: 
			self.win_player = False
		
		for child in self.children[0].children:
			child.game = value
			try:
				child.game = value
			except:
				continue
		print("New Game: ", value)
		
	def on_win_player(self, instance, value):
		if isinstance(value, Player):
			sm.current = "win"
			screen = sm.get_screen("win")
			screen.set_player(value.name)

class OrderButton(Button):
	def __init__(self, game, player, **kwargs):
		super(OrderButton, self).__init__(**kwargs)	
		self.player = player
		self.game = game
		self.pos_hint =  {"y": .05+ .2} if self.player.name == "Player 0" else {"top": .95 - .2}	
		self.color = [1,.5,.5,1] if self.player.name == "Player 0" else [.5,.5,1,1]
		
	def on_press(self):
		self.player.order_hand()
		gs.change_game(copy.copy(self.game))
	
class WinScreen(Screen):
	player = StringProperty("")
	def set_player(self, name):
		self.player = name
	
class PlayAgainButton(Button):
	def on_press(self):
		sm.get_screen("game").newGame()
		sm.current = "game"
		
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
		self.color = set_color(value.name)
		self.text = value.name + " Go!"
	
class FreePlay(Label):
	game = ObjectProperty()
	free = BooleanProperty(False)
	def __init__(self, game, **kwargs):
		super(FreePlay, self).__init__(**kwargs) 
		self.game = game
		
	def on_game(self, instance, value):
		self.free = False if value.get_plays() else True
			
	def on_free(self, instance, value):
		if value:
			self.color = [0,0,1,1]
		else:
			self.color = [0,0,1,.2]

class CombosGrid(GridLayout):
	game = ObjectProperty()
	def __init__(self, game, **kwargs):
		super(CombosGrid, self).__init__(**kwargs)	
		self.combos = ["single", "double", "triple", "bomb", "chain", "chop"]
		self.default_color = [.5,.5,.5,1]
		self.activated_color = [0,0,1,1]
		self.game = game
		for combo in self.combos: self.add_widget(Label(text = combo.title(), color = self.default_color))
		
	def on_game(self, instance, value):
		print("signature")
		play = value.field.get_actual_current_play()
		if isinstance(play, Play):
			for child in self.children: 
				if child.text == play.get_combo().title(): 
					child.color = self.activated_color 
				else:
					child.color = self.default_color
		
class Game():
	def __init__(self, **kwargs):
		self.players = [Player("Player 0", self), Player("Player 1", self)]
		self.start_game()
		self.field = Field(self)
		self.win_player = None
		
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
		if play:
			verdict = self.field.play(play, self.players)
			if verdict == False and isinstance(play.cards, list): 
				current_player.addCards(play.cards)
			else:
				self.checkWin(self.players)
			return verdict
		else:
			return False
	
	def checkWin(self, players):
		for player in players:
			if player.hand == []:
				self.win_player = player
				break
				
class Field():
#mainly deals with Current gamestate affairs
	def __init__(self, game, **kwargs):
		self.game = game
		self.lowest_value = self.get_lowest_value(self.game.players)
		self.plays = []
		self.player = self.first_to_go(self.lowest_value, self.game.players)
		self.first_turn = True
		self.free_pass = False

	def play(self, play, players):	#called by Player()'s play() method
		current_play = self.get_actual_current_play()
		if current_play: print("New play = ", play.get_combo(), ", Current Play = ", current_play.get_combo())
		if self.isValid(current_play, play):
			self.player = self.nextTurn(self.player, players)
			self.addPlay(play)
			return True
		else:
			return False
		
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
		if current_play:
			if new_play.get_combo() == "pass":
				return True
			elif new_play.get_value() <= current_play.get_value():
				print("That card(s) value too low. Try again...")
				return False
			elif new_play.get_combo() != current_play.get_combo():
				print("What you put was not a " + current_play.get_combo())
				return False
			else:
				return True		
		else:
			if new_play.get_combo() == "pass":
				print("You gotta put something down!")
				return False
			elif self.first_turn:
				if self.hasLowest(new_play):
					self.first_turn = False
					return True
				else:
					return False
			else:
				return True
	
	def hasLowest(self, play):
		verdict = False
		for card in play.cards:
			if card.value == self.lowest_value:
				verdict = True
				return verdict
				break
		if verdict == False: 
			print("You must use your lowest card first")
	
	def get_current(self, x):
		if x == "player":
			return self.player
		elif x == "play":
			return self.plays[0]
	
	def get_plays(self):
		return self.plays

	def get_actual_current_play(self):
		if self.plays:
			for play in self.plays:
				if play.get_combo() != "pass":
					return play
					break
				
	def addPlay(self, play):
		plays = self.plays
		plays.insert(0, play)
		if self.free_play(plays):
			for i in range(len(plays)):
				plays.pop()
			print("FREE PLAY")
			
	def free_play(self, plays):
		i = 0
		for play in plays:
			if play.get_combo() == "pass":
				i+= 1
		return i == len(self.game.players) - 1
				
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
			if play.get_combo():
				self.hand = hand_copy
				return play
			else:
				print("This is not a valid combo")
				return False
		else:
			return Play(cards = "pass")
			
	def order_hand(self):
		value = {}
		for card in self.hand:	#makes each card's value a key for the card
			value[card.value] = card
		list_value = sorted(list(value))	#converts all the keys to an ordered list
		self.hand = [value[item] for item in list_value]

	def addCards(self, cards):	
		self.hand += cards

	def getHand(self):	
		return self.hand
	
	def getName(self):
		return self.name
	
class Play():
	def __init__(self, cards):
		self.cards = cards
	
	def get_value(self):
		if self.cards == "pass":
			return self.cards
		else:
			new_list = sorted([card.value for card in self.cards])
			return new_list[len(new_list)-1]
	
	def get_combo(self):
		if self.cards == "pass":
			return self.cards
		elif self.isSingle(self.cards):
			return "single"
		elif self.isChop(self.cards):
			return "chop"
		elif self.isDouble(self.cards):
			return "double"
		elif self.isTriple(self.cards):
			return "triple"
		elif self.isBomb(self.cards):
			return "bomb"
		elif self.isChain(self.cards):
			return "chain"
		return False
	
	def order(self, cards):
		value = {}
		for card in cards:
			value[card.value] = card
		list_value = sorted(list(value))
		return [value[item] for item in list_value]
	
	def isSingle(self, cards):
		if len(cards) == 1: return "single"
			
	def isChain(self, cards): 
		if len(cards)< 3:	
			return False
		else:
			order = self.order(cards)
			for i in range(len(order)):
				if i == 0:
					if int(order[i].value + 1) != int(order[i+1].value): 
						return False
						break
				elif i == len(order) -1:
					if int(order[i].value - 1) != int(order[i-1].value):
						print("bad")
						return False
						break
				elif i > 0 and i < len(order) - 1: #doesnt work yet?
					if (int(order[i].value + 1) != int(order[i+1].value)) or (int(order[i].value - 1) != int(order[i-1].value)):
						return False				
						break
		return True
			
	def isDouble(self, cards):
		if len(cards) != 2:
			return False
		else:
			dub = [card.face for card in cards]
			return len(set(dub))== 1
		
	def isTriple(self, cards):
		if len(cards) != 3:
			return False
		else:
			trip = [card.face for card in cards]
			return len(set(trip))== 1
		return True
		
	def isBomb(self, cards):
		if len(cards) != 4:
			return False
		else:
			bomb = [card.face for card in cards]
			return len(set(bomb))== 1
		
	def isChop(self, cards):	#not complete
		if len(cards) != 6:
			return False
		else:
			chop = set([card.face for card in cards])	
			if len(chop) == 3:
				return self.isChain([Card(item, "s") for item in chop])
					
class Card():	#perfect
	def __init__(self, face, suit):
		self.face = face
		self.suit = suit
		self.value = self.get_value(self.face, self.suit)
		self.text = self.face + self.suit
		self.selected = False
		
	def get_value(self, face, suit):
		return self.get_face_value(face) + self.get_suit_value(suit)
	
	def get_face_value(self, face):
		faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
		value = {}
		i = 0
		for item in faces:
			value[item] = i
			i+=1
		return value[face]
			
	def get_suit_value(self, suit):
		suits = ['S', 'C', 'D', 'H']
		value = {}
		k = 0
		for item in suits:
			value[item] = k
			k+=.1
		return value[suit]
	
	

sm = WindowManager()
hmp = HowManyPlayers()
gs = GameScreen()
ws = WinScreen()
sm.add_widget(hmp)
sm.add_widget(gs)
sm.add_widget(ws)


class ThirteenApp(App):
	
	def build(self):
		Window.clearcolor = [1, 1, 1, 1]
		#Window.size = (560,940)
		Window.left = 0
		Window.top = 25
		return sm
			
if __name__ == '__main__':
	app = ThirteenApp()
	app.run()
