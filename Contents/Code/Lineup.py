# Python libs
import re

# plugin
import Util
import Channel

########################################
class Lineup:
    """
    Encapsulates all the information about a single 'lineup', which is a
    list of channels from a particular source. This is to match up with how
    SiliconDust's XML organized the returned channel data.
    """
    def __init__(self):
        # We make the attribute names match the XML tags
        self.DisplayName = None
        self.ProviderName = None
        self.DatabaseId = None
        self.channelList = []

        # This data is manipulated by user
        self.IconImageName = None

    ########################################
    def getId(self):
        Log( "Lineup.py getId ..." )
        return self.ProviderName
    
    ########################################
    def equals(self, other):
        Log( "Lineup.py equals ..." )
        return self.getId() == other.getId()
    
    ########################################
    def getNumChannels( self ):
        Log( "Lineup.py getNumChannels ..." )
        return len(self.channelList)
            
    ########################################
    def getChannelIdx( self, channelId ):
        Log( "Lineup.py getChannelIdx ..." )
        for channelIdx in xrange(len(self.channelList)):
            if self.channelList[channelIdx].getId() == channelId:
                return channelIdx
        return -1
    
    ########################################
    def getChannel( self, channelId ):
        Log( "Lineup.py getChannel ..." )
        channelIdx = self.getChannelIdx( channelId )
        if channelIdx < 0:
            return None
        return self.channelList[channelIdx]

    ########################################
    def update( self, updatedLineup ):
        Log( "Lineup.py update ..." )

        self.DisplayName = updatedLineup.DisplayName
        if updatedLineup.IconImageName:
            self.IconImageName = updatedLineup.IconImageName
            
        for updatedChannel in updatedLineup.channelList:
            channelIdx = self.getChannelIdx( updatedChannel.getId() )
            if channelIdx < 0:
                self.channelList.append( updatedChannel )
            else:
                self.channelList[channelIdx].update( updatedChannel )
                
    ########################################
    def getIconImageName(self):
        Log( "Lineup.py getIconImageName ..." )
        if self.IconImageName:
            return self.IconImageName
        return None
    
    ########################################
    def replaceChannel( self, newChannel ):
        Log( "Lineup.py replaceChannel ..." )

        channelIdx = self.getChannelIdx( newChannel.getId() )

        # Do nothing if the new newChannelLineup does not exist since this
        # routine is only for replacing existing data.
        if channelIdx < 0:
            return

        self.channelList[channelIdx] = newChannel
                
    ########################################
    def getTitle(self):
        Log( "Lineup.py getTitle ..." )
        if self.ProviderName:
            return self.ProviderName
        return L('NoName')
    
    ########################################
    def getSubtitle(self):
        Log( "Lineup.py getSubtitle ..." )
        return "%d %s" % ( len(self.channelList), L('Channels') )
    
    ########################################
    def getSummary(self):
        Log( "Lineup.py getSummary ..." )
        if self.DisplayName:
            return self.DisplayName
        return ''
    
########################################
def fromXml( lineupXml ):
    Log( "Lineup.py fromXml ..." )
    """
    Parses a snippet of the XML returned from the SiliconDust site for a
    given country and postal code. The XML for a single channel looks like
    this:

    <Lineup>
        <DisplayName>Grande Cable: Austin, TX, 78750</DisplayName>
        <ProviderName>Grande Cable</ProviderName>
        <DatabaseID>2262080</DatabaseID>
        <Program>
              ....
          </Program>
     </Lineup>
    """
    
    lineup = Lineup()

    lineup.DisplayName = Util.XPathSelectOne( lineupXml, 'DisplayName' )
    lineup.ProviderName = Util.XPathSelectOne( lineupXml, 'ProviderName' )
    lineup.DatabaseId = Util.XPathSelectOne( lineupXml, 'DatabaseID' )

    # ProvideName is used for equality comparison, so we want to work hard
    # to make sure it has some value.
    if not lineup.ProviderName:
        prefixRe = re.compile( r'^([^\:]+)\:' )
        reMatch = prefixRe.match( lineup.DisplayName )
        if reMatch:
            lineup.ProviderName = reMatch.group(1)
    if not lineup.ProviderName:
        lineup.ProviderName = lineup.DisplayName
    if not lineup.ProviderName:
        lineup.ProviderName = lineup.DatabaseId
          
    for programXml in lineupXml.xpath('Program'):
        lineup.channelList.append( Channel.fromXml( programXml ))

    return lineup
        
########################################
def getMyLineup( channel ):
    Log( "Lineup.py getMyLineup ..." )
    myLineup = Lineup()
    myLineup.DisplayName = "%s" % L('MyLineupDisplayName')
    myLineup.ProviderName = "%s" % L('MyLineupProviderName')
    myLineup.DatabaseId = '-1'
    myLineup.channelList.append( channel )
    return myLineup
