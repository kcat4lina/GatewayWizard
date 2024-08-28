### Features:

1. Monitoraggio Continuo: 
Lo strumento monitora continuamente una directory sorgente specificata per eventuali file o sottodirectory.

2. Copia Automatica: 
Copia automaticamente qualsiasi file o sottodirectory rilevata dal percorso sorgente a un percorso di destinazione specificato dall'utente.

3. Eliminazione Automatica: 
Dopo la copia, lo strumento elimina automaticamente i file o le sottodirectory originali dal percorso sorgente.

4. Registrazione in Tempo Reale: 
Lo strumento fornisce feedback in tempo reale, visualizzando i nomi degli elementi copiati ed eliminati e il numero totale di elementi elaborati.

5. Gestione dei Permessi: 
Tenta di gestire gli errori di permesso modificando i permessi dei file o delle directory quando necessario per garantire l'eliminazione riuscita.


### Istruzioni per l'Uso:

Avvio dell'Applicazione:

Fai doppio clic su Gateway_Wizard.exe per avviare l'applicazione.



Inserisci il Percorso di Origine:

Nel campo etichettato "Enter the source path to monitor:", inserisci il percorso completo alla directory in cui si trovano i dati che desideri monitorare, copiare ed eliminare (ad es., C:\Users\NomeUtente\Documents\CartellaSorgente).



Inserisci il Percorso di Destinazione:

Nel campo etichettato "Enter the destination path to copy data to:", inserisci il percorso completo alla directory dove desideri che i dati siano copiati prima dell'eliminazione (ad es., D:\Backup\CartellaDestinazione).



Avvia il Monitoraggio:

Clicca sul pulsante "Start Monitoring". 
Lo strumento inizierà a monitorare il percorso sorgente. 
Qualsiasi file o directory trovata sarà copiata nel percorso di destinazione (destination) e poi eliminata dal percorso sorgente(source).



Monitorare i Progressi:

L'etichetta di stato "Items copied and deleted:" verrà aggiornata con il numero totale di elementi elaborati.
La casella di testo sottostante visualizzerà i registri in tempo reale mostrando i nomi dei file e delle directory che sono stati copiati ed eliminati.



Arresto dell'Applicazione:

Per interrompere il monitoraggio e chiudere l'applicazione, basta fare clic sul pulsante di chiusura della finestra (la X nell'angolo in alto a destra). Lo strumento smetterà di monitorare il percorso e si chiuderà in sicurezza.



@V2 Versione 2.0

Sono resenti le stesse funzioni, con aggiunta di:
+ l'utente puo' scegliere tra copiare solo, cancellare solo, oppure entrambe le funzionalita'.
+ l'utente ha la possibilita' di stoppare l'applicazione cliccando su "Stop Monitoring".
+ l'utente puo' ora scegliere di avere o meno il backup di tutti i file per sessione (Start - Stop) e puo' accedere direttamente alla cartella contenete il backup in formato .zip cliccando su "Open Backup Folder"


Note:

Assicurati dei Permessi:
Se stai lavorando con directory che richiedono permessi elevati (ad es., directory di sistema), potrebbe essere necessario eseguire l'applicazione come amministratore.

Operazione Continua: 
Lo strumento opera in tempo reale e monitora continuamente la directory sorgente specificata. Assicurati che il percorso di destinazione abbia spazio di archiviazione sufficiente per ospitare i dati copiati.

Gestione degli Errori: 
Se lo strumento incontra un errore di permesso, tenterà di cambiare i permessi dei file o delle directory per consentire l'eliminazione. Se questo fallisce, lo strumento registrerà l'errore nella console o nella casella di testo di output.


Questa applicazione è progettata per semplificare e automatizzare le attività di gestione dei dati, rendendola ideale per gli utenti che necessitano di eseguire backup e pulizie delle directory senza intervento manuale.


Grazie,

Joana Catalina Gacea :)