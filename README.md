## Requirements
- pandas
- plottly
- streamlit

### oder
- `pip install -r requirements.txt`

## Verwendung

- Klonen sie das Github-Repository auf Ihren PC.
    - Dazu Git Bash öffnen und zum gewünschten Ordner navigieren
    - Führen sie folgende Befehl aus: `git clone <Link des Repositorys>` 
- (optional) aktivieren Sie Ihr Virtual Environment
- führen Sie den Befehl `streamlit run main.py` aus
- das Programm wird im Browser geöffnet
![alt text](screenshot.png)
- das Programm zeigt nun die EKG-Daten und Power-Daten an
- Durch eingabe der Maximalen Herzfrequenz werden die Zonen visuell angepasst


## Befehle um Virtual Environment zu erstellen
### Windows:
- `python -m venv <Name des venv Ordners>`
### Linux: 
- `python3 -m venv <Name des venv Ordners>`
    - funktioniert nur auf Systemfestplatte
    
## Befehle um Virtual Environment zu aktivieren
### Windows:
- `.\[Name des venv Ordners]\Scripts\activate`
    - wenn es sich nicht aktivieren lässt
        - Powershell als Admin ausführen
        - ausführen um zu sehen was erlaubt ist `Get-ExecutionPolicy -Lis`    
        - Erlaubt alles zu installieren `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`
### Linux:
- `source <Name des venv Ordners>/bin/activate`
