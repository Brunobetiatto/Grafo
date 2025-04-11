# Atualizei a nossa classe grafo colocando os metodos aqui

import os
import email
from email.policy import default
from collections import defaultdict
import heapq

class Grafo:
    def __init__(self):
        self.adj_list = defaultdict(dict)
        self.vertices = set()
        self.ordem = 0  # número de vértices
        self.tamanho = 0  # número de arestas

    def adiciona_vertice(self, u):
        if u not in self.vertices:
            self.vertices.add(u)
            self.ordem += 1

    def adiciona_aresta(self, u, v, peso):
        if peso < 0:
            raise ValueError("Pesos negativos não são permitidos.")

        if u not in self.vertices:
            self.adiciona_vertice(u)
        if v not in self.vertices:
            self.adiciona_vertice(v)

        if v in self.adj_list[u]:
            self.adj_list[u][v] += 1  # sempre incrementa em 1

        else:
            self.adj_list[u][v] = peso
            self.tamanho += 1  # nova aresta

    def remove_aresta(self, u, v):
        if v in self.adj_list[u]:
            del self.adj_list[u][v]
            self.tamanho -= 1

    def remove_vertice(self, u):
        if u in self.vertices:
            del self.adj_list[u]
            self.vertices.remove(u)
            self.ordem -= 1
            for chave in list(self.adj_list):
                if u in self.adj_list[chave]:
                    del self.adj_list[chave][u]
            self.tamanho = sum(len(v) for v in self.adj_list.values())

    def tem_aresta(self, u, v):
        return v in self.adj_list[u]

    def grau_entrada(self, u):
        return sum(1 for vizinhos in self.adj_list.values() if u in vizinhos)

    def grau_saida(self, u):
        return len(self.adj_list[u])

    def grau(self, u):
        return self.grau_entrada(u) + self.grau_saida(u)

    def get_peso(self, u, v):
        return self.adj_list[u].get(v)

    def imprime_lista_adjacencias(self):
        for vertice in self.vertices:
            arestas = " -> ".join(f"('{v}', {p})" for v, p in self.adj_list[vertice].items())
            print(f"{vertice}: {arestas}")

    def processar_email(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                mensagem = email.message_from_file(arquivo, policy=default)

            remetente = mensagem.get('From')
            destinatarios = mensagem.get('To', '')

            if not remetente or not destinatarios:
                return 0

            destinatarios = [d.strip() for d in destinatarios.split(',')]
            destinatarios = [d for d in destinatarios if d]

            arestas_adicionadas = 0
            for destinatario in destinatarios:
                self.adiciona_aresta(remetente, destinatario, 1)
                arestas_adicionadas += 1

            return arestas_adicionadas

        except Exception as e:
            print(f"Erro ao processar {caminho_arquivo}: {str(e)}")
            return 0

    def processar_diretorio(self, diretorio):
        total_arestas = 0
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                total_arestas += self.processar_email(caminho_completo)

        print(f"Total de arestas adicionadas: {total_arestas}")
        return total_arestas

    def salvar_lista_adjacencias_em_txt(self, caminho_arquivo):
        """
        Salva a lista de adjacências do grafo em um arquivo texto.
        """
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                for vertice in sorted(self.vertices):
                    arestas = " -> ".join(f"('{v}', {p})" for v, p in self.adj_list[vertice].items())
                    linha = f"{vertice}: {arestas}\n"
                    f.write(linha)
            print(f"Lista de adjacências salva com sucesso em '{caminho_arquivo}'.")
        except Exception as e:
            print(f"Erro ao salvar lista de adjacências: {e}")


    def imprime_num_vertices(self):
        print(f"Número de vértices (ordem): {self.ordem}")

    def imprime_num_arestas(self):
        print(f"Número de arestas (tamanho): {self.tamanho}")

    def conta_vertices_isolados(self):
        isolados = 0
        for vertice in self.vertices:
            if self.grau(vertice) == 0:
                isolados += 1
        print(f"Número de vértices isolados: {isolados}")

    def top_20_maior_grau_saida(self):
        graus_saida = [(v, self.grau_saida(v)) for v in self.vertices]
        graus_saida.sort(key=lambda x: x[1], reverse=True)
        top_20 = graus_saida[:20]
        print("Top 20 vértices com maior grau de saída:")
        for i, (v, grau) in enumerate(top_20, 1):
            print(f"{i}. {v}: {grau}")

    def top_20_maior_grau_entrada(self):
        graus_entrada = [(v, self.grau_entrada(v)) for v in self.vertices]
        graus_entrada.sort(key=lambda x: x[1], reverse=True)
        top_20 = graus_entrada[:20]
        print("Top 20 vértices com maior grau de entrada:")
        for i, (v, grau) in enumerate(top_20, 1):
            print(f"{i}. {v}: {grau}")

    #3)Eurelian Graf
    def eh_eureliano(self):
        razoes = []
        
        # 1) Verificar se todos os vértices têm grau de entrada igual ao grau de saída
        for v in self.vertices:
            if self.grau_entrada(v) != self.grau_saida(v):
                razoes.append(f"Vértice {v} tem grau de entrada ({self.grau_entrada(v)}) ≠ grau de saída ({self.grau_saida(v)})")
        
        # 2) Verificar se o grafo é fortemente conexo (para grafos direcionados)
        if len(self.vertices) > 0:
            # Usamos DFS a partir do primeiro vértice
            visitados = set()
            stack = [next(iter(self.vertices))]
            
            while stack:
                atual = stack.pop()
                if atual not in visitados:
                    visitados.add(atual)
                    # Adiciona todos os vizinhos (saída)
                    stack.extend(self.adj_list[atual].keys())
                    # Adiciona todos que apontam para atual (entrada)
                    for v in self.vertices:
                        if atual in self.adj_list[v]:
                            stack.append(v)
            
            if len(visitados) != len(self.vertices):
                razoes.append("O grafo não é fortemente conexo")
        
        # 3) Decisão final
        if not razoes:
            print("O grafo é euleriano")
            return True
        else:
            print("O grafo NÃO é euleriano pelas seguintes razões:")
            for razao in razoes:
                print(f"- {razao}")
            return False


    def vertices_ate_distancia(self, vertice_inicial, D):
      """
      Retorna os vértices alcançáveis a partir de 'vertice_inicial' cujo
      caminho (soma dos pesos) seja <= D, usando o algoritmo de Dijkstra.

      Parâmetros:
        vertice_inicial: vértice de partida.
        D: distância máxima permitida.

      Retorna:
        Lista de vértices que possuem caminho de custo <= D.
      """
      if vertice_inicial not in self.vertices:
          raise ValueError("Vértice inicial não existe.")

      # Inicializa as distâncias com infinito, exceto a do vértice inicial (0)
      distancias = {v: float('inf') for v in self.vertices}
      distancias[vertice_inicial] = 0

      # Fila de prioridade (min-heap) com tuplas (distância acumulada, vértice)
      heap = [(0, vertice_inicial)]

      while heap:
          d_atual, u = heapq.heappop(heap)
          if d_atual > distancias[u]:
              continue

          for vizinho, peso in self.adj_list[u].items():
              nova_distancia = d_atual + peso
              # Se excede D, não é necessário processar
              if nova_distancia > D:
                  continue
              if nova_distancia < distancias[vizinho]:
                  distancias[vizinho] = nova_distancia
                  heapq.heappush(heap, (nova_distancia, vizinho))

      return [v for v, d in distancias.items() if d <= D]

# Método Dijkstra para cálculo dos caminhos mínimos (necessário para o diâmetro)
    def dijkstra(self, origem):
          # Inicializa as distâncias e os antecessores para todos os vértices
          distancias = {v: float('inf') for v in self.vertices}
          antecessores = {v: None for v in self.vertices}
          distancias[origem] = 0

          # Fila de prioridade com tuplas (distância acumulada, vértice)
          heap = [(0, origem)]

          while heap:
              distancia_atual, vertice_atual = heapq.heappop(heap)
              if distancia_atual > distancias[vertice_atual]:
                  continue

              for vizinho, peso in self.adj_list[vertice_atual].items():
                  nova_distancia = distancia_atual + peso
                  if nova_distancia < distancias[vizinho]:
                      distancias[vizinho] = nova_distancia
                      antecessores[vizinho] = vertice_atual
                      heapq.heappush(heap, (nova_distancia, vizinho))

          return distancias, antecessores

      # Método para reconstruir o caminho a partir dos antecessores
    def reconstruir_caminho(self, antecessores, origem, destino):
          caminho = []
          vertice_atual = destino
          while vertice_atual is not None:
              caminho.append(vertice_atual)
              if vertice_atual == origem:
                  break
              vertice_atual = antecessores[vertice_atual]
          caminho.reverse()
          return caminho

      # Método para calcular o diâmetro do grafo
    def diametro(self):
          diametro_valor = 0
          diametro_origem = None
          diametro_destino = None
          diametro_antecessores = {}

          for vertice in self.vertices:
              distancias, antecessores = self.dijkstra(vertice)
              for outro_vertice in self.vertices:
                  if vertice == outro_vertice:
                      continue
                  if distancias[outro_vertice] < float('inf') and distancias[outro_vertice] > diametro_valor:
                      diametro_valor = distancias[outro_vertice]
                      diametro_origem = vertice
                      diametro_destino = outro_vertice
                      diametro_antecessores = antecessores

          if diametro_origem is None or diametro_destino is None:
              print("Grafo vazio ou totalmente desconexo.")
              return None, []

          caminho_diametro = self.reconstruir_caminho(diametro_antecessores, diametro_origem, diametro_destino)
          return diametro_valor, caminho_diametro
#!pip install tabulate

from tabulate import tabulate

def main():
    # Configurações iniciais
    DIRETORIO_EMAILS = "emails"
    VERTICE_INICIAL = "james.derrick@enron.com"
    DISTANCIA_MAXIMA = 1
    ARQUIVO_ADJACENCIAS = "lista_adjacencias.txt"

    grafo = Grafo()
    #teste para grafo eureliano
    #grafo.adiciona_aresta("A", "B", 1)
    #grafo.adiciona_aresta("B", "C", 1)
    #grafo.adiciona_aresta("C", "A", 1)



    print("=" * 60)
    print("📧 Construção do Grafo de E-mails")
    print("=" * 60)

    # Processamento dos e-mails
    print("\n🔄 Processando o diretório de e-mails...\n")
    total_arestas = grafo.processar_diretorio(DIRETORIO_EMAILS)
    print(f"✅ Arestas adicionadas: {total_arestas}")

    # Estatísticas gerais
    print("\n📊 Estatísticas do Grafo")
    print("-" * 60)
    print(f"🔹 Total de vértices: {grafo.ordem}")
    print(f"🔹 Total de arestas:  {grafo.tamanho}")
    grafo.conta_vertices_isolados()

    # Top 20 vértices com maior grau de saída
    print("\n🏆 Top 20 - Maior Grau de Saída")
    print("-" * 60)
    grafo.top_20_maior_grau_saida()

    # Top 20 vértices com maior grau de entrada
    print("\n🏆 Top 20 - Maior Grau de Entrada")
    print("-" * 60)
    grafo.top_20_maior_grau_entrada()

    # Teste Euleriano
    print("-" * 60)
    grafo.eh_eureliano()
    print("")

    # Vértices alcançáveis a partir de um vértice inicial
    print(f"\n📌 Vértices alcançáveis a partir de '{VERTICE_INICIAL}' com distância ≤ {DISTANCIA_MAXIMA}")
    print("-" * 60)
    try:
        alcancaveis = grafo.vertices_ate_distancia(VERTICE_INICIAL, DISTANCIA_MAXIMA)
        if alcancaveis:
            tabela = tabulate([[v] for v in alcancaveis], headers=["Vértice"], tablefmt="fancy_grid")
            print(tabela)
        else:
            print("⚠ Nenhum vértice alcançável encontrado.")
    except ValueError as e:
        print(f"❌ Erro: {e}")

    # --- Seção para calcular o diâmetro do grafo ---
    print("\n📏 Diâmetro do Grafo")
    print("-" * 60)
    diametro_valor, caminho = grafo.diametro()
    if diametro_valor is not None and caminho:
        print(f"📐 Diâmetro do grafo: {diametro_valor}")
        print("🧭 Caminho correspondente:")
        print(" -> ".join(caminho))
    else:
        print("⚠ Não foi possível calcular o diâmetro (grafo vazio ou desconexo).")
        print(f"ℹ Total de vértices no grafo: {len(grafo.vertices)}")
        print(f"ℹ Primeiros 5 vértices: {list(grafo.vertices)[:5]}")


    # --- Salvando a lista de adjacências ---
    print(f"\n💾 Salvando lista de adjacências em '{ARQUIVO_ADJACENCIAS}'...")
    grafo.salvar_lista_adjacencias_em_txt(ARQUIVO_ADJACENCIAS)
    print("✅ Arquivo salvo com sucesso.")

    print("\n✅ Execução concluída.")
    print("=" * 60)



if __name__ == "__main__":
  main()