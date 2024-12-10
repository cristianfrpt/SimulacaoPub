import random
import time
import threading

from garconete import Garconete
from pub import Pub


def main():
    print("Iniciando a simulação...")

    # parametros pub
    tempoLimiteParaChegadas = 30
    tempoEntreChegadasMedia = 5
    coposDisponiveis = 10

    # parametros cliente
    sedeMinima = 1
    sedeMaxima = 4
    tempoParaBeberMinimo = 5
    tempoParaBeberMaximo = 8

    # parametros garconetes
    numeroGarconetes = 2
    tempoLavarCopos = 5
    tempoAtendimentoMedia = 6
    tempoAtendimentoDesvio = 1

    pub = Pub(coposDisponiveis)

    cliente_thread = threading.Thread(target=pub.abrirPub, args=(tempoLimiteParaChegadas,
                                                                 tempoEntreChegadasMedia,
                                                                 tempoParaBeberMinimo,
                                                                 tempoParaBeberMaximo,
                                                                 sedeMinima,
                                                                 sedeMaxima))
    cliente_thread.start()

    garconetes = [Garconete(i + 1, pub, tempoAtendimentoMedia, tempoAtendimentoDesvio, tempoLavarCopos)
                  for i in range(numeroGarconetes)]

    garconete_threads = []

    for g in garconetes:
        garconete_thread = threading.Thread(target=g.trabalhar, args=())
        garconete_threads.append(garconete_thread)

    for gt in garconete_threads:
        gt.start()

    cliente_thread.join()

    pub.fechar_pub()

    for g in garconetes:
        g.finalizarAtendimento()

    for gt in garconete_threads:
        gt.join()

    print("Simulação concluída!")


if __name__ == "__main__":
    main()
