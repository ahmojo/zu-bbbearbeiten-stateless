# Continuous Integration und Delivery

## Grenzen lokaler Pre-Commit-Hooks

Pre-Commit-Hooks sollen verhindern, dass schlecht formatierter, syntaktisch
fehlerhafter oder ungetesteter Code in die Versionsgeschichte gelangt. Sie
laufen lokal mit den Programmen und Abhängigkeiten des Entwicklungsrechners.
Damit sind sie keine verlässliche Qualitätsschranke: Ein Hook lässt sich mit
`git commit --no-verify` umgehen, kann lokal anders konfiguriert sein oder wegen
fehlender Werkzeuge gar nicht laufen.

Verbindliche Prüfungen gehören deshalb zusätzlich in die Continuous
Integration. GitHub Actions führt dieselben Tests in einer definierten,
serverseitigen Umgebung aus. Ein geschützter Hauptbranch kann das erfolgreiche
Ergebnis verlangen, bevor ein Pull Request zusammengeführt wird.

## Aufbau eines GitHub-Actions-Workflows

Eine Workflow-Datei ist YAML. `name` bezeichnet den Workflow. Unter `on` stehen
die Ereignisse, etwa ein Pull Request auf `main` oder ein gepushter Versions-Tag.
`permissions` begrenzt den Zugriff des automatisch bereitgestellten Tokens.
Unter `jobs` folgen voneinander unabhängige Aufträge. `runs-on` wählt die
virtuelle Maschine. Jeder Job enthält `steps`: `uses` bindet eine bestehende
Action ein, `run` führt einen Befehl aus und `with` übergibt Eingaben an eine
Action.

Die Workflow-Datei `python-package.yml` prüft Pull Requests und Pushes auf
`main`. `release.yml` reagiert ausschliesslich auf Versions-Tags. Sie erstellt
eine GitHub-Release mit Windows-Programm und veröffentlicht dasselbe Projekt als
Container-Image in der GitHub Container Registry. Externe Actions sind auf
unveränderliche Commit-SHAs festgelegt und erhalten nur die jeweils benötigten
Berechtigungen.

Der CSV-Export neutralisiert Textfelder, die mit einem für Tabellenkalkulationen
relevanten Formelzeichen beginnen. Kommas, Anführungszeichen und Zeilenumbrüche
werden weiterhin durch den CSV-Writer korrekt kodiert.

## Container lokal prüfen

```powershell
docker build --tag zu-bbbearbeiten:local .
docker run --rm --publish 8000:8000 zu-bbbearbeiten:local
```

Danach ist die Anwendung unter <http://127.0.0.1:8000> erreichbar.
