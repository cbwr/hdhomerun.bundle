# plugin
from Country import Country
from Config import C

countries = []
for country in C["COUNTRIES"]:
    countries.append(Country(country))

########################################
def defaultCountry():
    Log( "CountryList.py defaultCountry ..." )
    return findByFullName(Prefs['country'])

########################################
def findByFullName(fullName):
    Log( "CountryList.py findByFullName ..." )
    for country in countries:
        if country.fullName() == fullName:
            return country

########################################
def findByAbbrev(abbrev):
    Log( "CountryList.py findByAbbrev ..." )
    for country in countries:
        if str(country.abbrev) == str(abbrev):
            return country

########################################
def toOptions():
    Log( "CountryList.py toOptions ..." )
    options = countries[:]
    options.reverse()
  
    values = '(None)|'
    for country in options:
        values += country.fullName() + '|'
    del options
  
    return values

