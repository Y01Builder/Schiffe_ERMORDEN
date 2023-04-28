from DTO.Game import Game

if __name__ == '__main__':
    Game().startGame()

    again = True
    while again == True:
        if input("Noch eine Runde? (J/N)") == "J":
            Game.startGame()
        else:
            again = False
    exit(0)
