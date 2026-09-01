# Anforderungsmanagement

Das Projekt verwendet GitHub Issues als leichtgewichtiges
Anforderungsmanagement. User Stories werden mit `type: user story` und
`status: new issue` erstellt. Eine Zuweisung entfernt automatisch den Status
`new issue`; die Zuordnung zu einem Meilenstein ergänzt `status: in progress`.
Anforderungen werden über Issue-Referenzen in Commits und Pull Requests mit Code
und Tests verbunden.

## Zuordnung zu Azure DevOps

| GitHub | Azure DevOps Boards |
| --- | --- |
| Acceptance criteria | Feld **Acceptance Criteria** einer User Story |
| Assignee | Feld **Assigned To** |
| Issue | Work Item, beispielsweise User Story oder Bug |
| Label | Tag |
| Milestone | Iteration Path beziehungsweise Sprint |

Azure Boards kann GitHub-Repositorys verbinden. Dadurch lassen sich Commits,
Branches und Pull Requests mit Work Items verknüpfen. Der organisatorische
Prozess bleibt dabei derselbe: Anforderung erfassen, Verantwortlichkeit und
Termin festlegen, Umsetzung und Prüfung verknüpfen und die Anforderung danach
abschliessen.
