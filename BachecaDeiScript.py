import selenium
from selenium import webdriver
import pickle #per salvare oggetti Python come stringhe di byte
import time
import smtplib
from selenium.webdriver.common.keys import Keys

#FilePath per ogni corso
BdDFilePath = "/Users/andrew/Desktop/Progetti/BachecaDeiScript/FilePerCorso/BasiDiDatiLista" #Basi di Dati
MSODFilePath = "/Users/andrew/Desktop/Progetti/BachecaDeiScript/FilePerCorso/MSODLista" #Modelli Software e Ottimizzazione Discreta
FdTFilePath = "/Users/andrew/Desktop/Progetti/BachecaDeiScript/FilePerCorso/FdTLista" #Fondamenti di Telecomunicazioni
FdEFilePath = "/Users/andrew/Desktop/Progetti/BachecaDeiScript/FilePerCorso/FdELista" #Fondamenti di Elettronica

#Credenziali SSO
Username = ""
Password = ""


def storeList(lista, filename):
    """Salva la lista fornita per argomento nel filename specificato"""
    outfile = open(filename, "wb") # se non esiste lo crea, filename è il path seguito dal nome del file
    pickle.dump(lista, outfile) # salva la lista usando modulo pickle
    outfile.close()

def loadList(filename):
    """Ritorna la lista ricostruita dalla lettura del filename fornito per argomento. Se il file non esiste ne viene creato uno nuovo. """
    try:
        infile = open(filename, "rb")
        lista = pickle.load(infile)
        infile.close()
        return lista

    except FileNotFoundError:
        print("Il file non esisteva, ne è stato creato uno nuovo.")
        newFile = open(filename, "wb")
        pickle.dump([], newFile)
        newFile.close()

def checkForUpdate(filename, newList):
    """Verifica se vi sono nuovi elementi nella lista passata per parametro, confrontandola con la lista recuperata dal filename specificato.
        Ritorna una lista contenente i nuovi elementi trovati, non modifica la lista passata per parametro."""

    newListCopy = newList.copy() #copia personale da modificare

    try:
        oldList = loadList(filename)
        i = 0
        while (i < len(oldList)):
            newListCopy.remove(oldList[i])
            i += 1
        return newListCopy

    except TypeError:
        print ("File danneggiato o nuovo!")
        return newList #file vuoto/nuovo o corrotto, sono tutti elementi nuovi



# PATH indica il percorso dove reperire il driver per il browser che voglio usare, NB le versioni del Browser e Driver devono sempre coincidere
PATH = "/Users/andrew/Desktop/Progetti/BachecaDeiScript/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("headless") # apertura del browser in modalità "headless" (in background)

# istanzio il driver, fornendo dove reperire il driver da usare
driver = webdriver.Chrome(PATH, options=options)

#apro il browser al link che passo per argomento
driver.get("https://elearning.dei.unipd.it/")

time.sleep(1)

login = driver.find_element_by_css_selector("#main_header > div > div.usermenu > span > a")
login.click()

time.sleep(1)

sso = driver.find_element_by_css_selector("#shibbox > div > center > a > img")
sso.click()

time.sleep(1)

dominio = driver.find_element_by_id("radio2") # @studenti.unipd.it
dominio.click()

time.sleep(1)

username = driver.find_element_by_id("j_username_js")
username.clear()
username.send_keys(Username)

password = driver.find_element_by_id("password")
password.clear()
password.send_keys(Password)

accedi = driver.find_element_by_id("login_button_js")
time.sleep(1)
accedi.click()

time.sleep(1)

#CSS Selectors per ogni corso all'interno della pagina home di elearning
BdDSelector = "#frontpage-course-list > div > div:nth-child(4) > div.panel-heading.info > span.coursename > a"
FdTSelector = "#frontpage-course-list > div > div:nth-child(2) > div.panel-heading.info > span.coursename > a"
MSODSelector = "#frontpage-course-list > div > div.panel.view.view-fifth.panel-default.coursebox.clearfix.odd.first > div.panel-heading.info > span.coursename > a"
FdESelector = "#frontpage-course-list > div > div:nth-child(3) > div.panel-heading.info > span.coursename > a"

listaSelectors = [BdDSelector, FdTSelector, MSODSelector, FdESelector] #lista dei Selettori
listaFilePath = [BdDFilePath, FdTFilePath, MSODFilePath, FdEFilePath] #lista dei filepath
listaNomiCorsi = ["Basi Di Dati", "Fondamenti di Telecomunicazioni", "Modelli Software e Ottimizzazione Discreta", "Fondamenti di Elettronica"] #lista nomi corsi
listaNuoveLezioniPerCorso = [] #lista di liste, viene riempita con la lista dei nuovi elementi individuati dallo script sottostante


for i in range(len(listaSelectors)):
    corso = driver.find_element_by_css_selector(listaSelectors[i]) #seleziono il corso mediante CSS Selector indicizzando la lista listaSelectors
    corso.click()

    main = driver.find_element_by_css_selector("#region-main > div > div > ul") #individuo il "pannello main" per ogni corso

    list = []

    lezioni = main.find_elements_by_class_name("instancename") #creo una lista contenente tutti gli elementi individuati mediante class name "instancename"
    for lezione in lezioni:
        #print(lezione.text)
        list.append(lezione.text)

    #list.append("nuova Lezione") #per fare una prova di aggiornamento

    listaNuoveLezioniPerCorso.append(checkForUpdate(listaFilePath[i], list)) #verifico se vi sono nuovi elementi e li salvo in una lista all'interno di listaNuoveLezioniPerCorso
    storeList(list, listaFilePath[i])  # salvo la lista contenente tutti gli elementi aggiornata al momento di esecuzione
    #newElementsList = checkForUpdate(listaFilePath[i], list) #verifico la presenza di nuovi elementi


    print(listaNomiCorsi[i] + " ha la seguente lista di elementi salvati nel file: \n")
    print(loadList(listaFilePath[i])) #Lista in memoria

    print("\n\n")

    print("Lista dei nuovi elementi individuati all'esecuzione del programma al giorno " + time.strftime("%d/%m/%Y") + ", ore " + time.strftime("%H:%M:%S") + "\n")
    print(listaNuoveLezioniPerCorso[i]) # Lista di nuovi elementi all'esecuzione del programma
    print("\n\n")

    driver.back() #per tornare alla pagina precedente prima di selezionare un nuovo corso



def createMessage(listaDiNuoviElementi, listaNomiCorsi):
    """Crea il messaggio da inviare, unendo il nome del corso alla lista di nuovi elementi individuati ad esso associato"""

    toRet = "L'esecuzione dello script il giorno " + time.strftime("%d/%m/%Y") + ", ore " + time.strftime("%H:%M:%S") + " ha individuato i seguenti nuovi elementi caricati per corso: \n"
    for i in range(len(listaNomiCorsi)):
        toRet += listaNomiCorsi[i] + ":  " + ", ".join(listaDiNuoviElementi[i]).encode("ascii", "ignore").decode("ascii") + "\n"
    return toRet

def sendMailIfUpdates(listaDiNuoviElementi):
    """Invia la mail solo se sono stati individuati nuovi elementi"""
    bool = False
    for i in range(len(listaDiNuoviElementi)):
         if len(listaDiNuoviElementi[i]) != 0:
            bool = True
    return bool

oggetto = "Nuove lezioni sono state caricate! \n\n" #richiesti sempre 2 caratteri \n terminali
contenuto = createMessage(listaNuoveLezioniPerCorso, listaNomiCorsi)
messaggio = (oggetto + contenuto)

print(messaggio)

email = smtplib.SMTP("smtp.gmail.com", 587)
email.ehlo()

time.sleep(1)

email.starttls()

time.sleep(1)

email.login("lamaildacuiinviare@gmail.com", "passwordMail")

time.sleep(2)

if sendMailIfUpdates(listaNuoveLezioniPerCorso):
    email.sendmail("lamaildacuiinviare@gmail.com", "achiinviarla@gmail.com", messaggio)

driver.quit() #termina il programma


