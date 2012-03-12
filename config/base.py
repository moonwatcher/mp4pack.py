# -*- coding: utf-8 -*-

base = {
    'system':{
        'home':'/usr/local/etc/mpk',
        'domain':None,
        'host':None,
        'threads':2,
        'language':'en',
    },
    'display':{
        'wrap':120, 
        'indent':30, 
        'margin':0, 
    },
    'hd threshold':720,
    'playback':{
        'width':1920,
        'height':1080,
        'aspect ratio':float(1920.0 / 1080.0)
    },
    'subtitles':{
        'filters':{
            'punctuation':{
                'scope':'line',
                'action':'replace',
                'ignore case':False,
                'expression':(
                    (ur'^[-?\.,!:;"\'\s]+(.*)$', '\\1'),
                    (ur'^(.*)[-?\.,!:;"\'\s]+$', '\\1'),
                ),
            },
            'leftover':{
                'scope':'line',
                'action':'drop',
                'ignore case':True,
                'expression':(
                    ur'^\([^\)]+\)$',
                    ur'^[\[\]\(\)]*$',
                    ur'^[-?\.,!:;"\'\s]*$',
                ),
            },
            'hebrew noise':{
                'scope':'slide',
                'action':'drop',
                'ignore case':True,
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
                'scope':'slide',
                'action':'drop',
                'ignore case':True,
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
                    ur'corrected by elderman',
                ),
            },
            'typo':{
                'scope':'line',
                'action':'replace',
                'ignore case':False,
                'expression':(
                    (ur'♪', ''),
                    (ur'¶', ''),
                    (ur'\b +(,|\.|\?|%|!)\b', '\\1 '),
                    (ur'\b(,|\.|\?|%|!) +\b', '\\1 '),
                    (ur'\.\s*\.\s*\.\.?', '...'),
                    (ur'</?[^>]+/?>', ''),
                    (ur'\'{2}', '"'),
                    (ur'\s+\)', ')'),
                    (ur'\(\s+', '('),
                    (ur'\s+\]', ']'),
                    (ur'\[\s+', '['),
                    (ur'\[[^\]]+\]\s*', ''),
                    (ur'^[^\]]+\]', ''),
                    (ur'\[[^\]]+$', ''),
                    (ur'\([#a-zA-Z0-9l\s]+\)', ''),
                    (ur'\([#a-zA-Z0-9l\s]+$', ''),
                    (ur'^[#a-zA-Z0-9l\s]+\)', ''),
                    (ur'^[-\s]+', ''),
                    (ur'[-\s]+$', ''),
                    (ur'\b^[-A-Z\s]+[0-9]*:\s*', ''),
                    (ur'(?<=[a-zA-Z\'])I', 'l'),
                    (ur'^[-\s]*$', ''),
                ),
            },
            'english typo':{
                'scope':'line',
                'action':'replace',
                'ignore case':False,
                'expression':(
                    (ur'Theysaid', u'They said'),
                    (ur'\bIast\b', u'last'),
                    (ur'\bIook\b', u'look'),
                    (ur'\bIetting\b', u'letting'),
                    (ur'\bIet\b', u'let'),
                    (ur'\bIooking\b', u'looking'),
                    (ur'\bIife\b', u'life'),
                    (ur'\bIeft\b', u'left'),
                    (ur'\bIike\b', u'like'),
                    (ur'\bIittle\b', u'little'),
                    (ur'\bIadies\b', u'ladies'),
                    (ur'\bIearn\b', u'learn'),
                    (ur'\bIanded\b', u'landed'),
                    (ur'\bIocked\b', u'locked'),
                    (ur'\bIie\b', u'lie'),
                    (ur'\bIong\b', u'long'),
                    (ur'\bIine\b', u'line'),
                    (ur'\bIives\b', u'lives'),
                    (ur'\bIeave\b', u'leave'),
                    (ur'\bIawyer\b', u'lawyer'),
                    (ur'\bIogs\b', u'logs'),
                    (ur'\bIack\b', u'lack'),
                    (ur'\bIove\b', u'love'),
                    (ur'\bIot\b', u'lot'),
                    (ur'\bIanding\b', u'landing'),
                    (ur'\bIet\'s\b', u'let\'s'),
                    (ur'\bIand\b', u'land'),
                    (ur'\bIying\b', u'lying'),
                    (ur'\bIist\b', u'list'),
                    (ur'\bIoved\b', u'loved'),
                    (ur'\bIoss\b', u'loss'),
                    (ur'\bIied\b', u'lied'),
                    (ur'\bIaugh\b', u'laugh'),
                    (ur'\b(h|H)avert\b', u'\\1aven\'t'),
                    (ur'\b(w|W)asrt\b', u'\\1asn\'t'),
                    (ur'\b(d|D)oesrt\b', u'\\1oesn\'t'),
                    (ur'\b(d|D)ort\b', u'\\1on\'t'),
                    (ur'\b(d|D)idrt\b', u'\\1idn\'t'),
                    (ur'\b(a|A)irt\b', u'\\1in\'t'),
                    (ur'\b(i|I)srt\b', u'\\1sn\'t'),
                    (ur'\b(w|W)ort\b', u'\\1on\'t'),
                    (ur'\b(c|C|w|W|s|S)ouldrt\b', u'\\1ouldn\'t'),
                    (ur'\barert\b', u'aren\'t'),
                    (ur'\bls\b', u'Is'),
                    (ur'\b(L|l)f\b', u'If'),
                    (ur'\blt\b', u'It'),
                    (ur'\blt\'s\b', u'It\'s'),
                    (ur'\bl\'m\b', u'I\'m'),
                    (ur'\bl\'ll\b', u'I\'ll'),
                    (ur'\bl\'ve\b', u'I\'ve'),
                    (ur'\bl\b', u'I'),
                    (ur'\bln\b', u'In'),
                    (ur'\blmpossible\b', u'Impossible'),
                    (ur'\bIight\b', u'light'),
                    (ur'\bIevitation\b', u'levitation'),
                    (ur'\bIeaving\b', u'leaving'),
                    (ur'\bIooked\b', u'looked'),
                    (ur'\bIucky\b', u'lucky'),
                    (ur'\bIuck\b', u'luck'),
                    (ur'\bIater\b', u'later'),
                    (ur'\bIift\b', u'lift'),
                    (ur'\bIip\b', u'lip'),
                    (ur'\bIooks\b', u'looks'),
                    (ur'\bIaid\b', u'laid'),
                    (ur'\bIikely\b', u'likely'),
                    (ur'\bIow\b', u'low'),
                    (ur'\bIeast\b', u'least'),
                    (ur'\bIeader\b', u'leader'),
                    (ur'\bIocate\b', u'locate'),
                    (ur'\bIaw\b', u'law'),
                    (ur'\bIately\b', u'lately'),
                    (ur'\bIiar\b', u'liar'),
                    (ur'\bIate\b', u'late'),
                    (ur'\bIonger\b', u'longer'),
                    (ur'\bIive\b', u'live'),
                ),
            },
        }
    },
    'report':{
        'full':{
            'file':(
                'size',
                'duration',
                'bit rate',
                'encoding',
                'modified date',
                'encode date',
                'tag date',
                'extension',
                'format',
            ),
            'tag':(
                'language',
                'profile',
                'volume',
                'imdb id',
                'kind',
                'tv show key',
                'name',
                'artist',
                'album artist',
                'album',
                'grouping',
                'composer',
                'comment',
                'genre type',
                'genre',
                'release date',
                'tempo',
                'compilation',
                'tv show',
                'tv episode id',
                'tv season',
                'tv episode',
                'tv network',
                'sort name',
                'sort artist',
                'sort album artist',
                'sort album',
                'sort composer',
                'sort tv show',
                'description',
                'long description',
                'lyrics',
                'copyright',
                'encoding tool',
                'encoded by',
                'purchase date',
                'podcast',
                'podcast url',
                'keywords',
                'category',
                'hd video',
                'gapless',
                'xid',
                'itunes content id',
                'itunes account',
                'itunes artist id',
                'itunes composer id',
                'itunes playlist id',
                'itunes genre id',
                'itunes country id',
                'itunes account type',
                'episode global id',
                'media kind',
                'content rating',
                'itunextc',
                'itunmovi',
                'cast',
                'directors',
                'codirectors',
                'producers',
                'screenwriters',
                'studio',
                'rating standard',
                'rating',
                'rating score',
                'rating annotation',
                'track #',
                'disk #',
                'track position',
                'track total',
                'disk position',
                'disk total',
                'cover',
            ),
            'track':{
                'audio':(
                    'type',
                    'track id',
                    'position',
                    'codec',
                    'codec profile',
                    'duration',
                    'bit rate',
                    'bit rate mode',
                    'bit depth',
                    'stream size',
                    'language',
                    'encoded date',
                    'name',
                    'delay',
                    'channel configuration',
                    'channels',
                    'channel position',
                    'sample rate',
                    'sample count',
                    'dialnorm',
                ),
                'video':(
                    'type',
                    'track id',
                    'position',
                    'codec',
                    'codec profile',
                    'duration',
                    'bit rate',
                    'bit rate mode',
                    'bit depth',
                    'stream size',
                    'language',
                    'encoded date',
                    'name',
                    'delay',
                    'width',
                    'height',
                    'pixel aspect ratio',
                    'display aspect ratio',
                    'frame rate mode',
                    'frame rate',
                    'frame rate minimum',
                    'frame rate maximum',
                    'frame count',
                    'color space',
                    'bpf',
                    'encoder',
                    'encoder settings',
                ),
                'text':(
                    'type',
                    'track id',
                    'position',
                    'codec',
                    'codec profile',
                    'duration',
                    'bit rate',
                    'bit rate mode',
                    'bit depth',
                    'stream size',
                    'language',
                    'encoded date',
                    'name',
                    'delay',
                ),
                'image':(
                    'type',
                    'track id',
                    'position',
                    'codec',
                    'codec profile',
                    'duration',
                    'bit rate',
                    'bit rate mode',
                    'bit depth',
                    'stream size',
                    'language',
                    'encoded date',
                    'name',
                    'delay',
                    'width',
                    'height',
                )
            },
        },
        'normal':{
            'file':(
                'size',
                'duration',
                'bit rate',
                'encoding',
                'modified date',
            ),
            'tag':(
                'kind',
                'media kind',
                'name',
                'language',
                'tv show',
                'tv season',
                'tv episode',
                'tv network',
                'cast',
                'directors',
                'codirectors',
                'producers',
                'screenwriters',
                'studio',
                'rating',
                'content rating',
                'genre type',
                'genre',
                'release date',
                'lyrics',
                'hd video',
                'imdb id',
                'description',
                'long description',
            ),
            'track':{
                'audio':(
                    'type',
                    'language',
                    'codec',
                    'codec profile',
                    'bit rate',
                    'stream size',
                    'channels',
                ),
                'video':(
                    'type',
                    'language',
                    'codec',
                    'codec profile',
                    'bit rate',
                    'stream size',
                    'width',
                    'height',
                    'pixel aspect ratio',
                    'display aspect ratio',
                    'frame rate',
                    'bpf',
                ),
                'text':(
                    'type',
                    'language',
                    'codec',
                    'codec profile',
                    'bit rate',
                    'stream size',
                ),
                'image':(
                    'type',
                    'language',
                    'codec',
                    'codec profile',
                    'bit rate',
                    'stream size',
                    'width',
                    'height',
                )
            },
        },
    }
}
