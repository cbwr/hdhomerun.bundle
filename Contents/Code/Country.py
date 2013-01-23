
class Country:
    def __init__(self, countryObj=None, abbrev=None, name=None):
        if countryObj:
            abbrev = countryObj['abbrev']
            name = countryObj['name']
  
        self.abbrev = abbrev
        self.name = name
  
    ########################################
    def fullName(self):
        Log( "Country.py fullName ..." )
        return "%s (%s)" % (self.name, self.abbrev)
  
    ########################################
    def isDefault(self):
        Log( "Country.py isDefault ..." )
        return self.fullName() == Prefs.Get('country')
