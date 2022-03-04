# Das CLI für SAP Datawarehouse Cloud

In diesem Dokument werden HowTos und sonstige Infos für das `node.js`-CLI der DWC gesammelt.

## Vorbereitungen
1. Checke, ob **node.js** installiert ist
   ~~~ shell
   $ node -v
   ~~~
   dieses liefert, wenn installiert, die aktuell installierte Version von **node.js**.
   Sollte **node.js** noch nicht installiert sein, ist es hier zu finden
   [node.js](https://nodejs.org/en/).
2. Checke, ob und welche Version des node-js Moduls **dwc-cli** installiert ist
   ~~~ shell
   $ dwc -v
   ~~~
   Sollte es nicht installiert sein:
   ~~~ shell
   $ npm install -g @sap/dwc-cli
   ~~~
   Aktualisieren
   ~~~ shell
   $ npm update -g @sap/dwc-cli
   ~~~
3. Hilfe zum CLI erhält man (wie üblich) mit `dwc -h`
4. Passcodes - Aktivieren einer Verbindung
   + Man kann entweder über den Browser gehen, das CLI öffnet dann den default-Browser:
      ~~~ shell
      $ dwc cache-init -H https://<prefix>.<region>.hcs.cloud.sap/
      ~~~
   + alternativ kann man auch sich einmal einloggen und dann den passcode selber abholen über die folgende Seite:
      1. Man besorgt sich die Seite, auf der der **passcode** angezeigt wird
         ~~~ shell
         $ dwc passcode-url -H <Tenant_url>
         ~~~
         dies liefert als Rückgabe die URL, auf der der Passcode angezeigt wird
      2. Dann aktiviert man die Verbindung/gibt den angezeigten **passcode** an
         ~~~ shell
         $ dwc cache-init -H <Tenant_url> -p <angezeigte_passcode>
         ~~~
   + Man kann die lokale Kopie des *service documents* aktualisieren, indem man erneut das `dwc cache-init`
   Kommando ausführt. Dies ist zum Teil nach einer gewissen Zeit nötig.
5. Kommandos ausführen, z.B. lesen von space-Informationen
   ~~~ shell
   $ dwc spaces read -s <SPACE_NAME> -H <TENATN_URL> -p <passcode>
   ~~~
   

## Spaces -- Definieren
Mit dem Kommando
~~~ shell
$ dwc spaces read -s <SPACE_NAME> -H <TENANT_URL> -p <passcode>
~~~
lässt sich die **Definition** eines spaces auslesen. Beachte, dass `<SPACE_NAME>` typischerweise
großgeschrieben werden muss.

Wenn man das Ergebnis des Auslesens in eine Datei geschrieben haben möchte, so muss die über
die *flag -o* angegeben werden:
~~~ shell
$ dwc spaces read -s <SPACE_NAME> -o <ZIEL_DATEINAME> -H <TENANT_URL> -p <passcode>
~~~ 

Man kann die heruntergeladene Datei entweder als Grundlage nehmen und hochladen, oder man 
definiert einen Space von Hand. 

Um eine Space-Definition aus einem *Json-File* hochzuladen genügt folgendes Kommando
~~~ shell
$ dwc spaces create -f <SPACE_DEFINITIONS_JSON_FILE> -H <TENANT_URL> -p <passcode>
~~~

Einen Space löscht man mit dem Kommando (dabei bedeutet die *Flag* `-F` *force*)
~~~ shell
$ dwc spaces delete -s <SPACE_NAME> -F -H <TENANT_URL> -p <passcode>
~~~

### Space-Definition -- Ändern
Um Spaces zu ändern, sollte man die ursprüngliche Definition herunterladen und dann anpassen.
**Beachte, dass die neue Definition die alte überschreibt!**  
Das bedeutet insbesondere,
**um weitere Benutzer zu einem Space hinzuzufügen, muss man die Liste
der schon vorhandenen Benutzer um die neuen Benutzer ergänzen**!

Ansonsten ist der Workflow sehr einfach:
~~~ mermaid
flowchart TD
dwc[(DWC)]-- Download via `dwc spaces read` -->local[definition.json]
local-- Adapt with an editor --> local2[edited_definition.json]
local2-- Deploy via `dwc spaces create` --> dwc 
~~~

#### (Viele) Benutzer hinzufügen
1. Lade die Space-Definition herunter
    ~~~ shell
    $ dwc spaces read -s <SPACE_NAME> -o <ZIEL_DATEINAME> -H <TENANT_URL> -p <passcode>
    ~~~ 
2. Füge in *<ZIEL_DATEINAME>* in der **members**-Liste der **spaceDefinition**-Sektion
   die gewünschten Benutzer-IDs hinzu:
    ~~~ json
    "members": [
      {
        "name": <BENUTZER1_ID>,
        "type": "user"
      },
      {
        "name": <BENUTZER2_ID>,
        "type": "user"
      },
      ...
    ]
   ~~~
3. Lade die neue Space-Definition wieder hoch
    ~~~ shell
    $ dwc spaces create -f <ZIEL_DATEINAME> -H <TENANT_URL> -p <passcode>
    ~~~
   
#### Datenbank Benutzer hinzufügen
**Einschränkung:** Leider muss man das Passwort des angelegten Benutzers später manuell
"selber" abholen, so dass man nicht vollkommen außerhalb der DWC arbeiten kann, und 
beispielsweise auch *openSQL*-Artefakte deployen kann.

1. Lade die Space-Definition herunter
    ~~~ shell
    $ dwc spaces read -s <SPACE_NAME> -o <ZIEL_DATEINAME> -H <TENANT_URL> -p <passcode>
    ~~~ 
2. Füge in *<ZIEL_DATEINAME>* in der **dbusers**-Sektion der **spaceDefinition**-Sektion
   die gewünschten *dbUser* hinzu:
    ~~~ json
   "dbusers": {
       "<SPACENAME>#<DBUSERNAME>": {
           "ingestion": {
               "auditing": {
                   "dppRead": {
                       "isAuditPolicyActive": false,
                       "retentionPeriod": 7
                   },
                   "dppChange": {
                       "isAuditPolicyActive": false,
                       "retentionPeriod": 7
                   }
               }
           },
           "consumption": {
               "localSchemaAccess": true,
               "spaceSchemaAccess": true,
               "hdiGrantorForCupsAccess": true,
               "consumptionWithGrant": true
           }
       }
   },
    ~~~
   Hierbei ist die **consumption**-Sektion die wesentliche:  
   * **localSchemaAccess**: `true` für **openSQL-Schreibzugriff** (SQL, DDL, DML) des OpenSQL Schemas
   * **spaceSchemaAccess**: `true` für **Space-Schema-Lesezugriff**
   * **hdiGrantorForCupsAccess**: `true` für die Erlaubnis, HDI-Container lesen zu können
   * **consumptionWithGrant**: `true` um **Leseerlaubnis erteilen zu dürfen**  
   
    Warnung: Es ist notwendig den dbuser-Teil vollständig zu machen, man kann auf keinen Teil
  verzichten, auch wenn es "default"-Werte gibt, da sonst anscheinend die Space-Definition nicht sauber
  hochgespielt werden kann.
3. Lade die neue Space-Definition wieder hoch
    ~~~
    $ dwc spaces create -f <ZIEL_DATEINAME> -H <TENANT_URL> -p <passcode>
    ~~~


#### Wichtige Sektionen der **Spaces-Definition**
TODO

### Space Content
In der Sektion **"definitions"** eines Spaces-Json-Files lassen sich die Views und
Tables definieren. Es genügt beim Hochladen mit `dwc spaces create ...` nur diese
Sektion hochzuladen, also eine JSON-Datei der Form
~~~ json
{
    <SPACE_NAME>: {
        "definitions": {
            ...
        }
    }
}
~~~
Dann wird die Space-Definition (also Benutzer, Größe,...) **nicht überschrieben**!

Ferner ist zu beachten, dass **im Gegensatz zur "Space-Definition"** das Hochladen 
**additiv** ist, es werden also nur existierende Objekte geändert oder neu generiert,
aber keine entfernt!

Ein ganz einfaches Beispiel:
~~~ json
# testspace_def.json
{
    "TESTSPACE": {
        "definitions": {
            "Table_2": {
                "kind": "entity",
                "@EndUserText.label": "Table 2",
                "@ObjectModel.modelingPattern": {
                    "#": "DATA_STRUCTURE"
                },
                "@ObjectModel.supportedCapabilities": [
                    {
                        "#": "DATA_STRUCTURE"
                    }
                ],
                "elements": {
                    "Column_2": {
                        "@EndUserText.label": "Column 2",
                        "type": "cds.String",
                        "length": 100
                    }
                }
            }
        }
    }
}
~~~
Dann erzeugt der Befehl
~~~ shell
$ dwc spaces create -f testspace_def.json -H <TENANT_URL> -p <passcode>
~~~
im Space *TESTSPACE* die Tabelle *Table_2*, die nur die eine Spalte *Column_2* vom Typ *String(100)*
besitzt. Alles andere, was sich vorher im Space *TESTSPACE* befand ist weiterhin
und ohne Änderungen vorhanden.

### Aktuelle Einschränkungen
* Man kann noch keine Connections definieren oder auslesen
* Man kann Entitäten (Views und Tables) noch nicht per Skript für andere
  spaces lesbar machen
* Es ist noch(?) nicht möglich, das Passwort eines Datenbank-Users bei der Erzeugung
  zu setzen, daher ist mindestens ein manuelles Abrufen des Passwortes nötig

