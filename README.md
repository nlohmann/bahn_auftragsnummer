# Abfrage von Reisedaten der Deutschen Bahn aus der Auftragsnummer

Dieses Projekt implementiert einen kleinen JSON-Wrapper um die Abfrage der Ticketdaten auf <https://www.bahn.de/p/view/index.shtml>.


## Installation

```
virtualenv venv
source venv/bin/activate
pip install -r requirements
```


## Start

```
gunicorn app:app
```

Dies startet einen lokalen Server auf <http://127.0.0.1:8000>.


## Nutzung

Unter <http://127.0.0.1:8000/> gibt es eine Dokumentation der API.

Für eine sechsstellige-Auftragsnummer `TYFMQE` können mit `http://127.0.0.1:8000/api/itineraries/TYFMQE` die Reisedaten abgerufen werden. Diese sehen in etwa so aus:

```js
{
    "date": "25.12.2016", 
    "name": "C0-0", 
    "referenceNumber": "TYFMQE", 
    "sections": [
        {
            "icon": "ic", 
            "locations": [
                {
                    "arr": "10:44", 
                    "count": "0", 
                    "dep": "10:46", 
                    "disabled": "", 
                    "evaId": "8000044", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000044,\"10:46\",\"no\")'>Bonn Hbf</div>IC  2216 ab 10:46, Gleis 2 ", 
                    "locType": "STATION", 
                    "name": "Bonn Hbf", 
                    "x": "7097136", 
                    "y": "50732008"
                }, 
                {
                    "arr": "11:05", 
                    "count": "1", 
                    "dep": "11:09", 
                    "disabled": "", 
                    "evaId": "8000207", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000207,\"11:09\",\"yes\")'>Köln Hbf</div>IC  2216 an 11:05, Gleis 5<br />IC  2216 ab 11:09 ", 
                    "locType": "STATION", 
                    "name": "Köln Hbf", 
                    "x": "6958730", 
                    "y": "50943029"
                }, 
                {
                    "arr": "11:31", 
                    "count": "2", 
                    "dep": "11:33", 
                    "disabled": "", 
                    "evaId": "8000085", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000085,\"11:33\",\"yes\")'>Düsseldorf Hbf</div>IC  2216 an 11:31, Gleis 17<br />IC  2216 ab 11:33 ", 
                    "locType": "STATION", 
                    "name": "Düsseldorf Hbf", 
                    "x": "6794317", 
                    "y": "51219960"
                }, 
                {
                    "arr": "11:44", 
                    "count": "3", 
                    "dep": "11:46", 
                    "disabled": "", 
                    "evaId": "8000086", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000086,\"11:46\",\"yes\")'>Duisburg Hbf</div>IC  2216 an 11:44, Gleis 13<br />IC  2216 ab 11:46 ", 
                    "locType": "STATION", 
                    "name": "Duisburg Hbf", 
                    "x": "6775907", 
                    "y": "51429786"
                }, 
                {
                    "arr": "11:57", 
                    "count": "4", 
                    "dep": "11:59", 
                    "disabled": "", 
                    "evaId": "8000098", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000098,\"11:59\",\"yes\")'>Essen Hbf</div>IC  2216 an 11:57, Gleis 6<br />IC  2216 ab 11:59 ", 
                    "locType": "STATION", 
                    "name": "Essen Hbf", 
                    "x": "7014795", 
                    "y": "51451351"
                }, 
                {
                    "arr": "12:21", 
                    "count": "5", 
                    "dep": "12:25", 
                    "disabled": "", 
                    "evaId": "8000080", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000080,\"12:25\",\"yes\")'>Dortmund Hbf</div>IC  2216 an 12:21, Gleis 8<br />IC  2216 ab 12:25 ", 
                    "locType": "STATION", 
                    "name": "Dortmund Hbf", 
                    "x": "7459294", 
                    "y": "51517899"
                }, 
                {
                    "arr": "12:54", 
                    "count": "6", 
                    "dep": "12:57", 
                    "disabled": "", 
                    "evaId": "8000263", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000263,\"12:57\",\"yes\")'>Münster(Westf)Hbf</div>IC  2216 an 12:54, Gleis 12<br />IC  2216 ab 12:57 ", 
                    "locType": "STATION", 
                    "name": "Münster(Westf)Hbf", 
                    "x": "7635716", 
                    "y": "51956563"
                }, 
                {
                    "arr": "13:21", 
                    "count": "7", 
                    "dep": "13:23", 
                    "disabled": "", 
                    "evaId": "8000294", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000294,\"13:23\",\"yes\")'>Osnabrück Hbf</div>IC  2216 an 13:21, Gleis 3<br />IC  2216 ab 13:23 ", 
                    "locType": "STATION", 
                    "name": "Osnabrück Hbf", 
                    "x": "8061778", 
                    "y": "52272849"
                }, 
                {
                    "arr": "14:14", 
                    "count": "8", 
                    "dep": "14:17", 
                    "disabled": "", 
                    "evaId": "8000050", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000050,\"14:17\",\"yes\")'>Bremen Hbf</div>IC  2216 an 14:14, Gleis 9<br />IC  2216 ab 14:17 ", 
                    "locType": "STATION", 
                    "name": "Bremen Hbf", 
                    "x": "8813833", 
                    "y": "53083478"
                }, 
                {
                    "arr": "15:00", 
                    "count": "9", 
                    "dep": "15:02", 
                    "disabled": "", 
                    "evaId": "8000147", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8000147,\"15:02\",\"yes\")'>Hamburg-Harburg</div>IC  2216 an 15:00, Gleis 2<br />IC  2216 ab 15:02 ", 
                    "locType": "STATION", 
                    "name": "Hamburg-Harburg", 
                    "x": "9991699", 
                    "y": "53455910"
                }, 
                {
                    "arr": "15:11", 
                    "count": "10", 
                    "dep": "15:17", 
                    "disabled": "", 
                    "evaId": "8002549", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8002549,\"15:17\",\"yes\")'>Hamburg Hbf</div>IC  2216 an 15:11, Gleis 12<br />IC  2216 ab 15:17 ", 
                    "locType": "STATION", 
                    "name": "Hamburg Hbf", 
                    "x": "10006909", 
                    "y": "53552733"
                }, 
                {
                    "arr": "16:12", 
                    "count": "11", 
                    "dep": "16:14", 
                    "disabled": "", 
                    "evaId": "8010324", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8010324,\"16:14\",\"yes\")'>Schwerin Hbf</div>IC  2216 an 16:12, Gleis 2<br />IC  2216 ab 16:14 ", 
                    "locType": "STATION", 
                    "name": "Schwerin Hbf", 
                    "x": "11407455", 
                    "y": "53634741"
                }, 
                {
                    "arr": "16:46", 
                    "count": "12", 
                    "dep": "16:48", 
                    "disabled": "", 
                    "evaId": "8010066", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8010066,\"16:48\",\"yes\")'>Bützow</div>IC  2216 an 16:46, Gleis 2<br />IC  2216 ab 16:48 ", 
                    "locType": "STATION", 
                    "name": "Bützow", 
                    "x": "11998190", 
                    "y": "53837115"
                }, 
                {
                    "arr": "17:06", 
                    "count": "13", 
                    "dep": "17:17", 
                    "disabled": "", 
                    "evaId": "8010304", 
                    "icon": "ic", 
                    "infocontent": "<div class='bold pointer' onclick='setActiveStation(0, 8010304,\"17:17\",\"no\")'>Rostock Hbf</div>IC  2216 an 17:06, Gleis 3 ", 
                    "locType": "STATION", 
                    "name": "Rostock Hbf", 
                    "typ": "active", 
                    "x": "12131078", 
                    "y": "54078242"
                }
            ], 
            "name": "IC  2216", 
            "productcode": "1", 
            "trainId": "704658/426503/474728/2478/80", 
            "type": "JOURNEY"
        }
    ]
}
```

## Nutzungsbedingungen

Bitte beachten Sie die [Nutzungsbedingungen](https://www.bahn.de/p/view/home/agb/nutzungsbedingungen.shtml) der Deutschen Bahn.


## Copyright

The code is licensed under the [MIT License](http://opensource.org/licenses/MIT):

Copyright © 2017 [Niels Lohmann](http://nlohmann.me)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
