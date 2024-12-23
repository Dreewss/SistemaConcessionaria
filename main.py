import sqlite3
from datetime import datetime
from time import sleep

# CONEXÃO COM O BANCO
conn = sqlite3.connect('meu-banco.db')
cursor = conn.cursor()

# TABELAS
cursor.execute('''CREATE TABLE IF NOT EXISTS veiculos (
    marca TEXT,
    modelo TEXT,
    ano INTEGER,
    cor TEXT,
    categoria TEXT,
    cambio TEXT,
    valor REAL,
    km REAL,
    placa TEXT PRIMARY KEY
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
    nome TEXT,
    idade INTEGER,
    cpf TEXT PRIMARY KEY,
    telefone TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS vendedores (
    nome TEXT,
    idade INTEGER,
    cpf TEXT PRIMARY KEY,
    salario REAL,
    comissao REAL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente TEXT,
    marca_veiculo TEXT,
    modelo_veiculo TEXT,
    placa_veiculo TEXT,
    nome_vendedor TEXT,
    cpf_cliente TEXT,
    cpf_vendedor TEXT,
    data_venda TEXT
)''')

conn.commit()

class Concessionaria:

    def __init__(self):
        self.veiculos = []
        self.clientes = []

    def listar_veiculos(self):
        print('--- LISTA DE VEÍCULOS ---\n')
        cursor.execute("SELECT * FROM veiculos")
        carros = cursor.fetchall()
        for carro in carros:
            print(f"--- {carro[0]} {carro[1]} ---\n Ano: {carro[2]}\n "
                  f"Cor: {carro[3]}\n Categoria: {carro[4]}\n Cambio: {carro[5]}\n "
                  f"Valor: R${carro[6]:,.2f}\n KM: {carro[7]}\n Placa: {carro[8]}\n")
            sleep(0.3)

    def cadastrar_veiculo(self):
        print("--- DADOS DO VEÍCULO --- \n")
        marca = input("Marca: ").upper()
        modelo = input("Modelo: ").upper()
        ano = input("Ano: ")
        cor = input("Cor: ").upper()
        cambio = input("Câmbio: ").upper()
        categoria = input("Categoria: ").upper()
        valor = input("Valor: ")
        km = input("Quilometragem aproximada: ")
        placa = input("Placa: ").upper()

        cursor.execute("SELECT placa FROM veiculos WHERE placa = ?", (placa,))
        if cursor.fetchone():
            print("Veículo já cadastrado.")
            return

        cursor.execute("INSERT INTO veiculos (marca, modelo, ano, cor, categoria, cambio, valor, km, placa) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (marca, modelo, ano, cor, categoria, cambio, valor, km, placa))
        conn.commit()
        print("Veículo cadastrado com sucesso!\n")

    def cadastrar_cliente(self, nome, idade, cpf, telefone):
        cursor.execute("SELECT cpf FROM clientes WHERE cpf = ?", (cpf,))
        if cursor.fetchone():
            print("Cliente já cadastrado.")
            return

        cursor.execute("INSERT INTO clientes (nome, idade, cpf, telefone) VALUES (?, ?, ?, ?)", (nome, idade, cpf, telefone))
        conn.commit()
        print("\nCliente cadastrado com sucesso!\n")

    def cadastrar_vendedor(self):
        print("--- DADOS DO VENDEDOR --- \n")
        cpf = input("Digite o CPF do vendedor: ")

        cursor.execute("SELECT cpf FROM vendedores WHERE cpf = ?", (cpf,))
        if cursor.fetchone():
            print("Vendedor já cadastrado.")
            return

        nome = input("Digite o nome do vendedor: ").title()
        idade = input("Digite a idade do vendedor: ")
        salario = input("Digite o salário do vendedor: ")
        comissao = 0

        cursor.execute("INSERT INTO vendedores (nome, idade, cpf, salario, comissao) VALUES (?, ?, ?, ?, ?)",
                       (nome, idade, cpf, salario, comissao))
        conn.commit()
        print("\nVendedor cadastrado com sucesso!\n")

    def vender(self):
        print("--- VENDER VEÍCULO ---\n")
        placa = input("Digite a placa do veículo a ser vendido: ").upper()

        cursor.execute("SELECT * FROM veiculos WHERE placa = ?", (placa,))
        veiculo = cursor.fetchone()
        if not veiculo:
            print("Veículo não encontrado.")
            return

        # BUSCA DE CLIENTE E VENDEDOR
        cpf_cliente = input("Digite o CPF do cliente: ")
        cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf_cliente,))
        cliente = cursor.fetchone()
        if not cliente:
            print("Cliente não encontrado. Por favor, cadastre o cliente primeiro.")
            return

        cpf_vendedor = input("Digite o CPF do vendedor: ")
        cursor.execute("SELECT * FROM vendedores WHERE cpf = ?", (cpf_vendedor,))
        vendedor = cursor.fetchone()
        if not vendedor:
            print("Vendedor não encontrado. Por favor, cadastre o vendedor primeiro.")
            return

        #COMISSAO
        comissao = veiculo[6] * 0.05
        cursor.execute("UPDATE vendedores SET comissao = comissao + ? WHERE cpf = ?", (comissao, cpf_vendedor))

        data_venda = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        cursor.execute("INSERT INTO vendas (nome_cliente, marca_veiculo, modelo_veiculo, placa_veiculo, nome_vendedor, cpf_cliente, cpf_vendedor, data_venda) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (cliente[0], veiculo[0], veiculo[1], veiculo[8], vendedor[0], cpf_cliente, cpf_vendedor, data_venda))

        cursor.execute("DELETE FROM veiculos WHERE placa = ?", (placa,))
        conn.commit()
        print(f"\nVenda registrada com sucesso: {veiculo[0]} {veiculo[1]} vendido para {cliente[0]} por R${veiculo[6]:,.2f}.\n")

    def apagar_vendedor(self):
        print("--- APAGAR VENDEDOR ---\n")
        cpf = input("Digite o CPF do vendedor a ser apagado: ")

        cursor.execute("SELECT * FROM vendedores WHERE cpf = ?", (cpf,))
        vendedor = cursor.fetchone()
        if not vendedor:
            print("Vendedor não encontrado.\n")
            return

        cursor.execute("DELETE FROM vendedores WHERE cpf = ?", (cpf,))
        conn.commit()
        print(f"Vendedor {vendedor[0]} apagado com sucesso.\n")

    def listar_vendedores(self):
        print('--- LISTA DE VENDEDORES ---\n')
        cursor.execute("SELECT * FROM vendedores")
        vendedores = cursor.fetchall()
        if not vendedores:
            print("Nenhum vendedor cadastrado.\n")
            return

        for vendedor in vendedores:
            print(f"Nome: {vendedor[0]}, Idade: {vendedor[1]}, CPF: {vendedor[2]}, "
                  f"Salário: R${vendedor[3]:,.2f}, Comissão: R${vendedor[4]:,.2f}\n")

    def listar_clientes(self):
        print('--- LISTA DE CLIENTES ---\n')
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        if not clientes:
            print("Nenhum cliente cadastrado.\n")
            return

        for cliente in clientes:
            print(f"Nome: {cliente[0]}, Idade: {cliente[1]}, CPF: {cliente[2]}\n")

    def listar_vendas(self):
        print('--- VENDAS ---\n')
        cursor.execute("SELECT * FROM vendas")
        vendas = cursor.fetchall()
        if not vendas:
            print("Nenhuma venda registrada.")
            return

        for venda in vendas:
            print(f"Veículo: {venda[2]} {venda[3]} \n"
                  f"Placa: {venda[4]}\n"
                  f"Cliente: {venda[1]}\n"
                  f"Vendedor: {venda[5]}\n"
                  f"Data: {venda[7]}\n")
            sleep(0.3)


if __name__ == "__main__":
    concessionaria = Concessionaria()
    concessionaria.cadastrar_veiculo()
    concessionaria.listar_veiculos()
