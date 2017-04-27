# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from fdfgen import forge_fdf
import os
import tempfile
import aniso8601
import pytz


class Case(object):
    def __init__(self):
        self.datum_reise = None
        self.startbahnhof = None
        self.startbahnhof_abfahrt_soll = None
        self.datum_ankunft = None
        self.zielbahnhof = None
        self.zielbahnhof_ankunft_soll = None
        self.zielbahnhof_ankunft_ist = None
        self.zug_ankunft = None
        self.zug_verspaetet = None
        self.zug_verspaetet_abfahrt_ist = None
        self.bahnhof_anschlusszug_verpasst = None
        self.bahnhof_letzter_umstieg = None
        self.bahnhof_reise_abgebrochen = None
        self.bahnhof_reise_unterbrochen = None

        self.geschlecht = None
        self.titel = None
        self.firma = None
        self.vorname = None
        self.nachname = None
        self.co = None
        self.telefonnumer = None
        self.strasse = None
        self.hausnummer = None
        self.staat = None
        self.postleitzahl = None
        self.wohnort = None

        self.bahncard_100_nummer = None
        self.zeitkarten_nummer = None
        self.geburtsdatum = None

        self.email = None
        self.marktforschung = False

        self.entschaedigung_ueberweisung = True
        self.kontoinhaber = None
        self.iban = None
        self.bic = None

    def fill(self, payload):
        def get_date(date_string):
            if date_string is not None:
                return aniso8601.parse_date(date_string)
            return None

        def get_datetime(datetime_string):
            if datetime_string is not None:
                result = aniso8601.parse_datetime(datetime_string)
                try:
                    result = result.astimezone(pytz.timezone('Europe/Berlin'))
                except ValueError:
                    pass
                return result
            return None

        def get_train(train_string):
            if train_string is not None:
                return train_string.split()
            return None

        self.datum_reise = get_date(payload.get('travelStartDate'))
        self.datum_ankunft = get_date(payload.get('travelEndDate'))
        self.startbahnhof = payload.get('startStation')
        self.startbahnhof_abfahrt_soll = get_datetime(payload.get('startStationPlannedDeparture'))
        self.zielbahnhof = payload.get('endStation')
        self.zielbahnhof_ankunft_soll = get_datetime(payload.get('startStationPlannedArrival'))
        self.zielbahnhof_ankunft_ist = get_datetime(payload.get('startStationActualArrival'))
        self.zug_ankunft = get_train(payload.get('trainArrived'))
        self.zug_verspaetet = get_train(payload.get('trainFirstDelayed'))
        self.zug_verspaetet_abfahrt_ist = get_datetime(payload.get('trainFirstDelayedPlannedDeparture'))
        self.bahnhof_anschlusszug_verpasst = payload.get('stationMissedTrain')
        self.bahnhof_letzter_umstieg = payload.get('stationLastChange')
        self.bahnhof_reise_abgebrochen = payload.get('stationTripAborted')
        self.bahnhof_reise_unterbrochen = payload.get('stationTripSuspended')
        self.geschlecht = payload.get('gender')
        self.titel = payload.get('title')
        self.firma = payload.get('company')
        self.nachname = payload.get('lastName')
        self.vorname = payload.get('firstName')
        self.co = payload.get('co')
        self.telefonnumer = payload.get('phone')
        self.strasse = payload.get('street')
        self.hausnummer = payload.get('houseNumber')
        self.staat = payload.get('state')
        self.postleitzahl = payload.get('postcode')
        self.wohnort = payload.get('city')
        self.bahncard_100_nummer = payload.get('numberBahncard100')
        self.zeitkarten_nummer = payload.get('numberSeasonTicket')
        self.geburtsdatum = get_date(payload.get('dateOfBirth'))
        self.email = payload.get('email')
        if payload.get('marketingResearch'):
            self.marktforschung = payload.get('marketingResearch')
        if payload.get('compensation'):
            self.entschaedigung_ueberweisung = payload.get('compensation') == 'transfer'
        self.kontoinhaber = payload.get('accountHolder')
        self.iban = payload.get('iban')
        self.bic = payload.get('bic')

    def __form_fields(self):
        """
        converts stored information to FDF values
        :return: list of pairs to use as FDF for the Fahrgastrechte PDF
        """
        result = []

        if self.datum_reise is not None:
            result.append(('S1F1', self.datum_reise.strftime('%d')))
            result.append(('S1F2', self.datum_reise.strftime('%m')))
            result.append(('S1F3', self.datum_reise.strftime('%y')))

        if self.startbahnhof is not None:
            result.append(('S1F4', self.startbahnhof))
        if self.startbahnhof_abfahrt_soll is not None:
            result.append(('S1F5', self.startbahnhof_abfahrt_soll.strftime('%H')))
            result.append(('S1F6', self.startbahnhof_abfahrt_soll.strftime('%M')))

        if self.zielbahnhof is not None:
            result.append(('S1F7', self.zielbahnhof))
        if self.zielbahnhof_ankunft_soll is not None:
            result.append(('S1F8', self.zielbahnhof_ankunft_soll.strftime('%H')))
            result.append(('S1F9', self.zielbahnhof_ankunft_soll.strftime('%M')))

        if self.datum_ankunft is not None:
            result.append(('S1F10', self.datum_ankunft.strftime('%d')))
            result.append(('S1F11', self.datum_ankunft.strftime('%m')))
            result.append(('S1F12', self.datum_ankunft.strftime('%y')))

        if self.zug_ankunft is not None:
            result.append(('S1F13', self.zug_ankunft[0]))
            result.append(('S1F14', self.zug_ankunft[1]))

        if self.zielbahnhof_ankunft_ist is not None:
            result.append(('S1F15', self.zielbahnhof_ankunft_ist.strftime('%H')))
            result.append(('S1F16', self.zielbahnhof_ankunft_ist.strftime('%M')))

        if self.zug_verspaetet is not None:
            result.append(('S1F17', self.zug_verspaetet[0]))
            result.append(('S1F18', self.zug_verspaetet[1]))

        if self.zug_verspaetet_abfahrt_ist is not None:
            result.append(('S1F19', self.zug_verspaetet_abfahrt_ist.strftime('%H')))
            result.append(('S1F20', self.zug_verspaetet_abfahrt_ist.strftime('%M')))

        if self.bahnhof_anschlusszug_verpasst is not None:
            result.append(('S1F21', 'Ja'))
            result.append(('S1F22', self.bahnhof_anschlusszug_verpasst))

        if self.bahnhof_letzter_umstieg is not None:
            result.append(('S1F23', 'Ja'))
            result.append(('S1F24', self.bahnhof_letzter_umstieg))

        if self.bahnhof_reise_abgebrochen is not None:
            result.append(('S1F25', 'Ja'))
            result.append(('S1F26', self.bahnhof_reise_abgebrochen))

        if self.bahnhof_reise_unterbrochen is not None:
            result.append(('S1F27', 'Ja'))
            result.append(('S1F28', self.bahnhof_reise_unterbrochen))

        if not self.entschaedigung_ueberweisung:
            result.append(('S1F29', 'Gutschein'))

        if self.geschlecht is not None:
            if self.geschlecht in ['Herr', u'Herr']:
                result.append(('S2F1', 'Herr'))
            elif self.geschlecht in ['Frau', u'Frau']:
                result.append(('S2F1', 'Frau'))
            else:
                raise ValueError

        if self.titel is not None:
            result.append(('S2F2', self.titel))
        if self.firma is not None:
            result.append(('S2F3', self.firma))
        if self.nachname is not None:
            result.append(('S2F4', self.nachname))
        if self.vorname is not None:
            result.append(('S2F5', self.vorname))
        if self.co is not None:
            result.append(('S2F6', self.co))
        if self.telefonnumer is not None:
            result.append(('S2F7', self.telefonnumer))
        if self.strasse is not None:
            result.append(('S2F8', self.strasse))
        if self.hausnummer is not None:
            result.append(('S2F9', self.hausnummer))
        if self.staat is not None and self.staat != 'D':
            result.append(('S2F10', self.staat))
        if self.postleitzahl is not None:
            result.append(('S2F11', self.postleitzahl))
        if self.wohnort is not None:
            result.append(('S2F12', self.wohnort))

        if self.bahncard_100_nummer is not None:
            result.append(('S2F13', 'BahnCard 100-Nr.'))
            result.append(('S2F15', self.bahncard_100_nummer))
        if self.zeitkarten_nummer is not None:
            result.append(('S2F13', 'Zeitkarten-Nr.'))
            result.append(('S2F15', self.zeitkarten_nummer))

        if self.geburtsdatum is not None:
            result.append(('S2F16', self.geburtsdatum.strftime('%d')))
            result.append(('S2F17', self.geburtsdatum.strftime('%m')))
            result.append(('S2F18', self.geburtsdatum.strftime('%Y')))

        if self.email is not None:
            result.append(('S2F19', self.email))

        if self.kontoinhaber is not None:
            result.append(('S2F20', self.kontoinhaber))
        if self.iban is not None:
            result.append(('S2F21', self.iban))
        if self.bic is not None:
            result.append(('S2F22', self.bic))

        if self.marktforschung:
            result.append(('S2F23', 'Ja'))

        return result

    def create_pdf(self):
        fdf = forge_fdf("", self.__form_fields(), [], [], [])
        fdf_file = tempfile.NamedTemporaryFile('wb', delete=False)
        fdf_file.write(fdf)
        fdf_file.close()

        pdf_file = tempfile.NamedTemporaryFile('wb', delete=False)
        pdf_file.close()

        # create absolute paths
        basedir = os.path.dirname(os.path.realpath(__file__))
        form_template = os.path.abspath(os.path.join(basedir, 'static', 'fgr.pdf'))

        pdftk_cmd = "pdftk {form_template} fill_form {fdf_file} output {form_output}".format(
            fdf_file=fdf_file.name, form_template=form_template, form_output=pdf_file.name)
        ret = os.system(pdftk_cmd)
        if ret != 0:
            raise SystemError
        os.remove(fdf_file.name)

        return pdf_file.name
