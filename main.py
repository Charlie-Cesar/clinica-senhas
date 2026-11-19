# Arquivo principal: é por ele que o sistema começa (python main.py).
# Ele só abre a janela; a lógica das filas fica na pasta clinica/.
from interface.app import App

if __name__ == "__main__":
    App().mainloop()  # mainloop = a janela fica aberta esperando os cliques (eventos)
