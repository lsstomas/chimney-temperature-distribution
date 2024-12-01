# pylint: disable=all

import numpy as np
import matplotlib.pyplot as plt


def calcular_parametros():
    # Propriedades e parâmetros
    propriedades = {
        "k": 1.4,  # Condutividade térmica (W/m°C)
        "h_i": 60,  # Coeficiente de convecção interno (W/m²°C)
        "h_o": 12,  # Coeficiente de convecção externo (W/m²°C)
        "T_interna": 350,  # Temperatura dos gases internos (°C)
        "T_externa": 25,  # Temperatura do ar externo (°C)
    }

    # Dimensões (em metros)
    dimensoes = {
        "L_ext": 0.30,  # Lado externo da chaminé (30 cm)
        "L_int": 0.25,  # Lado interno da chaminé (25 cm)
        "espessura": (0.30 - 0.25) / 2,  # Espessura da parede
    }

    # Parâmetros da malha
    malha = {
        "distancia_nos": 0.01,  # Distância entre nós (10 mm)
        "nx": int((dimensoes["L_ext"] / 2) / 0.01) + 1,
    }
    malha["ny"] = malha["nx"]

    return propriedades, dimensoes, malha


def inicializar_matriz_temperatura(ny, nx, T_externa, espessura, x, y, T_interna):
    T = np.full((ny, nx), T_externa)
    X, Y = np.meshgrid(x, y)
    mascara_solido = (X >= espessura) & (Y >= espessura)
    T[mascara_solido] = (T_interna + T_externa) / 2
    return T, X, Y, mascara_solido


def gauss_seidel(dimensoes, 
    T,
    X,
    Y,
    mascara_solido,
    propriedades,
    nx,
    ny,
    distancia_nos,
    max_iter=5000,
    tolerancia=1e-4,
):
    k, h_i, h_o, T_interna, T_externa = propriedades.values()
    for itr in range(max_iter):
        T_old = T.copy()
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                if mascara_solido[i, j]:
                    T[i, j] = 0.25 * (
                        T[i + 1, j] + T[i - 1, j] + T[i, j + 1] + T[i, j - 1]
                    )
                else:
                    if X[i, j] == dimensoes['espessura']:
                        T[i, j] = (
                            2 * k * T[i + 1, j] + 2 * h_i * distancia_nos * T_interna
                        ) / (2 * k + 2 * h_i * distancia_nos)
                    elif Y[i, j] == dimensoes['espessura']:
                        T[i, j] = (
                            2 * k * T[i, j + 1] + 2 * h_i * distancia_nos * T_interna
                        ) / (2 * k + 2 * h_i * distancia_nos)
                    elif X[i, j] == (dimensoes['L_ext'] / 2):
                        T[i, j] = (
                            2 * k * T[i - 1, j] + 2 * h_o * distancia_nos * T_externa
                        ) / (2 * k + 2 * h_o * distancia_nos)
                    elif Y[i, j] == (dimensoes['L_ext'] / 2):
                        T[i, j] = (
                            2 * k * T[i, j - 1] + 2 * h_o * distancia_nos * T_externa
                        ) / (2 * k + 2 * h_o * distancia_nos)
                    else:
                        T[i, j] = 0.25 * (
                            T[i + 1, j] + T[i - 1, j] + T[i, j + 1] + T[i, j - 1]
                        )
        erro = np.max(np.abs(T - T_old))
        if erro < tolerancia:
            print(f"Convergência alcançada em {itr} iterações.")
            break
    return T


def espelhar_matriz_temperatura(T):
    T_total = np.block([[np.flipud(np.fliplr(T)), np.flipud(T)], [np.fliplr(T), T]])
    return T_total


def plotar_distribuicao_temperatura(T_total, L_ext):
    x_total = np.linspace(-L_ext / 2, L_ext / 2, T_total.shape[1])
    y_total = np.linspace(-L_ext / 2, L_ext / 2, T_total.shape[0])
    X_total, Y_total = np.meshgrid(x_total, y_total)
    plt.figure(figsize=(8, 6))
    cp = plt.contourf(X_total * 100, Y_total * 100, T_total, cmap="hot")
    plt.colorbar(cp, label="Temperatura (°C)")
    plt.title("Distribuição de Temperatura na Chaminé")
    plt.xlabel("Largura (cm)")
    plt.ylabel("Altura (cm)")
    plt.axis("equal")
    plt.savefig("distribuicao_temperatura.png")
    plt.close()


def calcular_taxa_perda_calor(T, k, distancia_nos, L_ext):
    q_externo = -k * (T[1:-1, -1] - T[1:-1, -2]) / distancia_nos  # W/m²
    area_superficie = L_ext * 1.0  # Considerando 1 metro de comprimento
    Q_total = np.sum(q_externo) * distancia_nos * area_superficie  # W
    return Q_total


def simular_chamine():
    # Calcular parâmetros
    propriedades, dimensoes, malha = calcular_parametros()
    L_ext, espessura = dimensoes["L_ext"], dimensoes["espessura"]
    distancia_nos, nx, ny = malha["distancia_nos"], malha["nx"], malha["ny"]
    T_externa, T_interna = propriedades["T_externa"], propriedades["T_interna"]

    # Coordenadas
    x = np.linspace(0, L_ext / 2, nx)
    y = np.linspace(0, L_ext / 2, ny)

    # Inicializar matriz de temperatura
    T, X, Y, mascara_solido = inicializar_matriz_temperatura(
        ny, nx, T_externa, espessura, x, y, T_interna
    )

    # Método iterativo de Gauss-Seidel
    T = gauss_seidel(dimensoes, T, X, Y, mascara_solido, propriedades, nx, ny, distancia_nos)

    # Espelhar a matriz para obter a temperatura completa
    T_total = espelhar_matriz_temperatura(T)

    # Plotar distribuição de temperatura
    plotar_distribuicao_temperatura(T_total, L_ext)

    # Calcular a taxa de perda de calor
    Q_total = calcular_taxa_perda_calor(T, propriedades["k"], distancia_nos, L_ext)
    print(f"Taxa de Perda de Calor: {Q_total:.2f} W")


# Executar a simulação aprimorada
simular_chamine()
