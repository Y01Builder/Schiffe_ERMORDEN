from DTO.Game import Game

if __name__ == '__main__':
    game = Game().startGame()

    again = True
    while again == True:
        if input("Noch eine Runde? (J/N)") == "J":
            game = Game().startGame()
        else:
            again = False
    exit(0)
