from pyXSteam.XSteam import XSteam
import math
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







# impostiamo il nostro problema come un problema di circolazione naturale passiva dove 
# le nostre icognite sono la lunghezza dello steam generator x e 'altezza h del circuito
#oltre al dimensionamento dei tubi (Numero e lunghezza)
#per svolgere questo calcolo assumiamo la portata nota

m=5 #portata in kg/s
#1 bar=100kPa 
#STEAM GENERATOR

#conosciamo le condizioni di ingresso ed uscita del fluido dallo steam generator
#come liquido sottoraffreddato
T_in_sg=165 #°C
p_in_sg=2000 #kPa (per la funzione Xsteam va però utilizzato in bar)
h_in_sg=st.h_pt(p_in_sg/100, T_in_sg) #kJ/kg

#GEOMETRIA STEAM GENERATOR
D_sg=0.02 #m diametro del tubo

#come vapore saturo
T_out_sg=210 #°C
p_out_sg=1800 #kPa  
h_out_sg=st.hV_p(p_out_sg/100) #kJ/kg
 
#con un semplice bilancio termico calcoliamo il calore ceduto al fluido

Q_sg=m*(h_out_sg - h_in_sg) #kW
print(f"Calore ceduto dallo steam generator: {Q_sg:.2f} kW")

U_sg=1000 #W/m2K coefficiente globale di scambio termico
T_fiss=300 #°C temperatura delle pareti del tubo dello steam generator
T_log=((T_fiss - T_in_sg)-(T_fiss - T_out_sg))/ (  math.log( (T_fiss - T_in_sg)/(T_fiss - T_out_sg) )  ) #temperatura logaritmica media
print(f"Temperatura logaritmica media: {T_log:.2f} °C")
#calcolo Superficie di scambio necessaria
A_sg= (Q_sg*1000) / (U_sg * T_log) #m2
N_sg=860 #numero di tubi 
#trovo la lunghezza dello steam generator (che assumiamo come lunghezza dei tubi)
L_sg= A_sg / (math.pi * D_sg * N_sg) #m
print(f"Lunghezza steam generator: {L_sg:.2f} m")   

#CALCOLO CIRCOLAZIONE NATURALE PASSIVA
#conosciamo le condizioni del fluido in uscita dal condensatore, posso trovare la caduta di pressione

Dp_sg=p_in_sg - p_out_sg #kPa

#per assicurare la circolazione passiva devo imporre che la somma di tutte le perdite e della spinta data dalla differenza di densità
#e dalla caduta sia nulla

#il riser che va dal punto 1 al punto 2 corrisponde alla nostra altezza h che vogliamo calcolare
