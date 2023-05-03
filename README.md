# Schiffe_ERMORDEN

Verwendung:
	1. ZIP-Datei im Zielordner entpacken
	2. Terminal im Ordner öffnen und mittels „python3 main.py“ starten
  
  Sollte bereits ein Spiel gestartet worden sein und vor Ende wieder geschlossen wurden sein, so wird dies beim erneuten Öffnen des Spiels  automatisch wieder aufgenommen. Ist dies nicht gewünscht, so ist es nötig die „mapPlayer1.pickle“ und „mapPlayer2.pickle“ im Hauptverzeichnis zu löschen. 
  Sollte zu Ende eines Spiels die Fehlermeldung "Beim löschen der Datei ist ein Fehler aufgetreten {path}!" auftreten, wobei {path} der aktuelle Pfad in dem das Spiel liegt ist auftreten, so ist dem Nutzer zu raten, dass er die save-Dateien „mapPlayer1.pickle“ und „mapPlayer2.pickle“ im Hauptverzeichnis händisch löscht. Grund ist, dass hier das Vorgesehene Löschen zu Ende des Spiels fehlgeschlagen ist.

Verwendete Module:
  - re
  - pickle
  - unittest
  - random
  - os
  - sys
  
Kurzbeschreibung:
  Über die main.py wird das Spiel gesteuert. Sie ruft die start_game-Funktion der game.py auf, welche dann das Startmenu aufruft und später auch den Spielverlauf steuert. Es werden zwei Spieler angelegt, der erste ist immer ein Objekt der Playerklasse aus player.py, der zweite kann entweder ein echter Spieler als Objekt der Playerklasse oder ein Computergegner, als Objekt der BotPlayerklasse aus der bot_player.py sein. Jeder dieser Spieler hat eine Spielkarte, ein Objekt der Mapklasse aus map.py, welche wiederum aus je 100 Objekten der Fieldklasse aus field.py aufgebaut sind.
  
Ausführung der Unittests:
  - python -m unittest

Coverage:
  - python -m coverage run -m unittest
  - Aktuelles coverage von 88%
