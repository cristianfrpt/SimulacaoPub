import threading
import time
import random

from cliente import Cliente


class Pub:
    def __init__(self, coposDisponiveis):
        self.filaClientes = []
        self.coposLimpos = coposDisponiveis
        self.coposUsados = 0
        self.clientesAtivos = 0
        self.filaClientesLock = threading.Lock()
        self.coposLock = threading.Lock()
        self.lavaCoposLock = threading.Lock()
        self.clientesAtivosLock = threading.Lock()
        #Metricas
        self.somatorioTempoNaFila = 0
        self.quantidadeAtendimento = 0
        self.totalDeClientes = 0

    def entrarFilaClientes(self, cliente):
        with self.filaClientesLock:
            cliente.tempoEntradaNaFila = time.time()
            self.filaClientes.append(cliente)
        print(f"Cliente {cliente.id} entrou na fila.")

    def sairDoPub(self, cliente):
        with self.clientesAtivosLock:
            self.clientesAtivos -= 1
        print(f"Cliente {cliente.id} saiu do Pub.")

    def abrirPub(self, tempoParaFechamento, tempoEntreChegadasMedia, tempoParaBeberMinimo,
                 tempoParaBeberMaximo, sedeMinimaCliente, sedeMaximaCliente):
        tempoDecorrido = 0
        idCliente = 1

        while tempoDecorrido < tempoParaFechamento:
            tempoEntreChegada = random.expovariate(1 / tempoEntreChegadasMedia)
            tempoDecorrido += tempoEntreChegada

            if tempoDecorrido <= tempoParaFechamento:
                cliente = Cliente(idCliente, self, tempoParaBeberMinimo, tempoParaBeberMaximo, sedeMinimaCliente,
                                  sedeMaximaCliente)
                idCliente += 1
                with self.clientesAtivosLock:
                    self.clientesAtivos += 1
                    self.totalDeClientes += 1

                self.entrarFilaClientes(cliente)
                print(f"Cliente {cliente.id} chegou no Pub, tempo decorrido: {tempoDecorrido:.2f} minutos.")

            time.sleep(tempoEntreChegada)

    def fechar_pub(self):
        while True:
            with self.clientesAtivosLock:
                if self.clientesAtivos == 0:
                    break
                else:
                    print(f"Existem {self.clientesAtivos} clientes ativos.")
            time.sleep(5)

        print("Todos os clientes terminaram e saíram. O Pub fechou!")
        print("\n")
        if self.totalDeClientes > 0:
            print(f"Total de clientes da noite = {self.totalDeClientes}.")
            print(f"Tempo total de espera da fila = {self.somatorioTempoNaFila} minutos.")
            print(f"Quantidade total de atendimentos = {self.quantidadeAtendimento}.")
            print(f"Tempo médio de espera da fila de atendimento = {(self.somatorioTempoNaFila / self.quantidadeAtendimento):.2f} minutos.")
            print("\n")
