#!/usr/bin/env python
# -*- coding: utf-8 -*-


repository_config = {}
repository_config['volumes'] = {'alpha':'/pool/alpha', 'beta':'/pool/beta', 'gama':'/pool/gama', 'delta':'/pool/delta', 'epsilon':'/pool/epsilon', 'eta':'/pool/eta'}
repository_config['media-kinds'] = [ 'tvshow', 'movie', 'music', 'audiobook' ]
repository_config['kinds'] = {}

repository_config['kinds']['m4v'] = {}
repository_config['kinds']['m4v']['profiles'] = {}

repository_config['kinds']['m4v']['profiles']['universal'] = {}
repository_config['kinds']['m4v']['profiles']['universal']['crf'] = '18'
repository_config['kinds']['m4v']['profiles']['universal']['cabac'] = '1'
repository_config['kinds']['m4v']['profiles']['universal']['max_width'] = '720'
repository_config['kinds']['m4v']['profiles']['universal']['x264'] = "ref=2:me=umh:b-adapt=2:weightp=0:trellis=0:subme=9:cabac=%(cabac)s"
repository_config['kinds']['m4v']['profiles']['universal']['extra'] = "--large-file"

repository_config['kinds']['m4v']['profiles']['appletv'] = {}
repository_config['kinds']['m4v']['profiles']['appletv']['crf'] = '22'
repository_config['kinds']['m4v']['profiles']['appletv']['cabac'] = '1'
repository_config['kinds']['m4v']['profiles']['appletv']['max_width'] = '1280'
repository_config['kinds']['m4v']['profiles']['appletv']['x264'] = "ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=9500:vbv-bufsize=9500:cabac=%(cabac)s"
repository_config['kinds']['m4v']['profiles']['appletv']['extra'] = "--large-file"

repository_config['kinds']['m4v']['profiles']['high'] = {}
repository_config['kinds']['m4v']['profiles']['high']['crf'] = '19'
repository_config['kinds']['m4v']['profiles']['high']['cabac'] = '1'
repository_config['kinds']['m4v']['profiles']['high']['max_width'] = '1280'
repository_config['kinds']['m4v']['profiles']['high']['x264'] = "ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=10000:vbv-bufsize=10000:cabac=%(cabac)s"
repository_config['kinds']['m4v']['profiles']['high']['extra'] = "--large-file"

repository_config['kinds']['m4v']['profiles']['ipod'] = {}
repository_config['kinds']['m4v']['profiles']['ipod']['crf'] = '21'
repository_config['kinds']['m4v']['profiles']['ipod']['cabac'] = '0'
repository_config['kinds']['m4v']['profiles']['ipod']['max_width'] = '480'
repository_config['kinds']['m4v']['profiles']['ipod']['x264'] = "ref=2:me=umh:bframes=0:8x8dct=0:trellis=0:subme=6:weightp=0:cabac=%(cabac)s"
repository_config['kinds']['m4v']['profiles']['ipod']['extra'] = ""

repository_config['kinds']['mkv'] = {}
repository_config['kinds']['mkv']['profiles'] = {}
repository_config['kinds']['mkv']['profiles']['sd'] = {}
repository_config['kinds']['mkv']['profiles']['720'] = {}
repository_config['kinds']['mkv']['profiles']['1080'] = {}

repository_config['kinds']['m4a'] = {}
repository_config['kinds']['m4a']['profiles'] = {}
repository_config['kinds']['m4a']['profiles']['lossless'] = {}
repository_config['kinds']['m4a']['profiles']['portable'] = {}

repository_config['kinds']['srt'] = {}
repository_config['kinds']['srt']['profiles'] = {}
repository_config['kinds']['srt']['profiles']['original'] = {}
repository_config['kinds']['srt']['profiles']['clean'] = {}



tag_config = {}
tag_config['db'] = {}
tag_config['db']['name'] = "mp4pack"

tag_config['cache'] = "/Users/lg/mp4pack/cache/"
tag_config['tmdb'] = {}
tag_config['tmdb']['apikey'] = "a8b9f96dde091408a03cb4c78477bd14"
tag_config['tmdb']['urls'] = {}
tag_config['tmdb']['urls']['Movie.getInfo'] = "http://api.themoviedb.org/2.1/Movie.getInfo/en/xml/%(apikey)s/%%s" % (tag_config['tmdb'])
tag_config['tmdb']['urls']['Movie.imdbLookup'] = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/xml/%(apikey)s/%%s" % (tag_config['tmdb'])
tag_config['tmdb']['urls']['Person.getInfo'] = "http://api.themoviedb.org/2.1/Person.getInfo/en/xml/%(apikey)s/%%s" % (tag_config['tmdb'])
tag_config['tmdb']['urls']['Person.search'] = "http://api.themoviedb.org/2.1/Person.search/en/xml/%(apikey)s/%%s" % (tag_config['tmdb'])

tag_config['tvdb'] = {}
tag_config['tvdb']['apikey'] = "7B3B400B0146EA83"
tag_config['tvdb']['urls'] = {}
tag_config['tvdb']['urls']['Show.getInfo'] = "http://www.thetvdb.com/api/%(apikey)s/series/%%s/all/en.xml" % (tag_config['tvdb'])



# Tag name map
# Schema: canonic name, subler name, mp4info name
tag_name = []
tag_name.append(('Track #', 'Track #', 'Track'))
tag_name.append(('Disk #', 'Disk #', 'Disk'))
tag_name.append(('Album', 'Album', 'Album'))
tag_name.append(('Album Artist', 'Album Artist', 'Album Artist'))
tag_name.append(('Artist', 'Artist', 'Artist'))
tag_name.append(('ArtisID', None, 'Artist ID'))
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
itmf_genre.append({'_id':'blues', 'itmf_code':'2', 'name':'Blues'})
itmf_genre.append({'_id':'classic rock', 'itmf_code':'3', 'name':'Classic Rock'})
itmf_genre.append({'_id':'country', 'itmf_code':'4', 'name':'Country'})
itmf_genre.append({'_id':'dance', 'itmf_code':'5', 'name':'Dance'})
itmf_genre.append({'_id':'disco', 'itmf_code':'6', 'name':'Disco'})
itmf_genre.append({'_id':'funk', 'itmf_code':'7', 'name':'Funk'})
itmf_genre.append({'_id':'grunge', 'itmf_code':'8', 'name':'Grunge'})
itmf_genre.append({'_id':'hip hop', 'itmf_code':'9', 'name':'Hip Hop'})
itmf_genre.append({'_id':'jazz', 'itmf_code':'10', 'name':'Jazz'})
itmf_genre.append({'_id':'metal', 'itmf_code':'11', 'name':'Metal'})
itmf_genre.append({'_id':'new age', 'itmf_code':'12', 'name':'New Age'})
itmf_genre.append({'_id':'oldies', 'itmf_code':'13', 'name':'Oldies'})
itmf_genre.append({'_id':'other', 'itmf_code':'14', 'name':'Other'})
itmf_genre.append({'_id':'pop', 'itmf_code':'15', 'name':'Pop'})
itmf_genre.append({'_id':'r&b', 'itmf_code':'16', 'name':'R&B'})
itmf_genre.append({'_id':'rap', 'itmf_code':'17', 'name':'Rap'})
itmf_genre.append({'_id':'reggae', 'itmf_code':'18', 'name':'Reggae'})
itmf_genre.append({'_id':'rock', 'itmf_code':'19', 'name':'Rock'})
itmf_genre.append({'_id':'techno', 'itmf_code':'20', 'name':'Techno'})
itmf_genre.append({'_id':'industrial', 'itmf_code':'21', 'name':'Industrial'})
itmf_genre.append({'_id':'alternative', 'itmf_code':'22', 'name':'Alternative'})
itmf_genre.append({'_id':'ska', 'itmf_code':'23', 'name':'Ska'})
itmf_genre.append({'_id':'death metal', 'itmf_code':'24', 'name':'Death Metal'})
itmf_genre.append({'_id':'pranks', 'itmf_code':'25', 'name':'Pranks'})
itmf_genre.append({'_id':'soundtrack', 'itmf_code':'26', 'name':'Soundtrack'})
itmf_genre.append({'_id':'euro techno', 'itmf_code':'27', 'name':'Euro Techno'})
itmf_genre.append({'_id':'ambient', 'itmf_code':'28', 'name':'Ambient'})
itmf_genre.append({'_id':'trip hop', 'itmf_code':'29', 'name':'Trip Hop'})
itmf_genre.append({'_id':'vocal', 'itmf_code':'30', 'name':'Vocal'})
itmf_genre.append({'_id':'jazz funk', 'itmf_code':'31', 'name':'Jazz Funk'})
itmf_genre.append({'_id':'fusion', 'itmf_code':'32', 'name':'Fusion'})
itmf_genre.append({'_id':'trance', 'itmf_code':'33', 'name':'Trance'})
itmf_genre.append({'_id':'classical', 'itmf_code':'34', 'name':'Classical'})
itmf_genre.append({'_id':'instrumental', 'itmf_code':'35', 'name':'Instrumental'})
itmf_genre.append({'_id':'acid', 'itmf_code':'36', 'name':'Acid'})
itmf_genre.append({'_id':'house', 'itmf_code':'37', 'name':'House'})
itmf_genre.append({'_id':'game', 'itmf_code':'38', 'name':'Game'})
itmf_genre.append({'_id':'sound clip', 'itmf_code':'39', 'name':'Sound Clip'})
itmf_genre.append({'_id':'gospel', 'itmf_code':'40', 'name':'Gospel'})
itmf_genre.append({'_id':'noise', 'itmf_code':'41', 'name':'Noise'})
itmf_genre.append({'_id':'alternrock', 'itmf_code':'42', 'name':'Alternrock'})
itmf_genre.append({'_id':'bass', 'itmf_code':'43', 'name':'Bass'})
itmf_genre.append({'_id':'soul', 'itmf_code':'44', 'name':'Soul'})
itmf_genre.append({'_id':'punk', 'itmf_code':'45', 'name':'Punk'})
itmf_genre.append({'_id':'space', 'itmf_code':'46', 'name':'Space'})
itmf_genre.append({'_id':'meditative', 'itmf_code':'47', 'name':'Meditative'})
itmf_genre.append({'_id':'instrumental pop', 'itmf_code':'48', 'name':'Instrumental Pop'})
itmf_genre.append({'_id':'instrumental rock', 'itmf_code':'49', 'name':'Instrumental Rock'})
itmf_genre.append({'_id':'ethnic', 'itmf_code':'50', 'name':'Ethnic'})
itmf_genre.append({'_id':'gothic', 'itmf_code':'51', 'name':'Gothic'})
itmf_genre.append({'_id':'darkwave', 'itmf_code':'52', 'name':'Darkwave'})
itmf_genre.append({'_id':'techno industrial', 'itmf_code':'53', 'name':'Techno Industrial'})
itmf_genre.append({'_id':'electronic', 'itmf_code':'54', 'name':'Electronic'})
itmf_genre.append({'_id':'pop folk', 'itmf_code':'55', 'name':'Pop Folk'})
itmf_genre.append({'_id':'eurodance', 'itmf_code':'56', 'name':'Eurodance'})
itmf_genre.append({'_id':'dream', 'itmf_code':'57', 'name':'Dream'})
itmf_genre.append({'_id':'southern rock', 'itmf_code':'58', 'name':'Southern Rock'})
itmf_genre.append({'_id':'comedy', 'itmf_code':'59', 'name':'Comedy'})
itmf_genre.append({'_id':'cult', 'itmf_code':'60', 'name':'Cult'})
itmf_genre.append({'_id':'gangsta', 'itmf_code':'61', 'name':'Gangsta'})
itmf_genre.append({'_id':'top 40', 'itmf_code':'62', 'name':'Top 40'})
itmf_genre.append({'_id':'christian rap', 'itmf_code':'63', 'name':'Christian Rap'})
itmf_genre.append({'_id':'pop funk', 'itmf_code':'64', 'name':'Pop Funk'})
itmf_genre.append({'_id':'jungle', 'itmf_code':'65', 'name':'Jungle'})
itmf_genre.append({'_id':'native American', 'itmf_code':'66', 'name':'Native American'})
itmf_genre.append({'_id':'cabaret', 'itmf_code':'67', 'name':'Cabaret'})
itmf_genre.append({'_id':'new wave', 'itmf_code':'68', 'name':'New Wave'})
itmf_genre.append({'_id':'psychedelic', 'itmf_code':'69', 'name':'Psychedelic'})
itmf_genre.append({'_id':'rave', 'itmf_code':'70', 'name':'Rave'})
itmf_genre.append({'_id':'showtunes', 'itmf_code':'71', 'name':'Showtunes'})
itmf_genre.append({'_id':'trailer', 'itmf_code':'72', 'name':'Trailer'})
itmf_genre.append({'_id':'lo fi', 'itmf_code':'73', 'name':'Lo Fi'})
itmf_genre.append({'_id':'tribal', 'itmf_code':'74', 'name':'Tribal'})
itmf_genre.append({'_id':'acid punk', 'itmf_code':'75', 'name':'Acid Punk'})
itmf_genre.append({'_id':'acid jazz', 'itmf_code':'76', 'name':'Acid Jazz'})
itmf_genre.append({'_id':'polka', 'itmf_code':'77', 'name':'Polka'})
itmf_genre.append({'_id':'retro', 'itmf_code':'78', 'name':'Retro'})
itmf_genre.append({'_id':'musical', 'itmf_code':'79', 'name':'Musical'})
itmf_genre.append({'_id':'rock and roll', 'itmf_code':'80', 'name':'Rock and Roll'})


