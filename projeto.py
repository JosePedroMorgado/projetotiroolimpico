import os
import pickle
from datetime import datetime

class ModalidadeTiroOlimpico:
    def __init__(self):
        self.atletas = {}
        self.resultados = {}
    
    def create(self, tipo, dados):
        if tipo == "atleta":
            self.atletas[dados['matricula']] = dados
        elif tipo == "resultado":
            if dados['matricula'] not in self.resultados:
                self.resultados[dados['matricula']] = []
            self.resultados[dados['matricula']].append(dados)
        self.salvar_dados()

    def read(self, tipo, matricula=None):
        if tipo == "atleta":
            return self.atletas.get(matricula, None)
        elif tipo == "resultado":
            return self.resultados.get(matricula, [])
        elif tipo == "todos_atletas":
            return self.atletas
        elif tipo == "todos_resultados":
            return self.resultados

    def update(self, tipo, matricula, dados):
        if tipo == "atleta" and matricula in self.atletas:
            self.atletas[matricula].update(dados)
            self.salvar_dados()
            return "Atleta atualizado com sucesso."
        elif tipo == "resultado" and matricula in self.resultados:
            for resultado in self.resultados[matricula]:
                if resultado['etapa'] == dados['etapa'] and resultado['modalidade'] == dados['modalidade']:
                    resultado.update(dados)
                    self.salvar_dados()
                    return "Resultado atualizado com sucesso."
            return "Etapa ou modalidade não encontrada para este atleta."
        return "Dados não encontrados para atualização."

    def delete(self, tipo, matricula=None):
        if tipo == "atleta" and matricula in self.atletas:
            del self.atletas[matricula]
            if matricula in self.resultados:
                del self.resultados[matricula]
            self.salvar_dados()
            return "Atleta e seus resultados deletados com sucesso."
        elif tipo == "resultado" and matricula in self.resultados:
            del self.resultados[matricula]
            self.salvar_dados()
            return "Resultados do atleta deletados com sucesso."
        elif tipo == "todos":
            self.atletas.clear()
            self.resultados.clear()
            self.salvar_dados()
            return "Todos os dados foram limpos."
        return "Dados não encontrados para deleção."

    def salvar_dados(self):
        with open('atletas.pkl', 'wb') as f:
            pickle.dump(self.atletas, f)
        with open('resultados.pkl', 'wb') as f:
            pickle.dump(self.resultados, f)

    def carregar_dados(self):
        if os.path.exists('atletas.pkl'):
            with open('atletas.pkl', 'rb') as f:
                self.atletas = pickle.load(f)
        if os.path.exists('resultados.pkl'):
            with open('resultados.pkl', 'rb') as f:
                self.resultados = pickle.load(f)

class GerenciamentoTiroOlimpico:
    def __init__(self):
        self.modalidade = ModalidadeTiroOlimpico()
        self.modalidade.carregar_dados()

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu(self):
        while True:
            self.limpar_tela()
            print("=== Menu de Gerenciamento de Tiro Olímpico ===")
            print("1 - Cadastrar atleta")
            print("2 - Cadastrar resultados")
            print("3 - Visualizar resultados cadastrados")
            print("4 - Atualizar Resultados já cadastrados")
            print("5 - Verificar o campeonato")
            print("6 - Limpar todos os dados")
            print("7 - Sair do sistema")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.cadastrar_atleta()
            elif opcao == '2':
                self.cadastrar_resultados()
            elif opcao == '3':
                self.visualizar_resultados()
            elif opcao == '4':
                self.atualizar_resultados()
            elif opcao == '5':
                self.verificar_campeonato()
            elif opcao == '6':
                self.limpar_dados()
            elif opcao == '7':
                print("Saindo do sistema...")
                break
            else:
                input("Opção inválida. Pressione Enter para continuar...")

    def cadastrar_atleta(self):
        while True:
            matricula = input("Digite a matrícula do Atleta: ")
            nome = input("Digite o nome do Atleta: ")
            uf = input("Digite a UF da Federação: ")

            print("\nConfirme os dados:")
            print(f"Matrícula: {matricula}")
            print(f"Nome: {nome}")
            print(f"UF: {uf}")

            confirmacao = input("\nTodos os dados estão corretos? (S/N): ")
            if confirmacao.lower() == 's':
                self.modalidade.create("atleta", {"matricula": matricula, "nome": nome, "uf": uf})
                print("Dados confirmados e cadastrados com sucesso!")
                input("Pressione Enter para voltar ao menu inicial...")
                break
            else:
                print("Dados descartados. Vamos recomeçar o cadastro.")

    def cadastrar_resultados(self):
        while True:
            matricula = input("Digite a matrícula do atleta: ")
            atleta = self.modalidade.read("atleta", matricula)
            if not atleta:
                print("Erro: Atleta não cadastrado.")
                input("Pressione Enter para voltar ao menu principal...")
                return

            etapa = input("Número da etapa: ")
            while not etapa.isdigit():
                print("Erro: O número da etapa deve ser um número inteiro.")
                etapa = input("Número da etapa: ")
            etapa = int(etapa)

            data = input("Data da etapa (dd/mm/aaaa): ")
            while True:
                try:
                    data_formatada = datetime.strptime(data, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Erro: Formato de data inválido. Use dd/mm/aaaa.")
                    data = input("Data da etapa (dd/mm/aaaa): ")

            tipo_etapa = input("Tipo de etapa (1 - Regional / 2 - Final / 3 - Normal): ")
            while tipo_etapa not in ['1', '2', '3']:
                print("Erro: Opção inválida.")
                tipo_etapa = input("Tipo de etapa (1 - Regional / 2 - Final / 3 - Normal): ")

            modalidade = input("Modalidade (1 - Carabina de Ar / 2 - Três Posições): ")
            while modalidade not in ['1', '2']:
                print("Erro: Opção inválida.")
                modalidade = input("Modalidade (1 - Carabina de Ar / 2 - Três Posições): ")

            if modalidade == '1':
                tipo_resultado = "número com decimal"
                converter = float
            else:
                tipo_resultado = "número sem decimal"
                converter = int

            resultados = []
            while True:
                for i in range(1, 7):
                    while True:
                        try:
                            resultado = converter(input(f"Resultado da {i}ª rodada ({tipo_resultado}): "))
                            resultados.append(resultado)
                            break
                        except ValueError:
                            print(f"Erro: Digite um {tipo_resultado}.")

                soma_total = sum(resultados)

                # Ajuste o total com base no tipo de etapa
                total = soma_total
                if tipo_etapa == '1':  # Regional
                    total *= 2
                elif tipo_etapa == '2':  # Final
                    total *= 3

                print("\nResultados digitados:")
                for i, res in enumerate(resultados, 1):
                    print(f"{i}ª rodada: {res}")
                print(f"Soma total das rodadas: {soma_total}")
                print(f"Total ajustado: {total}")

                confirmacao = input("\nTodos os resultados estão corretos? (S/N): ")
                if confirmacao.lower() == 's':
                    break
                else:
                    print("Resultados descartados. Vamos recomeçar o cadastro dos resultados.")
                    resultados.clear()

            dados_resultado = {
                "matricula": matricula,
                "etapa": etapa,
                "data": data_formatada.strftime("%d/%m/%Y"),
                "modalidade": "Carabina de Ar" if modalidade == '1' else "Três Posições",
                "resultados": resultados,
                "soma_total": soma_total,
                "total": total,
                "tipo_etapa": "Regional" if tipo_etapa == '1' else "Final" if tipo_etapa == '2' else "Normal"
            }

            self.modalidade.create("resultado", dados_resultado)
            print("Resultados cadastrados com sucesso!")

            continuar = input("Deseja cadastrar um novo resultado? (S/N): ")
            if continuar.lower() != 's':
                break



    def visualizar_resultados(self):
        matricula = input("Matrícula do atleta (deixe em branco para ver todos): ")
        
        # Adicionando opção para selecionar modalidade
        print("\nEscolha a modalidade para visualizar:")
        print("1 - Carabina de Ar")
        print("2 - Três Posições")
        print("3 - Todas")
        escolha_modalidade = input("Escolha uma opção (1/2/3): ")

        modalidades = {
            '1': "Carabina de Ar",
            '2': "Três Posições"
        }
        
        modalidade_selecionada = modalidades.get(escolha_modalidade, None)
        
        if matricula:
            atleta = self.modalidade.read("atleta", matricula)
            if not atleta:
                print("Atleta não encontrado.")
            else:
                resultados = self.modalidade.read("resultado", matricula)
                # Filtrando resultados pela modalidade selecionada
                if modalidade_selecionada:
                    resultados = [res for res in resultados if res['modalidade'] == modalidade_selecionada]
                
                print(f"Resultados de {atleta['nome']} (Matrícula: {matricula}):")
                if not resultados:
                    print("Nenhum resultado encontrado para a modalidade selecionada.")
                else:
                    for resultado in resultados:
                        print(f"Etapa: {resultado['etapa']}")
                        print(f"Data: {resultado['data']}")
                        print(f"Modalidade: {resultado['modalidade']}")
                        print(f"Tipo de Etapa: {resultado['tipo_etapa']}")
                        print(f"Resultados: {resultado['resultados']}")
                        print(f"Total: {resultado['total']}")
                        print("---")
        else:
            todos_resultados = self.modalidade.read("todos_resultados")
            for matricula, resultados in todos_resultados.items():
                atleta = self.modalidade.read("atleta", matricula)
                # Filtrando resultados pela modalidade selecionada
                if modalidade_selecionada:
                    resultados = [res for res in resultados if res['modalidade'] == modalidade_selecionada]
                
                if resultados:
                    print(f"Atleta: {atleta['nome']} (Matrícula: {matricula})")
                    for resultado in resultados:
                        print(f"  Etapa: {resultado['etapa']}")
                        print(f"  Data: {resultado['data']}")
                        print(f"  Modalidade: {resultado['modalidade']}")
                        print(f"  Tipo de Etapa: {resultado['tipo_etapa']}")
                        print(f"  Resultados: {resultado['resultados']}")
                        print(f"  Total: {resultado['total']}")
                        print("  ---")
        
        input("Pressione Enter para continuar...")

    def atualizar_resultados(self):
        matricula = input("Digite a matrícula do atleta: ")
        atleta = self.modalidade.read("atleta", matricula)
        if not atleta:
            print("Atleta não cadastrado.")
            input("Pressione Enter para voltar ao menu principal...")
            return

        print(f"Atleta: {atleta['nome']}")
        
        modalidade = input("Escolha a modalidade (1 - Carabina de Ar / 2 - Três Posições): ")
        while modalidade not in ['1', '2']:
            print("Opção inválida.")
            modalidade = input("Escolha a modalidade (1 - Carabina de Ar / 2 - Três Posições): ")
        
        modalidade_nome = "Carabina de Ar" if modalidade == '1' else "Três Posições"
        
        resultados = self.modalidade.read("resultado", matricula)
        resultados_modalidade = [r for r in resultados if r['modalidade'] == modalidade_nome]
        
        if not resultados_modalidade:
            print(f"Não há resultados cadastrados para {modalidade_nome}.")
            input("Pressione Enter para voltar ao menu principal...")
            return

        print(f"\nEtapas cadastradas para {modalidade_nome}:")
        for i, resultado in enumerate(resultados_modalidade, 1):
            print(f"{i}. Etapa {resultado['etapa']} - Data: {resultado['data']} - Total: {resultado['total']}")

        while True:
            try:
                escolha = int(input("\nDigite o número da etapa que deseja atualizar: ")) - 1
                if 0 <= escolha < len(resultados_modalidade):
                    resultado_escolhido = resultados_modalidade[escolha]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")

        print("\nResultados atuais:")
        for i, res in enumerate(resultado_escolhido['resultados'], 1):
            print(f"{i}. {res}")

        while True:
            try:
                rodada = int(input("\nQual resultado deseja atualizar (1-6)? "))
                if 1 <= rodada <= 6:
                    break
                else:
                    print("Escolha inválida. Digite um número entre 1 e 6.")
            except ValueError:
                print("Por favor, digite um número válido.")

        while True:
            try:
                if modalidade == '1':
                    novo_resultado = float(input("Digite o novo resultado (com decimal): "))
                else:
                    novo_resultado = int(input("Digite o novo resultado (sem decimal): "))
                break
            except ValueError:
                print("Valor inválido. Tente novamente.")

        print(f"\nNovo resultado para a rodada {rodada}: {novo_resultado}")
        confirmacao = input("Está correto? (S/N): ")

        if confirmacao.lower() == 's':
            resultado_escolhido['resultados'][rodada-1] = novo_resultado
            resultado_escolhido['total'] = sum(resultado_escolhido['resultados'])
            
            self.modalidade.update("resultado", matricula, resultado_escolhido)
            print("Resultado atualizado com sucesso!")
        else:
            print("Atualização cancelada. O resultado original será mantido.")

        input("Pressione Enter para voltar ao menu principal...")

    def visualizar_campeonato(self):
        todos_resultados = self.modalidade.read("todos_resultados")
        for matricula, resultados in todos_resultados.items():
            atleta = self.modalidade.read("atleta", matricula)
            print(f"Atleta: {atleta['nome']} (Matrícula: {matricula}, UF: {atleta['uf']})")
            for resultado in resultados:
                print(f"  Etapa: {resultado['etapa']}")
                print(f"  Data: {resultado['data']}")
                print(f"  Modalidade: {resultado['modalidade']}")
                print(f"  Total: {resultado['total']}")
            print("---")
        input("Pressione Enter para continuar...")

    def limpar_dados(self):
        confirmacao = input("Tem certeza que deseja limpar todos os dados? (s/n): ")
        if confirmacao.lower() == 's':
            mensagem = self.modalidade.delete("todos")
            print(mensagem)
        else:
            print("Operação cancelada.")
        input("Pressione Enter para continuar...")

    def verificar_campeonato(self):
        matricula = input("Digite a matrícula do atleta: ")
        atleta = self.modalidade.read("atleta", matricula)
        if not atleta:
            print("Atleta não encontrado.")
        else:
            self.mostrar_resultados_atleta(matricula)
        
        input("Pressione Enter para continuar...")

    def mostrar_resultados_atleta(self, matricula):
        resultados = self.modalidade.read("resultado", matricula)
        if not resultados:
            print("Não há resultados cadastrados para este atleta.")
            return

        print(f"Resultados do atleta (Matrícula: {matricula}):")
        
        # Separar resultados por modalidade
        carabina_ar = [r for r in resultados if r['modalidade'] == 'Carabina de Ar']
        tres_posicoes = [r for r in resultados if r['modalidade'] == 'Três Posições']

        for modalidade, resultados_modalidade in [("Carabina de Ar", carabina_ar), ("Três Posições", tres_posicoes)]:
            print(f"\nModalidade: {modalidade}")
            if resultados_modalidade:
                # Ordenar resultados por total, em ordem decrescente
                resultados_ordenados = sorted(resultados_modalidade, key=lambda x: x['total'], reverse=True)
                
                # Três maiores resultados totais
                print("Três maiores resultados totais:")
                for i, r in enumerate(resultados_ordenados[:3], 1):
                    print(f"{i}. Etapa {r['etapa']} - Data: {r['data']} - Total: {r['total']}")
                
                # Maior resultado - regional (assumindo que a etapa 1 é a regional)
                regional = next((r for r in resultados_modalidade if r['etapa'] == 1), None)
                if regional:
                    print(f"Maior resultado - Regional: Etapa {regional['etapa']} - Total: {regional['total']}")
                else:
                    print("Não há resultado da etapa regional.")
                
                # Resultado da final (assumindo que a etapa 2 é a final)
                final = next((r for r in resultados_modalidade if r['etapa'] == 2), None)
                if final:
                    print(f"Resultado da Final: Etapa {final['etapa']} - Total: {final['total']}")
                else:
                    print("Não há resultado da etapa final.")
            else:
                print("Não há resultados para esta modalidade.")

    def mostrar_resultados_ano(self, ano):
        todos_resultados = self.modalidade.read("todos_resultados")
        resultados_ano = {}

        for matricula, resultados in todos_resultados.items():
            resultados_ano[matricula] = [r for r in resultados if r['data'].startswith(ano)]

        if not any(resultados_ano.values()):
            print(f"Não há resultados cadastrados para o ano {ano}.")
            return

        print(f"Resultados do campeonato do ano {ano}:")

        for modalidade in ["Carabina de Ar", "Três Posições"]:
            print(f"\nModalidade: {modalidade}")
            resultados_modalidade = []

            for matricula, resultados in resultados_ano.items():
                atleta = self.modalidade.read("atleta", matricula)
                for r in resultados:
                    if r['modalidade'] == modalidade:
                        resultados_modalidade.append({
                            "atleta": atleta['nome'],
                            "matricula": matricula,
                            "etapa": r['etapa'],
                            "total": r['total']
                        })

            if resultados_modalidade:
                # Ordenar resultados por total, em ordem decrescente
                resultados_ordenados = sorted(resultados_modalidade, key=lambda x: x['total'], reverse=True)
                
                # Três maiores resultados totais
                print("Três maiores resultados totais:")
                for i, r in enumerate(resultados_ordenados[:3], 1):
                    print(f"{i}. Atleta: {r['atleta']} (Matrícula: {r['matricula']}) - Etapa {r['etapa']} - Total: {r['total']}")
                
                # Maior resultado - regional (assumindo que a etapa 1 é a regional)
                regional = max((r for r in resultados_modalidade if r['etapa'] == 1), key=lambda x: x['total'], default=None)
                if regional:
                    print(f"Maior resultado - Regional: Atleta: {regional['atleta']} (Matrícula: {regional['matricula']}) - Total: {regional['total']}")
                else:
                    print("Não há resultados da etapa regional.")
                
                # Resultados da final (assumindo que a etapa 2 é a final)
                finais = [r for r in resultados_modalidade if r['etapa'] == 2]
                if finais:
                    print("Resultados da Final:")
                    for r in sorted(finais, key=lambda x: x['total'], reverse=True):
                        print(f"Atleta: {r['atleta']} (Matrícula: {r['matricula']}) - Total: {r['total']}")
                else:
                    print("Não há resultados da etapa final.")
            else:
                print("Não há resultados para esta modalidade.")

    def limpar_dados(self):
        self.limpar_tela()
        print("=== Limpar todos os dados ===")
        confirmacao = input("Tem certeza que deseja limpar toda a base de dados? (S/N): ")
        if confirmacao.lower() == 's':
            self.modalidade.delete("todos")
            print("Todos os dados foram apagados com sucesso.")
        else:
            print("Operação cancelada. Nenhum dado foi apagado.")
        input("Pressione Enter para voltar ao menu inicial...")    

if __name__ == "__main__":
    gerenciamento = GerenciamentoTiroOlimpico()
    gerenciamento.menu()