# BachecaDeiScript
Python script that looks for new uploaded elements in BachecaDei UniPD Site

Il codice python fa uso del modulo webdriver di selenium:richiede di installare il webdriver corrispondente al browser usato (nel codice Chrome) e di specificarne il PATH all'interno del codice nella variabile "PATH". Attenzione le versioni di Browser e Webdriver devono sempre coincidere!

Si richiede poi di specificare nelle variabili "nomeCorsoFilePath" il path dove salvare i file che terranno traccia degli elementi già noti allo script specificando il percorso/nomeCorso.

All'interno delle variabili Username e Password inserire le credenziali per il login SSO.

Le ultime righe del codice richiedono di inserire username e password dell'account di posta elettronica dal quale inviare le mail di notifica.
Attenzione: se si usa Gmail è richiesto di disabilitare alcune impostazioni di sicurezza.

Infine si richiede la mail a cui recapitare la notifica di aggiornamento.



