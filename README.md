# Simulação de Transferência de Calor em uma Chaminé

Este projeto simula a distribuição de temperatura e a taxa de perda de calor em uma chaminé quadrada utilizando o método de diferenças finitas. Ele modela a condução de calor através das paredes e a convecção nas superfícies interna e externa.

---

## **Pré-requisitos**

Certifique-se de ter o Python instalado em sua máquina. Além disso, as bibliotecas abaixo são necessárias:

- **NumPy**: Para cálculos numéricos.
- **Matplotlib**: Para geração de gráficos.

Você pode instalá-las utilizando:

```bash
pip install numpy matplotlib
```

---

## **Como Executar**

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Entre no diretório do projeto:
   ```bash
   cd seu-repositorio
   ```
3. Execute o script principal:
   ```bash
   python main.py
   ```

---

## **Saídas**

- **Gráficos:**
  - Uma grade de nós representando a seção transversal da chaminé.
  - Um gráfico da distribuição de temperatura nas paredes.
- **Taxa de Perda de Calor:** Exibida no console ao final da simulação.

---

## **Personalizações**

- **Parâmetros ajustáveis:** 
  No arquivo `main.py`, você pode modificar:
  - Dimensões da chaminé.
  - Temperaturas interna e externa.
  - Coeficientes de transferência de calor.
