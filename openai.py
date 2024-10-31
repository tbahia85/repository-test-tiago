from random import randint
import math
import openai
import tkinter as tk
from tkinter import ttk, messagebox
import os
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis do arquivo .env
openai.api_key = os.getenv('OPENAI_API_KEY')

def criar_interface():
    # Criar janela principal
    janela = tk.Tk()
    janela.title("Calculadora Deusbeto")
    janela.geometry("400x500")
    janela.configure(bg="#f0f0f0")

    # Estilo
    style = ttk.Style()
    style.configure("TButton", padding=10, font=('Arial', 10))
    style.configure("TLabel", padding=10, font=('Arial', 12))

    # Frame principal
    frame = ttk.Frame(janela, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Título
    titulo = ttk.Label(frame, text="CALCULADORA DEUSBETO", font=('Arial', 16, 'bold'))
    titulo.grid(row=0, column=0, columnspan=2, pady=20)

    # Variáveis
    numero_var = tk.StringVar()
    resultado_var = tk.StringVar()
    raiz_var = tk.StringVar()

    # Função para processar número manual
    def processar_manual():
        try:
            numero = float(numero_entrada.get())
            calcular(numero)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite um número válido!")

    # Função para processar número aleatório
    def processar_aleatorio():
        numero = gerar_numero_openai()
        numero_entrada.delete(0, tk.END)
        numero_entrada.insert(0, str(numero))
        calcular(numero)

    # Função para calcular
    def calcular(numero):
        resultado = numero * 100
        raiz = math.sqrt(resultado)
        
        resultado_var.set(f"Multiplicado por 100: {resultado}")
        raiz_var.set(f"Raiz quadrada: {raiz:.2f}")

    # Entrada de número
    ttk.Label(frame, text="Digite um número:").grid(row=1, column=0, pady=10)
    numero_entrada = ttk.Entry(frame)
    numero_entrada.grid(row=1, column=1, pady=10)

    # Botões
    ttk.Button(frame, text="Calcular", command=processar_manual).grid(row=2, column=0, pady=10)
    ttk.Button(frame, text="Gerar Aleatório", command=processar_aleatorio).grid(row=2, column=1, pady=10)

    # Labels para resultados
    ttk.Label(frame, textvariable=resultado_var).grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Label(frame, textvariable=raiz_var).grid(row=4, column=0, columnspan=2, pady=10)

    return janela

def iniciar_interface():
    janela = criar_interface()
    janela.mainloop()

def gerar_numero_openai():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um gerador de números aleatórios."},
                {"role": "user", "content": "Gere um número aleatório entre 1 e 100. Responda apenas com o número."}
            ]
        )
        numero = int(response.choices[0].message.content)
        return numero if 1 <= numero <= 100 else randint(1, 100)
    except:
        print('\033[0;31mErro ao conectar com OpenAI. Usando gerador local.\033[m')
        return randint(1, 100)

def Deusbeto():
    while True:
        print('~' * 50)
        print('CALCULADORA DEUSBETO'.center(50))
        print('~' * 50)
        
        while True:
            escolha = input('Escolha uma opção:\n[1] - Inserir número manualmente\n[2] - Gerar número aleatório\nSua escolha: ')
            
            if escolha == '1':
                try:
                    numero = float(input('Digite um número: '))
                    break
                except ValueError:
                    print('\033[0;31mErro! Digite um número válido.\033[m')
                    
            elif escolha == '2':
                numero = gerar_numero_openai()
                print(f'Número gerado pela OpenAI: {numero}')
                break
                
            else:
                print('\033[0;31mOpção inválida! Digite 1 ou 2.\033[m')
        
        resultado = numero * 100
        raiz = math.sqrt(resultado)
        
        print('\n\033[0;32mRESULTADO:\033[m')
        print(f'Número original: {numero}')
        print(f'Multiplicado por 100: {resultado}')
        print(f'Raiz quadrada do resultado: {raiz:.2f}')

        continuar = input('\nDeseja usar a calculadora novamente? [S/N]: ').upper()
        if continuar != 'S':
            print('\nObrigado por usar a Calculadora Deusbeto!')
            break

# Executar a função
iniciar_interface()
