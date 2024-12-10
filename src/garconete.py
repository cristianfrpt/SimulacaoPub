import threading
import time
import random


class Garconete(threading.Thread):
    def __init__(self, idGarconete, pub, tempoAtendimentoMedia, tempoAtendimentoDesvio, tempoLavarCopos):
        super().__init__()
        self.id = idGarconete
        self.tempoAtendimentoMedia = tempoAtendimentoMedia
        self.tempoAtendimentoDesvio = tempoAtendimentoDesvio
        self.tempoLavarCopos = tempoLavarCopos
        self.pub = pub
        self.executando = True
        # Metricas
        self.quantidadeAtendimentos = 0
        self.quantidadeLavando = 0
        self.tempoOcupadoAtendendo = 0
        self.tempoOcupadoLavando = 0
        self.tempoFinalUltimaAcao = 0
        self.tempoOcioso = 0
        self.tempoTotal = 0

    def trabalhar(self):
        while self.executando:
            tempoInicio = time.time()

            self.pub.filaClientesLock.acquire()
            self.pub.coposLock.acquire()
            if self.pub.filaClientes and self.pub.coposLimpos > 0:
                tempoInicioAcao = time.time()
                if self.tempoFinalUltimaAcao != 0:
                    self.tempoOcioso += tempoInicioAcao - self.tempoFinalUltimaAcao
                cliente = self.pub.filaClientes.pop(0)
                tempoAtual = time.time()
                tempoClienteNaFila = tempoAtual - cliente.tempoEntradaNaFila
                self.pub.coposLimpos -= 1
                self.pub.somatorioTempoNaFila += tempoClienteNaFila
                self.pub.quantidadeAtendimento += 1

                # release dos locks
                self.pub.filaClientesLock.release()
                self.pub.coposLock.release()

                self.atender(cliente)
                with self.pub.coposLock:
                    self.pub.coposUsados += 1
                self.tempoOcupadoAtendendo += time.time() - tempoInicioAcao
                self.quantidadeAtendimentos += 1
                self.tempoFinalUltimaAcao = time.time()
            elif self.pub.coposUsados > 0:
                # release dos locks
                self.pub.filaClientesLock.release()
                self.pub.coposLock.release()

                if self.pub.lavaCoposLock.acquire(blocking=False):
                    try:
                        tempoInicioAcao = time.time()
                        if self.tempoFinalUltimaAcao != 0:
                            self.tempoOcioso += tempoInicioAcao - self.tempoFinalUltimaAcao
                        self.lavarCopos()
                        self.tempoOcupadoLavando += time.time() - tempoInicioAcao
                        self.quantidadeLavando += 1
                        self.tempoFinalUltimaAcao = time.time()
                    finally:
                        self.pub.lavaCoposLock.release()
            else:
                # release dos locks
                self.pub.filaClientesLock.release()
                self.pub.coposLock.release()
                self.tempoOcioso += time.time() - tempoInicio

            self.tempoTotal += time.time() - tempoInicio
            time.sleep(0.5)

    def atender(self, cliente):
        print(f"Garçonete {self.id} está servindo o cliente {cliente.id}.")
        time.sleep(random.gauss(self.tempoAtendimentoMedia, self.tempoAtendimentoDesvio))

        # Criar thread pro cliente beber
        clienteThread = threading.Thread(target=cliente.beber)
        clienteThread.start()

    def lavarCopos(self):
        print(f"Garçonete {self.id} começou a lavar copos.")
        time.sleep(self.tempoLavarCopos)
        with self.pub.coposLock:
            coposLavados = min(self.pub.coposUsados, 10)
            self.pub.coposLimpos += coposLavados
            self.pub.coposUsados -= coposLavados
        print(f"Garçonete {self.id} terminou de lavar os copos.")

    def finalizarAtendimento(self):
        self.executando = False
        self.calcular_metricas()

    def calcular_metricas(self):
        if self.tempoTotal > 0:
            taxaOcupacaoLavando = self.tempoOcupadoLavando / self.tempoTotal
            taxaOcupacaoAtendendo = self.tempoOcupadoAtendendo / self.tempoTotal
            taxaOcupacaoOcioso = self.tempoOcioso / self.tempoTotal

            print(f"Garçonete {self.id}:")
            print(f"Tempo total: {self.tempoTotal:.2f} minutos.")
            print(f"Tempo ocupado (LAVANDO): {self.tempoOcupadoLavando:.2f} minutos.")
            print(f"Taxa de ocupação (LAVANDO): {taxaOcupacaoLavando * 100:.2f}%")

            print(f"Tempo ocupado (ENCHENDO): {self.tempoOcupadoAtendendo:.2f} minutos.")
            print(f"Taxa de ocupação (ENCHENDO): {taxaOcupacaoAtendendo * 100:.2f}%")

            print(f"Tempo ocioso: {self.tempoOcioso:.2f} minutos.")
            print(f"Taxa de ociosidade: {taxaOcupacaoOcioso * 100:.2f}%")

            print(f"Quantidade de atendimentos: {self.quantidadeAtendimentos}")
            print(f"Quantidade de vezes lavando: {self.quantidadeLavando}")
            print("\n")

