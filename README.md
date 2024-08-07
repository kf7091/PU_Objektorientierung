## Requirements
- pandas
- plottly
- streamlit
- tinydb

### oder
- `pip install -r requirements.txt`

## Verwendung mit share.streamlit
- Über diesen Link ist eine Verwendung ohne Download des Repos möglich:
- [Hier geht's zur App](https://progueb2hopfkoch.streamlit.app/)

## Verwendung

- Klonen sie das Github-Repository auf Ihren PC.
    - Dazu Git Bash öffnen und zum gewünschten Ordner navigieren
    - Führen sie folgende Befehl aus: `git clone <Link des Repositorys>` 
- (optional) aktivieren Sie Ihr Virtual Environment
- führen Sie den Befehl `streamlit run Startseite.py` aus
- die Anwendung sollte sich in Ihrem Browser öffnen
- Sie können nun die gewünschte Person auswählen
- die Anwendung zeigt Ihnen die Daten der gewählten Person an und können ausgewählt werden
- zu den ausgewählten Daten werden nun zwei Tabs mit Daten und einer Grafik angezeigt


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
