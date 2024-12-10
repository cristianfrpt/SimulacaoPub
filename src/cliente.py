import random
import time
import threading


class Cliente:
    def __init__(self, id_cliente, pub, tempoParaBeberMinimo, tempoParaBeberMaximo, sedeMinima, sedeMaxima):
        self.id = id_cliente
        self.tempoParaBeberMinimo = tempoParaBeberMinimo
        self.tempoParaBeberMaximo = tempoParaBeberMaximo
        self.sede = random.randint(sedeMinima, sedeMaxima)
        self.pub = pub
        self.tempoEntradaNaFila = time.time()

    def beber(self):
        self.sede -= 1

        time.sleep(random.randint(self.tempoParaBeberMinimo, self.tempoParaBeberMaximo))
        print(f"Cliente {self.id} bebeu. Sede restante: {self.sede}.")

        if self.sede > 0:
            self.pub.entrarFilaClientes(self)
        else:
            self.pub.sairDoPub(self)
