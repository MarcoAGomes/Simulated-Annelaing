import math
import numpy as np
from matplotlib import pyplot

def fator_boltzmann(dif_energia,temperatura):
    return math.e**(-dif_energia/temperatura)

#definir a funcao a ser otimizada

#funcao (x-4)^2+(y+3)^2+(z-3)^2:     (Min Global em[4,-3,3] e energia min = 0)
"""def funcao(lista_param):
    return (lista_param[0]-4)**2+(lista_param[1]+3)**2+(lista_param[2]-3)**2"""

#funcao de Rosenbrock:     (Min Global em [1,1] e energia min = 0)
def funcao(lista_param):
    return (1-lista_param[0])**2+100*(lista_param[1]-lista_param[0]**2)**2

#funcao de Matyas:     (Min Global em [0,0] e energia min = 0) ({-10 <= x,y <= 10})
"""def funcao(lista_param):
    return 0.26*(lista_param[0]**2+lista_param[1]**2)-0.48*lista_param[0]*lista_param[1]"""

#funcao Bukin N.6:     (Min Global em [-10,1] e energia min = 0) ({-15 <= x <= -5} e {-3 <= y <= 3})
"""def funcao(lista_param):
    x = lista_param[0]
    y = lista_param[1]
    return (100*math.sqrt(abs(y-0.01*x**2))+0.01*abs(x+10))"""

#funcao McCormick:     (Min Global em [-0.54719,-1.54719] e energia min = -1.9133) ({-1.5 < x <= 4} e {-3 <= y <= 4})
"""def funcao(lista_param):
    x = lista_param[0]
    y = lista_param[1]
    return (math.sin(x+y)+(x-y)**2-1.5*x+2.5*y+1)"""

def simulated_annealing(temp_inicial,max_iteracoes,temp_final,fator_decaimento,param_iniciais,step):
    """Entradas: temperatura inicial, maximo de iteracoes, temperatura final, fator de decaimento, parametros iniciais, step
    \nSaidas: lista dos melhores valores de cada iteracao, energia de cada iteracao, lista de 0 ate iteracao maxima, menor energia encontrada
    """
    e_inicial = funcao(param_iniciais)

    lista_energias , lista_resultados = [] , []

    lista_energias.append(e_inicial)

    for contador in range(len(param_iniciais)):
        lista_resultados.append([])
        lista_resultados[contador].append(param_iniciais[contador])
    

    while (temp_inicial > temp_final):
        for iteracao in range(max_iteracoes):
            param_atual = param_iniciais.copy()
            
            indice = np.random.randint(0,len(param_iniciais))
            candidato = param_atual[indice] + np.random.uniform(-step,step)
            
            param_atual[indice] = candidato

            e_atual = funcao(param_atual)
            dif_e = e_atual - e_inicial

            if(dif_e <= 0):
                e_inicial = e_atual
                param_iniciais = param_atual.copy()
            
            else:
                teste = np.random.uniform(0,1)

                if (teste < fator_boltzmann(dif_e , temp_inicial)):
                    e_inicial = e_atual
                    param_iniciais = param_atual.copy()
                
                else:
                    pass
            
            lista_energias.append(e_inicial)
            
            for idx in range(len(param_iniciais)):
                lista_resultados[idx].append(param_iniciais[idx])


        temp_inicial *= fator_decaimento

    indice_otimizacao = np.argmin(lista_energias)
    resultados_otimizados = []

    for counter in range(len(param_iniciais)):
        resultados_otimizados.append(lista_resultados[counter][indice_otimizacao])
    
    tam_str = len("resultados otimizados: ")
    print("resultados otimizados: ",end="")
    
    for i in range(len(resultados_otimizados)):
        if i == 0:
            print("x"+str(i)+" = ",resultados_otimizados[i])
        
        else:
            print((tam_str-1)*' ',"x"+str(i)+" = ",resultados_otimizados[i])

    print("Temperatura final = ",temp_inicial)
    print("Menor energia: ",lista_energias[indice_otimizacao])
    
    eixo_h = list(range(len(lista_energias)))

    return(lista_resultados,lista_energias,eixo_h,lista_energias[indice_otimizacao])



#teste dos resultados:
maior_1 = True

while maior_1:
    x , y = np.random.randint(-10,10,size=2)
    resultados , energias , x , menor = simulated_annealing(1000,1000,1,0.9,[x,y],1)
    
    if menor < 0.001:
        maior_1 = False
        
        pyplot.figure()
        pyplot.subplot(2,1,1)
        pyplot.plot(x,energias)

        pyplot.subplot(2,1,2)
        pyplot.plot(x,resultados[0],'-g')
        pyplot.plot(x,resultados[1],'-r')  
        print("\n")

    else:
        pyplot.figure()
        pyplot.subplot(2,1,1)
        pyplot.plot(x,energias)

        pyplot.subplot(2,1,2)
        pyplot.plot(x,resultados[0],'-g')
        pyplot.plot(x,resultados[1],'-r')
        print("\n")

pyplot.show()