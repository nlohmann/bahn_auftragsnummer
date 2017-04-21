# Abfrage von Reisedaten der Deutschen Bahn aus der Auftragsnummer

Dieses Projekt implementiert einen kleinen JSON-Wrapper um die Abfrage der Ticketdaten auf <https://www.bahn.de/p/view/index.shtml>.


## Installation

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
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
  "referenceNumber": "TYFMQE",
  "travelDate": "2016-12-25",
  "legs": [
    {
      "transport": "ic",
      "name": "IC 2216",
      "type": "JOURNEY",
      "productCode": 1,
      "trainId": "372846/315899/176438/36063/80",
      "locations": [
        {
          "type": "STATION",
          "name": "Bonn Hbf",
          "arrival": "2016-12-25T10:44:00",
          "departure": "2016-12-25T10:46:00",
          "stationId": "8000044",
          "coordinates": {
            "latitude": 50.732008,
            "longitude": 7.097136
          }
        },
        {
          "type": "STATION",
          "name": "Köln Hbf",
          "arrival": "2016-12-25T11:05:00",
          "departure": "2016-12-25T11:09:00",
          "stationId": "8000207",
          "coordinates": {
            "latitude": 50.943029,
            "longitude": 6.95873
          }
        },
        {
          "type": "STATION",
          "name": "Düsseldorf Hbf",
          "arrival": "2016-12-25T11:31:00",
          "departure": "2016-12-25T11:33:00",
          "stationId": "8000085",
          "coordinates": {
            "latitude": 51.21996,
            "longitude": 6.794317
          }
        },
        {
          "type": "STATION",
          "name": "Duisburg Hbf",
          "arrival": "2016-12-25T11:44:00",
          "departure": "2016-12-25T11:46:00",
          "stationId": "8000086",
          "coordinates": {
            "latitude": 51.429786,
            "longitude": 6.775907
          }
        },
        {
          "type": "STATION",
          "name": "Essen Hbf",
          "arrival": "2016-12-25T11:57:00",
          "departure": "2016-12-25T11:59:00",
          "stationId": "8000098",
          "coordinates": {
            "latitude": 51.451351,
            "longitude": 7.014795
          }
        },
        {
          "type": "STATION",
          "name": "Dortmund Hbf",
          "arrival": "2016-12-25T12:21:00",
          "departure": "2016-12-25T12:25:00",
          "stationId": "8000080",
          "coordinates": {
            "latitude": 51.517899,
            "longitude": 7.459294
          }
        },
        {
          "type": "STATION",
          "name": "Münster(Westf)Hbf",
          "arrival": "2016-12-25T12:54:00",
          "departure": "2016-12-25T12:57:00",
          "stationId": "8000263",
          "coordinates": {
            "latitude": 51.956563,
            "longitude": 7.635716
          }
        },
        {
          "type": "STATION",
          "name": "Osnabrück Hbf",
          "arrival": "2016-12-25T13:21:00",
          "departure": "2016-12-25T13:23:00",
          "stationId": "8000294",
          "coordinates": {
            "latitude": 52.272849,
            "longitude": 8.061778
          }
        },
        {
          "type": "STATION",
          "name": "Bremen Hbf",
          "arrival": "2016-12-25T14:14:00",
          "departure": "2016-12-25T14:17:00",
          "stationId": "8000050",
          "coordinates": {
            "latitude": 53.083478,
            "longitude": 8.813833
          }
        },
        {
          "type": "STATION",
          "name": "Hamburg-Harburg",
          "arrival": "2016-12-25T15:00:00",
          "departure": "2016-12-25T15:02:00",
          "stationId": "8000147",
          "coordinates": {
            "latitude": 53.45591,
            "longitude": 9.991699
          }
        },
        {
          "type": "STATION",
          "name": "Hamburg Hbf",
          "arrival": "2016-12-25T15:11:00",
          "departure": "2016-12-25T15:17:00",
          "stationId": "8002549",
          "coordinates": {
            "latitude": 53.552733,
            "longitude": 10.006909
          }
        },
        {
          "type": "STATION",
          "name": "Schwerin Hbf",
          "arrival": "2016-12-25T16:12:00",
          "departure": "2016-12-25T16:14:00",
          "stationId": "8010324",
          "coordinates": {
            "latitude": 53.634741,
            "longitude": 11.407455
          }
        },
        {
          "type": "STATION",
          "name": "Bützow",
          "arrival": "2016-12-25T16:46:00",
          "departure": "2016-12-25T16:48:00",
          "stationId": "8010066",
          "coordinates": {
            "latitude": 53.837115,
            "longitude": 11.99819
          }
        },
        {
          "type": "STATION",
          "name": "Rostock Hbf",
          "arrival": "2016-12-25T17:06:00",
          "departure": "2016-12-25T17:17:00",
          "stationId": "8010304",
          "coordinates": {
            "latitude": 54.078242,
            "longitude": 12.131078
          }
        }
      ],
      "zugfinderUrl": "http://www.zugfinder.de/zuginfo.php?zugnr=IC_2216",
      "mapUrl": "http://maps.googleapis.com/maps/api/staticmap?size=640x640&scale=2&maptype=terrain&path=enc:arstHcdij@{eh@``Zyau@pb_@m~g@`rBweCatm@}~KayuAsttAuma@yw|@{erAmi}Ci{qCuvgAu`eFc|Qa~Aq_OmppG{of@akrB_bn@q}X&sensor=false&language=de"
    }
  ],
  "mapUrl": "http://maps.googleapis.com/maps/api/staticmap?size=640x640&scale=2&maptype=terrain&path=enc:arstHcdij@{eh@``Zyau@pb_@m~g@`rBweCatm@}~KayuAsttAuma@yw|@{erAmi}Ci{qCuvgAu`eFc|Qa~Aq_OmppG{of@akrB_bn@q}X&sensor=false&language=de"
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
