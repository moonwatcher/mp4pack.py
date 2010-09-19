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
repository_config['Volume'] = {'alpha':'/Users/lg/pool/alpha', 'beta':'/Users/lg/pool/beta', 'gama':'/Users/lg/pool/gama', 'delta':'/Users/lg/pool/delta', 'epsilon':'/Users/lg/pool/epsilon', 'eta':'/Users/lg/pool/eta'}
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

repository_config['Kind']['m4v']['Profile']['universal'] = {}
repository_config['Kind']['m4v']['Profile']['universal']['description'] = 'an SD profile that decodes on every cabac capable apple device'
repository_config['Kind']['m4v']['Profile']['universal']['crf'] = '18'
repository_config['Kind']['m4v']['Profile']['universal']['cabac'] = '1'
repository_config['Kind']['m4v']['Profile']['universal']['max_width'] = '720'
repository_config['Kind']['m4v']['Profile']['universal']['x264'] = "ref=2:me=umh:b-adapt=2:weightp=0:trellis=0:subme=9:cabac=%(cabac)s"
repository_config['Kind']['m4v']['Profile']['universal']['extra'] = "--large-file"

repository_config['Kind']['m4v']['Profile']['appletv'] = {}
repository_config['Kind']['m4v']['Profile']['appletv']['crf'] = '22'
repository_config['Kind']['m4v']['Profile']['appletv']['cabac'] = '1'
repository_config['Kind']['m4v']['Profile']['appletv']['max_width'] = '1280'
repository_config['Kind']['m4v']['Profile']['appletv']['x264'] = "ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=9500:vbv-bufsize=9500:cabac=%(cabac)s"
repository_config['Kind']['m4v']['Profile']['appletv']['extra'] = "--large-file"

repository_config['Kind']['m4v']['Profile']['high'] = {}
repository_config['Kind']['m4v']['Profile']['high']['crf'] = '19'
repository_config['Kind']['m4v']['Profile']['high']['cabac'] = '1'
repository_config['Kind']['m4v']['Profile']['high']['max_width'] = '1280'
repository_config['Kind']['m4v']['Profile']['high']['x264'] = "ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=10000:vbv-bufsize=10000:cabac=%(cabac)s"
repository_config['Kind']['m4v']['Profile']['high']['extra'] = "--large-file"

repository_config['Kind']['m4v']['Profile']['ipod'] = {}
repository_config['Kind']['m4v']['Profile']['ipod']['crf'] = '21'
repository_config['Kind']['m4v']['Profile']['ipod']['cabac'] = '0'
repository_config['Kind']['m4v']['Profile']['ipod']['max_width'] = '480'
repository_config['Kind']['m4v']['Profile']['ipod']['x264'] = "ref=2:me=umh:bframes=0:8x8dct=0:trellis=0:subme=6:weightp=0:cabac=%(cabac)s"
repository_config['Kind']['m4v']['Profile']['ipod']['extra'] = ""

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
repository_config['Kind']['mkv']['Profile']['sd'] = {}
repository_config['Kind']['mkv']['Profile']['720'] = {}
repository_config['Kind']['mkv']['Profile']['720'] = {
    'related':(
        {'type':'srt', 'profile':'clean', 'language':'heb'},
        {'type':'srt', 'profile':'clean', 'language':'eng'}
    ),
    'tracks':(
        {'type':'audio', 'codec_kind':'AC3'},
        {'type':'audio', 'codec_kind':'MP3'},
        {'type':'audio', 'codec_kind':'AAC'},
        {'type':'audio', 'codec_kind':'DTS'}
    )
}

repository_config['Kind']['mkv']['Profile']['1080'] = {}

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

tag_config['cache'] = "/Users/lg/pool/cache/"
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
tag_name = []
tag_name.append(('Track #', 'Track #', 'Track'))
tag_name.append(('Disk #', 'Disk #', 'Disk'))
tag_name.append(('Album', 'Album', 'Album'))
tag_name.append(('Album Artist', 'Album Artist', 'Album Artist'))
tag_name.append(('Artist', 'Artist', 'Artist'))
tag_name.append(('ArtistID', None, 'Artist ID'))
tag_name.append(('Tempo', 'Tempo', 'BPM'))
tag_name.append(('Cast', 'Cast', None))
tag_name.append(('Codirector', 'Codirector', None))
tag_name.append(('Category', None, 'Category'))
tag_name.append(('Comments', 'Comments', 'Comments'))
tag_name.append(('Composer', 'Composer', 'Composer'))
tag_name.append(('ComposerID', None, 'Composer ID'))
tag_name.append(('contentID', 'contentID', 'Content ID'))
tag_name.append(('Content Rating', 'Content Rating', 'Content Rating'))
tag_name.append(('Copyright', 'Copyright', 'Copyright'))
tag_name.append(('Artwork Pieces', None, 'Cover Art pieces'))
tag_name.append(('Director', 'Director', None))
tag_name.append(('Encoded By', 'Encoded By', 'Encoded by'))
tag_name.append(('Encoding Tool', 'Encoding Tool', 'Encoded with'))
tag_name.append(('Genre', 'Genre', 'Genre'))
tag_name.append(('GenreID', None, 'Genre ID'))
tag_name.append(('GenreType', None, 'GenreType'))
tag_name.append(('Grouping', 'Grouping', 'Grouping'))
tag_name.append(('HD Video', 'HD Video', 'HD Video'))
tag_name.append(('Keywords', None, 'Keywords'))
tag_name.append(('Long Description', 'Long Description', 'Long Description'))
tag_name.append(('Lyrics', 'Lyrics', 'Lyrics'))
tag_name.append(('Media Kind', 'Media Kind', 'Media Type'))
tag_name.append(('Name', 'Name', 'Name'))
tag_name.append(('Compilation', None, 'Part of Compilation'))
tag_name.append(('Gapless', 'Gapless', 'Part of Gapless Album'))
tag_name.append(('PlaylistID', None, 'Playlist ID'))
tag_name.append(('Podcast', None, 'Podcast'))
tag_name.append(('Producers', 'Producers', None))
tag_name.append(('Purchase Date', 'Purchase Date', 'Purchase Date'))
tag_name.append(('Rating', 'Rating', None))
tag_name.append(('Rating Annotation', 'Rating Annotation', None))
tag_name.append(('Release Date', 'Release Date', 'Release Date'))
tag_name.append(('Screenwriters', 'Screenwriters', None))
tag_name.append(('Description', 'Description', 'Short Description'))
tag_name.append(('Sort Album', None, 'Sort Album'))
tag_name.append(('Sort Album Artist', None, 'Sort Album Artist'))
tag_name.append(('Sort Artist', None, 'Sort Artist'))
tag_name.append(('Sort Composer', None, 'Sort Composer'))
tag_name.append(('Sort Name', None, 'Sort Name'))
tag_name.append(('Sort TV Show', None, 'Sort TV Show'))
tag_name.append(('Studio', 'Studio', None))
tag_name.append(('TV Episode #', 'TV Episode #', 'TV Episode'))
tag_name.append(('TV Episode ID', 'TV Episode ID', 'TV Episode Number'))
tag_name.append(('TV Network', 'TV Network', 'TV Network'))
tag_name.append(('TV Season', 'TV Season', 'TV Season'))
tag_name.append(('TV Show', 'TV Show', 'TV Show'))
tag_name.append(('iTunes Account', 'iTunes Account', 'iTunes Account'))
tag_name.append(('iTunes Account Type', None, 'iTunes Account Type'))
tag_name.append(('iTunes Store Country', None, 'iTunes Store Country'))
tag_name.append(('XID', 'XID', 'xid'))


# Genre map
# allows mapping different names for genres to another
genre_map = []
genre_map.append(('science-fiction', 'sci-fi'))


# ITMF Genre
# The standard itmf names and codes for genres
itmf_genre = []
itmf_genre.append({'_id':'blues', 'itmf':2, 'name':'Blues'})
itmf_genre.append({'_id':'classic rock', 'itmf':3, 'name':'Classic Rock'})
itmf_genre.append({'_id':'country', 'itmf':4, 'name':'Country'})
itmf_genre.append({'_id':'dance', 'itmf':5, 'name':'Dance'})
itmf_genre.append({'_id':'disco', 'itmf':6, 'name':'Disco'})
itmf_genre.append({'_id':'funk', 'itmf':7, 'name':'Funk'})
itmf_genre.append({'_id':'grunge', 'itmf':8, 'name':'Grunge'})
itmf_genre.append({'_id':'hip hop', 'itmf':9, 'name':'Hip Hop'})
itmf_genre.append({'_id':'jazz', 'itmf':10, 'name':'Jazz'})
itmf_genre.append({'_id':'metal', 'itmf':11, 'name':'Metal'})
itmf_genre.append({'_id':'new age', 'itmf':12, 'name':'New Age'})
itmf_genre.append({'_id':'oldies', 'itmf':13, 'name':'Oldies'})
itmf_genre.append({'_id':'other', 'itmf':14, 'name':'Other'})
itmf_genre.append({'_id':'pop', 'itmf':15, 'name':'Pop'})
itmf_genre.append({'_id':'r&b', 'itmf':16, 'name':'R&B'})
itmf_genre.append({'_id':'rap', 'itmf':17, 'name':'Rap'})
itmf_genre.append({'_id':'reggae', 'itmf':18, 'name':'Reggae'})
itmf_genre.append({'_id':'rock', 'itmf':19, 'name':'Rock'})
itmf_genre.append({'_id':'techno', 'itmf':20, 'name':'Techno'})
itmf_genre.append({'_id':'industrial', 'itmf':21, 'name':'Industrial'})
itmf_genre.append({'_id':'alternative', 'itmf':22, 'name':'Alternative'})
itmf_genre.append({'_id':'ska', 'itmf':23, 'name':'Ska'})
itmf_genre.append({'_id':'death metal', 'itmf':24, 'name':'Death Metal'})
itmf_genre.append({'_id':'pranks', 'itmf':25, 'name':'Pranks'})
itmf_genre.append({'_id':'soundtrack', 'itmf':26, 'name':'Soundtrack'})
itmf_genre.append({'_id':'euro techno', 'itmf':27, 'name':'Euro Techno'})
itmf_genre.append({'_id':'ambient', 'itmf':28, 'name':'Ambient'})
itmf_genre.append({'_id':'trip hop', 'itmf':29, 'name':'Trip Hop'})
itmf_genre.append({'_id':'vocal', 'itmf':30, 'name':'Vocal'})
itmf_genre.append({'_id':'jazz funk', 'itmf':31, 'name':'Jazz Funk'})
itmf_genre.append({'_id':'fusion', 'itmf':32, 'name':'Fusion'})
itmf_genre.append({'_id':'trance', 'itmf':33, 'name':'Trance'})
itmf_genre.append({'_id':'classical', 'itmf':34, 'name':'Classical'})
itmf_genre.append({'_id':'instrumental', 'itmf':35, 'name':'Instrumental'})
itmf_genre.append({'_id':'acid', 'itmf':36, 'name':'Acid'})
itmf_genre.append({'_id':'house', 'itmf':37, 'name':'House'})
itmf_genre.append({'_id':'game', 'itmf':38, 'name':'Game'})
itmf_genre.append({'_id':'sound clip', 'itmf':39, 'name':'Sound Clip'})
itmf_genre.append({'_id':'gospel', 'itmf':40, 'name':'Gospel'})
itmf_genre.append({'_id':'noise', 'itmf':41, 'name':'Noise'})
itmf_genre.append({'_id':'alternrock', 'itmf':42, 'name':'Alternrock'})
itmf_genre.append({'_id':'bass', 'itmf':43, 'name':'Bass'})
itmf_genre.append({'_id':'soul', 'itmf':44, 'name':'Soul'})
itmf_genre.append({'_id':'punk', 'itmf':45, 'name':'Punk'})
itmf_genre.append({'_id':'space', 'itmf':46, 'name':'Space'})
itmf_genre.append({'_id':'meditative', 'itmf':47, 'name':'Meditative'})
itmf_genre.append({'_id':'instrumental pop', 'itmf':48, 'name':'Instrumental Pop'})
itmf_genre.append({'_id':'instrumental rock', 'itmf':49, 'name':'Instrumental Rock'})
itmf_genre.append({'_id':'ethnic', 'itmf':50, 'name':'Ethnic'})
itmf_genre.append({'_id':'gothic', 'itmf':51, 'name':'Gothic'})
itmf_genre.append({'_id':'darkwave', 'itmf':52, 'name':'Darkwave'})
itmf_genre.append({'_id':'techno industrial', 'itmf':53, 'name':'Techno Industrial'})
itmf_genre.append({'_id':'electronic', 'itmf':54, 'name':'Electronic'})
itmf_genre.append({'_id':'pop folk', 'itmf':55, 'name':'Pop Folk'})
itmf_genre.append({'_id':'eurodance', 'itmf':56, 'name':'Eurodance'})
itmf_genre.append({'_id':'dream', 'itmf':57, 'name':'Dream'})
itmf_genre.append({'_id':'southern rock', 'itmf':58, 'name':'Southern Rock'})
itmf_genre.append({'_id':'comedy', 'itmf':59, 'name':'Comedy'})
itmf_genre.append({'_id':'cult', 'itmf':60, 'name':'Cult'})
itmf_genre.append({'_id':'gangsta', 'itmf':61, 'name':'Gangsta'})
itmf_genre.append({'_id':'top 40', 'itmf':62, 'name':'Top 40'})
itmf_genre.append({'_id':'christian rap', 'itmf':63, 'name':'Christian Rap'})
itmf_genre.append({'_id':'pop funk', 'itmf':64, 'name':'Pop Funk'})
itmf_genre.append({'_id':'jungle', 'itmf':65, 'name':'Jungle'})
itmf_genre.append({'_id':'native American', 'itmf':66, 'name':'Native American'})
itmf_genre.append({'_id':'cabaret', 'itmf':67, 'name':'Cabaret'})
itmf_genre.append({'_id':'new wave', 'itmf':68, 'name':'New Wave'})
itmf_genre.append({'_id':'psychedelic', 'itmf':69, 'name':'Psychedelic'})
itmf_genre.append({'_id':'rave', 'itmf':70, 'name':'Rave'})
itmf_genre.append({'_id':'showtunes', 'itmf':71, 'name':'Showtunes'})
itmf_genre.append({'_id':'trailer', 'itmf':72, 'name':'Trailer'})
itmf_genre.append({'_id':'lo fi', 'itmf':73, 'name':'Lo Fi'})
itmf_genre.append({'_id':'tribal', 'itmf':74, 'name':'Tribal'})
itmf_genre.append({'_id':'acid punk', 'itmf':75, 'name':'Acid Punk'})
itmf_genre.append({'_id':'acid jazz', 'itmf':76, 'name':'Acid Jazz'})
itmf_genre.append({'_id':'polka', 'itmf':77, 'name':'Polka'})
itmf_genre.append({'_id':'retro', 'itmf':78, 'name':'Retro'})
itmf_genre.append({'_id':'musical', 'itmf':79, 'name':'Musical'})
itmf_genre.append({'_id':'rock and roll', 'itmf':80, 'name':'Rock and Roll'})


# TV Show map
# The initial TVDB TV Show id map
tvshow_map = []
tvshow_map.append([79501, 'Heroes'])
tvshow_map.append([75930, 'Alias'])
tvshow_map.append([76290, '24'])
tvshow_map.append([73800, 'Desperate Housewives'])
tvshow_map.append([79349, 'Dexter'])
tvshow_map.append([73871, 'Futurama'])
tvshow_map.append([73255, 'House'])
tvshow_map.append([73739, 'Lost'])
tvshow_map.append([79169, 'Seinfeld'])
tvshow_map.append([75299, 'The Sopranos'])
tvshow_map.append([73762, 'Greys Anatomy'])
tvshow_map.append([79126, 'The Wire'])
tvshow_map.append([75164, 'Samurai Jack'])
tvshow_map.append([74543, 'Entourage'])
tvshow_map.append([85527, 'Yellowstone'])
tvshow_map.append([79257, 'Planet Earth'])
tvshow_map.append([74845, 'Weeds'])
tvshow_map.append([75450, 'Six Feet Under'])
tvshow_map.append([80252, 'Flight of the Conchords'])
tvshow_map.append([82066, 'Fringe'])
tvshow_map.append([80337, 'Mad Men'])
tvshow_map.append([73508, 'Rome'])
tvshow_map.append([77398, 'The X-Files'])
tvshow_map.append([70682, 'Oz'])
tvshow_map.append([77526, 'Star Trek'])
tvshow_map.append([77231, 'Mission Impossible'])
tvshow_map.append([83268, 'Star Wars - The Clone Wars'])
tvshow_map.append([74805, 'The Prisoner'])
tvshow_map.append([85242, 'The Prisoner 2009'])
tvshow_map.append([83602, 'Lie To Me'])
tvshow_map.append([80349, 'Californication'])
tvshow_map.append([82109, 'Generation Kill'])
tvshow_map.append([70533, 'Twin Peaks'])
tvshow_map.append([72628, 'The Singing Detective'])
tvshow_map.append([80593, 'Dirty Sexy Money'])
tvshow_map.append([79177, 'Life on Mars'])
tvshow_map.append([82289, 'Life on Mars US'])
tvshow_map.append([118421, 'Life BBC'])
tvshow_map.append([130421, 'Faces of Earth'])
tvshow_map.append([147071, 'Wonders of the Solar System'])
tvshow_map.append([108611, 'White Collar'])
tvshow_map.append([85149, 'Berlin Alexanderplatz'])
tvshow_map.append([94971, 'V 2009'])
tvshow_map.append([82459, 'The Mentalist'])
tvshow_map.append([82283, 'True Blood'])
