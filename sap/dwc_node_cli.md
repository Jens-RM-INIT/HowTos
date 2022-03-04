# Das CLI für SAP Datawarehouse Cloud

In diesem Dokument werden HowTos und sonstige Infos für das `node.js`-CLI der DWC gesammelt.

## Vorbereitungen
1. Checke, ob **node.js** installiert ist
   ~~~
   $ node -v
   ~~~
   dieses liefert, wenn installiert, die aktuell installierte Version von **node.js**.
   Sollte **node.js** noch nicht installiert sein, ist es hier zu finden
   [node.js](https://nodejs.org/en/).
2. Checke, ob und welche Version des node-js Moduls **dwc-cli** installiert ist
   ~~~
   $ dwc -v
   ~~~
   Sollte es nicht installiert sein:
   ~~~
   $ npm install -g @sap/dwc-cli
   ~~~
   Aktualisieren
   ~~~
   $ npm update -g @sap/dwc-cli
   ~~~
3. Hilfe zum CLI erhält man (wie üblich) mit `dwc -h`
4. Passcodes - Aktivieren einer Verbindung
   + Man kann entweder über den Browser gehen, das CLI öffnet dann den default-Browser:
      ~~~
      $ dwc cache-init -H https://<prefix>.<region>.hcs.cloud.sap/
      ~~~
   + alternativ kann man auch sich einmal einloggen und dann den passcode selber abholen über die folgende Seite:
      1. Man besorgt sich die Seite, auf der der **passcode** angezeigt wird
         ~~~
         $ dwc passcode-url -H <Tenant_url>
         ~~~
         dies liefert als Rückgabe die URL, auf der der Passcode angezeigt wird
      2. Dann aktiviert man die Verbindung/gibt den angezeigten **passcode** an
         ~~~
         $ dwc cache-init -H <Tenant_url> -p <angezeigte_passcode>
         ~~~
   + Man kann die lokale Kopie des *service documents* aktualisieren, indem man erneut das `dwc cache-init`
   Kommando ausführt. Dies ist zum Teil nach einer gewissen Zeit nötig.
5. Kommandos ausführen, z.B. lesen von space-Informationen
   ~~~
   $ dwc spaces read -s <SPACE_NAME> -H <TENATN_URL> -p <passcode>
   ~~~
   
     Usage: index spaces read [options]

fetch space details for a specified space

Options:
-o, --output <output>            specifies the file to store the output of the command
-s, --space <space>              space ID
-n, --no-space-definition        read space definition (optional)
-d, --definitions [definitions]  read definitions (optional)
-V, --verbose                    print detailed log information to console (optional)
-H, --host <host>                specifies the url host where the tenant is hosted
-p, --passcode <passcode>        passcode for interactive session authentication (optional)
-h, --help                       display help for command


