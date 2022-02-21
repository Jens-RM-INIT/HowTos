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
   