# DevOps-Glossar

| Begriff | Englischer Begriff | Definition in eigenen Worten |
| --- | --- | --- |
| Verantwortlichkeit | Accountability | Die klare Zuständigkeit für ein Ergebnis und die Pflicht, Entscheidungen und Folgen nachvollziehbar zu vertreten. |
| Agilität | Agility | Die Fähigkeit eines Teams, schnell auf neue Erkenntnisse oder geänderte Bedürfnisse zu reagieren. |
| Kontinuierliche Integration | Continuous Integration (CI) | Kleine Änderungen werden häufig zusammengeführt und automatisch geprüft, damit Integrationsfehler früh auffallen. |
| Kontinuierliche Auslieferung/Bereitstellung | Continuous Delivery/Deployment (CD) | Geprüfte Änderungen werden automatisiert für eine Veröffentlichung vorbereitet oder direkt in eine Zielumgebung ausgeliefert. |
| Auslieferung | Deployment | Eine bestimmte Softwareversion wird in einer Zielumgebung installiert und gestartet. |
| Infrastruktur als Code | Infrastructure as Code (IaC) | Infrastruktur wird in versionierten, wiederholbar ausführbaren Konfigurationsdateien beschrieben. |
| Veröffentlichungszyklus | Release cycle | Der wiederkehrende Ablauf von Planung, Entwicklung, Prüfung und Veröffentlichung einer Version. |
| Markteinführungszeit | Time to Market | Die Zeit von einer Idee oder Anforderung bis zur nutzbaren Veröffentlichung. |
| Versionskontrolle | Version Control | Ein System, das Änderungen an Dateien nachvollziehbar speichert und parallele Entwicklung ermöglicht. |
| DevOps | DevOps | Eine Arbeitsweise, die Entwicklung und Betrieb gemeinsam für den gesamten Lebenszyklus einer Software verantwortlich macht und Zusammenarbeit sowie Automatisierung fördert. |
| Anforderung | Requirement | Eine überprüfbare Aussage darüber, welches Bedürfnis ein System erfüllen soll. |
| Anforderungserhebung | Requirements Engineering | Das Ermitteln, Klären, Dokumentieren und Prüfen von Bedürfnissen und Anforderungen. |
| Anforderungsverwaltung | Requirements Management | Das Priorisieren, Ändern, Zuordnen und Nachverfolgen von Anforderungen über den Produktlebenszyklus. |
| Issue | Issue | Ein nachverfolgbarer GitHub-Eintrag für eine Aufgabe, einen Fehler oder eine Anforderung. |
| Meilenstein | Milestone | Eine Gruppe von Issues, die für ein gemeinsames Ziel oder eine Version vorgesehen sind. |
| Einfachste praktikable Lösung | Minimum Viable Product (MVP) | Die kleinste nutzbare Produktversion, mit der ein Kernproblem gelöst und Feedback gewonnen wird. |
| Produktverwalter | Product Manager | Die Person, die Bedürfnisse, Prioritäten und Produktziele koordiniert. |
| Anforderungsmanagementplan | Requirements Management Plan (RMP) | Vereinbarte Regeln dafür, wie Anforderungen erfasst, bewertet, geändert und abgeschlossen werden. |
| Rückverfolgbarkeit | Traceability | Die nachvollziehbare Verbindung zwischen Bedürfnis, Anforderung, Umsetzung, Test und Veröffentlichung. |
| User Story | User story | Eine Anforderung aus Sicht einer Rolle nach dem Muster: Als Rolle möchte ich Handlung, damit Nutzen. |
| Vorlage | Template | Eine wiederverwendbare Struktur, die vollständige und einheitliche Einträge unterstützt. |
| Zuständige Person | Assignee | Die Person, die für die Bearbeitung eines Issues verantwortlich ist. |
| Abnahmekriterium | Acceptance criterion | Eine konkrete, überprüfbare Bedingung dafür, wann eine Anforderung erfüllt ist. |
| Epos | Epic | Eine grössere Anforderung, die mehrere zusammengehörige User Stories bündelt. |
| Commit | Commit | Ein gespeicherter, beschriebener Stand von Änderungen in einem Git-Repository. |
| Repository | Repository | Der versionierte Projektbestand samt vollständiger Git-Historie. |
| Bereitstellungsbereich | Staging area | Der Zwischenspeicher, in dem Änderungen für den nächsten Commit ausgewählt werden. |
| Ast | Branch | Eine unabhängige Entwicklungslinie innerhalb eines Repositorys. |
| GitHub Flow | GitHub Flow | Ein Arbeitsablauf aus Issue, Branch, Commits, Pull Request, Review, Merge und Branch-Löschung. |
| Hauptast | Main branch | Die massgebende, auslieferbare Entwicklungslinie eines Repositorys. |
| Zusammenführen | Merge | Das Übernehmen der Änderungen einer Entwicklungslinie in eine andere. |
| Änderungsantrag | Pull request (PR) | Eine überprüfbare Anfrage, Branch-Änderungen in einen Zielbranch zu übernehmen. |
| Arbeitsablauf | Workflow | Eine festgelegte Folge von Schritten und Prüfungen für wiederkehrende Arbeit. |
| Marke | Tag | Ein dauerhafter Name für einen bestimmten Commit, häufig für eine Version. |
| Veröffentlichung | Release | Eine benannte, für Nutzer bereitgestellte Version der Software. |
| Abhängigkeit | Dependency | Externe Software, die ein Projekt zum Ausführen oder Entwickeln benötigt. |
| Abhängigkeitsverwalter | Dependency manager | Ein Werkzeug, das Abhängigkeiten und kompatible Versionen installiert und dokumentiert. |
| Untermodul | Submodule | Eine referenzierte Version eines anderen Git-Repositorys innerhalb eines Projekts. |

## Semantische Versionierung

Eine Versionsnummer im Format `MAJOR.MINOR.PATCH` beschreibt die Wirkung einer
Änderung: `MAJOR` steht für inkompatible Schnittstellenänderungen, `MINOR` für
rückwärtskompatible Funktionen und `PATCH` für rückwärtskompatible Fehlerbehebungen.
Versionen `0.y.z` kennzeichnen eine frühe Entwicklungsphase, in der sich die
Schnittstelle noch verändern kann.
