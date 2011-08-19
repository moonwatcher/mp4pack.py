#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from subprocess import Popen, PIPE
from datetime import timedelta

tmdb_apikey = u'a8b9f96dde091408a03cb4c78477bd14'
tvdb_apikey = u'7B3B400B0146EA83'
cache_path = u'/net/multivac/Volumes/alphaville/cache/'
db_uri = u'mongodb://mp4pack:poohbear@multivac.lan/mp4pack'



# Default base configuration

media_property = {
    'file':(
        {
            'name':'encoding',
            'print':'Encoding',
            'mediainfo':None,
            'type':'string',
        },
        {
            'name':'path',
            'print':'Path',
            'mediainfo':'CompleteName',
            'type':'string',
        },
        {
            'name':'directory',
            'print':'Directory',
            'mediainfo':'FolderName',
            'type':'string',
            'display':False,
        },
        {
            'name':'name',
            'print':'Name',
            'mediainfo':'FileName',
            'type':'string',
            'display':False,
        },
        {
            'name':'extension',
            'print':'Extension',
            'mediainfo':'FileExtension',
            'type':'string',
            'display':False,
        },
        {
            'name':'format',
            'print':'Format',
            'mediainfo':'Format',
            'type':'string',
        },
        {
            'name':'size',
            'print':'Size',
            'mediainfo':'FileSize',
            'type':'int',
            'format':'byte',
        },
        {
            'name':'duration',
            'print':'Duration',
            'mediainfo':'Duration',
            'type':'int',
            'format':'millisecond',
        },
        {
            'name':'bit rate',
            'print':'Bit Rate',
            'mediainfo':'OverallBitRate',
            'type':'int',
            'format':'bitrate',
        },
        {
            'name':'encode date',
            'print':'Encode Date',
            'mediainfo':'Encoded_Date',
            'type':'date'
        },
        {
            'name':'modified date',
            'print':'Modified Date',
            'mediainfo':'File_Modified_Date',
            'type':'date',
        },
        {
            'name':'tag date',
            'print':'Tag Date',
            'mediainfo':'Tagged_Date',
            'type':'date',
        },
    ),
    'tag':(
        {
            'name':'language',
            'print':'Language',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'type':'string'
        },
        {
            'name':'profile',
            'print':'Profile',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'type':'string'
        },
        {
            'name':'volume',
            'print':'Volume',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'type':'string'
        },
        {
            'name':'imdb id',
            'print':'IMDb',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'type':'string'
        },
        {
            'name':'kind',
            'atom':None,
            'print':'Kind',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'type':'string',
        },
        {
            'name':'tv show key',
            'atom':None,
            'print':'TV Show Key',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'type':'string',
        },
        {
            'name':'name',
            'atom':'©nam',
            'mediainfo':'Title',
            'mp4info': None,
            'subler':'Name',
            'print':'Name',
            'type':'string',
        },
        {
            'name':'artist',
            'atom':'@ART',
            'mediainfo':None,
            'mp4info': 'Artist',
            'subler':'Artist',
            'print':'Artist',
            'type':'string',
        },
        {
            'name':'album artist',
            'atom':'aART',
            'mediainfo':None,
            'mp4info': 'Album Artist',
            'subler':'Album Artist',
            'print':'Album Artist',
            'type':'string',
        },
        {
            'name':'album',
            'atom':'©alb',
            'mediainfo':'Album',
            'mp4info': None,
            'subler':'Album',
            'print':'Album',
            'type':'string',
        },
        {
            'name':'grouping',
            'atom':'grup',
            'mediainfo':None,
            'mp4info': 'Grouping',
            'subler':'Grouping',
            'print':'Grouping',
            'type':'string',
        },
        {
            'name':'composer',
            'atom':'©wrt',
            'mediainfo':'ScreenplayBy',
            'mp4info': None,
            'subler':'Composer',
            'print':'Composer',
            'type':'string',
        },
        {
            'name':'comment',
            'atom':'©cmt',
            'mediainfo':'Comment',
            'mp4info': None,
            'subler':'Comments',
            'print':'Comment',
            'type':'string',
        },
        {
            'name':'genre type',
            'atom':'gnre',
            'mediainfo':None,
            'mp4info': 'GenreType',
            'subler':None,
            'print':'Genre Type',
            'type':'enum',
        },
        {
            'name':'genre',
            'atom':'©gen',
            'mediainfo':None,
            'mp4info': 'Genre',
            'subler':'Genre',
            'print':'Genre',
            'type':'string',
        },
        {
            'name':'release date',
            'atom':'©day',
            'mediainfo':'Recorded_Date',
            'mp4info': None,
            'subler':'Release Date',
            'print':'Release Date',
            'type':'date',
        },
        {
            'name':'tempo',
            'atom':'tmpo',
            'mediainfo':None,
            'mp4info': 'BPM',
            'subler':'Tempo',
            'print':'Tempo',
            'type':'int',
        },
        {
            'name':'compilation',
            'atom':'cpil',
            'mediainfo':None,
            'mp4info': 'Part of Compilation',
            'subler':None,
            'print':'Compilation',
            'type':'bool',
        },
        {
            'name':'tv show',
            'atom':'tvsh',
            'mediainfo':'tvsh',
            'mp4info': None,
            'subler':'TV Show',
            'print':'TV Show',
            'type':'string',
        },
        {
            'name':'tv episode id',
            'atom':'tven',
            'mediainfo':'tven',
            'mp4info': None,
            'subler':'TV Episode ID',
            'print':'TV Episode ID',
            'type':'string',
        },
        {
            'name':'tv season',
            'atom':'tvsn',
            'mediainfo':'tvsn',
            'mp4info': None,
            'subler':'TV Season',
            'print':'TV Season',
            'type':'int',
        },
        {
            'name':'tv episode #',
            'atom':'tves',
            'mediainfo':'tves',
            'mp4info': None,
            'subler':'TV Episode #',
            'print':'TV Episode',
            'type':'int',
        },
        {
            'name':'tv network',
            'atom':'tvnn',
            'mediainfo':'tvnn',
            'mp4info': None,
            'subler':'TV Network',
            'print':'TV Network',
            'type':'string',
        },
        {
            'name':'sort name',
            'atom':'sonm',
            'mediainfo':'sonm',
            'mp4info': None,
            'subler':'Sort Name',
            'print':'Sort Name',
            'type':'string',
            'display':False,
        },
        {
            'name':'sort artist',
            'atom':'soar',
            'mediainfo':'soar',
            'mp4info': None,
            'subler':'Sort Artist',
            'print':'Sort Artist',
            'type':'string',
            'display':False,
        },
        {
            'name':'sort album artist',
            'atom':'soaa',
            'mediainfo':'soaa',
            'mp4info': None,
            'subler':'Sort Album Artist',
            'print':'Sort Album Artist',
            'type':'string',
            'display':False,
        },
        {
            'name':'sort album',
            'atom':'soal',
            'mediainfo':'soal',
            'mp4info': None,
            'subler':'Sort Album',
            'print':'Sort Album',
            'type':'string',
            'display':False,
        },
        {
            'name':'sort composer',
            'atom':'soco',
            'mediainfo':'soco',
            'mp4info': None,
            'subler':'Sort Composer',
            'print':'Sort Composer',
            'type':'string',
            'display':False,
        },
        {
            'name':'sort tv show',
            'atom':'sosn',
            'mediainfo':'sosn',
            'mp4info': None,
            'subler':'Sort TV Show',
            'print':'Sort TV Show',
            'type':'string',
            'display':False,
        },
        {
            'name':'description',
            'atom':'desc',
            'mediainfo':'desc',
            'mp4info': None,
            'subler':'Description',
            'print':'Description',
            'type':'string',
        },
        {
            'name':'long description',
            'atom':'ldes',
            'mediainfo':'ldes',
            'mp4info': None,
            'subler':'Long Description',
            'print':'Long Description',
            'type':'string',
        },
        {
            'name':'lyrics',
            'atom':'©lyr',
            'mediainfo':None,
            'mp4info': 'Lyrics',
            'subler':'Lyrics',
            'print':'Lyrics',
            'type':'string',
        },
        {
            'name':'copyright',
            'atom':'cprt',
            'mediainfo':'Copyright',
            'mp4info': None,
            'subler':'Copyright',
            'print':'Copyright',
            'type':'string',
        },
        {
            'name':'encoding tool',
            'atom':'©too',
            'mediainfo':None,
            'mp4info': 'Encoded with',
            'subler':'Encoding Tool',
            'print':'Encoding Tool',
            'type':'string',
        },
        {
            'name':'encoded by',
            'atom':'@enc',
            'mediainfo':'Encoded_Application',
            'mp4info': None,
            'subler':'Encoded by',
            'print':'Encoded by',
            'type':'string',
            'display':False,
        },
        {
            'name':'purchase date',
            'atom':'purd',
            'mediainfo':'purd',
            'mp4info': None,
            'subler':'Purchase Date',
            'print':'Purchase Date',
            'type':'date',
        },
        {
            'name':'podcast',
            'atom':'pcst',
            'mediainfo':'pcst',
            'mp4info': None,
            'subler':None,
            'print':'Podcast',
            'type':'bool',
        },
        {
            'name':'podcast url',
            'atom':'purl',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'print':'Podcast URL',
            'type':'string',
        },
        {
            'name':'keywords',
            'atom':'keyw',
            'mediainfo':'keyw',
            'mp4info': None,
            'subler':None,
            'print':'Keywords',
            'type':'string',
        },
        {
            'name':'category',
            'atom':'catg',
            'mediainfo':'catg',
            'mp4info': None,
            'subler':None,
            'print':'Category',
            'type':'string',
        },
        {
            'name':'hd video',
            'atom':'hdvd',
            'mediainfo':'hdvd',
            'mp4info': None,
            'subler':'HD Video',
            'print':'HD Video',
            'type':'bool',
        },
        {
            'name':'gapless',
            'atom':'pgap',
            'mediainfo':None,
            'mp4info': 'Part of Gapless Album',
            'subler':'Gapless',
            'print':'Gapless',
            'type':'bool',
        },
        {
            'name':'xid',
            'atom':'xid',
            'mediainfo':'xid',
            'mp4info': None,
            'subler':'XID',
            'print':'XID',
            'type':'string',
        },
        {
            'name':'content id',
            'atom':'cnID',
            'mediainfo':'cnID',
            'mp4info': None,
            'subler':'contentID',
            'print':'Content ID',
            'type':'int',
        },
        {
            'name':'itunes account',
            'atom':'apID',
            'mediainfo':'apID',
            'mp4info': None,
            'subler':'iTunes Account',
            'print':'iTunes Account',
            'type':'string',
        },
        {
            'name':'artist id',
            'atom':'atID',
            'mediainfo':'atID',
            'mp4info': None,
            'subler':None,
            'print':'Artist ID',
            'type':'int',
        },
        {
            'name':'composer id',
            'atom':'cmID',
            'mediainfo':'cmID',
            'mp4info': None,
            'subler':None,
            'print':'Composer ID',
            'type':'int',
        },
        {
            'name':'playlist id',
            'atom':'plID',
            'mediainfo':'plID',
            'mp4info': None,
            'subler':None,
            'print':'Playlist ID',
            'type':'int',
        },
        {
            'name':'genre id',
            'atom':'geID',
            'mediainfo':'geID',
            'mp4info': None,
            'subler':None,
            'print':'Genre ID',
            'type':'int',
        },
        {
            'name':'itunes store country',
            'atom':'sfID',
            'mediainfo':'sfID',
            'mp4info': None,
            'subler':None,
            'print':'iTunes Store Country',
            'type':'enum',
        },
        {
            'name':'itunes account type',
            'atom':'akID',
            'mediainfo':'akID',
            'mp4info': None,
            'subler':None,
            'print':'iTunes Account Type',
            'type':'enum',
        },
        {
            'name':'episode global id',
            'atom':'egid',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'print':'Episode Global ID',
            'type':'int',
        },
        {
            'name':'media kind',
            'atom':'stik',
            'mediainfo':'stik',
            'mp4info': None,
            'subler':'Media Kind',
            'print':'Media Kind',
            'type':'enum',
        },
        {
            'name':'content rating',
            'atom':'rtng',
            'mediainfo':'rtng',
            'mp4info': None,
            'subler':'Content Rating',
            'print':'Content Rating',
            'type':'enum',
        },
        {
            'name':'itunextc',
            'atom':'iTunEXTC',
            'mediainfo':'iTunEXTC',
            'mp4info': None,
            'subler':None,
            'print':'iTunEXTC',
            'type':'string',
            'display':False
        },
        {
            'name':'itunmovi',
            'atom':'iTunMOVI',
            'mediainfo':'iTunMOVI',
            'mp4info': None,
            'subler':None,
            'print':'iTunMOVI',
            'type':'string',
            'format':'xml',
            'display':False
        },
        {
            'name':'cast',
            'atom':'iTunMOVI',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Cast',
            'print':'Cast',
            'type':'list',
        },
        {
            'name':'directors',
            'atom':'iTunMOVI',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Director',
            'print':'Directors',
            'type':'list',
        },
        {
            'name':'codirectors',
            'atom':'iTunMOVI',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Codirectors',
            'print':'Codirectors',
            'type':'list',
        },
        {
            'name':'producers',
            'atom':'iTunMOVI',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Producers',
            'print':'Producers',
            'type':'list',
        },
        {
            'name':'screenwriters',
            'atom':'iTunMOVI',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Screenwriters',
            'print':'Screenwriters',
            'type':'list',
        },
        {
            'name':'studio',
            'atom':'iTunMOVI',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Studio',
            'print':'Studio',
            'type':'list',
        },
        {
            'name':'rating standard',
            'atom':'iTunEXTC',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'print':'Rating Standard',
            'type':'string',
            'display':False,
        },
        {
            'name':'rating',
            'atom':'iTunEXTC',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Rating',
            'print':'Rating',
            'type':'string',
        },
        {
            'name':'rating score',
            'atom':'iTunEXTC',
            'mediainfo':None,
            'mp4info': None,
            'subler':None,
            'print':'Rating Score',
            'type':'int',
            'display':False,
        },
        {
            'name':'rating annotation',
            'atom':'iTunEXTC',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Rating Annotation',
            'print':'Rating Annotation',
            'type':'string',
            'display':False,
        },
        {
            'name':'track #',
            'atom':'trkn',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Track #',
            'print':'Track',
            'type':'string',
        },
        {
            'name':'disk #',
            'atom':'disk',
            'mediainfo':None,
            'mp4info': None,
            'subler':'Disk #',
            'print':'Disk',
            'type':'string',
        },
        {
            'name':'track position',
            'atom':'trkn',
            'mediainfo':'Track_Position',
            'mp4info': None,
            'subler':None,
            'print':'Track Position',
            'type':'int',
            'display':False,
        },
        {
            'name':'track total',
            'atom':'trkn',
            'mediainfo':'Track_Position_Total',
            'mp4info': None,
            'subler':None,
            'print':'Track Total',
            'type':'int',
            'display':False
        },
        {
            'name':'disk position',
            'atom':'disk',
            'mediainfo':'Part_Position',
            'mp4info': None,
            'subler':None,
            'print':'Disk Position',
            'type':'int',
            'display':False,
        },
        {
            'name':'disk total',
            'atom':'disk',
            'mediainfo':'Part_Position_Total',
            'mp4info': None,
            'subler':None,
            'print':'Disk Total',
            'type':'int',
            'display':False,
        },
        {
            'name':'cover',
            'atom':'covr',
            'mediainfo':'Cover',
            'mp4info': None,
            'subler':None,
            'print':'Cover Pieces',
            'type':'int',
        },
    ),
    'track':{
        'common':(
            {
                'name':'type',
                'print':'Type',
                'mediainfo':None,
                'type':'string',
            },
            {
                'name':'id',
                'print':'ID',
                'mediainfo':'ID',
                'type':'int',
            },
            {
                'name':'position',
                'print':'Position',
                'mediainfo':'StreamKindPos',
                'type':'int',
            },
            {
                'name':'codec',
                'print':'Codec',
                'mediainfo':'Format',
                'type':'string',
            },
            {
                'name':'codec profile',
                'print':'Codec Profile',
                'mediainfo':'Format_Profile',
                'type':'string',
            },
            {
                'name':'duration',
                'print':'Duration',
                'mediainfo':'Duration',
                'type':'int',
                'format':'millisecond',
            },
            {
                'name':'bit rate',
                'print':'Bit Rate',
                'mediainfo':'BitRate',
                'type':'int',
                'format':'bitrate',
            },
            {
                'name':'bit rate mode',
                'print':'Bit Rate Mode',
                'mediainfo':'BitRate_Mode',
                'type':'string',
            },
            {
                'name':'bit depth',
                'print':'Bit Depth',
                'mediainfo':'BitDepth',
                'type':'int',
                'format':'bit',
            },
            {
                'name':'stream size',
                'print':'Stream Size',
                'mediainfo':'StreamSize',
                'type':'int',
                'format':'byte',
            },
            {
                'name':'language',
                'print':'Language',
                'mediainfo':'Language_String3',
                'type':'string',
            },
            {
                'name':'encoded date',
                'print':'Encoded Date',
                'mediainfo':'Encoded_Date',
                'type':'date',
                'display':False,
            },
            {
                'name':'name',
                'print':'Name',
                'mediainfo':'Title',
                'type':'string',
            },
            {
                'name':'delay',
                'print':'Delay',
                'mediainfo':'Delay',
                'type':'int',
            },
        ),
        'audio':(
            {
                'name':'channels',
                'print':'Channels',
                'mediainfo':'Channel_s_',
                'type':'int',
            },
            {
                'name':'channel position',
                'print':'Channel Position',
                'mediainfo':'ChannelPositions',
                'type':'string',
            },
            {
                'name':'sample rate',
                'print':'Sample Rate',
                'mediainfo':'SamplingRate',
                'type':'int',
                'format':'frequency',
            },
            {
                'name':'sample count',
                'print':'Sample Count',
                'mediainfo':'SamplingCount',
                'type':'int',
            },
            {
                'name':'dialnorm',
                'print':'Dialnorm',
                'mediainfo':'dialnorm',
                'type':'int',
            },
        ),
        'video':(
            {
                'name':'width',
                'print':'Width',
                'mediainfo':'Width',
                'type':'int',
                'format':'pixel',
            },
            {
                'name':'height',
                'print':'Height',
                'mediainfo':'Height',
                'type':'int',
                'format':'pixel',
            },
            {
                'name':'pixel aspect ratio',
                'print':'Pixel Aspect Ratio',
                'mediainfo':'PixelAspectRatio',
                'type':'float',
            },
            {
                'name':'display aspect ratio',
                'print':'Display Aspect Ratio',
                'mediainfo':'DisplayAspectRatio',
                'type':'float',
            },
            {
                'name':'frame rate mode',
                'print':'Frame Rate Mode',
                'mediainfo':'FrameRate_Mode',
                'type':'string',
            },
            {
                'name':'frame rate',
                'print':'Frame Rate',
                'mediainfo':'FrameRate',
                'type':'float',
                'format':'framerate',
            },
            {
                'name':'frame rate minimum',
                'print':'Frame Rate Minimum',
                'mediainfo':'FrameRate_Minimum',
                'type':'float',
                'format':'framerate',
            },
            {
                'name':'frame rate maximum',
                'print':'Frame Rate Maximum',
                'mediainfo':'FrameRate_Maximum',
                'type':'float',
                'format':'framerate',
            },
            {
                'name':'frame count',
                'print':'Frame Count',
                'mediainfo':'FrameCount',
                'type':'int',
            },
            {
                'name':'color space',
                'print':'Color Space',
                'mediainfo':'ColorSpace',
                'type':'string',
            },
            {
                'name':'bpf',
                'print':'Bits / Pixel * Frame',
                'mediainfo':'Bits-_Pixel_Frame_',
                'type':'float',
            },
            {
                'name':'encoder',
                'print':'Encoder',
                'mediainfo':'Encoded_Library',
                'type':'string',
            },
            {
                'name':'encoder settings',
                'print':'Encoder Settings',
                'mediainfo':'Encoded_Library_Settings',
                'type':'list',
                'display':False,
            },
        ),
        'text':(
        ),
        'image':(
            {
                'name':'width',
                'print':'Width',
                'mediainfo':'Width',
                'type':'int',
                'format':'pixel',
            },
            {
                'name':'height',
                'print':'Height',
                'mediainfo':'Height',
                'type':'int',
                'format':'pixel',
            },
        )
    },
    'language':(
        {
            'name':'unknown',
            'print':'Unknown',
            'iso2':None,
            'iso3t':'und',
            'iso3b':'und'
        },
        {
            'name':'afar',
            'print':'Afar',
            'iso2':'aa',
            'iso3t':'aar',
            'iso3b':'aar'
        },
        {
            'name':'abkhazian',
            'print':'Abkhazian',
            'iso2':'ab',
            'iso3t':'abk',
            'iso3b':'abk'
        },
        {
            'name':'afrikaans',
            'print':'Afrikaans',
            'iso2':'af',
            'iso3t':'afr',
            'iso3b':'afr'
        },
        {
            'name':'akan',
            'print':'Akan',
            'iso2':'ak',
            'iso3t':'aka',
            'iso3b':'aka'
        },
        {
            'name':'albanian',
            'print':'Albanian',
            'iso2':'sq',
            'iso3t':'sqi',
            'iso3b':'alb'
        },
        {
            'name':'amharic',
            'print':'Amharic',
            'iso2':'am',
            'iso3t':'amh',
            'iso3b':'amh'
        },
        {
            'name':'arabic',
            'print':'Arabic',
            'iso2':'ar',
            'iso3t':'ara',
            'iso3b':'ara'
        },
        {
            'name':'aragonese',
            'print':'Aragonese',
            'iso2':'an',
            'iso3t':'arg',
            'iso3b':'arg'
        },
        {
            'name':'armenian',
            'print':'Armenian',
            'iso2':'hy',
            'iso3t':'hye',
            'iso3b':'arm'
        },
        {
            'name':'assamese',
            'print':'Assamese',
            'iso2':'as',
            'iso3t':'asm',
            'iso3b':'asm'
        },
        {
            'name':'avaric',
            'print':'Avaric',
            'iso2':'av',
            'iso3t':'ava',
            'iso3b':'ava'
        },
        {
            'name':'avestan',
            'print':'Avestan',
            'iso2':'ae',
            'iso3t':'ave',
            'iso3b':'ave'
        },
        {
            'name':'aymara',
            'print':'Aymara',
            'iso2':'ay',
            'iso3t':'aym',
            'iso3b':'aym'
        },
        {
            'name':'azerbaijani',
            'print':'Azerbaijani',
            'iso2':'az',
            'iso3t':'aze',
            'iso3b':'aze'
        },
        {
            'name':'bashkir',
            'print':'Bashkir',
            'iso2':'ba',
            'iso3t':'bak',
            'iso3b':'bak'
        },
        {
            'name':'bambara',
            'print':'Bambara',
            'iso2':'bm',
            'iso3t':'bam',
            'iso3b':'bam'
        },
        {
            'name':'basque',
            'print':'Basque',
            'iso2':'eu',
            'iso3t':'eus',
            'iso3b':'baq'
        },
        {
            'name':'belarusian',
            'print':'Belarusian',
            'iso2':'be',
            'iso3t':'bel',
            'iso3b':'bel'
        },
        {
            'name':'bengali',
            'print':'Bengali',
            'iso2':'bn',
            'iso3t':'ben',
            'iso3b':'ben'
        },
        {
            'name':'bihari',
            'print':'Bihari',
            'iso2':'bh',
            'iso3t':'bih',
            'iso3b':'bih'
        },
        {
            'name':'bislama',
            'print':'Bislama',
            'iso2':'bi',
            'iso3t':'bis',
            'iso3b':'bis'
        },
        {
            'name':'bosnian',
            'print':'Bosnian',
            'iso2':'bs',
            'iso3t':'bos',
            'iso3b':'bos'
        },
        {
            'name':'breton',
            'print':'Breton',
            'iso2':'br',
            'iso3t':'bre',
            'iso3b':'bre'
        },
        {
            'name':'bulgarian',
            'print':'Bulgarian',
            'iso2':'bg',
            'iso3t':'bul',
            'iso3b':'bul'
        },
        {
            'name':'burmese',
            'print':'Burmese',
            'iso2':'my',
            'iso3t':'mya',
            'iso3b':'bur'
        },
        {
            'name':'catalan',
            'print':'Catalan',
            'iso2':'ca',
            'iso3t':'cat',
            'iso3b':'cat'
        },
        {
            'name':'chamorro',
            'print':'Chamorro',
            'iso2':'ch',
            'iso3t':'cha',
            'iso3b':'cha'
        },
        {
            'name':'chechen',
            'print':'Chechen',
            'iso2':'ce',
            'iso3t':'che',
            'iso3b':'che'
        },
        {
            'name':'chinese',
            'print':'Chinese',
            'iso2':'zh',
            'iso3t':'zho',
            'iso3b':'chi'
        },
        {
            'name':'church slavic',
            'print':'Church Slavic',
            'iso2':'cu',
            'iso3t':'chu',
            'iso3b':'chu'
        },
        {
            'name':'chuvash',
            'print':'Chuvash',
            'iso2':'cv',
            'iso3t':'chv',
            'iso3b':'chv'
        },
        {
            'name':'cornish',
            'print':'Cornish',
            'iso2':'kw',
            'iso3t':'cor',
            'iso3b':'cor'
        },
        {
            'name':'corsican',
            'print':'Corsican',
            'iso2':'co',
            'iso3t':'cos',
            'iso3b':'cos'
        },
        {
            'name':'cree',
            'print':'Cree',
            'iso2':'cr',
            'iso3t':'cre',
            'iso3b':'cre'
        },
        {
            'name':'czech',
            'print':'Czech',
            'iso2':'cs',
            'iso3t':'ces',
            'iso3b':'cze'
        },
        {
            'name':'danish',
            'print':'Danish',
            'iso2':'da',
            'iso3t':'dan',
            'iso3b':'dan'
        },
        {
            'name':'divehi',
            'print':'Divehi',
            'iso2':'dv',
            'iso3t':'div',
            'iso3b':'div'
        },
        {
            'name':'dutch',
            'print':'Dutch',
            'iso2':'nl',
            'iso3t':'nld',
            'iso3b':'dut'
        },
        {
            'name':'dzongkha',
            'print':'Dzongkha',
            'iso2':'dz',
            'iso3t':'dzo',
            'iso3b':'dzo'
        },
        {
            'name':'english',
            'print':'English',
            'iso2':'en',
            'iso3t':'eng',
            'iso3b':'eng'
        },
        {
            'name':'esperanto',
            'print':'Esperanto',
            'iso2':'eo',
            'iso3t':'epo',
            'iso3b':'epo'
        },
        {
            'name':'estonian',
            'print':'Estonian',
            'iso2':'et',
            'iso3t':'est',
            'iso3b':'est'
        },
        {
            'name':'ewe',
            'print':'Ewe',
            'iso2':'ee',
            'iso3t':'ewe',
            'iso3b':'ewe'
        },
        {
            'name':'faroese',
            'print':'Faroese',
            'iso2':'fo',
            'iso3t':'fao',
            'iso3b':'fao'
        },
        {
            'name':'fijian',
            'print':'Fijian',
            'iso2':'fj',
            'iso3t':'fij',
            'iso3b':'fij'
        },
        {
            'name':'finnish',
            'print':'Finnish',
            'iso2':'fi',
            'iso3t':'fin',
            'iso3b':'fin'
        },
        {
            'name':'french',
            'print':'French',
            'iso2':'fr',
            'iso3t':'fra',
            'iso3b':'fre'
        },
        {
            'name':'western frisian',
            'print':'Western Frisian',
            'iso2':'fy',
            'iso3t':'fry',
            'iso3b':'fry'
        },
        {
            'name':'fulah',
            'print':'Fulah',
            'iso2':'ff',
            'iso3t':'ful',
            'iso3b':'ful'
        },
        {
            'name':'georgian',
            'print':'Georgian',
            'iso2':'ka',
            'iso3t':'kat',
            'iso3b':'geo'
        },
        {
            'name':'german',
            'print':'German',
            'iso2':'de',
            'iso3t':'deu',
            'iso3b':'ger'
        },
        {
            'name':'gaelic (scots)',
            'print':'Gaelic (Scots)',
            'iso2':'gd',
            'iso3t':'gla',
            'iso3b':'gla'
        },
        {
            'name':'irish',
            'print':'Irish',
            'iso2':'ga',
            'iso3t':'gle',
            'iso3b':'gle'
        },
        {
            'name':'galician',
            'print':'Galician',
            'iso2':'gl',
            'iso3t':'glg',
            'iso3b':'glg'
        },
        {
            'name':'manx',
            'print':'Manx',
            'iso2':'gv',
            'iso3t':'glv',
            'iso3b':'glv'
        },
        {
            'name':'greek, modern',
            'print':'Greek, Modern',
            'iso2':'el',
            'iso3t':'ell',
            'iso3b':'gre'
        },
        {
            'name':'guarani',
            'print':'Guarani',
            'iso2':'gn',
            'iso3t':'grn',
            'iso3b':'grn'
        },
        {
            'name':'gujarati',
            'print':'Gujarati',
            'iso2':'gu',
            'iso3t':'guj',
            'iso3b':'guj'
        },
        {
            'name':'haitian',
            'print':'Haitian',
            'iso2':'ht',
            'iso3t':'hat',
            'iso3b':'hat'
        },
        {
            'name':'hausa',
            'print':'Hausa',
            'iso2':'ha',
            'iso3t':'hau',
            'iso3b':'hau'
        },
        {
            'name':'hebrew',
            'print':'Hebrew',
            'iso2':'he',
            'iso3t':'heb',
            'iso3b':'heb'
        },
        {
            'name':'herero',
            'print':'Herero',
            'iso2':'hz',
            'iso3t':'her',
            'iso3b':'her'
        },
        {
            'name':'hindi',
            'print':'Hindi',
            'iso2':'hi',
            'iso3t':'hin',
            'iso3b':'hin'
        },
        {
            'name':'hiri motu',
            'print':'Hiri Motu',
            'iso2':'ho',
            'iso3t':'hmo',
            'iso3b':'hmo'
        },
        {
            'name':'hungarian',
            'print':'Hungarian',
            'iso2':'hu',
            'iso3t':'hun',
            'iso3b':'hun'
        },
        {
            'name':'igbo',
            'print':'Igbo',
            'iso2':'ig',
            'iso3t':'ibo',
            'iso3b':'ibo'
        },
        {
            'name':'icelandic',
            'print':'Icelandic',
            'iso2':'is',
            'iso3t':'isl',
            'iso3b':'ice'
        },
        {
            'name':'ido',
            'print':'Ido',
            'iso2':'io',
            'iso3t':'ido',
            'iso3b':'ido'
        },
        {
            'name':'sichuan yi',
            'print':'Sichuan Yi',
            'iso2':'ii',
            'iso3t':'iii',
            'iso3b':'iii'
        },
        {
            'name':'inuktitut',
            'print':'Inuktitut',
            'iso2':'iu',
            'iso3t':'iku',
            'iso3b':'iku'
        },
        {
            'name':'interlingue',
            'print':'Interlingue',
            'iso2':'ie',
            'iso3t':'ile',
            'iso3b':'ile'
        },
        {
            'name':'interlingua',
            'print':'Interlingua',
            'iso2':'ia',
            'iso3t':'ina',
            'iso3b':'ina'
        },
        {
            'name':'indonesian',
            'print':'Indonesian',
            'iso2':'id',
            'iso3t':'ind',
            'iso3b':'ind'
        },
        {
            'name':'inupiaq',
            'print':'Inupiaq',
            'iso2':'ik',
            'iso3t':'ipk',
            'iso3b':'ipk'
        },
        {
            'name':'italian',
            'print':'Italian',
            'iso2':'it',
            'iso3t':'ita',
            'iso3b':'ita'
        },
        {
            'name':'javanese',
            'print':'Javanese',
            'iso2':'jv',
            'iso3t':'jav',
            'iso3b':'jav'
        },
        {
            'name':'japanese',
            'print':'Japanese',
            'iso2':'ja',
            'iso3t':'jpn',
            'iso3b':'jpn'
        },
        {
            'name':'kalaallisut (greenlandic)',
            'print':'Kalaallisut (Greenlandic)',
            'iso2':'kl',
            'iso3t':'kal',
            'iso3b':'kal'
        },
        {
            'name':'kannada',
            'print':'Kannada',
            'iso2':'kn',
            'iso3t':'kan',
            'iso3b':'kan'
        },
        {
            'name':'kashmiri',
            'print':'Kashmiri',
            'iso2':'ks',
            'iso3t':'kas',
            'iso3b':'kas'
        },
        {
            'name':'kanuri',
            'print':'Kanuri',
            'iso2':'kr',
            'iso3t':'kau',
            'iso3b':'kau'
        },
        {
            'name':'kazakh',
            'print':'Kazakh',
            'iso2':'kk',
            'iso3t':'kaz',
            'iso3b':'kaz'
        },
        {
            'name':'central khmer',
            'print':'Central Khmer',
            'iso2':'km',
            'iso3t':'khm',
            'iso3b':'khm'
        },
        {
            'name':'kikuyu',
            'print':'Kikuyu',
            'iso2':'ki',
            'iso3t':'kik',
            'iso3b':'kik'
        },
        {
            'name':'kinyarwanda',
            'print':'Kinyarwanda',
            'iso2':'rw',
            'iso3t':'kin',
            'iso3b':'kin'
        },
        {
            'name':'kirghiz',
            'print':'Kirghiz',
            'iso2':'ky',
            'iso3t':'kir',
            'iso3b':'kir'
        },
        {
            'name':'komi',
            'print':'Komi',
            'iso2':'kv',
            'iso3t':'kom',
            'iso3b':'kom'
        },
        {
            'name':'kongo',
            'print':'Kongo',
            'iso2':'kg',
            'iso3t':'kon',
            'iso3b':'kon'
        },
        {
            'name':'korean',
            'print':'Korean',
            'iso2':'ko',
            'iso3t':'kor',
            'iso3b':'kor'
        },
        {
            'name':'kuanyama',
            'print':'Kuanyama',
            'iso2':'kj',
            'iso3t':'kua',
            'iso3b':'kua'
        },
        {
            'name':'kurdish',
            'print':'Kurdish',
            'iso2':'ku',
            'iso3t':'kur',
            'iso3b':'kur'
        },
        {
            'name':'lao',
            'print':'Lao',
            'iso2':'lo',
            'iso3t':'lao',
            'iso3b':'lao'
        },
        {
            'name':'latin',
            'print':'Latin',
            'iso2':'la',
            'iso3t':'lat',
            'iso3b':'lat'
        },
        {
            'name':'latvian',
            'print':'Latvian',
            'iso2':'lv',
            'iso3t':'lav',
            'iso3b':'lav'
        },
        {
            'name':'limburgan',
            'print':'Limburgan',
            'iso2':'li',
            'iso3t':'lim',
            'iso3b':'lim'
        },
        {
            'name':'lingala',
            'print':'Lingala',
            'iso2':'ln',
            'iso3t':'lin',
            'iso3b':'lin'
        },
        {
            'name':'lithuanian',
            'print':'Lithuanian',
            'iso2':'lt',
            'iso3t':'lit',
            'iso3b':'lit'
        },
        {
            'name':'luxembourgish',
            'print':'Luxembourgish',
            'iso2':'lb',
            'iso3t':'ltz',
            'iso3b':'ltz'
        },
        {
            'name':'luba-katanga',
            'print':'Luba-Katanga',
            'iso2':'lu',
            'iso3t':'lub',
            'iso3b':'lub'
        },
        {
            'name':'ganda',
            'print':'Ganda',
            'iso2':'lg',
            'iso3t':'lug',
            'iso3b':'lug'
        },
        {
            'name':'macedonian',
            'print':'Macedonian',
            'iso2':'mk',
            'iso3t':'mkd',
            'iso3b':'mac'
        },
        {
            'name':'marshallese',
            'print':'Marshallese',
            'iso2':'mh',
            'iso3t':'mah',
            'iso3b':'mah'
        },
        {
            'name':'malayalam',
            'print':'Malayalam',
            'iso2':'ml',
            'iso3t':'mal',
            'iso3b':'mal'
        },
        {
            'name':'maori',
            'print':'Maori',
            'iso2':'mi',
            'iso3t':'mri',
            'iso3b':'mao'
        },
        {
            'name':'marathi',
            'print':'Marathi',
            'iso2':'mr',
            'iso3t':'mar',
            'iso3b':'mar'
        },
        {
            'name':'malay',
            'print':'Malay',
            'iso2':'ms',
            'iso3t':'msa',
            'iso3b':'msa'
        },
        {
            'name':'malagasy',
            'print':'Malagasy',
            'iso2':'mg',
            'iso3t':'mlg',
            'iso3b':'mlg'
        },
        {
            'name':'maltese',
            'print':'Maltese',
            'iso2':'mt',
            'iso3t':'mlt',
            'iso3b':'mlt'
        },
        {
            'name':'moldavian',
            'print':'Moldavian',
            'iso2':'mo',
            'iso3t':'mol',
            'iso3b':'mol'
        },
        {
            'name':'mongolian',
            'print':'Mongolian',
            'iso2':'mn',
            'iso3t':'mon',
            'iso3b':'mon'
        },
        {
            'name':'nauru',
            'print':'Nauru',
            'iso2':'na',
            'iso3t':'nau',
            'iso3b':'nau'
        },
        {
            'name':'navajo',
            'print':'Navajo',
            'iso2':'nv',
            'iso3t':'nav',
            'iso3b':'nav'
        },
        {
            'name':'ndebele, south',
            'print':'Ndebele, South',
            'iso2':'nr',
            'iso3t':'nbl',
            'iso3b':'nbl'
        },
        {
            'name':'ndebele, north',
            'print':'Ndebele, North',
            'iso2':'nd',
            'iso3t':'nde',
            'iso3b':'nde'
        },
        {
            'name':'ndonga',
            'print':'Ndonga',
            'iso2':'ng',
            'iso3t':'ndo',
            'iso3b':'ndo'
        },
        {
            'name':'nepali',
            'print':'Nepali',
            'iso2':'ne',
            'iso3t':'nep',
            'iso3b':'nep'
        },
        {
            'name':'norwegian nynorsk',
            'print':'Norwegian Nynorsk',
            'iso2':'nn',
            'iso3t':'nno',
            'iso3b':'nno'
        },
        {
            'name':'norwegian bokmål',
            'print':'Norwegian Bokmål',
            'iso2':'nb',
            'iso3t':'nob',
            'iso3b':'nob'
        },
        {
            'name':'norwegian',
            'print':'Norwegian',
            'iso2':'no',
            'iso3t':'nor',
            'iso3b':'nor'
        },
        {
            'name':'chichewa; nyanja',
            'print':'Chichewa; Nyanja',
            'iso2':'ny',
            'iso3t':'nya',
            'iso3b':'nya'
        },
        {
            'name':'occitan (post 1500); provençal',
            'print':'Occitan (post 1500); Provençal',
            'iso2':'oc',
            'iso3t':'oci',
            'iso3b':'oci'
        },
        {
            'name':'ojibwa',
            'print':'Ojibwa',
            'iso2':'oj',
            'iso3t':'oji',
            'iso3b':'oji'
        },
        {
            'name':'oriya',
            'print':'Oriya',
            'iso2':'or',
            'iso3t':'ori',
            'iso3b':'ori'
        },
        {
            'name':'oromo',
            'print':'Oromo',
            'iso2':'om',
            'iso3t':'orm',
            'iso3b':'orm'
        },
        {
            'name':'ossetian; ossetic',
            'print':'Ossetian; Ossetic',
            'iso2':'os',
            'iso3t':'oss',
            'iso3b':'oss'
        },
        {
            'name':'panjabi',
            'print':'Panjabi',
            'iso2':'pa',
            'iso3t':'pan',
            'iso3b':'pan'
        },
        {
            'name':'persian',
            'print':'Persian',
            'iso2':'fa',
            'iso3t':'fas',
            'iso3b':'per'
        },
        {
            'name':'pali',
            'print':'Pali',
            'iso2':'pi',
            'iso3t':'pli',
            'iso3b':'pli'
        },
        {
            'name':'polish',
            'print':'Polish',
            'iso2':'pl',
            'iso3t':'pol',
            'iso3b':'pol'
        },
        {
            'name':'portuguese',
            'print':'Portuguese',
            'iso2':'pt',
            'iso3t':'por',
            'iso3b':'por'
        },
        {
            'name':'pushto',
            'print':'Pushto',
            'iso2':'ps',
            'iso3t':'pus',
            'iso3b':'pus'
        },
        {
            'name':'quechua',
            'print':'Quechua',
            'iso2':'qu',
            'iso3t':'que',
            'iso3b':'que'
        },
        {
            'name':'romansh',
            'print':'Romansh',
            'iso2':'rm',
            'iso3t':'roh',
            'iso3b':'roh'
        },
        {
            'name':'romanian',
            'print':'Romanian',
            'iso2':'ro',
            'iso3t':'ron',
            'iso3b':'rum'
        },
        {
            'name':'rundi',
            'print':'Rundi',
            'iso2':'rn',
            'iso3t':'run',
            'iso3b':'run'
        },
        {
            'name':'russian',
            'print':'Russian',
            'iso2':'ru',
            'iso3t':'rus',
            'iso3b':'rus'
        },
        {
            'name':'sango',
            'print':'Sango',
            'iso2':'sg',
            'iso3t':'sag',
            'iso3b':'sag'
        },
        {
            'name':'sanskrit',
            'print':'Sanskrit',
            'iso2':'sa',
            'iso3t':'san',
            'iso3b':'san'
        },
        {
            'name':'serbian',
            'print':'Serbian',
            'iso2':'sr',
            'iso3t':'srp',
            'iso3b':'scc'
        },
        {
            'name':'croatian',
            'print':'Croatian',
            'iso2':'hr',
            'iso3t':'hrv',
            'iso3b':'scr'
        },
        {
            'name':'sinhala',
            'print':'Sinhala',
            'iso2':'si',
            'iso3t':'sin',
            'iso3b':'sin'
        },
        {
            'name':'slovak',
            'print':'Slovak',
            'iso2':'sk',
            'iso3t':'slk',
            'iso3b':'slo'
        },
        {
            'name':'slovenian',
            'print':'Slovenian',
            'iso2':'sl',
            'iso3t':'slv',
            'iso3b':'slv'
        },
        {
            'name':'northern sami',
            'print':'Northern Sami',
            'iso2':'se',
            'iso3t':'sme',
            'iso3b':'sme'
        },
        {
            'name':'samoan',
            'print':'Samoan',
            'iso2':'sm',
            'iso3t':'smo',
            'iso3b':'smo'
        },
        {
            'name':'shona',
            'print':'Shona',
            'iso2':'sn',
            'iso3t':'sna',
            'iso3b':'sna'
        },
        {
            'name':'sindhi',
            'print':'Sindhi',
            'iso2':'sd',
            'iso3t':'snd',
            'iso3b':'snd'
        },
        {
            'name':'somali',
            'print':'Somali',
            'iso2':'so',
            'iso3t':'som',
            'iso3b':'som'
        },
        {
            'name':'sotho, southern',
            'print':'Sotho, Southern',
            'iso2':'st',
            'iso3t':'sot',
            'iso3b':'sot'
        },
        {
            'name':'spanish',
            'print':'Spanish',
            'iso2':'es',
            'iso3t':'spa',
            'iso3b':'spa'
        },
        {
            'name':'sardinian',
            'print':'Sardinian',
            'iso2':'sc',
            'iso3t':'srd',
            'iso3b':'srd'
        },
        {
            'name':'swati',
            'print':'Swati',
            'iso2':'ss',
            'iso3t':'ssw',
            'iso3b':'ssw'
        },
        {
            'name':'sundanese',
            'print':'Sundanese',
            'iso2':'su',
            'iso3t':'sun',
            'iso3b':'sun'
        },
        {
            'name':'swahili',
            'print':'Swahili',
            'iso2':'sw',
            'iso3t':'swa',
            'iso3b':'swa'
        },
        {
            'name':'swedish',
            'print':'Swedish',
            'iso2':'sv',
            'iso3t':'swe',
            'iso3b':'swe'
        },
        {
            'name':'tahitian',
            'print':'Tahitian',
            'iso2':'ty',
            'iso3t':'tah',
            'iso3b':'tah'
        },
        {
            'name':'tamil',
            'print':'Tamil',
            'iso2':'ta',
            'iso3t':'tam',
            'iso3b':'tam'
        },
        {
            'name':'tatar',
            'print':'Tatar',
            'iso2':'tt',
            'iso3t':'tat',
            'iso3b':'tat'
        },
        {
            'name':'telugu',
            'print':'Telugu',
            'iso2':'te',
            'iso3t':'tel',
            'iso3b':'tel'
        },
        {
            'name':'tajik',
            'print':'Tajik',
            'iso2':'tg',
            'iso3t':'tgk',
            'iso3b':'tgk'
        },
        {
            'name':'tagalog',
            'print':'Tagalog',
            'iso2':'tl',
            'iso3t':'tgl',
            'iso3b':'tgl'
        },
        {
            'name':'thai',
            'print':'Thai',
            'iso2':'th',
            'iso3t':'tha',
            'iso3b':'tha'
        },
        {
            'name':'tibetan',
            'print':'Tibetan',
            'iso2':'bo',
            'iso3t':'bod',
            'iso3b':'tib'
        },
        {
            'name':'tigrinya',
            'print':'Tigrinya',
            'iso2':'ti',
            'iso3t':'tir',
            'iso3b':'tir'
        },
        {
            'name':'tonga (tonga islands)',
            'print':'Tonga (Tonga Islands)',
            'iso2':'to',
            'iso3t':'ton',
            'iso3b':'ton'
        },
        {
            'name':'tswana',
            'print':'Tswana',
            'iso2':'tn',
            'iso3t':'tsn',
            'iso3b':'tsn'
        },
        {
            'name':'tsonga',
            'print':'Tsonga',
            'iso2':'ts',
            'iso3t':'tso',
            'iso3b':'tso'
        },
        {
            'name':'turkmen',
            'print':'Turkmen',
            'iso2':'tk',
            'iso3t':'tuk',
            'iso3b':'tuk'
        },
        {
            'name':'turkish',
            'print':'Turkish',
            'iso2':'tr',
            'iso3t':'tur',
            'iso3b':'tur'
        },
        {
            'name':'twi',
            'print':'Twi',
            'iso2':'tw',
            'iso3t':'twi',
            'iso3b':'twi'
        },
        {
            'name':'uighur',
            'print':'Uighur',
            'iso2':'ug',
            'iso3t':'uig',
            'iso3b':'uig'
        },
        {
            'name':'ukrainian',
            'print':'Ukrainian',
            'iso2':'uk',
            'iso3t':'ukr',
            'iso3b':'ukr'
        },
        {
            'name':'urdu',
            'print':'Urdu',
            'iso2':'ur',
            'iso3t':'urd',
            'iso3b':'urd'
        },
        {
            'name':'uzbek',
            'print':'Uzbek',
            'iso2':'uz',
            'iso3t':'uzb',
            'iso3b':'uzb'
        },
        {
            'name':'venda',
            'print':'Venda',
            'iso2':'ve',
            'iso3t':'ven',
            'iso3b':'ven'
        },
        {
            'name':'vietnamese',
            'print':'Vietnamese',
            'iso2':'vi',
            'iso3t':'vie',
            'iso3b':'vie'
        },
        {
            'name':'volapük',
            'print':'Volapük',
            'iso2':'vo',
            'iso3t':'vol',
            'iso3b':'vol'
        },
        {
            'name':'welsh',
            'print':'Welsh',
            'iso2':'cy',
            'iso3t':'cym',
            'iso3b':'wel'
        },
        {
            'name':'walloon',
            'print':'Walloon',
            'iso2':'wa',
            'iso3t':'wln',
            'iso3b':'wln'
        },
        {
            'name':'wolof',
            'print':'Wolof',
            'iso2':'wo',
            'iso3t':'wol',
            'iso3b':'wol'
        },
        {
            'name':'xhosa',
            'print':'Xhosa',
            'iso2':'xh',
            'iso3t':'xho',
            'iso3b':'xho'
        },
        {
            'name':'yiddish',
            'print':'Yiddish',
            'iso2':'yi',
            'iso3t':'yid',
            'iso3b':'yid'
        },
        {
            'name':'yoruba',
            'print':'Yoruba',
            'iso2':'yo',
            'iso3t':'yor',
            'iso3b':'yor'
        },
        {
            'name':'zhuang',
            'print':'Zhuang',
            'iso2':'za',
            'iso3t':'zha',
            'iso3b':'zha'
        },
        {
            'name':'zulu',
            'print':'Zulu',
            'iso2':'zu',
            'iso3t':'zul',
            'iso3b':'zul'
        },
    ),
    'itunemovi':(
        {
            'name':'cast',
            'print':'Cast',
            'plist':'cast'
        },
        {
            'name':'directors',
            'print':'Directors',
            'plist':'directors'
        },
        {
            'name':'codirectors',
            'print':'Codirectors',
            'plist':'codirectors'
        },
        {
            'name':'producers',
            'print':'Producers',
            'plist':'producers'
        },
        {
            'name':'screenwriters',
            'print':'Screenwriters',
            'plist':'screenwriters'
        },
        {
            'name':'studio',
            'print':'Studio',
            'plist':'studio'
        },
    ),
    'gnre':(
        {'name':'blues','code':1, 'print':'Blues'},
        {'name':'classic rock','code':2, 'print':'Classic Rock'},
        {'name':'country','code':3, 'print':'Country'},
        {'name':'dance','code':4, 'print':'Dance'},
        {'name':'disco','code':5, 'print':'Disco'},
        {'name':'funk','code':6, 'print':'Funk'},
        {'name':'grunge','code':7, 'print':'Grunge'},
        {'name':'hip hop','code':8, 'print':'Hip Hop'},
        {'name':'jazz','code':9, 'print':'Jazz'},
        {'name':'metal','code':10, 'print':'Metal'},
        {'name':'new age','code':11, 'print':'New Age'},
        {'name':'oldies','code':12, 'print':'Oldies'},
        {'name':'other','code':13, 'print':'Other'},
        {'name':'pop','code':14, 'print':'Pop'},
        {'name':'r&b','code':15, 'print':'R&B'},
        {'name':'rap','code':16, 'print':'Rap'},
        {'name':'reggae','code':17, 'print':'Reggae'},
        {'name':'rock','code':18, 'print':'Rock'},
        {'name':'techno','code':19, 'print':'Techno'},
        {'name':'industrial','code':20, 'print':'Industrial'},
        {'name':'alternative','code':21, 'print':'Alternative'},
        {'name':'ska','code':22, 'print':'Ska'},
        {'name':'death metal','code':23, 'print':'Death Metal'},
        {'name':'pranks','code':24, 'print':'Pranks'},
        {'name':'soundtrack','code':25, 'print':'Soundtrack'},
        {'name':'euro techno','code':26, 'print':'Euro Techno'},
        {'name':'ambient','code':27, 'print':'Ambient'},
        {'name':'trip hop','code':28, 'print':'Trip Hop'},
        {'name':'vocal','code':29, 'print':'Vocal'},
        {'name':'jazz funk','code':30, 'print':'Jazz Funk'},
        {'name':'fusion','code':31, 'print':'Fusion'},
        {'name':'trance','code':32, 'print':'Trance'},
        {'name':'classical','code':33, 'print':'Classical'},
        {'name':'instrumental','code':34, 'print':'Instrumental'},
        {'name':'acid','code':35, 'print':'Acid'},
        {'name':'house','code':36, 'print':'House'},
        {'name':'game','code':37, 'print':'Game'},
        {'name':'sound clip','code':38, 'print':'Sound Clip'},
        {'name':'gospel','code':39, 'print':'Gospel'},
        {'name':'noise','code':40, 'print':'Noise'},
        {'name':'alternrock','code':41, 'print':'Alternrock'},
        {'name':'bass','code':42, 'print':'Bass'},
        {'name':'soul','code':43, 'print':'Soul'},
        {'name':'punk','code':44, 'print':'Punk'},
        {'name':'space','code':45, 'print':'Space'},
        {'name':'meditative','code':46, 'print':'Meditative'},
        {'name':'instrumental pop','code':47, 'print':'Instrumental Pop'},
        {'name':'instrumental rock','code':48, 'print':'Instrumental Rock'},
        {'name':'ethnic','code':49, 'print':'Ethnic'},
        {'name':'gothic','code':50, 'print':'Gothic'},
        {'name':'darkwave','code':51, 'print':'Darkwave'},
        {'name':'techno industrial','code':52, 'print':'Techno Industrial'},
        {'name':'electronic','code':53, 'print':'Electronic'},
        {'name':'pop folk','code':54, 'print':'Pop Folk'},
        {'name':'eurodance','code':55, 'print':'Eurodance'},
        {'name':'dream','code':56, 'print':'Dream'},
        {'name':'southern rock','code':57, 'print':'Southern Rock'},
        {'name':'comedy','code':58, 'print':'Comedy'},
        {'name':'cult','code':59, 'print':'Cult'},
        {'name':'gangsta','code':60, 'print':'Gangsta'},
        {'name':'top 40','code':61, 'print':'Top 40'},
        {'name':'christian rap','code':62, 'print':'Christian Rap'},
        {'name':'pop funk','code':63, 'print':'Pop Funk'},
        {'name':'jungle','code':64, 'print':'Jungle'},
        {'name':'native American','code':65, 'print':'Native American'},
        {'name':'cabaret','code':66, 'print':'Cabaret'},
        {'name':'new wave','code':67, 'print':'New Wave'},
        {'name':'psychedelic','code':68, 'print':'Psychedelic'},
        {'name':'rave','code':69, 'print':'Rave'},
        {'name':'showtunes','code':70, 'print':'Showtunes'},
        {'name':'trailer','code':71, 'print':'Trailer'},
        {'name':'lo fi','code':72, 'print':'Lo Fi'},
        {'name':'tribal','code':73, 'print':'Tribal'},
        {'name':'acid punk','code':74, 'print':'Acid Punk'},
        {'name':'acid jazz','code':75, 'print':'Acid Jazz'},
        {'name':'polka','code':76, 'print':'Polka'},
        {'name':'retro','code':77, 'print':'Retro'},
        {'name':'musical','code':78, 'print':'Musical'},
        {'name':'rock and roll','code':79, 'print':'Rock and Roll'},
        {'name':'hard rock','code':80, 'print':'Hard Rock'},
        {'name':'folk','code':81, 'print':'Folk'},
        {'name':'folk rock','code':82, 'print':'Folk-Rock'},
        {'name':'national folk','code':83, 'print':'National Folk'},
        {'name':'swing','code':84, 'print':'Swing'},
        {'name':'fast fusion','code':85, 'print':'Fast Fusion'},
        {'name':'bebob','code':86, 'print':'Bebob'},
        {'name':'latin','code':87, 'print':'Latin'},
        {'name':'revival','code':88, 'print':'Revival'},
        {'name':'celtic','code':89, 'print':'Celtic'},
        {'name':'bluegrass','code':90, 'print':'Bluegrass'},
        {'name':'avantgarde','code':91, 'print':'Avantgarde'},
        {'name':'gothic rock','code':92, 'print':'Gothic Rock'},
        {'name':'progressive rock','code':93, 'print':'Progresive Rock'},
        {'name':'psychedelic rock','code':94, 'print':'Psychedelic Rock'},
        {'name':'symphonic rock','code':95, 'print':'Symphonic Rock'},
        {'name':'slow rock','code':96, 'print':'Slow Rock'},
        {'name':'big band','code':97, 'print':'Big Band'},
        {'name':'chorus','code':98, 'print':'Chorus'},
        {'name':'easy listening','code':99, 'print':'Easy Listening'},
        {'name':'acoustic','code':100, 'print':'Acoustic'},
        {'name':'humour','code':101, 'print':'Humor'},
        {'name':'speech','code':102, 'print':'Speech'},
        {'name':'chanson','code':103, 'print':'Chason'},
        {'name':'opera','code':104, 'print':'Opera'},
        {'name':'chamber music','code':105, 'print':'Chamber Music'},
        {'name':'sonata','code':106, 'print':'Sonata'},
        {'name':'symphony','code':107, 'print':'Symphony'},
        {'name':'booty bass','code':108, 'print':'Booty Bass'},
        {'name':'primus','code':109, 'print':'Primus'},
        {'name':'porn groove','code':110, 'print':'Porn Groove'},
        {'name':'satire','code':111, 'print':'Satire'},
        {'name':'slow jam','code':112, 'print':'Slow Jam'},
        {'name':'club','code':113, 'print':'Club'},
        {'name':'tango','code':114, 'print':'Tango'},
        {'name':'samba','code':115, 'print':'Samba'},
        {'name':'folklore','code':116, 'print':'Folklore'},
        {'name':'ballad','code':117, 'print':'Ballad'},
        {'name':'power ballad','code':118, 'print':'Power Ballad'},
        {'name':'rhythmic soul','code':119, 'print':'Rhythmic Soul'},
        {'name':'freestyle','code':120, 'print':'Freestyle'},
        {'name':'duet','code':121, 'print':'Duet'},
        {'name':'punk rock','code':122, 'print':'Punk Rock'},
        {'name':'drum solo','code':123, 'print':'Drum Solo'},
        {'name':'a capella','code':124, 'print':'A capella'},
        {'name':'euro house','code':125, 'print':'Euro-House'},
        {'name':'dance hall','code':126, 'print':'Dance Hall'},
    ),
    'stik':(
        {
            'name':'oldmovie',
            'print':'Movie',
            'code':0
        },
        {
            'name':'normal',
            'print':'Normal',
            'code':1
        },
        {
            'name':'audiobook',
            'print':'Audio Book',
            'code':2
        },
        {
            'name':'musicvideo',
            'print':'Music Video',
            'code':6
        },
        {
            'name':'movie',
            'print':'Movie',
            'code':9,
            'schema':re.compile(ur'^IMDb(tt[0-9]+)(?: (.*))?\.([^\.]+)$', re.UNICODE), 
        },
        {
            'name':'tvshow',
            'print':'TV Show',
            'code':10,
            'schema':re.compile(ur'^(.+) (s([0-9]+)e([0-9]+))(?:\s*(.*))?\.([^\.]+)$', re.UNICODE),
        },
        {
            'name':'booklet',
            'print':'Booklet',
            'code':11
        },
        {
            'name':'ringtone',
            'print':'Ringtone',
            'code':14
        },
    ),
    'sfID':(
        {'name':'usa', 'print':'United States', 'code':143441},
        {'name':'fra', 'print':'France', 'code':143442},
        {'name':'ger', 'print':'Germany', 'code':143443},
        {'name':'gbr', 'print':'United Kingdom', 'code':143444},
        {'name':'aut', 'print':'Austria', 'code':143445},
        {'name':'bel', 'print':'Belgium', 'code':143446},
        {'name':'fin', 'print':'Finland', 'code':143447},
        {'name':'grc', 'print':'Greece', 'code':143448},
        {'name':'irl', 'print':'Ireland', 'code':143449},
        {'name':'ita', 'print':'Italy', 'code':143450},
        {'name':'lux', 'print':'Luxembourg', 'code':143451},
        {'name':'nld', 'print':'Netherlands', 'code':143452},
        {'name':'prt', 'print':'Portugal', 'code':143453},
        {'name':'esp', 'print':'Spain', 'code':143454},
        {'name':'can', 'print':'Canada', 'code':143455},
        {'name':'swe', 'print':'Sweden', 'code':143456},
        {'name':'nor', 'print':'Norway', 'code':143457},
        {'name':'dnk', 'print':'Denmark', 'code':143458},
        {'name':'che', 'print':'Switzerland', 'code':143459},
        {'name':'aus', 'print':'Australia', 'code':143460},
        {'name':'nzl', 'print':'New Zealand', 'code':143461},
        {'name':'jpn', 'print':'Japan', 'code':143462},
    ),
    'rtng':(
        {'name':'none', 'print':'None', 'code':0},
        {'name':'clean', 'print':'Clean', 'code':2},
        {'name':'explicit', 'print':'Explicit', 'code':4},
    ),
    'akID':(
        {'name':'itunes', 'print':'iTunes', 'code':0},
        {'name':'aol', 'print':'AOL', 'code':1},
    ),
}

repository_config = {
    'Default':{
        'hd video min width':720,
        'display aspect ratio':float(float(16)/float(9)),
        'threads':8,
        'sync delay':timedelta(days=14),
    },
    'Database':{
        'cache':cache_path,
        'uri':db_uri,
        'name':'mp4pack',
        'tmdb':{
            'apikey':tmdb_apikey,
            'urls':{
                'Movie.getInfo':u'http://api.themoviedb.org/2.1/Movie.getInfo/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Movie.imdbLookup':u'http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Person.getInfo':u'http://api.themoviedb.org/2.1/Person.getInfo/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Person.search':u'http://api.themoviedb.org/2.1/Person.search/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Genres.getList':u'http://api.themoviedb.org/2.1/Genres.getList/en/json/{0}'.format(tmdb_apikey),
            },
        },
        'tvdb':{
            'apikey':tvdb_apikey,
            'fuzzy':{
                'minimum_person_name_length':3,
            },
            'urls':{
                'Show.getInfo':u'http://www.thetvdb.com/api/{0}/series/{{0}}/all/en.xml'.format(tvdb_apikey),
                'Banner.getImage':u'http://www.thetvdb.com/banners/{0}'
            },
        },
    },
    'Volume':{
        'alpha':{
            'path':'/pool/alpha',
            'alternative':(
                '/net/multivac/Volumes/alphaville/alpha',
                '/Volumes/alphaville/alpha',
            )
        },
        'beta':{
            'path':'/pool/beta',
            'alternative':(
                '/net/multivac/Volumes/nyc/beta',
                '/Volumes/nyc/beta',
            )
        },
        'gama':{
            'path':'/pool/gama',
            'alternative':(
                '/net/multivac/Volumes/cambridge/gama',
                '/Volumes/cambridge/gama',
            )
            
        },
        'delta':{
            'path':'/pool/delta',
            'alternative':(
                '/net/vito/media/fairfield/delta',
                '/Volumes/fairfield/delta',
            )
        },
        'eta':{
            'path':'/pool/eta',
            'alternative':(
                '/net/vito/media/tlv/eta',
                '/Volumes/tlv/eta',
            )
        },
        'epsilon':{
            'path':'/pool/epsilon',
            'alternative':(
                '/net/vito/media/nagasaki/epsilon',
                '/Volumes/nagasaki/epsilon',
            )
        },
        'kapa':{
            'path':'/pool/kapa',
            'alternative':(
                '/Volumes/moonbook/kapa',
            )
        },
    },
    'Command':{
        'rsync':{
            'binary':u'rsync',
        },
        'mv':{
            'binary':u'mv',
        },
        'handbrake':{
            'binary':u'HandbrakeCLI',
        },
        'subler':{
            'binary':u'SublerCLI',
        },
        'mkvmerge':{
            'binary':u'mkvmerge',
        },
        'mkvextract':{
            'binary':u'mkvextract',
        },
        'mp4info':{
            'binary':u'mp4info',
        },
        'mp4file':{
            'binary':u'mp4file',
        },
        'mp4art':{
            'binary':u'mp4art',
        },
        'mediainfo':{
            'binary':u'mediainfo',
        },
        'ffmpeg':{
            'binary':u'ffmpeg',
        }
    },
    'Display':{
        'wrap':120, 
        'indent':30, 
        'margin':2,
    },
    'Action':{
        'info':{
            'depend':('mediainfo', 'mp4info',),
        },
        'copy':{
            'depend':('rsync',),
        },
        'rename':{
            'depend':('mv',),
        },
        'extract':{
            'depend':('mkvextract',),
        },
        'tag':{
            'depend':('subler',),
        },
        'optimize':{
            'depend':('mp4file',),
        },
        'pack':{
            'depend':('mkvmerge',),
            'kind':('mkv','m4v', ),
        },
        'transcode':{
            'depend':('handbrake',),
            'kind':('m4v', 'mkv', 'srt', 'txt', 'jpg', 'png', 'ac3'),
        },
        'transform':{
            'depend':('handbrake',),
            'kind':('m4v',),
        },
        'update':{
            'depend':('subler',),
            'kind':('srt', 'png', 'jpg', 'txt', 'm4v'),
        },
    },
    'Kind':{
        'm4v':{
            'container':'mp4',
            'default':{'volume':'epsilon', 'profile':'appletv'},
            'Profile':{
                'universal':{
                    'description':'an SD profile that decodes on every cabac capable apple device',
                    'default':{
                        10:{'volume':'beta'},
                        9:{'volume':'gama'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':18,
                            '--encoder':'x264',
                            '--encopts':'ref=2:me=umh:b-adapt=2:weightp=0:trellis=0:subme=9:cabac=1:b-pyramid=none',
                            '--maxWidth':720,
                        },
                        'flags':('--large-file','--loose-anamorphic'),
                        'audio':(
                            (
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'},
                                },
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'copy', '--ab':'auto', '--mixdown':'auto'},
                                }, 
                            ),
                            (
                                {
                                    'from': {'codec':'AAC', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':2},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':1},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                            ),
                        ),
                    },
                },
                'A4':{
                    'description':'All A4 based apple devices',
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':18,
                            '--encoder':'x264',
                            '--encopts':'mixed-refs=1:ref=3:bframes=3:me=umh:b-adapt=2:trellis=0:b-pyramid=none:subme=9:vbv-maxrate=5500:vbv-bufsize=5500:cabac=1',
                            '--maxWidth':1280,
                        },
                        'flags':('--large-file','--loose-anamorphic'),
                        'audio':(
                            (
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'},
                                },
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'copy', '--ab':'auto', '--mixdown':'auto'},
                                },
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':2, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                                {
                                    'from': {'codec':'AAC', 'type':'audio', 'channels':2, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':1, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                                {
                                    'from': {'codec':'AAC', 'type':'audio', 'channels':1, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'AAC', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':2},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':1},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                            ),
                        ),
                    },
                },
                'appletv':{
                    'description':'Intel based AppleTV profile',
                    'default':{
                        10:{'volume':'beta'},
                        9:{'volume':'gama'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':22,
                            '--encoder':'x264',
                            '--encopts':'ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=1:8x8dct=1:trellis=0:b-pyramid=none:subme=9:vbv-maxrate=5500:vbv-bufsize=5500:cabac=1',
                            '--maxWidth':1280,
                        },
                        'flags':('--large-file','--loose-anamorphic'),
                        'audio':(
                            (
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'},
                                },
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'copy', '--ab':'auto', '--mixdown':'auto'},
                                }, 
                            ),
                            (
                                {
                                    'from': {'codec':'AAC', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':2},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':1},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                            ),
                        ),
                    },
                },
                'ipod':{
                    'description':'All iPod touch models profile',
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':21,
                            '--encoder':'x264',
                            '--encopts':'ref=2:me=umh:bframes=0:8x8dct=0:trellis=0:subme=6:weightp=0:cabac=0:b-pyramid=none',
                            '--maxWidth':480,
                        },
                        'flags':('--large-file','--loose-anamorphic'),
                        'audio':(
                            (
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'AAC', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':2},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':1},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                            ),
                        ),
                    },
                },
                'high':{
                    'description':'High profile',
                    'default':{
                        10:{'volume':'beta'},
                        9:{'volume':'eta'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':18,
                            '--encoder':'x264',
                            '--encopts':'ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=1:trellis=0:b-pyramid=none:subme=9:vbv-maxrate=10000:vbv-bufsize=10000:cabac=1',
                            '--maxWidth':1280
                        },
                        'flags':('--large-file','--loose-anamorphic'),
                        'audio':(
                            (
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':192, '--mixdown':'dpl2'},
                                },
                                {
                                    'from': {'codec':'AC-3', 'type':'audio'},
                                    'to': {'--aencoder':'copy', '--ab':'auto', '--mixdown':'auto'},
                                },
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':2, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                                {
                                    'from': {'codec':'AAC', 'type':'audio', 'channels':2, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                                {
                                    'from': {'codec':'MPEG Audio', 'type':'audio', 'channels':1, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                                {
                                    'from': {'codec':'AAC', 'type':'audio', 'channels':1, 'language':'heb'},
                                    'to': {'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                            ),
                            (
                                {
                                    'from': {'codec':'AAC', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                        ),
                    },
                },
            },
        },
        'm4a':{
            'container':'mp4',
            'default':{'volume':'alpha'},
            'Profile':{
                'lossless':{},
                'portable':{},
            },
        },
        'mkv':{
            'container':'matroska',
            'default':{'volume':'epsilon'},
            'Profile':{
                'sd':{
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'pack':{
                        'related':(
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
                            {'kind':'txt', 'profile':'chapter'},
                            {'kind':'ac3'},
                        ),
                        'tracks':(
                            {'type':'video'},
                            {'type':'audio', 'codec':'AC-3'},
                            {'type':'audio', 'codec':'MPEG Audio'},
                            {'type':'audio', 'codec':'AAC'},
                            {'type':'audio', 'codec':'DTS'},
                        ),
                    },
                },
                '720':{
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'pack':{
                        'related':(
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
                            {'kind':'txt', 'profile':'chapter'},
                            {'kind':'ac3'},
                        ),
                        'tracks':(
                            {'type':'video'},
                            {'type':'audio', 'codec':'AC-3'},
                            {'type':'audio', 'codec':'AAC'},
                            {'type':'audio', 'codec':'DTS'},
                            {'type':'audio', 'codec':'MPEG Audio'},
                        ),
                    },
                },
                '1080':{
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'pack':{
                        'related':(
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
                            {'kind':'txt', 'profile':'chapter'},
                            {'kind':'ac3'},
                        ),
                        'tracks':(
                            {'type':'video'},
                            {'type':'audio', 'codec':'AC-3'},
                            {'type':'audio', 'codec':'AAC'},
                            {'type':'audio', 'codec':'DTS'},
                            {'type':'audio', 'codec':'MPEG Audio'},
                        ),
                    },
                },
            },
        },
        'avi':{
            'container':'avi',
            'default':{'volume':'epsilon', 'profile':'sd'},
            'Profile':{
                'sd':{
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                },
            },
        },
        'srt':{
            'container':'subtitles',
            'default':{'profile':'clean'},
            'Profile':{
                'dump':{
                    'description':'Special profile used for extracting.',
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'extract':{
                        'tracks':(
                            {'type':'text', 'language':'heb', 'codec':'UTF-8'},
                            {'type':'text', 'language':'eng', 'codec':'UTF-8'},
                        ),
                    },
                },
                'original':{
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                    'update':{
                        'reset':True,
                        'smart':{'language':'swe', 'Name':'Default', 'order':('heb', 'eng'), 'height':0.148},
                        'related':(
                            {
                                'from': {'language':'heb', 'kind':'srt', 'profile':'original'},
                                'to': {'height':0.132, 'Name':'Normal', },
                            },
                            {
                                'from': {'language':'eng', 'kind':'srt', 'profile':'original'},
                                'to': {'height':0.132, 'Name':'Normal'},
                            },
                        ),
                    },
                },
                'clean':{
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                    'transcode':{
                        'filter':{
                            'heb':('noise', 'hebrew noise', 'typo', 'punctuation', 'leftover'),
                            'eng':('noise', 'typo', 'english typo', 'leftover'),
                        },
                    },
                    'update':{
                        'reset':True,
                        'smart':{'language':'swe', 'Name':'Default', 'order':('heb', 'eng'), 'height':0.148},
                        'related':(
                            {
                                'from': {'language':'heb', 'kind':'srt', 'profile':'clean'},
                                'to': {'height':0.132, 'Name':'Normal'},
                            },
                            {
                                'from': {'language':'eng', 'kind':'srt', 'profile':'clean'},
                                'to': {'height':0.132, 'Name':'Normal'},
                            },
                        ),
                    },
                },
                'remove':{
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                    'update':{
                        'reset':True,
                    },
                },
            },
        },
        'ass':{
            'container':'subtitles',
            'default':{'profile':'dump'},
            'Profile':{
                'dump':{
                    'description':'Special profile used by extract command',
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'extract':{
                        'tracks':(
                            {'type':'text', 'language':'heb', 'codec':'ASS'},
                            {'type':'text', 'language':'eng', 'codec':'ASS'},
                        ),
                    },
                },
            },
        },
        'txt':{
            'container':'chapters',
            'default':{
                'profile':'chapter',
                'volume':'alpha'
            },
            'Profile':{
                'chapter':{
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                    'update':{
                        'reset':True,
                        'related':{'kind':'txt', 'profile':'chapter'}
                    }
                },
                'remove':{
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                    'update':{
                        'reset':True,
                    }
                },
            },
        },
        'jpg':{
            'container':'image',
            'default':{
                'profile':'original',
                'volume':'alpha'
            },
            'Profile':{
                'original':{
                    'description':'Full size image. No resize.',
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                },
            },
        },
        'png':{
            'container':'image',
            'default':{
                'profile':'normal',
                'volume':'alpha'
            },
            'Profile':{
                'original':{
                    'description':'Full size image. No resize.',
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                },
                'normal':{
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                    'transcode':{
                        'aspect ratio':'preserve',
                        'size':1024,
                        'constraint':'max',
                    },
                },
                'criterion':{
                    'default':{
                        10:{'volume':'alpha'},
                        9:{'volume':'alpha'},
                    },
                    'transcode':{
                        'aspect ratio':'preserve',
                        'size':1024,
                        'constraint':'min'
                    },
                },
            },
        },
        'ac3':{
            'container':'raw audio',
            'default':{
                'profile':'original',
                'volume':'epsilon',
            },
            'Profile':{
                'original':{
                    'description':'Special profile for ac3 track from dts',
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'transcode':{
                        'audio':(
                            {
                                'from': {'codec':'DTS', 'type':'audio', 'channels':6},
                                'to': {'-ab':640},
                            },
                            {
                                'from': {'codec':'DTS', 'type':'audio', 'channels':5},
                                'to': {'-ab':640},
                            },
                            {
                                'from': {'codec':'DTS', 'type':'audio', 'channels':4},
                                'to': {'-ab':640},
                            },
                            {
                                'from': {'codec':'DTS', 'type':'audio', 'channels':3},
                                'to': {'-ab':448},
                            },
                            {
                                'from': {'codec':'DTS', 'type':'audio', 'channels':2},
                                'to': {'-ab':256},
                            },
                            {
                                'from': {'codec':'DTS', 'type':'audio', 'channels':1},
                                'to': {'-ab':192},
                            },
                        ),
                    }
                }
            },
        },
        'dts':{
            'container':'raw audio',
            'default':{
                'profile':'dump',
                'volume':'epsilon',
            },
            'Profile':{
                'dump':{
                    'description':'Special profile for dts track exctracted from matroska',
                    'default':{
                        10:{'volume':'epsilon'},
                        9:{'volume':'epsilon'},
                    },
                    'extract':{
                        'tracks':(
                            {'type':'audio', 'codec':'DTS'},
                        ),
                    },
                },
            },
        },
    },
}

subtitle_config = {
    'punctuation':{
        'scope':'line',
        'action':'replace',
        'case':'sensitive',
        'expression':(
            (r'^[-?\.,!:;"\'\s]+(.*)$', '\\1'),
            (r'^(.*)[-?\.,!:;"\'\s]+$', '\\1'),
        ),
    },
    'leftover':{
        'scope':'line',
        'action':'drop',
        'case':'insensitive',
        'expression':(
            ur'^\([^\)]+\)$',
            ur'^[\[\]\(\)]*$',
            ur'^[-?\.,!:;"\'\s]*$',
        ),
    },
    'hebrew noise':{
        'scope':'block',
        'action':'drop',
        'case':'insensitive',
        'expression':(
            ur':סנכרון',
            ur':תרגום',
            ur':שיפוץ',
            ur':לפרטים',
            ur'סונכרן',
            ur'תורגם על ידי',
            ur'תורגם חלקית',
            ur'סנכרן לגרסה זו',
            ur'תורגם ע"י',
            ur'שופץ ע"י',
            ur'תורגם משמיעה',
            ur'קריעה וסינכרון',
            ur'תוקן על ידי',
            ur'תורגם על-ידי',
            ur'תורגם ע"י',
            ur'תוקן ע"י',
            ur'הובא והוכן ע"י',
            ur'תורגם וסוכנרן',
            ur'תורגם וסונכרן',
            ur'תוקן קלות ע"י',
            ur'תרגום זה בוצע על ידי',
            ur'סונכרן לגירסא זו ע"י',
            ur'תרגום זה נעשה על ידי',
            ur'תורגם עם הרבה זיעה על ידי',
            ur'תורגם מספרדית ע"י אסף פארי',
            ur'כתוביות ע"י',
            ur'הגהה וסנכרון ע"י',
            ur'שנוכל להמשיך לתרגם',
            ur'הפרק מוקדש',
            ur'מצוות טורק',
            ur'shayx ע"י',
            ur'pusel :סנכרון',
            ur'תרגום: רותם ושמעון',
            ur'שיפוץ: השייח\' הסעודי',
            ur'שופץ ע"י השייח\' הסעודי',
            ur'תרגום: שמעון ורותם אברג\'יל',
            ur'כתובית זו הובאה',
            ur'שופצה, נערכה וסונכרנה לגרסה זו',
            ur'ברוכה הבאה אלוירה',
            ur'לצוות מתרגמי האוס',
            ur'אלוירה ברוכה הבאה',
            ur'עמוס נמני',
            ur'אינדיאנית שלי',
            ur'יומולדת שמח',
            ur'מוקדש לך',
            ur'מונחים רפואיים - ג\'ון דו',
            ur'מפורום תפוז',
            ur'מוקדש לפולי שלי',
            ur':כתוביות',
            ur'^בלעדית עבור$',
            ur'הורד מהאתר',
            ur'על ההגהה workbook',
            ur'מוקדש לכל אוהבי האוס אי שם',
            ur'theterminator נערך ותוקן בשיתוף עם',
            ur'התרגום נעשה על ידי המוריד',
            ur'תורגם וסונוכרן משמיעה ע"י',
            ur'\bצפייה מהנה\b',
            ur'\bצפיה מהנה\b',
            ur'נקרע ותוקן',
            ur'אבי דניאלי',
            ur'אוהבים את התרגומים שלנו',
            ur'נקלענו למאבק',
            ur'משפטי מתמשך',
            ur'לבילד המתקשה בהבנת קרדיטים',
            ur'אנא תרמו לנו כדי',
            ur'הגהה על-ידי',
            ur'^עריכה לשונית$',
            ur'^white fang-תרגום: עמית יקיר ו$',
            ur'ערן טלמור',
            ur'\bעדי-בלי-בצל\b',
            ur'\bבקרו אותנו בפורום\b',
            ur'הודה בוז',
            ur'\b-תודה מיוחדת ל\b',
            ur'^extreme מקבוצת$',
            ur'ialfan-ו mb0:עברית',
            ur'י ביצה קשה',
            ur'^ב$',
            ur'^בי$',
            ur'^ביצ$',
            ur'^ביצה$',
            ur'^ביצה ק$',
            ur'^ביצה קש$',
            ur'^ביצה קשה$',
            ur'ליונהארט',
            ur'\bמצוות פושל\b',
            ur'\bassem נקרע ע"י\b',
            ur'\bkawa: סנכרון\b',
            ur'אוהבת לנצח, שרון',
        ),
    },
    'noise':{
        'scope':'block',
        'action':'drop',
        'case':'insensitive',
        'expression':(
            ur'www\.allsubs\.org',
            ur'\bswsub\b',
            ur'\bresync\b',
            ur'\b[a-za-z0-9\.]+@gmail.\s*com\b',
            ur'cync\sby\slanmao',
            ur'www\.1000fr\.com',
            ur'www\.tvsubtitles\.net',
            ur'ytet-vicky8800',
            ur'www\.ydy\.com',
            ur'sync:gagegao',
            ur'frm-lanma',
            ur'nowa\swizja',
            ur'ssmink',
            ur'\blinx\b',
            ur'torec',
            ur'\byanx26\b',
            ur'\bgreenscorpion\b',
            ur'\bneotrix\b',
            ur'\bglfinish\b',
            ur'\bshloogy\b',
            ur'\.co\.il',
            ur'\by0natan\b',
            ur'\belad\b',
            ur'sratim',
            ur'donkey cr3w',
            ur'r-subs',
            ur'\[d-s\]',
            ur'ponkoit',
            ur'\bsubbie\b',
            ur'\bxsesa\b',
            ur'napisy pobrane',
            ur'\bphaelox\b',
            ur'divxstation',
            ur'\bpetabit\b',
            ur'\bronkey\b',
            ur'chococat3@walla',
            ur'warez',
            ur'\bdrsub\b',
            ur'\beliavgold\b',
            ur'^elvira$',
            ur'\blob93\b',
            ur'\belvir\b',
            ur'\boofir\b',
            ur'\bkrok\b',
            ur'\bqsubd\b',
            ur'\bariel046\b',
            ur'\bzipc\b',
            ur'\btecnodrom\b',
            ur'visiontext subtitles',
            ur'english sdh',
            ur'srulikg',
            ur'lh translators team',
            ur'[-=\s]+sub-zero[-=\s]+',
            ur'lionetwork',
            ur'^eric$',
            ur'subz3ro',
            ur'^david-z$',
            ur'drziv@yahoo',
            ur'elran_o',
            ur'mcsnagel',
            ur'\boutwit\b',
            ur'^gimly$',
            ur'\btinyurl\b',
            ur'\bfoxriver\b',
            ur'\bextremesubs\b',
            ur'megalomania tree',
            ur'xmonwow',
            ur'\bciwan\b',
            ur'\bnata4ever\b',
            ur'\byosefff\b',
            ur'\bhentaiman\b',
            ur'\bfoxi9\b',
            ur'\bgamby\b',
            ur'\bbrassica nigra\b',
            ur'\bqsubs\b',
            ur'\bsharetw\b',
            ur'\bserethd\b',
            ur'hazy7868',
            ur'subscenter\.org'
            ur'\blakota\b',
            ur'\bnzigi\b'
            ur'\bqwer90\b',
            ur'roni_eliav',
            ur'subscenter',
            ur'\bkuniva\b',
            ur'hdbits.org',
            ur'addic7ed',
            ur'hdsubs',
        ),
    },
    'typo':{
        'scope':'line',
        'action':'replace',
        'case':'sensitive',
        'expression':(
            (r'\b +(,|\.|\?|%|!)\b', '\\1 '),
            (r'\b(,|\.|\?|%|!) +\b', '\\1 '),
            (r'\.\s*\.\s*\.\.?', '...'),
            (r'</?[a-z]+/?>', ''),
            (r'\'{2}', '"'),
            (r'\s+\)', ')'),
            (r'\(\s+', '('),
            (r'\s+\]', ']'),
            (r'\[\s+', '['),
            (r'\[[^\]]+\]\s*', ''),
            (r'^[^\]]+\]', ''),
            (r'\[[^\]]+$', ''),
            (r'\([#a-zA-Z0-9l\s]+\)', ''),
            (r'\([#a-zA-Z0-9l\s]+$', ''),
            (r'^[#a-zA-Z0-9l\s]+\)', ''),
            (r'^[-\s]+', ''),
            (r'[-\s]+$', ''),
            (r'\b^[-A-Z\s]+[0-9]*:\s*', ''),
            (r'(?<=[a-zA-Z\'])I', 'l'),
            (r'^[-\s]*$', ''),
        ),
    },
    'english typo':{
        'scope':'line',
        'action':'replace',
        'case':'sensitive',
        'expression':(
            (r'♪', ''),
            (r'¶', ''),
            (r'Theysaid', 'They said'),
            (r'\bIast\b', 'last'),
            (r'\bIook\b', 'look'),
            (r'\bIetting\b', 'letting'),
            (r'\bIet\b', 'let'),
            (r'\bIooking\b', 'looking'),
            (r'\bIife\b', 'life'),
            (r'\bIeft\b', 'left'),
            (r'\bIike\b', 'like'),
            (r'\bIittle\b', 'little'),
            (r'\bIadies\b', 'ladies'),
            (r'\bIearn\b', 'learn'),
            (r'\bIanded\b', 'landed'),
            (r'\bIocked\b', 'locked'),
            (r'\bIie\b', 'lie'),
            (r'\bIong\b', 'long'),
            (r'\bIine\b', 'line'),
            (r'\bIives\b', 'lives'),
            (r'\bIeave\b', 'leave'),
            (r'\bIawyer\b', 'lawyer'),
            (r'\bIogs\b', 'logs'),
            (r'\bIack\b', 'lack'),
            (r'\bIove\b', 'love'),
            (r'\bIot\b', 'lot'),
            (r'\bIanding\b', 'landing'),
            (r'\bIet\'s\b', 'let\'s'),
            (r'\bIand\b', 'land'),
            (r'\bIying\b', 'lying'),
            (r'\bIist\b', 'list'),
            (r'\bIoved\b', 'loved'),
            (r'\bIoss\b', 'loss'),
            (r'\bIied\b', 'lied'),
            (r'\bIaugh\b', 'laugh'),
            (r'\b(h|H)avert\b', '\\1aven\'t'),
            (r'\b(w|W)asrt\b', '\\1asn\'t'),
            (r'\b(d|D)oesrt\b', '\\1oesn\'t'),
            (r'\b(d|D)ort\b', '\\1on\'t'),
            (r'\b(d|D)idrt\b', '\\1idn\'t'),
            (r'\b(a|A)irt\b', '\\1in\'t'),
            (r'\b(i|I)srt\b', '\\1sn\'t'),
            (r'\b(w|W)ort\b', '\\1on\'t'),
            (r'\b(c|C|w|W|s|S)ouldrt\b', '\\1ouldn\'t'),
            (r'\barert\b', 'aren\'t'),
            (r'\bls\b', 'Is'),
            (r'\b(L|l)f\b', 'If'),
            (r'\blt\b', 'It'),
            (r'\blt\'s\b', 'It\'s'),
            (r'\bl\'m\b', 'I\'m'),
            (r'\bl\'ll\b', 'I\'ll'),
            (r'\bl\'ve\b', 'I\'ve'),
            (r'\bl\b', 'I'),
            (r'\bln\b', 'In'),
            (r'\blmpossible\b', 'Impossible'),
            (r'\bIight\b', 'light'),
            (r'\bIevitation\b', 'levitation'),
            (r'\bIeaving\b', 'leaving'),
            (r'\bIooked\b', 'looked'),
            (r'\bIucky\b', 'lucky'),
            (r'\bIuck\b', 'luck'),
            (r'\bIater\b', 'later'),
            (r'\bIift\b', 'lift'),
            (r'\bIip\b', 'lip'),
            (r'\bIooks\b', 'looks'),
            (r'\bIaid\b', 'laid'),
            (r'\bIikely\b', 'likely'),
            (r'\bIow\b', 'low'),
            (r'\bIeast\b', 'least'),
            (r'\bIeader\b', 'leader'),
            (r'\bIocate\b', 'locate'),
            (r'\bIaw\b', 'law'),
            (r'\bIately\b', 'lately'),
            (r'\bIiar\b', 'liar'),
            (r'\bIate\b', 'late'),
            (r'\bIonger\b', 'longer'),
            (r'\bIive\b', 'live'),
        ),
    },
}

base_config = {
    'tvshow':(
        # TV Show map
        # The initial TVDB TV Show id map
        (79501, u'heroes'),
        (75930, u'alias'),
        (76290, u'24'),
        (73800, u'desperate housewives'),
        (79349, u'dexter'),
        (73871, u'futurama'),
        (73255, u'house'),
        (73739, u'lost'),
        (79169, u'seinfeld'),
        (75299, u'the sopranos'),
        (73762, u'greys anatomy'),
        (79126, u'the wire'),
        (75164, u'samurai jack'),
        (74543, u'entourage'),
        (85527, u'yellowstone'),
        (79257, u'planet earth'),
        (74845, u'weeds'),
        (75450, u'six feet under'),
        (80252, u'flight of the conchords'),
        (82066, u'fringe'),
        (80337, u'mad men'),
        (73508, u'rome'),
        (77398, u'the x files'),
        (70682, u'oz'),
        (77526, u'star trek'),
        (77231, u'mission impossible'),
        (83268, u'star wars the clone wars'),
        (74805, u'the prisoner'),
        (85242, u'the prisoner 2009'),
        (83602, u'lie to me'),
        (80349, u'californication'),
        (82109, u'generation kill'),
        (70533, u'twin peaks'),
        (72628, u'the singing detective'),
        (80593, u'dirty sexy money'),
        (79177, u'life on mars uk'),
        (82289, u'life on mars us'),
        (118421, u'life bbc'),
        (130421, u'faces of earth'),
        (147071, u'wonders of the solar system'),
        (108611, u'white collar'),
        (85149, u'berlin alexanderplatz'),
        (94971, u'v 2009'),
        (82459, u'the mentalist'),
        (82283, u'true blood'),
        (79488, u'30 rock'),
        (74205, u'band of brothers'),
        (124561, u'world war 2 in high definition'),
        (81189, u'breaking bad'),
        (71663, u'the simpsons'),
        (85040, u'caprica'),
    ),
}


class Configuration(object):
    def __init__(self):
        self.options = None
        self.property = media_property
        self.repository = repository_config
        self.subtitle = subtitle_config
        self.property_map = {}
        
        self.locate_commands()
        self.load_default()
    
    
    def load_default(self):
        self.build_property_map()
        
        self.track_with_language = ('audio', 'subtitles', 'video')
        self.kind_with_language = self.property_map['container']['subtitles']['kind'] + self.property_map['container']['raw audio']['kind']
        self.supported_media_kind = [ mk for mk in self.property['stik'] if 'schema' in mk ]
        self.available_profiles = []
        for v in self.repository['Kind'].values():
            self.available_profiles.extend(v['Profile'].keys())
        self.available_profiles = tuple(set(self.available_profiles))
    
    
    def build_property_map(self):
        for key in ('name', 'mediainfo', 'mp4info'):
            if key not in self.property_map:
                self.property_map[key] = {}
            
            # Build file and tag propery map
            for block in ('file', 'tag'):
                if block not in self.property_map[key]:
                    self.property_map[key][block] = {}
                    
                for p in self.property[block]:
                    if key in p and p[key] is not None:
                        self.property_map[key][block][p[key]] = p
            
            # Build track property map
            self.property_map[key]['track'] = {}
            for block in ('audio', 'video', 'text', 'image'):
                if block not in self.property_map[key]['track']:
                    self.property_map[key]['track'][block] = {}
                for p in self.property['track']['common']:
                    if key in p and p[key] is not None:
                        self.property_map[key]['track'][block][p[key]] = p
                    
                for p in self.property['track'][block]:
                    if key in p and p[key] is not None:
                        self.property_map[key]['track'][block][p[key]] = p
        
        # Build itunemovi plist properties map
        for key in ('name', 'plist'):
            if key not in self.property_map:
                self.property_map[key] = {}
            self.property_map[key]['itunemovi'] = {}
            for p in self.property['itunemovi']:
                self.property_map[key]['itunemovi'][p[key]] = p
        
        # Build special iTunes atom map
        for key in ('name', 'code'):
            if key not in self.property_map:
                self.property_map[key] = {}
            for block in ('stik', 'sfID', 'rtng', 'akID', 'gnre'):
                if block not in self.property_map[key]:
                    self.property_map[key][block] = {}
                for p in self.property[block]:
                    self.property_map[key][block][p[key]] = p
        
        # Build language code map
        for key in ('name', 'iso3t', 'iso3b', 'iso2'):
            if key not in self.property_map:
                self.property_map[key] = {}
            self.property_map[key]['language'] = {}
            for p in self.property['language']:
                if key in p:
                    self.property_map[key]['language'][p[key]] = p
        
        # Build container kind map
        self.property_map['container'] = {}
        for c in tuple(set([ v['container'] for k,v in self.repository['Kind'].iteritems() ])):
            self.property_map['container'][c] = {'kind':[ k for (k,v) in self.repository['Kind'].iteritems() if v['container'] == c ]}
            
        # Build volume map
        self.property_map['volume'] = {}
        for k,v in self.repository['Volume'].iteritems():
            v['realpath'] = os.path.realpath(v['path'])
            alt = []
            alt.append(v['path'])
            alt.append(v['realpath'])
            alt.extend(v['alternative'])
            alt = tuple(set(alt))
            for p in alt:
                self.property_map['volume'][p] = v
    
    
    def locate_commands(self):
        for c in self.repository['Command']:
            command = ['which', self.repository['Command'][c]['binary']]
            proc = Popen(command, stdout=PIPE, stderr=PIPE)
            report = proc.communicate()
            if report[0]:
                self.repository['Command'][c]['path'] = report[0].splitlines()[0]
            else:
                result = False
                self.repository['Command'][c]['path'] = None
    
    


# singleton
theConfiguration = Configuration()
