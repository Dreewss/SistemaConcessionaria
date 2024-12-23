import tkinter as tk
from tkinter import messagebox
from main import Concessionaria

class InterfaceConcessionaria:
    def __init__(self, concessionaria):
        self.concessionaria = concessionaria

        # MENU
        self.root = tk.Tk()
        self.root.title("Concessionária")
        self.root.geometry("800x600")

        # BOTOES
        tk.Label(self.root, text="PAINEL DE CADASTRO", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="Cadastrar Veículo", command=self.cadastrar_veiculo, width=25).pack(pady=20)
        tk.Button(self.root, text="Listar Veículos", command=self.listar_veiculos, width=25).pack(pady=20)
        tk.Button(self.root, text="Cadastrar Cliente", command=self.cadastrar_cliente, width=25).pack(pady=20)
        tk.Button(self.root, text="Cadastrar Vendedor", command=self.cadastrar_vendedor, width=25).pack(pady=20)
        tk.Button(self.root, text="Listar Vendedores", command=self.listar_vendedor, width=25).pack(pady=20)
        tk.Button(self.root, text="Listar Clientes", command=self.listar_clientes, width=25).pack(pady=20)
        tk.Button(self.root, text="Vender Veículo", command=self.vender, width=25).pack(pady=20)
        tk.Button(self.root, text="Sair", command=self.root.quit, width=25).pack(pady=20)

        self.root.mainloop()

    def validate_input(self, value, length):
     
        return len(value) == length and value.isdigit()

    def cadastrar_veiculo(self):
        def salvar():
            marca = entrada_marca.get()
            modelo = entrada_modelo.get()
            ano = entrada_ano.get()
            cor = entrada_cor.get()
            categoria = entrada_categoria.get()
            cambio = entrada_cambio.get()
            valor = entrada_valor.get()
            km = entrada_km.get()
            placa = entrada_placa.get()

            if all([marca, modelo, ano, cor, categoria, cambio, valor, km, placa]):
                try:
                    ano = int(ano)
                    valor = float(valor)
                    km = float(km)
                    self.concessionaria.cadastrar_veiculo(marca, modelo, ano, cor, categoria, cambio, valor, km, placa)
                    messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")
                    janela.destroy()
                except ValueError as e:
                    messagebox.showerror("Erro", f"Erro ao cadastrar veículo: {str(e)}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Veículo")
        janela.geometry("400x500")

        tk.Label(janela, text="Marca").pack()
        entrada_marca = tk.Entry(janela)
        entrada_marca.pack()

        tk.Label(janela, text="Modelo").pack()
        entrada_modelo = tk.Entry(janela)
        entrada_modelo.pack()

        tk.Label(janela, text="Ano").pack()
        entrada_ano = tk.Entry(janela)
        entrada_ano.pack()

        tk.Label(janela, text="Cor").pack()
        entrada_cor = tk.Entry(janela)
        entrada_cor.pack()

        tk.Label(janela, text="Categoria").pack()
        entrada_categoria = tk.Entry(janela)
        entrada_categoria.pack()

        tk.Label(janela, text="Câmbio").pack()
        entrada_cambio = tk.Entry(janela)
        entrada_cambio.pack()

        tk.Label(janela, text="Valor").pack()
        entrada_valor = tk.Entry(janela)
        entrada_valor.pack()

        tk.Label(janela, text="KM").pack()
        entrada_km = tk.Entry(janela)
        entrada_km.pack()

        tk.Label(janela, text="Placa").pack()
        entrada_placa = tk.Entry(janela)
        entrada_placa.pack()

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def listar_veiculos(self):
        veiculos = self.concessionaria.listar_veiculos()
        if not veiculos:
            messagebox.showinfo("Veículos Cadastrados", "Nenhum veículo cadastrado.")
        else:
            janela = tk.Toplevel(self.root)
            janela.title("Listar Veículos")
            janela.geometry("400x500")

            listbox_veiculos = tk.Listbox(janela, width=50, height=15)
            listbox_veiculos.pack(pady=10)

            for veiculo in veiculos:
                listbox_veiculos.insert(tk.END, veiculo)

            tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)

    def cadastrar_cliente(self):
        def salvar():
            nome = entrada_nome.get()
            idade = entrada_idade.get()
            cpf = entrada_cpf.get()
            telefone = entrada_telefone.get()

            if not self.validate_input(cpf, 9):
                messagebox.showerror("Erro", "CPF inválido.")
                return
            if not self.validate_input(telefone, 11):
                messagebox.showerror("Erro", "Telefone inválido.")
                return

            if all([nome, idade, cpf, telefone]):
                try:
                    self.concessionaria.cadastrar_cliente(nome, int(idade), cpf, telefone)
                    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                    janela.destroy()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao cadastrar o cliente: {e}")
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Cliente")
        janela.geometry("400x500")

        tk.Label(janela, text="Nome").pack()
        entrada_nome = tk.Entry(janela)
        entrada_nome.pack()

        tk.Label(janela, text="Idade").pack()
        entrada_idade = tk.Entry(janela)
        entrada_idade.pack()

        tk.Label(janela, text="CPF (9 dígitos)").pack()
        entrada_cpf = tk.Entry(janela)
        entrada_cpf.pack()

        tk.Label(janela, text="Telefone (11 dígitos)").pack()
        entrada_telefone = tk.Entry(janela)
        entrada_telefone.pack()

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def listar_clientes(self):
        clientes = self.concessionaria.listar_clientes()
        if not clientes:
            messagebox.showinfo("Clientes Cadastrados", "Nenhum cliente cadastrado.")
        else:
            messagebox.showinfo("Clientes Cadastrados", "\n".join(clientes))

    def cadastrar_vendedor(self):
        def salvar():
            nome = entrada_nome.get()
            idade = entrada_idade.get()
            cpf = entrada_cpf.get()
            salario = entrada_salario.get()
            comissao = entrada_comissao.get()
            telefone = entrada_telefone.get()

            if not self.validate_input(cpf, 9):
                messagebox.showerror("Erro", "CPF inválido.")
                return
            if not self.validate_input(telefone, 11):
                messagebox.showerror("Erro", "Telefone inválido.")
                return

            if all([nome, idade, cpf, salario, comissao, telefone]):
                try:
                    self.concessionaria.cadastrar_vendedor(nome, int(idade), cpf, float(salario), float(comissao), telefone)
                    messagebox.showinfo("Sucesso", "Vendedor cadastrado com sucesso!")
                    janela.destroy()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao cadastrar o vendedor: {e}")
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Vendedor")
        janela.geometry("400x400")

        tk.Label(janela, text="Nome").pack()
        entrada_nome = tk.Entry(janela)
        entrada_nome.pack()

        tk.Label(janela, text="Idade").pack()
        entrada_idade = tk.Entry(janela)
        entrada_idade.pack()

        tk.Label(janela, text="CPF (9 dígitos)").pack()
        entrada_cpf = tk.Entry(janela)
        entrada_cpf.pack()

        tk.Label(janela, text="Salário").pack()
        entrada_salario = tk.Entry(janela)
        entrada_salario.pack()

        tk.Label(janela, text="Comissão").pack()
        entrada_comissao = tk.Entry(janela)
        entrada_comissao.pack()

        tk.Label(janela, text="Telefone (11 dígitos)").pack()
        entrada_telefone = tk.Entry(janela)
        entrada_telefone.pack()

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def listar_vendedor(self):
        vendedores = self.concessionaria.listar_vendedores()
        if not vendedores:
            messagebox.showinfo("Vendedores Cadastrados", "Nenhum vendedor cadastrado.")
        else:
            messagebox.showinfo("Vendedores Cadastrados", "\n".join(vendedores))

    def vender(self):
        def realizar_venda():
            veiculo_selecionado = listbox_veiculos.curselection()
            if not veiculo_selecionado:
                messagebox.showerror("Erro", "Selecione um veículo da lista.")
                return

            veiculo_placa = listbox_veiculos.get(veiculo_selecionado)
            cpf_cliente = entrada_cliente.get()
            cpf_vendedor = entrada_vendedor.get()
            valor_venda = entrada_valor_venda.get()

            veiculo = self.concessionaria.buscar_veiculo(veiculo_placa)
            if not veiculo:
                messagebox.showerror("Erro", "Veículo não encontrado.")
                return

            cliente = self.concessionaria.buscar_cliente(cpf_cliente)
            vendedor = self.concessionaria.buscar_vendedor(cpf_vendedor)

            if not cliente:
                messagebox.showerror("Erro", "Cliente não encontrado.")
                return
            if not vendedor:
                messagebox.showerror("Erro", "Vendedor não encontrado.")
                return

            try:
                valor_venda = float(valor_venda)
            except ValueError:
                messagebox.showerror("Erro", "Valor da venda inválido.")
                return

            if valor_venda <= 0:
                messagebox.showerror("Erro", "O valor da venda deve ser positivo.")
                return

            try:
                self.concessionaria.vender_veiculo(veiculo_placa, cpf_cliente, cpf_vendedor, valor_venda)
                messagebox.showinfo("Sucesso", "Venda realizada com sucesso!")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao realizar a venda: {e}")

        janela = tk.Toplevel(self.root)
        janela.title("Vender Veículo")
        janela.geometry("400x400")

        tk.Label(janela, text="Selecione o Veículo").pack()
        listbox_veiculos = tk.Listbox(janela, width=50, height=10)
        listbox_veiculos.pack(pady=10)

        veiculos = self.concessionaria.listar_veiculos()
        for veiculo in veiculos:
            listbox_veiculos.insert(tk.END, veiculo)

        tk.Label(janela, text="CPF do Cliente").pack()
        entrada_cliente = tk.Entry(janela)
        entrada_cliente.pack()

        tk.Label(janela, text="CPF do Vendedor").pack()
        entrada_vendedor = tk.Entry(janela)
        entrada_vendedor.pack()

        tk.Label(janela, text="Valor da Venda").pack()
        entrada_valor_venda = tk.Entry(janela)
        entrada_valor_venda.pack()

        tk.Button(janela, text="Realizar Venda", command=realizar_venda).pack(pady=10)
        tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)


concessionaria = Concessionaria()
interface = InterfaceConcessionaria(concessionaria)
