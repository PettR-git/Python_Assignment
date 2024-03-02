import pandas as pd
import matplotlib.pyplot as plt

#Author: Petter Rignell
#Date: 2024-02-15
#Updated: 2024-02-27

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

#Hämta data beroende på struktur och sätt att avläsa
df_cpi_default = pd.read_csv('cpi.csv', sep=';', encoding='latin_1')
df_region = pd.read_csv('regions.csv', sep=';', encoding='latin_1')
df_inflation = pd.read_csv('inflation.csv', sep=',', encoding='utf-8-sig')
#För att få 'Land' i cpi-dataframe
df_cpi = pd.merge(df_region[['Land','Landskod','Kontinent']], df_cpi_default, on='Landskod')

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
    
def visualizeCpiData():
    #Hämta land från lista
    c_data = df_cpi[df_cpi['Land'].isin(cntry_list)]
    #Initiera rader och kolumner
    columns = ['Land'] + [str(year) for year in range(1960, 2022)]
    c_data = c_data[columns]
    c_data.set_index('Land', inplace=True)
    
    #Initiera figurs storlek
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_axes([0,0,1,1])
    
    for c in c_data.index:
        #Plotta inflationsdata för varje land
        ax.plot(c_data.columns, c_data.loc[c], label = c)
        #Skriv ut max och min punkter mha scatter
        ax.scatter(c_data.loc[c].idxmax(), c_data.loc[c].max(), color = 'r', marker = 'o')
        ax.scatter(c_data.loc[c].idxmin(), c_data.loc[c].min(), color = 'b', marker = 'o')
    
    #Visualisera axelvärden, labels, och rutnät
    ax.set_title("Inflation på årsbasis")
    ax.set_xlabel("År")
    ax.set_ylabel("Inflation (%)")
    ax.legend(loc='upper right')
    ax.grid(axis='both', color='lightgrey', linewidth='1.0')
    plt.xticks(rotation=90)
    plt.show()
    

cntry_list = []

while(True):
    #Plotta vid tre länder
    if len(cntry_list) == 3:
        visualizeCpiData()
        break
    else:
        inp = input('Skriv ett land, eller avsluta (END): ')
        #Kunna sluta
        if(inp == 'END'):
            #Säkerställa att lista inte är tom
            if cntry_list:
                visualizeCpiData()
            break
        #Om namnet inte finns
        elif inp not in df_cpi['Land'].values:
            print('Fel namn på land')
        else:
            #Felhantera om inga värden för just inflation finns, med start från kolumn 4 (1960)
            if not df_cpi.loc[df_cpi['Land'] == inp, df_cpi.columns[3]:].isnull().all().all(): 
                cntry_list.append(inp)
            else:
                print(f"Inga inflationsvärden för {inp}")


# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2B
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

#Räkna ut inflationsförändring
def calcCpiDerivFactor(country):
    filt = (df_cpi['Land'] == country)
    ff_list = []
    year_list = []
    
    #Ta reda på om det finns instans av specifikt land i dataframe
    if(filt.any()):
        #Räkna ut ff för år i intervall
        for year in range(1960, 2022):
            year_str = str(year)
            prev_year_str = str(year-1)
            #Båda årtalen måste finnas som kolumn
            if year_str in df_cpi.columns and prev_year_str in df_cpi.columns:
                #Räkna ut ff för ett år
                ff = 100*((df_cpi.loc[filt, year_str] - df_cpi.loc[filt, prev_year_str])/df_cpi.loc[filt, prev_year_str])
                ff_list.append(ff.item())
                year_list.append(year_str)
                
    else:
        print("Landet finns ej.")
         
    return ff_list, year_list

#Skapa ett stapeldiagram
def visualizeCpiChange(ff_list, year_list, country):
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_axes([0,0,1,1])
    #Ange värden med listor
    ax.bar(year_list, ff_list, color = 'steelblue')
    #Visualisera axelvärden och rutnät
    ax.set_title(f"{country} - Inflationsförändring från ett år till ett annat")
    ax.set_xlabel("År")
    ax.set_ylabel("Inflationsförändring (%)")
    ax.grid(axis='both', color='lightgrey', linewidth='1.0')
    plt.xticks(rotation=90)
    plt.show()
    

inp = input("Ange det land du vill analysera inflationsförändring på: ")
ff_list, year_list = calcCpiDerivFactor(inp)
#För att säkerställa korrekt typ av värden (inte nan)
ff_is_numeric = any(isinstance(x, (int, float)) for x in ff_list)

#Säkerställa numeriska värden och att årslista inte är tom
if (ff_is_numeric and year_list):
    visualizeCpiChange(ff_list, year_list, inp)
else:
    print("Landet har ej valida värden")
    print("")

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 3
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

#Få högsta 6 och lägsta 6 inflationsvärden för ett specifikt år
def getHighestAndLowestInflation(year):
    #Data från alla länder i det specifika året
    inf_data = df_cpi[['Land', str(year)]].dropna()
    #Sortera för att lättare filtrera
    sort_inf = inf_data.sort_values(by = str(year), ascending = False)
    
    #Filtrera högst och lägst värden
    highest_inf = sort_inf.head(6)
    lowest_inf = sort_inf.tail(6)
    #Ta bort index från df
    highest_inf.to_string(index=False)
    lowest_inf.to_string(index=False)
    
    return highest_inf, lowest_inf


#Plotta högsta 6 och lägsta 6 inflationsvärden för ett specifikt år
def visualizeMaxMinInflation(highest_inf, lowest_inf, year):
    #TABELL
    title_r1 = "LÄNDER MED HÖGST OCH LÄGST INFLATION"
    title_r2 = f"ÅR {year}"
    
    print("")
    print("="*72)
    #Skapa mellanrum i titeln
    print(" ".join(title_r1))
    print(25*" ", " ".join(title_r2))
    print("-"*72)
    print(" "*11, "Högsy", " "*30, "Lägst")
    print(" "*10, " -----", " "*30, "-----")
    print("{:20}{:20}{:20}{:20}".format( "Land", "Inflation[%]", "Land", "Inflation[%]"))
    
    #Skriva ut högst och lägst inflation, med formatering
    for i in range(len(highest_inf.iloc[:, 0])):
        print("{:<20}{:<20.1f}{:<20}{:<20.1f}".format(highest_inf.iloc[i][0][:18], highest_inf.iloc[i][1], lowest_inf.iloc[i][0][:18], lowest_inf.iloc[i][1]))

    print("="*72)
    
    #STAPELDIAGRAM
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_axes([0,0,1,1])
    max_min_inf = pd.concat([lowest_inf, highest_inf])
    max_min_inf = max_min_inf.sort_values(by = max_min_inf.columns[1], ascending = True)
    #Hämta data för varje stapel (kolumn: 0 = Land, kolumn: 1 = inflation)
    for i in range(len(max_min_inf.iloc[:,0])):
        ax.bar(max_min_inf.iloc[i, 0][:18], max_min_inf.iloc[i, 1], color="steelblue")
    
    #Axelvärden och rutnät
    ax.set_title(f"Högst och lägst inflation uppmätt {year}")
    ax.set_xlabel("Länder")
    ax.set_ylabel("Inflation (%)")
    ax.grid(axis='both', color='lightgrey', linewidth='1.0')
    plt.xticks(rotation=90)
    plt.show() 
    

#Hantera input
year = input("Skriv årtal för att visa länder med högst och lägst inflation under perioden: ")
highest_inf, lowest_inf = getHighestAndLowestInflation(year)
visualizeMaxMinInflation(highest_inf, lowest_inf, year)



# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

#Plotta kontinenters medelinflation och dess länders högsta och lägsta inflation
def plotContinentMeanMaxMinInflation():
    #Gruppera data med avseende på kontinenter
    group_continents = df_cpi.groupby('Kontinent')  
    mean_list = []
    
    #TABELL
    title_r1 = "OLIKA KONTINENTERS INFLATION UNDER"
    title_r2 = "TIDSPERIODEN 1960 -- 2022"
    
    print("")
    print("="*76)
    print(" ".join(title_r1))
    print(15*" ", " ".join(title_r2))
    print("-"*76)
    print("{:20}{:25}{:20}{:5}".format(""*15, "Högst", "Lägst", "Medel(1960-2022)"))
    print("{:20}{:10}{:15}{:10}{:10}{:20}".format("Kontinent/Land", "Inf[%]", "År", "Inf[%]", "År", "Inf[%]"))
    print("-"*76)
    
    #För att skriva ut varje kontinents medelvärde på inflation och länders högsta och lägsta inflation
    for continent, group_data in group_continents:
        #Ta ut specifika alla rader och specifika kolumner: Land och årtalen
        df_conti = group_data.iloc[:, [0] + list(range(3, len(group_data.columns)))]
        
        #Räkna ut medelvärde för kontinent
        mean_val = df_conti.iloc[:, 2:].mean().mean()      
        mean_list.append({'Kontinent': continent, 'Mean Inflation': mean_val})
        
        #Skriv ut medelinflation (kan göras senare med listan, men onödigt då loop kan användas)
        print("{:66}{:<10.1f}".format(continent, mean_val))
        
        #Avrunda inflationsdata
        df_round = df_conti.round(1)
        #Stack för att förenkla senare med filtrering
        df_stack = df_round.set_index('Land').stack().reset_index()
        df_stack.columns = ['Land', 'År', 'Inflation']
        
        #Få ut de högsta och lägsta värdena
        top_three = df_stack.nlargest(3, 'Inflation')
        bot_three = df_stack.nsmallest(3, 'Inflation')
        #Lägg till kontinent först av kolumner
        top_three.insert(0, 'Kontinent', continent)
        bot_three.insert(0, 'Kontinent', continent)
        
        #Skriv ut länders högsta inflation
        for i in range(len(top_three)):
            print("{:2}{:18}{:<10.1f}{:20}".format("", top_three.iloc[i, 1][:15], top_three.iloc[i, 3], top_three.iloc[i, 2]))
        
        #Skriv ut länders lägsta inflation
        for i in range(len(bot_three)):
            print("{:2}{:43}{:<10.2f}{:20}".format("", bot_three.iloc[i, 1][:15], bot_three.iloc[i, 3], bot_three.iloc[i, 2]))
        
        print("-"*76)
    
    print("="*76)


plotContinentMeanMaxMinInflation()

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

#Skriv ut inflation baserat på användarinput
def plotInflation():
    #Gör om dataframe till engelska ord och lägg till COUNTRY i dataframe för inflation
    df_region.rename(columns={'Landskod':'LOCATION'}, inplace=True)
    df_inf = pd.merge(df_inflation, df_region[['LOCATION', 'Land']], on='LOCATION')
    df_inf.rename(columns={'Land':'COUNTRY'}, inplace=True)
    
    country_inp = input("Ange ett land att analysera: ")
    subject_inp = input("Ange ett ämne: ")
    freq_inp = input("Ange tidsfrekvensen: ")
    measure_inp = input("Ange sätt att avmäta och visa inflationen: ")
    
    #Filtrera beroende på användarinput
    df_input = df_inf[(df_inf['COUNTRY'].str.upper() == country_inp.upper()) &
                      (df_inf['SUBJECT'].str.upper() == subject_inp.upper()) &
                      (df_inf['FREQUENCY'].str.upper() == freq_inp.upper()) &
                      (df_inf['MEASURE'].str.upper() == measure_inp.upper())]
    
    #Sortera alla data
    df_sorted_inp = df_input.sort_values(by='TIME')
    #Ta ut de 5 högsta och lägsta värdena
    top_vals = df_sorted_inp.nlargest(5, 'Value')
    bot_vals = df_sorted_inp.nsmallest(5, 'Value')
    
    #Plotta figur med årtal och värden
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_axes([0,0,1,1])
    ax.plot(df_sorted_inp['TIME'],df_sorted_inp['Value'])
    
    #Poängtera extrempunkter med prickar i matplotlibs defaultfärger 
    for i, row in top_vals.iterrows():
        ax.scatter(row['TIME'], row['Value'], color=f'C{i}', marker='o', label=f"Högst: År: {row['TIME']}, Inflation: {row['Value']}")
    
    for i, row in bot_vals.iterrows():
        ax.scatter(row['TIME'], row['Value'], color=f'C{i}', marker='o', label=f"Lägst: År: {row['TIME']}, Inflation: {row['Value']}")
    
    #Axelvärden, rutnät, och labels
    ax.set_title(f"Inflation för {country_inp}, {subject_inp}, {freq_inp}, {measure_inp}")
    ax.set_xlabel("År")
    ax.set_ylabel("Inflation")
    ax.legend(loc='upper left')
    ax.grid(axis='both', color='lightgrey', linewidth='1.0')
    plt.xticks(rotation=55)
    plt.show()


plotInflation()
