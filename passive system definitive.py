from pyXSteam.XSteam import XSteam
import math
from scipy.optimize import fsolve 

import numpy as np

# Inizializza l'oggetto con il sistema di unità MKS:
# Pressione in bar, Temperatura in °C, Energia in kJ/kg
st = XSteam(XSteam.UNIT_SYSTEM_MKS)

# --- ESEMPI DI UTILIZZO ---

# 1. Proprietà alla SATURAZIONE (basta una sola variabile, P o T)
p_operativa = 10.0 # bar
h_liquido_sat = st.hL_p(p_operativa)  # Entalpia liquido saturo (f)
h_vapore_sat = st.hV_p(p_operativa)   # Entalpia vapore saturo (g)
t_sat = st.tsat_p(p_operativa)        # Temperatura di saturazione

# 2. SOTTORAFFREDDATO o SURRISCALDATO (servono due variabili: P e T)
temp_reale = 20.0 # °C
press_reale = 15.0 # bar
rho = st.rho_pt(press_reale, temp_reale) # Densità [kg/m³]
h_sub = st.h_pt(press_reale, temp_reale) # Entalpia [kJ/kg]
# 3. MISCELA LIQUIDO-VAPORE (servono due variabili: P e X
#dove X è la qualità del vapore, ovvero la frazione in massa di vapore nella miscela)
qualita_vapore = 0.8 # 80% vapore, 20%
press_miscel = 5.0 # bar
h_mix = st.h_px(press_miscel, qualita_vapore) # Entalpia miscela [kJ/kg]
# --- FINE ESEMPI DI UTILIZZO ---

def solve_colebrook(Re, e_d, tol=1e-6):
    f = 0.02  # Valore iniziale
    while True:
        # Formula di Colebrook riarrangiata per f
        f_new = (1 / (-2 * math.log10(e_d/3.7 + 2.51/(Re * math.sqrt(f)))))**2
        if abs(f_new - f) < tol:
            return f_new
        f = f_new
#costanti




g=9.81 #m/s2
R=0.4615 #kJ/kgK  costante del gas per il vapore acqueo
r=0.6e-6 #m scabrezza assoluta dei tubi 

# impostiamo il nostro problema come un problema di circolazione naturale passiva dove 
# le nostre icognite sono la lunghezza dello steam generator x e 'altezza h del circuito
#oltre al dimensionamento dei tubi (Numero e lunghezza)
#per svolgere questo calcolo assumiamo la portata nota

m=5 #portata in kg/s
#1 bar=100kPa 
#STEAM GENERATOR

#conosciamo le condizioni di ingresso ed uscita del fluido dallo steam generator
#come liquido sottoraffreddato
x_in_sg=0 #liquido sottoraffreddato
T_in_sg=165 #°C
p_in_sg=2000 #kPa (per la funzione Xsteam va però utilizzato in bar)
h_in_sg=st.h_pt(p_in_sg/100, T_in_sg) #kJ/kg
rho_in_sg=st.rho_pt(p_in_sg/100, T_in_sg) #kg/m3
mu_in_sg=st.my_pt(p_in_sg/100, T_in_sg) #Pa.s   
#GEOMETRIA STEAM GENERATOR
D_sg=0.005 #m diametro del tubo coincidente col diametro idraulico

#come vapore saturo
x_out_sg=1 #vapore saturo
T_out_sg=210 #°C
p_out_sg=1906 #kPa  
h_out_sg=st.hV_p(p_out_sg/100) #kJ/kg
rho_out_sg=st.rhoV_p(p_out_sg/100) #kg/m3
mu_out_sg=st.my_pt(p_out_sg/100, T_out_sg) #Pa.s
#con un semplice bilancio termico calcoliamo il calore ceduto al fluido

Q_sg=m*(h_out_sg - h_in_sg) #kW
print(f"Calore ceduto dallo steam generator: {Q_sg/1000:.2f} MW")

U_sg=1860 #W/m2K coefficiente globale di scambio termico
T_fiss=300 #°C temperatura delle pareti del tubo dello steam generator
T_log=((T_fiss - T_in_sg)-(T_fiss - T_out_sg))/ (  math.log( (T_fiss - T_in_sg)/(T_fiss - T_out_sg) )  ) #temperatura logaritmica media
print(f"Temperatura logaritmica media: {T_log:.2f} °C")
#calcolo Superficie di scambio necessaria
A_sg= (Q_sg*1000) / (U_sg * T_log) #m2
N_sg=862 #numero di tubi 
#trovo la lunghezza dello steam generator (che assumiamo come lunghezza dei tubi)
L_sg= A_sg / (math.pi * D_sg * N_sg) #m
print(f"Lunghezza steam generator: {L_sg:.2f} m")   
print(f"densità in uscita dallo steam generator: {rho_out_sg:.2f} kg/m3")
#CALCOLO CADUTA DI PRESSIONE NELLO STEAM GENERATOR CON FORMULE BIFASE DAL FILE EXCEL

Dp_sg=102.035 #kPa




#AIR HEAT EXCHANGER
x_in_ahx=1 #vapore saturo
T_in_ahx=210 #°C vapore saturo in ingresso
p_in_ahx=1862.4 #kPa
h_in_ahx=st.hV_p(p_in_ahx/100) #kJ/kg
rho_in_ahx=st.rhoV_p(p_in_ahx/100) #kg/m3  

x_out_ahx=0 #liquido sottoraffreddato
T_out_ahx=208.8 #°C liquido sottoraffreddato in uscita
p_out_ahx=1800 #kPa 
h_out_ahx=st.hL_p(p_out_ahx/100) #kJ/kg
rho_out_ahx=st.rhoL_p(p_out_ahx/100) #kg/m3  

print(f"entalpia in ingresso ahx: {h_in_ahx:.2f} kJ/kg")
print(f"entalpia in uscita ahx: {h_out_ahx:.2f} kJ/kg") 


Q_ahx=m*(h_in_ahx - h_out_ahx) #kW
print(f"Calore ceduto dall'hair heat exchanger: {Q_ahx/1000:.2f} MW")    
U_ahx=1736 #W/m2K coefficiente globale di scambio termico
T_fiss_ahx=35 #°C temperatura delle pareti del tubo dell'hair heat exchanger
T_log_ahx=((T_in_ahx - T_fiss_ahx)-(T_out_ahx - T_fiss_ahx))/ (  math.log( (T_in_ahx - T_fiss_ahx)/(T_out_ahx - T_fiss_ahx) )  ) #temperatura logaritmica media
print(f"Temperatura logaritmica media hair heat exchanger: {T_log_ahx:.2f} °C")
#calcolo Superficie di scambio necessaria   
A_ahx= (Q_ahx*1000) / (U_ahx * T_log_ahx) #m2
L_ahx=2 #m  
D_ahx=0.004 #m diametro del tubo coincidente col diametro idraulico
#trovo il numero di tubi dell'hair heat exchanger (che assumiamo come lunghezza dei tubi)
N_ahx= math.ceil( A_ahx / (math.pi * D_ahx * L_ahx) ) #numero di tubi   
print(f"Numero di tubi hair heat exchanger: {N_ahx:.2f}")          

#CALCOLO CADUTA DI PRESSIONE NELL'AIR HEAT EXCHANGER

#prendo il valore dal file excel
Dp_AHX=39.81 #kPa


#WATER WATER HEAT EXCHANGER

T_in_wwhx=208.8 #°C liquido sottoraffreddato in ingresso
p_in_wwhx=1862.1 #kPa 
h_in_wwhx=st.hL_p(p_in_wwhx/100) #kJ/kg
rho_in_wwhx=st.rhoL_p(p_in_wwhx/100) #kg/m3

x_out_wwhx=-0.1
T_out_wwhx=165 #°C liquido sottoraffreddato in uscita
p_out_wwhx=1854.28 #kPa
h_out_wwhx=(x_out_wwhx)*st.hV_p(p_out_wwhx/100)+(1-x_out_wwhx)*st.hL_p(p_out_wwhx/100) #kJ/kg
rho_out_wwhx=st.rhoL_p(p_out_wwhx/100) #kg/m3
mu_out_wwhx=st.my_pt(p_out_wwhx/100, T_out_wwhx) #Pa.s

Q_wwhx=m*(h_in_wwhx - h_out_wwhx) #kW
print(f"Calore ceduto dal water water heat exchanger: {Q_wwhx/1000:.2f} MW")    
U_wwhx=1122 #W/m2K coefficiente globale di scambio termico
T_fiss_wwhx=100 #°C temperatura delle pareti del tubo del water water heat exchanger
T_log_wwhx=((T_in_wwhx - T_fiss_wwhx)-(T_out_wwhx - T_fiss_wwhx))/ (math.log( (T_in_wwhx - T_fiss_wwhx)/(T_out_wwhx - T_fiss_wwhx))) #temperatura logaritmica media
print(f"Temperatura logaritmica media water water heat exchanger: {T_log_wwhx:.2f} °C")
#calcolo Superficie di scambio necessaria   
A_wwhx= (Q_wwhx*1000) / (U_wwhx * T_log_wwhx) #m2
L_wwhx=1.5 #m
D_wwhx=0.01 #m diametro del tubo coincidente col diametro idraulico
#trovo il numero di tubi del water-water heat exchanger (che assumiamo come lunghezza dei tubi)
N_wwhx= math.ceil( A_wwhx / (math.pi * D_wwhx * L_wwhx) ) #numero di tubi
print(f"Numero di tubi water water heat exchanger: {N_wwhx:.2f}")   

#CALCOLO CADUTA DI PRESSIONE NEL WATER WATER HEAT EXCHANGER dal FILE EXCEL

Dp_wwhx=7.1863 #kPa

Dp_scambiatori=Dp_sg + Dp_AHX + Dp_wwhx #kPa
print(f"Caduta di pressione totale negli scambiatori: {Dp_scambiatori:.2f} kPa")    

#a questo punto bisogna considerare la perdita di pressione nel riser 1-2 e la ricrescita di pressione nella discesa 3-4 entrambi dipendenti da h
# e le perdite concentrate delle curve, ne consideriamo 4 in totale (2 in alto e 2 in basso)

#considero ora le perdite concentrate delle curve potremo calcolare  solo quella nella parte in basso poiché l'altra dipende dall'altezza h
K_curve_up=1.207 #coefficiente di perdita per le curve sopra
K_curve_down=1.822 #coefficiente di perdita per le curve sotto


rho_5=rho_out_wwhx #kg/m3
D_56=0.15 #m diametro della discesa
w5=m/(math.pi*D_56**2/4*rho_5) #velocità del fluido nella discesa #m/s   

Re56=(w5*D_56*rho_5)/mu_out_wwhx #numero di Reynolds nella discesa
e56=r/D_56 #scabrezza relativa nella discesa
f56=solve_colebrook(Re56, e56)
print(f"indice di resistenza downcomer 56: {f56:.6f}")
print(f"Velocità del fluido nel downcomer 56: {w5:.2f} m/s")
print(f"densità in uscita dal water water heat exchanger: {rho_5:.2f} kg/m3")


Dp_conc_down= K_curve_down * rho_5 * w5**2 /1000 #kPa #tenedo già conto che ci sono 2 curve 



print(f"Caduta di pressione nella curva in basso: {Dp_conc_down:.2f} kPa")



#il riser che va dal punto 1 al punto 2 corrisponde alla nostra altezza h che vogliamo calcolare
#calcoliamone prima velocità ed indice di resistenza 

D12=0.15 #m diametro del riser
#calcolo velocità del fluido nel riser 1-2 e relativo numero di Reynolds e fattore di attrito

w1=m/(math.pi*D12**2/4*rho_out_sg) #velocità del fluido nel riser #m/s

Re12=(w1*D12*rho_out_sg)/mu_out_sg #numero di Reynolds nel riser
e12=r/D12 #scabrezza relativa nel riser

f12=solve_colebrook(Re12, e12)
print(f"indice di resistenza riser12: {f12:.6f}")
print(f"Velocità del fluido nel riser 1_2: {w1:.2f} m/s")


rho1=rho_out_sg #kg/m3

#bilancio di pressioni nel circuito chiuso

Dp_parziale=Dp_scambiatori+Dp_conc_down #kPa

print(f"Caduta di pressione degli scambiatori e concentrato in basso: {Dp_parziale:.2f} kPa")  

#Consideriamo infine le perdite di pressione nel riser, nella discesa e concentrate in alto che dipendono dalla nostra altezz h
#siccome le formule sono non lineari risolviamo con fsolve e troviamo il valore per cui il bilancio di pressione è nullo

def bilancio_pressione(h):
    F=(f12/(R*(T_out_sg+273.15)))*(w1**2/2*h-g/2*h**2)
    Dp_12= p_out_sg*(np.exp(-1*F)-1)  #kPa
    Dp_conc_up= K_curve_up * (w1**2/2-g*h)**2 * (w1*rho1/np.sqrt(w1**2-2*g*h)) /1000 #kPa
    Dp_g12=(w1*rho1/(np.sqrt(w1**2-2*g*h)) + rho1)*g*h/(2*1000) #kPa
    Dp_56=-(rho_5*g*(h+L_sg)-rho_5*w5**2/2*f56/D_56*(h+L_sg))/1000 #kPa
    Dp_totale= Dp_parziale + Dp_12 + Dp_conc_up+Dp_56
    return Dp_totale    


h_sol=fsolve(bilancio_pressione, 10) #valore iniziale di 10 m
print(f"l'altezza h del circuito di circolazione naturale passiva è di: {h_sol[0]:.2f} m")


#l'altezza h trovata è compatibile con il bilancio di pressione del circuito chiuso e anche con il vincolo geometrico
#che sia minore dell'altezza massima della nave di 40 m


print(f"l'altezza totale data da h+Lsg è di: {h_sol[0]+L_sg:.2f} m che è minore di 40 m quindi compatibile con il vincolo geometrico")
