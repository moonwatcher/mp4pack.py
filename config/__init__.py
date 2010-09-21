#!/usr/bin/env python
# -*- coding: utf-8 -*-


repository_config = {}

repository_config['Codec'] = {}
repository_config['Codec']['Audio'] = {}
repository_config['Codec']['Audio']['AC3'] = 'ac-3|AC3'
repository_config['Codec']['Audio']['AAC'] = 'AAC'
repository_config['Codec']['Audio']['DTS'] = 'DTS'
repository_config['Codec']['Audio']['MP3'] = 'MPEG/L3'


repository_config['Language'] = {'heb':'Hebrew', 'eng':'English'}
repository_config['Volume'] = {'alpha':'/Users/lg/Downloads/pool/alpha', 'beta':'/Users/lg/Downloads/pool/beta', 'gama':'/Users/lg/Downloads/pool/gama', 'delta':'/Users/lg/Downloads/pool/delta', 'epsilon':'/Users/lg/Downloads/pool/epsilon', 'eta':'/Users/lg/Downloads/pool/eta'}
repository_config['Media Kind'] = {}
repository_config['Media Kind']['tvshow'] = {'schema':'^(.*) (s([0-9]+)e([0-9]+))(?: (.*))?\.([^\.]+)$', 'name':'TV Show', 'stik':10}
repository_config['Media Kind']['movie'] = {'schema':'^IMDb(tt[0-9]+) ?(.*)\.([^\.]+)$', 'name':'Movie', 'stik':9}
#repository_config['Media Kind']['music'] = {'schema':'^([0-9]+)(?:-([0-9]+))?(?: (.*))?\.([^\.]+)$', 'name':'Music', 'stik':1}
#repository_config['Media Kind']['audiobook'] = {'schema':'^([0-9]+)(?:-([0-9]+))?(?: (.*))?\.([^\.]+)$', 'name':'Audiobook', 'stik':2}


repository_config['Kind'] = {}

repository_config['Kind']['m4v'] = {}
repository_config['Kind']['m4v']['container'] = 'mp4'
repository_config['Kind']['m4v']['default'] = {'volume':'epsilon'}
repository_config['Kind']['m4v']['Profile'] = {}
repository_config['Kind']['m4v']['Profile']['universal'] = {
    'description': 'an SD profile that decodes on every cabac capable apple device',
    'handbrake':{
        'crf':18
        'cabac':True
        'max_width':720
        'x264':'ref=2:me=umh:b-adapt=2:weightp=0:trellis=0:subme=9:cabac=%(cabac)s'
        'extra':'--large-file'
    },
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'video'},
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
    )
}
repository_config['Kind']['m4v']['Profile']['appletv'] = {
    'description': 'AppleTV Intel based',
    'handbrake':{
        'crf':22
        'cabac':True
        'max_width':1280
        'x264':'ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=9500:vbv-bufsize=9500:cabac=%(cabac)s'
        'extra':'--large-file'
    },
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'video'},
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
    )
}
repository_config['Kind']['m4v']['Profile']['ipod'] = {
    'description': 'All iPod touch models profile',
    'handbrake':{
        'crf':21
        'cabac':True
        'max_width':480
        'x264':'ref=2:me=umh:bframes=0:8x8dct=0:trellis=0:subme=6:weightp=0:cabac=%(cabac)s'
        'extra':None
    },
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'video'},
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
    )
}
repository_config['Kind']['m4v']['Profile']['high'] = {
    'description': 'High profile',
    'handbrake':{
        'crf':18
        'cabac':True
        'max_width':1280
        'x264':'ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=10000:vbv-bufsize=10000:cabac=%(cabac)s'
        'extra':'--large-file'
    },
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'video'},
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
    )
}


repository_config['Kind']['m4a'] = {}
repository_config['Kind']['m4a']['container'] = 'mp4'
repository_config['Kind']['m4a']['default'] = {'volume':'alpha'}
repository_config['Kind']['m4a']['Profile'] = {}
repository_config['Kind']['m4a']['Profile']['lossless'] = {}
repository_config['Kind']['m4a']['Profile']['portable'] = {}


repository_config['Kind']['mkv'] = {}
repository_config['Kind']['mkv']['container'] = 'matroska'
repository_config['Kind']['mkv']['default'] = {'volume':'epsilon'}
repository_config['Kind']['mkv']['Profile'] = {}
repository_config['Kind']['mkv']['Profile']['sd'] = {
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'video'},
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
        {'type':'audio', 'codec_kind':'DTS'}
    )
}
repository_config['Kind']['mkv']['Profile']['720'] = {
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'video'},
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
        {'type':'audio', 'codec_kind':'DTS'}
    )
}
repository_config['Kind']['mkv']['Profile']['1080'] = {
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'video'},
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
        {'type':'audio', 'codec_kind':'DTS'}
    )
}

repository_config['Kind']['srt'] = {}
repository_config['Kind']['srt']['container'] = 'subtitles'
repository_config['Kind']['srt']['codec'] = 'S_TEXT/UTF8'
repository_config['Kind']['srt']['default'] = {'profile':'original', 'volume':'alpha'}
repository_config['Kind']['srt']['Profile'] = {}
repository_config['Kind']['srt']['Profile']['original'] = {}
repository_config['Kind']['srt']['Profile']['clean'] = {}

repository_config['Kind']['ass'] = {}
repository_config['Kind']['ass']['container'] = 'subtitles'
repository_config['Kind']['ass']['codec'] = 'S_TEXT/ASS'
repository_config['Kind']['ass']['default'] = {'profile':'original', 'volume':'alpha'}
repository_config['Kind']['ass']['Profile'] = {}
repository_config['Kind']['ass']['Profile']['original'] = {}

repository_config['Kind']['sub'] = {}
repository_config['Kind']['sub']['container'] = 'subtitles'
repository_config['Kind']['sub']['codec'] = 'S_TEXT/SUB'
repository_config['Kind']['sub']['default'] = {'profile':'original', 'volume':'alpha'}
repository_config['Kind']['sub']['Profile'] = {}
repository_config['Kind']['sub']['Profile']['original'] = {}



tag_config = {}
tag_config['db'] = {}
tag_config['db']['name'] = "mp4pack"

tag_config['cache'] = "/Users/lg/Downloads/pool/cache/"
tag_config['tmdb'] = {}
tag_config['tmdb']['apikey'] = "a8b9f96dde091408a03cb4c78477bd14"
tag_config['tmdb']['urls'] = {}
tag_config['tmdb']['urls']['Movie.getInfo'] = "http://api.themoviedb.org/2.1/Movie.getInfo/en/json/%(apikey)s/%%s" % (tag_config['tmdb'])
tag_config['tmdb']['urls']['Movie.imdbLookup'] = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/%(apikey)s/%%s" % (tag_config['tmdb'])
tag_config['tmdb']['urls']['Person.getInfo'] = "http://api.themoviedb.org/2.1/Person.getInfo/en/json/%(apikey)s/%%s" % (tag_config['tmdb'])
tag_config['tmdb']['urls']['Person.search'] = "http://api.themoviedb.org/2.1/Person.search/en/json/%(apikey)s/%%s" % (tag_config['tmdb'])

tag_config['tvdb'] = {}
tag_config['tvdb']['apikey'] = "7B3B400B0146EA83"
tag_config['tvdb']['urls'] = {}
tag_config['tvdb']['urls']['Show.getInfo'] = "http://www.thetvdb.com/api/%(apikey)s/series/%%s/all/en.xml" % (tag_config['tvdb'])
tag_config['tvdb']['urls']['Banner.getImage'] = "http://www.thetvdb.com/banners/%s"




# Tag name map
# Schema: canonic name, subler name, mp4info name
tag_name = [
    ('Track #', 'Track #', 'Track'),
    ('Disk #', 'Disk #', 'Disk'),
    ('Album', 'Album', 'Album'),
    ('Album Artist', 'Album Artist', 'Album Artist'),
    ('Artist', 'Artist', 'Artist'),
    ('ArtistID', None, 'Artist ID'),
    ('Tempo', 'Tempo', 'BPM'),
    ('Cast', 'Cast', None),
    ('Codirector', 'Codirector', None),
    ('Category', None, 'Category'),
    ('Comments', 'Comments', 'Comments'),
    ('Composer', 'Composer', 'Composer'),
    ('ComposerID', None, 'Composer ID'),
    ('contentID', 'contentID', 'Content ID'),
    ('Content Rating', 'Content Rating', 'Content Rating'),
    ('Copyright', 'Copyright', 'Copyright'),
    ('Artwork Pieces', None, 'Cover Art pieces'),
    ('Director', 'Director', None),
    ('Encoded By', 'Encoded By', 'Encoded by'),
    ('Encoding Tool', 'Encoding Tool', 'Encoded with'),
    ('Genre', 'Genre', 'Genre'),
    ('GenreID', None, 'Genre ID'),
    ('GenreType', None, 'GenreType'),
    ('Grouping', 'Grouping', 'Grouping'),
    ('HD Video', 'HD Video', 'HD Video'),
    ('Keywords', None, 'Keywords'),
    ('Long Description', 'Long Description', 'Long Description'),
    ('Lyrics', 'Lyrics', 'Lyrics'),
    ('Media Kind', 'Media Kind', 'Media Type'),
    ('Name', 'Name', 'Name'),
    ('Compilation', None, 'Part of Compilation'),
    ('Gapless', 'Gapless', 'Part of Gapless Album'),
    ('PlaylistID', None, 'Playlist ID'),
    ('Podcast', None, 'Podcast'),
    ('Producers', 'Producers', None),
    ('Purchase Date', 'Purchase Date', 'Purchase Date'),
    ('Rating', 'Rating', None),
    ('Rating Annotation', 'Rating Annotation', None),
    ('Release Date', 'Release Date', 'Release Date'),
    ('Screenwriters', 'Screenwriters', None),
    ('Description', 'Description', 'Short Description'),
    ('Sort Album', None, 'Sort Album'),
    ('Sort Album Artist', None, 'Sort Album Artist'),
    ('Sort Artist', None, 'Sort Artist'),
    ('Sort Composer', None, 'Sort Composer'),
    ('Sort Name', None, 'Sort Name'),
    ('Sort TV Show', None, 'Sort TV Show'),
    ('Studio', 'Studio', None),
    ('TV Episode #', 'TV Episode #', 'TV Episode'),
    ('TV Episode ID', 'TV Episode ID', 'TV Episode Number'),
    ('TV Network', 'TV Network', 'TV Network'),
    ('TV Season', 'TV Season', 'TV Season'),
    ('TV Show', 'TV Show', 'TV Show'),
    ('iTunes Account', 'iTunes Account', 'iTunes Account'),
    ('iTunes Account Type', None, 'iTunes Account Type'),
    ('iTunes Store Country', None, 'iTunes Store Country'),
    ('XID', 'XID', 'xid')
]


# Genre map
# allows mapping different names for genres to another
genre_map = [
    ('science-fiction', 'sci-fi')
]

# ITMF Genre
# The standard itmf names and codes for genres
itmf_genre = [
    {'_id':'blues', 'itmf':2, 'name':'Blues'},
    {'_id':'classic rock', 'itmf':3, 'name':'Classic Rock'},
    {'_id':'country', 'itmf':4, 'name':'Country'},
    {'_id':'dance', 'itmf':5, 'name':'Dance'},
    {'_id':'disco', 'itmf':6, 'name':'Disco'},
    {'_id':'funk', 'itmf':7, 'name':'Funk'},
    {'_id':'grunge', 'itmf':8, 'name':'Grunge'},
    {'_id':'hip hop', 'itmf':9, 'name':'Hip Hop'},
    {'_id':'jazz', 'itmf':10, 'name':'Jazz'},
    {'_id':'metal', 'itmf':11, 'name':'Metal'},
    {'_id':'new age', 'itmf':12, 'name':'New Age'},
    {'_id':'oldies', 'itmf':13, 'name':'Oldies'},
    {'_id':'other', 'itmf':14, 'name':'Other'},
    {'_id':'pop', 'itmf':15, 'name':'Pop'},
    {'_id':'r&b', 'itmf':16, 'name':'R&B'},
    {'_id':'rap', 'itmf':17, 'name':'Rap'},
    {'_id':'reggae', 'itmf':18, 'name':'Reggae'},
    {'_id':'rock', 'itmf':19, 'name':'Rock'},
    {'_id':'techno', 'itmf':20, 'name':'Techno'},
    {'_id':'industrial', 'itmf':21, 'name':'Industrial'},
    {'_id':'alternative', 'itmf':22, 'name':'Alternative'},
    {'_id':'ska', 'itmf':23, 'name':'Ska'},
    {'_id':'death metal', 'itmf':24, 'name':'Death Metal'},
    {'_id':'pranks', 'itmf':25, 'name':'Pranks'},
    {'_id':'soundtrack', 'itmf':26, 'name':'Soundtrack'},
    {'_id':'euro techno', 'itmf':27, 'name':'Euro Techno'},
    {'_id':'ambient', 'itmf':28, 'name':'Ambient'},
    {'_id':'trip hop', 'itmf':29, 'name':'Trip Hop'},
    {'_id':'vocal', 'itmf':30, 'name':'Vocal'},
    {'_id':'jazz funk', 'itmf':31, 'name':'Jazz Funk'},
    {'_id':'fusion', 'itmf':32, 'name':'Fusion'},
    {'_id':'trance', 'itmf':33, 'name':'Trance'},
    {'_id':'classical', 'itmf':34, 'name':'Classical'},
    {'_id':'instrumental', 'itmf':35, 'name':'Instrumental'},
    {'_id':'acid', 'itmf':36, 'name':'Acid'},
    {'_id':'house', 'itmf':37, 'name':'House'},
    {'_id':'game', 'itmf':38, 'name':'Game'},
    {'_id':'sound clip', 'itmf':39, 'name':'Sound Clip'},
    {'_id':'gospel', 'itmf':40, 'name':'Gospel'},
    {'_id':'noise', 'itmf':41, 'name':'Noise'},
    {'_id':'alternrock', 'itmf':42, 'name':'Alternrock'},
    {'_id':'bass', 'itmf':43, 'name':'Bass'},
    {'_id':'soul', 'itmf':44, 'name':'Soul'},
    {'_id':'punk', 'itmf':45, 'name':'Punk'},
    {'_id':'space', 'itmf':46, 'name':'Space'},
    {'_id':'meditative', 'itmf':47, 'name':'Meditative'},
    {'_id':'instrumental pop', 'itmf':48, 'name':'Instrumental Pop'},
    {'_id':'instrumental rock', 'itmf':49, 'name':'Instrumental Rock'},
    {'_id':'ethnic', 'itmf':50, 'name':'Ethnic'},
    {'_id':'gothic', 'itmf':51, 'name':'Gothic'},
    {'_id':'darkwave', 'itmf':52, 'name':'Darkwave'},
    {'_id':'techno industrial', 'itmf':53, 'name':'Techno Industrial'},
    {'_id':'electronic', 'itmf':54, 'name':'Electronic'},
    {'_id':'pop folk', 'itmf':55, 'name':'Pop Folk'},
    {'_id':'eurodance', 'itmf':56, 'name':'Eurodance'},
    {'_id':'dream', 'itmf':57, 'name':'Dream'},
    {'_id':'southern rock', 'itmf':58, 'name':'Southern Rock'},
    {'_id':'comedy', 'itmf':59, 'name':'Comedy'},
    {'_id':'cult', 'itmf':60, 'name':'Cult'},
    {'_id':'gangsta', 'itmf':61, 'name':'Gangsta'},
    {'_id':'top 40', 'itmf':62, 'name':'Top 40'},
    {'_id':'christian rap', 'itmf':63, 'name':'Christian Rap'},
    {'_id':'pop funk', 'itmf':64, 'name':'Pop Funk'},
    {'_id':'jungle', 'itmf':65, 'name':'Jungle'},
    {'_id':'native American', 'itmf':66, 'name':'Native American'},
    {'_id':'cabaret', 'itmf':67, 'name':'Cabaret'},
    {'_id':'new wave', 'itmf':68, 'name':'New Wave'},
    {'_id':'psychedelic', 'itmf':69, 'name':'Psychedelic'},
    {'_id':'rave', 'itmf':70, 'name':'Rave'},
    {'_id':'showtunes', 'itmf':71, 'name':'Showtunes'},
    {'_id':'trailer', 'itmf':72, 'name':'Trailer'},
    {'_id':'lo fi', 'itmf':73, 'name':'Lo Fi'},
    {'_id':'tribal', 'itmf':74, 'name':'Tribal'},
    {'_id':'acid punk', 'itmf':75, 'name':'Acid Punk'},
    {'_id':'acid jazz', 'itmf':76, 'name':'Acid Jazz'},
    {'_id':'polka', 'itmf':77, 'name':'Polka'},
    {'_id':'retro', 'itmf':78, 'name':'Retro'},
    {'_id':'musical', 'itmf':79, 'name':'Musical'},
    {'_id':'rock and roll', 'itmf':80, 'name':'Rock and Roll'}
]


# TV Show map
# The initial TVDB TV Show id map
tvshow_map = [
    [79501, 'Heroes'],
    [75930, 'Alias'],
    [76290, '24'],
    [73800, 'Desperate Housewives'],
    [79349, 'Dexter'],
    [73871, 'Futurama'],
    [73255, 'House'],
    [73739, 'Lost'],
    [79169, 'Seinfeld'],
    [75299, 'The Sopranos'],
    [73762, 'Greys Anatomy'],
    [79126, 'The Wire'],
    [75164, 'Samurai Jack'],
    [74543, 'Entourage'],
    [85527, 'Yellowstone'],
    [79257, 'Planet Earth'],
    [74845, 'Weeds'],
    [75450, 'Six Feet Under'],
    [80252, 'Flight of the Conchords'],
    [82066, 'Fringe'],
    [80337, 'Mad Men'],
    [73508, 'Rome'],
    [77398, 'The X-Files'],
    [70682, 'Oz'],
    [77526, 'Star Trek'],
    [77231, 'Mission Impossible'],
    [83268, 'Star Wars - The Clone Wars'],
    [74805, 'The Prisoner'],
    [85242, 'The Prisoner 2009'],
    [83602, 'Lie To Me'],
    [80349, 'Californication'],
    [82109, 'Generation Kill'],
    [70533, 'Twin Peaks'],
    [72628, 'The Singing Detective'],
    [80593, 'Dirty Sexy Money'],
    [79177, 'Life on Mars'],
    [82289, 'Life on Mars US'],
    [118421, 'Life BBC'],
    [130421, 'Faces of Earth'],
    [147071, 'Wonders of the Solar System'],
    [108611, 'White Collar'],
    [85149, 'Berlin Alexanderplatz'],
    [94971, 'V 2009'],
    [82459, 'The Mentalist'],
    [82283, 'True Blood']
]