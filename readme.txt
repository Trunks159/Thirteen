To Run:
1. Need Python 3.9 or below to Run
2. py -3.9 -m pip install kivy if you dont have it already
3. py -3.9 main.py



-----------------------------
Game Flow and Rules


Let me just explain how the game works.

1. Each player gets 13 cards
2. Each card is ranked in terms of how powerful they are. 
    '3's are the weakest,
    '2's are the strongest
    So i goes 3, 4,5,6,...2

So far so good?

3. There are many different card combinations:
    a. Pair
        2 cards of the same face : a pair of kings
    b. Triple
        3 cards of the same face
    c. Bomb
        4 cards of the same face.
        This is unique in that if someone puts any amount of 2s down (the strongest
        cards), any bomb can beat it. So if opponent puts a pair of 2s down, you can
        beat it with a bomb of 3s.
    d. Chain/Spread
        3 or more cards in sequential order : 3,4,5
        So you can do 3,4,5,6,7,8,9 and thats valid
        Only limitation is a '2' cant be a part of it.
    e. Chop
        3 or more sequential pairs :  3,3,4,4,5,5
        Yes you can do 3,3,4,4,5,5,6,6
        Chops can beat 2s also just like bombs.
        However, a three pair chop beats one '2', a four pair chop beats two '2's etc.
        So to beat 2,2, you need 3,3,4,4,5,5,6,6

4. Card Value
    So as you know 4s beat 3s but 3s can also beat 3s by comparing suits.
    So in order, the suits rank as : spade < club < diamond < heart
    So a 3 of hearts will beat a 3 of clubs and etc.
    For the card combos like pairs and such, the pair that has the higher suit wins:
    [3 of spades, 3 of hearts] is > than [3 of clubs, 3 of diamonds] because it has the hearts
    [3 spade, 4 spade, 5 heart] is > than [3 diamond, 4 diamond, 5 diamond]

5. Game Flow
    a. Game starts with the player with the lowest card in play going first. Its often a 3.
    b. With that lowest card the player can put down any combo involving that card:
        i. 3 spade, 4 spade, 5 spade for instance
        ii. 3 spade, 3 club, 3 heart for instance
        iii. You can put anything down as long as the lowest card is involved
    c. Next player needs to put card(s) down that beat yours but stay within the current
        combo. 
        So to beat the i. example above, you can put [4,5,6] down, but you cant just put
        a 2 down.
    d. At any point either player can skip.
        When someone skips and its a free play for the one who didnt concede.
        Which means that player can put down ANY combo of cards down. Maybe a single
        chain or whatever.
    e. Player who empties their hand first wins.

**RULE
You can't end a game on 2(s). So a 2 can't be the last thing in you hand.

Have fun!!
    