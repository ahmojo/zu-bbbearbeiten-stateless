# Azure-Bereitstellung

## Ressourcen

Die produktive stateful Umgebung besteht aus folgenden Ressourcen:

- App Service `zu-bbbearbeiten-stateful-ahmojo` im Linux-Basic-Plan B1 in
  Germany West Central
- PostgreSQL Flexible Server `zu-bbbearbeiten-stateful-db-ahmojo` im Burstable-
  Tarif B1ms in Switzerland North
- PostgreSQL-Datenbank `todo`

Die Datenbankregion wurde gewählt, weil die Subscription-Policy ausschließlich
Switzerland North, Norway East, Poland Central, Germany West Central und Belgium
Central erlaubt, während PostgreSQL in Germany West Central für diese Subscription
nicht bereitgestellt werden kann.

## Konfiguration und Geheimnisse

Die Anwendung liest `DBUSER`, `DBPASS`, `DBNAME`, `DBHOST` und `DBSSLMODE` aus
den verschlüsselten App-Service-Einstellungen. `DBHOST` hat das Azure-Format
`host:5432`, und TLS wird mit `DBSSLMODE=require` erzwungen. Werte und
Zugangsdaten werden nicht in Git gespeichert.

Der PostgreSQL-Server besitzt einen öffentlichen Netzwerkendpunkt mit
Default-Deny. Firewallregeln erlauben ausschließlich die aktuellen ausgehenden
IP-Adressen des App Service. Bei einer Änderung des App-Service-Plans muss diese
Liste erneut mit `outboundIpAddresses` abgeglichen werden.

Azure startet die Anwendung mit:

```text
gunicorn --bind=0.0.0.0 --timeout 600 main:app
```

## Automatische Tag-Auslieferung

`.github/workflows/release.yml` reagiert auf Versions-Tags. Der Workflow führt
zuerst die Tests aus. Nur bei erfolgreichen Tests werden GitHub Release,
Windows-EXE, GHCR-Image und die Azure-Web-App ausgeliefert.

Wie im Azure Deployment Center vorgesehen, verwendet der Workflow das auf diese
Web App begrenzte Publish-Profil. Es liegt ausschließlich als verschlüsseltes
GitHub-Secret `AZURE_WEBAPP_PUBLISH_PROFILE_STATEFUL` vor und wird nur an den
Deployment-Schritt übergeben. Der Wert darf weder in Git noch in Logs erscheinen.
