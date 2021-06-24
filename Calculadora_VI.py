import tkinter as tk
from math import log,exp,sqrt
from scipy import stats
window=tk.Tk()
window.title('Calculadora VI')
ventana=tk.Frame(master=window)
ventana.pack()


#Filas de entrada de datos
tipo=tk.Entry(master=ventana, width=25)
labtipo=tk.Label(master=ventana, text='C para call, P para put')
tipo.grid(row=0,column=1)
labtipo.grid(row=0,column=0,sticky='e')

spot=tk.Entry(master=ventana, width=25)
labspot=tk.Label(master=ventana, text='Precio spot')
spot.grid(row=1,column=1)
labspot.grid(row=1,column=0,sticky='e')

strike=tk.Entry(master=ventana, width=25)
labstrike=tk.Label(master=ventana, text='Strike de la opción')
strike.grid(row=2,column=1)
labstrike.grid(row=2,column=0,sticky='e')

dias=tk.Entry(master=ventana, width=25)
labdias=tk.Label(master=ventana, text='Días a vencimiento')
dias.grid(row=3,column=1)
labdias.grid(row=3, column=0,sticky='e')

tasa=tk.Entry(master=ventana, width=25)
labtasa=tk.Label(master=ventana, text='Tasa libre de riesgo en %')
tasa.grid(row=4,column=1)
labtasa.grid(row=4,column=0,sticky='e')

prima=tk.Entry(master=ventana, width=25)
labprima=tk.Label(master=ventana,text='Precio de la prima')
prima.grid(row=5,column=1)
labprima.grid(row=5,column=0,sticky='e')



#Resultado
result=tk.Label(master=ventana, text='%')
result.grid(row=7,column=1)

def cargardata():
    N = stats.norm.cdf
    S0 = float(spot.get())
    K = float(strike.get())
    T = float(dias.get())/365
    r = float(tasa.get())
    C0 = float(prima.get())
    Sigma_init = 0.5
    opcion=tipo.get()
    if opcion=='C':
        def BS(S0,K,T,r,sigma):
            S0 = float(S0)
            d1 = (log(S0/K)+(r + 0.5 * sigma**2)*T)/(sigma*sqrt(T))
            d2 = (log(S0/K)+(r - 0.5*sigma**2)*T)/(sigma*sqrt(T))
            value = (S0*N(d1)-K*exp(-r*T)*N(d2))
            return value
    elif opcion=='P':
        def BS(S0,K,T,r,sigma):
            S0 = float(S0)
            d1 = (log(S0/K)+(r + 0.5 * sigma**2)*T)/(sigma*sqrt(T))
            d2 = (log(S0/K)+(r - 0.5*sigma**2)*T)/(sigma*sqrt(T))
            value = (K*exp(-r*T)*N(-d2))-(S0*N(-d1))
            return value
    def Vega(S0,K,T,r,sigma):
        S0 = float(S0)
        d1 = (log(S0/K)+(r + 0.5 * sigma**2)*T)/(sigma*sqrt(T))
        vega = S0 * N(d1)*sqrt(T)
        return vega
    def ImpliedVol(S0, K, T, r, C0, sigma_est, it=100):
        for i in range(it):
            sigma_est -= ((BS(S0,K,T,r, sigma_est)-C0)/Vega(S0,K,T,r,sigma_est))
        result["text"]= f'La volatilidad implícita es de {round(sigma_est,2)*100}%'
    ImpliedVol(S0, K, T, r, C0, Sigma_init, it=100)


#Botones
cargar=tk.Button(master=ventana, text='Calcular VI',command=cargardata)
cargar.grid(row=6,column=0)
#resolv=tk.Button(master=ventana,text='Calcular VI',command=ImpliedVol(S0,K,T,r,C0,Sigma_init))
#resolv.grid(row=6,column=3)
window.mainloop()