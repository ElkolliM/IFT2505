# Ninous, Saoumi, 20132936 
# Montassar, Elkolli , 20137575

import math
import random
import copy
class LinkedList:
    class _Node:
        def __init__(self, v, n):
            self.value = v
            self.next = n

    def __init__(self):
        self._head = None
        self._size = 0

    def __str__(self):
        temp = self._head
        if(temp == None):
            return "[]"
        listString = "["
        while(temp.next != None):
            listString += str(temp.value)
            if(temp.next != None):
                listString = listString + ", "
            temp = temp.next
        listString += str(temp.value)
        return listString+"]"

    def __len__(self):
        return self._size

    def isEmpty(self):
        if(self._size == 0):
            return True
        return False

    # Adds a node of value v to the beginning of the list
    def add(self, v):
        node = self._Node(v, self._head)
        self._head = node
        self._size += 1

    # Adds a node of value v to the end of the list
    def append(self,v):
        node =self._Node(v , None)
        self._size+=1
        if(self._size == 1):
            self._head = node
            self._head.next = None
            return
        
        tempNode = self._head
        while(tempNode.next != None):
            tempNode = tempNode.next
        tempNode.next = node
        if(self._size == 0):
            self._head = node

    # Removes and returns the first node of the list
    def pop(self):
        if(self._head == None):
            return None
        self._size -= 1
        if(self._size == 0):
            node = self._head
            self._head = None
            return node.value
        node = self._head
        self._head = node.next
        return node.value

    # Returns the value of the first node of the list
    def peek(self):
        if(self.isEmpty()):
            return None
        node = self._head
        return node.value

    # Removes the first node of the list with value v and return v
    def remove(self, v):
        node = self._head
        if(node == None):
            return None
        if(node.value == v):
            self._head = node.next
            self._size -= 1
            return v
        else:
            if(node.next == None):
                return None
            while(node.next.value != v):
                node = node.next
                if(node.next == None):
                    #print("Value not found")
                    return None
        node.next = node.next.next 
        self._size -= 1
        return v

class CircularLinkedList(LinkedList):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        head = self._head
        if(self._size == 0):
            return "[]"
        listString = "["
        temp = self._head.next
        listString += str(head.value)
        if(self._size > 1):
            listString += ", "
        while(temp != head):
            listString += str(temp.value)
            if(temp.next != head):
                listString += ", "
            temp = temp.next

        return listString+"]"

    def __iter__(self):
        if(self._size == 0):
            return None
        yield self._head.value

        currentElement = self._head.next
        while(currentElement is not self._head):
            yield currentElement.value
            currentElement = currentElement.next

    # Moves head pointer to next node in list
    def next(self):
        self._head = self._head.next
        return self._head

    # add gives error in circular lists
    # Apres avoir coder cela jai vu sur le forum qu'il ne fonctionne pas pour les circula list
    # Mais je le garde quand meme
    def add(self, v):
        self._size += 1
        if(self._size == 1):
            node = self._Node(v, None)
            self._head = node
            self._head.next = self._head
            return
        node = self._Node(v, self._head)
        self._head = node
        lastElement = self._head
        for _ in range(self._size -1):
            lastElement = lastElement.next
        lastElement.next = self._head

    # Adds a node of value v to the end of the list
    def append(self, v):
        self._size += 1
        if(self._size == 1):
            self._head = self._Node(v, None)
            self._head.next = self._head
            return
        temp = self._head
        while(temp.next != self._head):
            temp = temp.next
        temp.next = self._Node(v, self._head)
        
    # Reverses the next pointers of all nodes to previous node
    def reverse(self):
        if(self._head is None):
            return
        currentNode = self._head
        nextNode = currentNode.next
        while(nextNode != self._head):
            tmp = nextNode.next
            nextNode.next = currentNode
            currentNode = nextNode
            nextNode = tmp
            if nextNode == self._head:
                nextNode.next = currentNode
        
    # Removes head node and returns its value
    def pop(self):
        if(self._size == 0):
            return None
        self._size -= 1
        if(self._size == 0):
            temp = self._head.value
            self._head = None
            return temp

        head = currentNode = self._head
        while(currentNode.next != head):
            currentNode = currentNode.next

        currentNode.next = head.next
        self.next()

        return head.value

class Card:
    def __init__(self, r, s):
        self._rank = r
        self._suit = s

    suits = {'s': '\U00002660', 'h': '\U00002661', 'd': '\U00002662', 'c': '\U00002663'}

    def __str__(self):
        return self._rank + self.suits[self._suit]


    def __eq__(self, other):
        try:
            if(self._suit == other._suit):
                if(self._rank == other._rank):
                    return True
                if(self._rank in ["1", "A"] and other._rank in ["1", "A"]):
                    return True
                if(self._rank in ["11", "J"] and other._rank in ["11", "J"]):
                    return True
                if(self._rank in ["12", "Q"] and other._rank in ["12", "Q"]):
                    return True
                if(self._rank in ["13", "K"] and other._rank in ["13", "K"]):
                    return True
            return False
        except:
            return False
class Hand:
    def __init__(self):
        self.cards = {'s': LinkedList(), 'h': LinkedList(), 'd': LinkedList(), 'c': LinkedList()}

    def __str__(self):
        result = ''
        for suit in self.cards.values():
            result += str(suit)
        return result

    def __getitem__(self, item):
        return self.cards[item]

    def __len__(self):
        result = 0
        for suit in list(self.cards):
            result += len(self.cards[suit])
        return result

    def add(self, card):
        self.cards[card._suit].add(card)

    def get_most_common_suit(self):
        return max(list(self.cards), key = lambda x: len(self[x]))

    # Returns a card included in the hand according to
    # the criteria contained in *args and None if the card
    # isn't in the hand. The tests show how *args must be used.
    def play(self, *args):
        suit = rank = None
        for arg in args:
            if(str(arg) in "shdc"):
                suit = arg
            if(str(arg) in "A123456789JQK" or str(arg) in ["10", "11", "12", "13"]):
                rank = arg
        try:
            if(rank is not None):
                if(suit is not None):
                    card = self.cards[suit].remove(Card(rank, suit))
                    return card
                for i in "shdc":
                    temp = self.cards[i].remove(Card(rank,i))
                    if(not (temp == None)):
                        return temp
            return self.cards[suit].pop()
        except:
            return None
class Deck(LinkedList):
    def __init__(self, custom=False):
        super().__init__()
        if not custom:
            # for all suits
            for i in range(4):
                # for all ranks
                for j in range(13):
                    s = list(Card.suits)[i]
                    r = ''
                    if j == 0:
                        r = 'A'
                    elif j > 0 and j < 10:
                        r = str(j+1)
                    elif j == 10:
                        r = 'J'
                    elif j== 11:
                        r = 'Q'
                    elif j == 12:
                        r = 'K'
                    self.add(Card(r,s))

    def draw(self):
        return self.pop()

    def shuffle(self, cut_precision = 0.05):
        # Cutting the two decks in two
        center = len(self) / 2
        k = round(random.gauss(center, cut_precision*len(self)))
        # other_deck must point the kth node in self
        # (starting at 0 of course)
        # other_deck = #TO DO
        first_deck = LinkedList()
        other_deck = LinkedList()
        
        for _ in range(k):
            t = self.pop()
            first_deck.append(t)
        for _ in range((self._size+first_deck._size)-k):
            t = self.pop()
            other_deck.append(t)
        if random.uniform(0,1) < 0.5:
            #switch self._head and other_deck pointers
            tempH = other_deck._head
            tempS = other_deck._size
            other_deck._head = first_deck._head
            other_deck._size = first_deck._size
            first_deck._head = tempH
            first_deck._size = tempS
        new_deck = LinkedList()
        #new_deck._head = first_deck.pop()
        while(first_deck.isEmpty() == False and other_deck.isEmpty() == False):
            tmp = first_deck.pop()
            new_deck.append(tmp)
            tmp = other_deck.pop()
            new_deck.append(tmp)
        while(not first_deck.isEmpty()):
            tmp = first_deck.pop()
            new_deck.append(tmp)
        while(not other_deck.isEmpty()):
            tmp = other_deck.pop()
            new_deck.append(tmp)
        

        self._head = new_deck._head
        self._size = new_deck._size


class Player():
    def __init__(self, name, strategy='naive'):
        self.name = name
        self.score = 8
        self.hand = Hand()
        self.strategy = strategy

    def __str__(self):
        return self.name

    # This function must modify the player's hand,
    # the discard pile, and the game's declared_suit 
    # attribute. No other variables must be changed.
    # The player's strategy can ONLY be based
    # on his own cards, the discard pile, and
    # the number of cards his opponents hold.
    def play(self, game):
        if(self.strategy == 'naive'):
            top_card = game.discard_pile.peek()
            cardToBePlayed = None
            if(game.draw_count != 0):
                if(top_card._rank == '2' or top_card == Card('Q', 's') or top_card == Card('12', 's')):
                    cardToBePlayed = self.hand.play('2')
                    if(cardToBePlayed == None):
                        cardToBePlayed = self.hand.play('Q', 's')
                        if(cardToBePlayed == None):
                            #draw cards
                            print(game.players.peek().name+" draws "+str(game.draw_count)+" cards")
                            cardsDrawn = game.draw_from_deck(game.draw_count-1) 
                            game.draw_count = 0
                            while(not cardsDrawn.isEmpty()):
                                self.hand.add(cardsDrawn.pop())
            elif(game.declared_suit != ''):
                cardToBePlayed = self.hand.play(game.declared_suit)
                if(cardToBePlayed == None):
                    cardToBePlayed = self.hand.play(self.score)
                    if(cardToBePlayed == None):
                        #draw
                        pass
                    else:
                        mostCommon = self.hand.get_most_common_suit()
                        game.declared_suit = mostCommon
                else:
                    game.declared_suit = ''
            else:
                cardToBePlayed = self.hand.play(top_card._suit)
                if(cardToBePlayed == None):
                    pass
                elif(cardToBePlayed._rank == self.score): #if frime put back in hand
                    self.hand.add(cardToBePlayed)
                    cardToBePlayed = None
                if(cardToBePlayed == None):
                    cardToBePlayed = self.hand.play(top_card._rank)
                    if(cardToBePlayed == None): #play frime
                        cardToBePlayed = self.hand.play(self.score)
                        if(cardToBePlayed == None):
                            #draw card
                            #happens in game
                            pass
                        else:
                            mostCommon = self.hand.get_most_common_suit()
                            game.declared_suit = mostCommon
            if(not cardToBePlayed == None):
                if(cardToBePlayed._rank == '2'):
                    game.draw_count+=2
                if(cardToBePlayed == Card('Q', 's')):
                    game.draw_count+=5
                game.discard_pile.add(cardToBePlayed)
            return game
class Game:
    def __init__(self):
        self.players = CircularLinkedList()

        for i in range(1,5):
            self.players.append(Player('Player '+ str(i)))

        self.deck = Deck()
        self.discard_pile = LinkedList()

        self.draw_count = 0
        self.declared_suit = ''

    def __str__(self):
        result = '--------------------------------------------------\n'
        result += 'Deck: ' + str(self.deck) + '\n'
        result += 'Declared Suit: ' + str(self.declared_suit) + ', '
        result += 'Draw Count: ' + str(self.draw_count) + ', '
        result += 'Top Card: ' + str(self.discard_pile.peek()) + '\n'

        for player in self.players:
            result += str(player) + ': '
            result += 'Score: ' + str(player.score) + ', '
            result += str(player.hand) + '\n'
        return result


    # Puts all cards from discard pile except the 
    # top card back into the deck in reverse order
    # and shuffles it 7 times
    def reset_deck(self):
        if(self.discard_pile.isEmpty()):
            return None
        topCard = self.discard_pile.pop()
        tempPile = Deck(custom=True)    #empty deck
        while(not self.discard_pile.isEmpty()):
            tempCard = self.discard_pile.pop()
            tempPile.add(tempCard)
        for _ in range(7):
            tempPile.shuffle()
        self.discard_pile.add(topCard)
        self.deck._head = tempPile._head
        self.deck._size = tempPile._size

    # Safe way of drawing a card from the deck
    # that resets it if it is empty after card is drawn
    def draw_from_deck(self, num = 7):
        tempDeckDrawn = Deck(custom=True)
        if(self.deck.isEmpty()):
                self.reset_deck()
        for _ in range(num):
            tempCard = self.deck.pop()
            tempDeckDrawn.add(tempCard)
            if(self.deck.isEmpty()):
                self.reset_deck()
        return tempDeckDrawn

    def start(self, debug=False):
        # Ordre dans lequel les joeurs gagnent la partie
        result = LinkedList()

        self.reset_deck()
        self.deck.shuffle()
        # Each player draws 8 cards
        for player in self.players:
            for _ in range(8):
                player.hand.add(self.deck.draw())

        self.discard_pile.add(self.deck.draw())

        transcript = open('result.txt','w', encoding='utf-8')
        if debug:
            transcript = open('result_debug.txt','w', encoding='utf-8')
        while(not self.players.isEmpty()):
            if debug:
                transcript.write(str(self))
                #print(str(self))

            # player plays turn
            player = self.players.peek()

            old_top_card = self.discard_pile.peek()

            self = player.play(self)

            new_top_card = self.discard_pile.peek()

            # Player didn't play a card => must draw from pile
            if new_top_card == old_top_card:
                cardDrawn = self.draw_from_deck(1)
                player.hand.add(cardDrawn.pop())
            # Player played a card
            else:
                if(new_top_card._rank in ['1', 'A']):
                    self.players.reverse()
                elif(new_top_card._rank in ['11', 'J']):
                    self.players.next()
                
            #player._head = self.players.next()
            # Handling player change
            # Player has finished the game
            if len(player.hand) == 0 and player.score == 1:
                finisher = self.players.pop()
                finishingPosition = 4-self.players._size
                tmp = self.discard_pile.peek()
                print(player.name+" plays "+str(tmp))
                print(finisher.name +" finishes in position "+str(finishingPosition))
                if(finishingPosition == 3):
                    print(self.players.pop().name+" finishes last")
                    return "simulation is over\n gg"
            else:
                # Player is out of cards to play
                if len(player.hand) == 0:
                    player.score -= 1
                    print(player.name +" is out of cards to play! "+player.name+" draws "+str(player.score)+" cards")
                    newDeck = self.draw_from_deck(player.score)
                    while(not newDeck.isEmpty()):
                        player.hand.add(newDeck.pop())
                    
                # Player has a single card left to play
                elif len(player.hand) == 1:
                    tmp = self.discard_pile.peek()
                    print(player.name+" plays "+str(tmp))
                    print("*knock, knock* - "+ player.name + " has a single card left!")
                self.players.next()
        return result


if __name__ == '__main__':

    random.seed(420)
    game = Game()
    print(game.start(debug=True))

    # TESTS
    # LinkedList
    l = LinkedList()
    l.append('b')
    l.append('c')
    l.add('a')

    assert(str(l) == '[a, b, c]')
    assert(l.pop() == 'a')
    assert(len(l) == 2)
    assert(str(l.remove('c')) == 'c')
    assert(l.remove('d') == None)
    assert(str(l) == '[b]')
    assert(l.peek() == 'b')
    assert(l.pop() == 'b')
    assert(len(l) == 0)
    assert(l.isEmpty())

    # CircularLinkedList
    l = CircularLinkedList()
    l.append('a')
    l.append('b')
    l.append('c')

    assert(str(l) == '[a, b, c]')
    l.next()
    assert(str(l) == '[b, c, a]')
    l.next()
    assert(str(l) == '[c, a, b]')
    l.next()
    assert(str(l) == '[a, b, c]')
    l.reverse()
    assert(str(l) == '[a, c, b]') 
    assert(l.pop() == 'a')
    assert(str(l) == '[c, b]')

    # Card
    c1 = Card('A','s')
    c2 = Card('A','s')
    # Il est pertinent de traiter le rang 1
    # comme étant l'ace
    c3 = Card('1','s')
    assert(c1 == c2)
    assert(c1 == c3)
    assert(c3 == c2)

    # Hand
    h = Hand()
    h.add(Card('A','s'))
    h.add(Card('8','s'))
    h.add(Card('8','h'))
    h.add(Card('Q','d'))
    h.add(Card('3','d'))
    h.add(Card('3','c'))

    assert(str(h) == '[8♠, A♠][8♡][3♢, Q♢][3♣]')
    assert(str(h['d']) == '[3♢, Q♢]')
    assert(h.play('3','d') == Card('3','d'))
    assert(str(h) == '[8♠, A♠][8♡][Q♢][3♣]')
    assert(str(h.play('8')) == '8♠')
    assert(str(h.play('c')) == '3♣')
    assert(str(h) == '[A♠][8♡][Q♢][]')
    assert(h.play('d','Q') == Card('Q','d'))
    assert(h.play('1') == Card('A','s'))
    assert(h.play('J') == None)

    # Deck
    d = Deck(custom=True)
    d.append(Card('A','s'))
    d.append(Card('2','s'))
    d.append(Card('3','s'))
    d.append(Card('A','h'))
    d.append(Card('2','h'))
    d.append(Card('3','h'))

    random.seed(15)

    temp = copy.deepcopy(d)
    assert(str(temp) == '[A♠, 2♠, 3♠, A♡, 2♡, 3♡]')
    temp.shuffle()
    assert(str(temp) == '[A♠, A♡, 2♠, 2♡, 3♠, 3♡]')
    temp = copy.deepcopy(d)
    temp.shuffle()
    assert(str(temp) == '[A♡, A♠, 2♡, 2♠, 3♡, 3♠]')
    assert(d.draw() == Card('A','s'))
