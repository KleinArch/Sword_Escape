from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from play import *

janela = Window(1000,600)
janela.set_title("Jogo")

mouse=janela.get_mouse()

button_Play= Sprite("Play.png")
button_Sair= Sprite("Sair.png")

button_Play.x = janela.width/2 -100
button_Sair.x = janela.width/2 -100

button_Play.y = 150
button_Sair.y = 450

#GameLoop
while True:
    if(mouse.is_over_object(button_Play) and mouse.is_button_pressed(1)):
       jogar() 

    if(mouse.is_over_object(button_Sair) and mouse.is_button_pressed(1)):
      break

    janela.set_background_color("blue")

    button_Play.draw()
    button_Sair.draw()

    janela.update()
