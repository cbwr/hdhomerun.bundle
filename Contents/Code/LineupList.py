# plugin
import Util
import Lineup

class LineupList(list):
    """
    A list of all channel lineups
    """

    ########################################
    def __init__(self, country, postalCode):
        """
        Load the lineup list for a specific country/postalcode from
        SiliconDust website
        """
        self.country = country
        self.postalCode = postalCode
        self.loadLineups(country, postalCode)
  
    ########################################
    def loadLineups(self, country, postalCode):
        Log( "LineupList.py loadLineups ..." )
        """
        Fetch lineup/channel data from silicondust.com and generate a list
        of Lineup objects. XML structure is:

        <LineupUIResponse>
            <Location>US:78750</Location>
           <Lineup>
              <DisplayName>Digital Antenna: Austin, TX, 78750</DisplayName>
              <DatabaseID>2252478</DatabaseID>
              <Program>
                   ... channel info
              </Program>
            </Lineup>
        </LineupUIResponse>
        """

        lineupUrl = 'http://www.silicondust.com/hdhomerun/lineup_web/%s:%s' % ( country.abbrev, postalCode )
        Log( "LOAD LINEUPS URL: %s" % lineupUrl )

        responseXml = XML.ElementFromURL( lineupUrl )
        
        location = Util.XPathSelectOne( responseXml,
                                        '/LineupUIResponse/Location')
        Log( "LOCATION %s" % location )

        for lineupItemXml in responseXml.xpath('/LineupUIResponse/Lineup'):
            lineup = Lineup.fromXml( lineupItemXml )
            self.append( lineup )

    ########################################
    def getNumChannels( self ):
        Log( "LineupList.py getNumChannels ..." )
        count = 0
        for lineup in self:
            count += lineup.getNumChannels()
        return count
    
    ########################################
    def getLineupIdx( self, lineupId ):
        Log( "LineupList.py getLineupIdx ..." )
        for lineupIdx in xrange(len(self)):
            if self[lineupIdx].getId() == lineupId:
                return lineupIdx
        return -1
    
    ########################################
    def getLineup( self, lineupId ):
        Log( "LineupList.py getLineup ..." )
        lineupIdx = self.getLineupIdx( lineupId )
        if lineupIdx < 0:
            return None
        return self[lineupIdx]
    
    ########################################
    def update(self, updatedLineupList):
        Log( "LineupList.py update ..." )

        for updatedLineup in updatedLineupList:
            lineupIdx = self.getLineupIdx( updatedLineup.getId() )
            if lineupIdx < 0:
                self.append( updatedLineup )
            else:
                self[lineupIdx].update( updatedLineup )

    ########################################
    def replaceChannel(self, lineupId, newChannel):
        Log( "LineupList.py ReplaceChannel ..." )

        lineupIdx = self.getLineupIdx( lineupId )

        # Do nothing if the new newChannelLineup does not exist since this
        # routine is only for replacing existing data.
        if lineupIdx < 0:
            return
        
        self[lineupIdx].replaceChannel( newChannel )
