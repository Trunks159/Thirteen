import kivy
from GameLogic import GameRun
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
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from os import path	
faces = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
suits = ['S', 'C', 'D', 'H']		
Builder.load_file("thirteen2.kv")

		


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
	#current_play = ObjectProperty()
	#def __init__(self, field, **kwargs):
		#super(FieldGrid, self).__init__(**kwargs)
		#self.field = field
		#self.current_play = self.field.current["play"]
	
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			new_play = self.field.current["player"].play()
			if isValid(new_play):
				self.current["play"] = new_play
			else:
				self.field.returnCards(self.current["player"])
				
	def on_current_play(self, instance, value):
		self.clear_widgets()
		for card in value.cards: self.add_widget(card)
				
class CardButton(ToggleButton):
	def __init__(self, card, **kwargs):
		super(CardButton, self).__init__(**kwargs)		
		self.card = card
		self.background_normal = "Pictures/JPEG/" + self.card.face + self.card.suit + ".jpg"
	
	def on_state(self, instance, value):
		self.card.selected = True if value == "down" else False
		
class Player(GridLayout):
	hand = ListProperty([])
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.name = name
		
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
			self.hand = hand_copy
			return(Play(selected))
		else:
			return "pass"

	def order_hand(self):
		value = {}
		for card in self.hand:	#makes each card's value a key for the card
			value[card.value] = card
		list_value = sorted(list(value))	#converts all the keys to an ordered list
		new_list = []
		for item in list_value:
			new_list.append(value[item])
		self.hand = new_list
	
	def on_hand(self, instance, value):
		self.clear_widgets()
		for card in value:
			self.add_widget(card)


class GameScreen(Screen):
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.game = GameRun()
		
	def add_players:
		player1.
		self.ids.player1
	
	
	
			
class CurrentPlayer(Label):
	currentplayer = ObjectProperty()
	def __init__(self, field, **kwargs):
		super(CurrentPlayer, self).__init__(**kwargs)
		self.field = field
		self.current_player = self.field.current["player"]
		self.text = self.current_player.name
			


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
