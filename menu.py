from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from play import *

janela = Window(1000,600)
janela.set_title("Jogo")

mouse=janela.get_mouse()

button_Play= Sprite("PNG\Play.png")
button_Sair= Sprite("PNG\Sair.png")
background_menu = Sprite("PNG\Abackground.png")

button_Play.x = janela.width/2 - button_Play.width/2
button_Sair.x = janela.width/2 - button_Sair.width/2

button_Play.y = 200
button_Sair.y = 375

#GameLoop
while True:
    if(mouse.is_over_object(button_Play) and mouse.is_button_pressed(1)):
       jogar() 

    if(mouse.is_over_object(button_Sair) and mouse.is_button_pressed(1)):
      break

    background_menu.draw()

    button_Play.draw()
    button_Sair.draw()

    janela.update()
