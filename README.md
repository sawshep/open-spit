# Spit
This was my final project for AP Computer Science Principles. At the time, I
had no knowledge of object oriented programming and no knowledge of game
programming. Under threat of a strict deadline, I managed to pump out a
horribly organized, scarecly commented program that barely worked. The only
purpose I'd recommend for this is as an antithesis of good program design, but
I've decided to unprivate the repository in case anyone cares to look at it.

I'll probably do a complete rewrite of the card game in a different language.

> # Compiled Version
> At this moment, there is no compiled version of `spit.py` due to a circular import error with `numpy` in Nuitka.
> 
> Also, only the Linux version of `server.py` is availible. Nuitka does not cooperate with MacOS/Windows.
> 
> ~~The binaries provided in `bin` were compiled with Nuitka
> Just clone the repo and run the binary for your system!~~
> 
> # Interpereted Version:
> 1. Make sure you have Python 3
> 2. Clone the repo `git clone https://github.com/sawshep/spit`
> 3. Change directory to the repo `cd spit`
> 4. Install dependencies `pip3 install -r requirements.txt`
> 5. Run `python3 src/spit.py`
> 
> # How to play:
> Spit is a 2-player, reflex-based game.
> It is sort of similar to a multiplayer Solitaire.
> Each player has 5 piles of cards in front of them.
> Each player also has a stack of auxillary cards that they draw from to form the 2 decks at the center in the start of the round.
> The goal of the game is to place the cards in your piles on the 2 center piles in ascending/descending order (suit does not matter).
> If you uncover a face-down card, you can flip that card face-up to make it availible for play.
> You can stack multiple cards of the same number/face on top of eachother in your piles.
> If you play all the cards from a pile, you may place another card face-up in that location.
> When you and your opponent run out of cards, both draw a card from their auxilary decks and places it on the center piles, respectively.
> When you run out of cards in your piless, slap the smaller center deck. This is then added to your auxilary deck, which you create new piles from for the next round.
> 
> # Controls:
> Hold the Left or Right arrow to enter pick-up/put-down mode.
> Press A, S, D, F, or Spacebar to pick-up/put-down a card from/on decks 1-5, respectively.
> 
> Hold Keypad 0 to enter flip mode.
> Press A, S, D, F, or Spacebar to flip up a face-down card from piles 1-5, respectively.
> 
> Press R once you are ready to draw a card and play!
> 
> # Configuration
> The config file is located in `src/config.py`. If you wish to use a custom configuration with the compiled version, you must compile the binary yourself after editing the config file.
> 
> # Hosting a Server
> To host a server, you must first port forward. By default, port 31415 is used.
> Once the server is running, you must give your opponent your public IPv4 address so he/she can connect.
