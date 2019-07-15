def order_cards(cards):
	value = dict()
	for card in cards:	#makes each card's value a key for the card
		value[card.value] = card
	list_value = sorted(list(value))	#converts all the keys to an ordered list
	new_list = list()
	for item in list_value:
		new_list.append(value[item])
	return new_list

def isSingle(cards):
	return len(cards) == 1
		
def isChain(cards, identity = False): 
	if len(cards) > 3:
		cards = order_cards(cards)
		for i in range(len(cards)):
			if i == 0:	#if we're looking at the first element, the next element is our concern
				identity = int(cards[i].value + 1) != int(cards[i+1].value)
			elif i == len(order) -1:	#if we're looking at the last element, the previous element is our concern
				identity = int(cards[i].value - 1) != int(cards[i-1].value)
			else: #doesnt work yet?
				identity = (int(cards[i].value + 1) != int(cards[i+1].value)) and (int(cards[i].value - 1) != int(cards[i-1].value))

	return identity
					
def isDuplicate(cards, number, identity = False):
	if len(cards) == number:
		dub = list()
		for card in cards:
			dub.append(card.face)
		identity = len(set(dub))== 1
	if identity == False:
		print("ITS NOT A DUPE")
	return identity
		
def isChop(cards):	#not complete
	chop = []
	new_list = []
	if len(cards) != 6:
		identity  = False
	else:
		for card in cards:
			chop.append(card.face)
		identity = len(set(chop)) == .5*len(chop)
#	for i in range(len(faces)):
#		val[faces[i]] = i
	
#	for item in chop:
#		new_list.append
	
	return identity	
