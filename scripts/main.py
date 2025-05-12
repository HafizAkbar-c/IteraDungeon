from game import Game
from scenes.mainmenu_scene import MainMenuScene


def main():
    game = Game()

    main_menu = MainMenuScene(game)
    game.scene_manager.go_to(main_menu)
    game.run()


main()
