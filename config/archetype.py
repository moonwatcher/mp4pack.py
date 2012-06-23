# -*- coding: utf-8 -*-

{
    'archetype':{
        'character encoding':{
            'name':u'Character encoding',
            'keyword':u'character_encoding',
            'type':'unicode',
        },
        'url':{
            'name':u'URL',
            'keyword':u'url',
            'type':'unicode',
        },
        'scheme':{
            'name':u'Scheme',
            'keyword':u'scheme',
            'type':'unicode',
        },
        'domain':{
            'name':u'Domain',
            'keyword':u'domain',
            'type':'unicode',
        },
        'host':{
            'name':u'Host',
            'keyword':u'host',
            'type':'unicode',
        },
        'port':{
            'name':u'Port',
            'keyword':u'port',
            'type':'int',
        },
        'path':{
            'name':u'Path',
            'keyword':u'path',
            'type':'unicode',
        },
        'path digest':{
            'name':u'Path SHA1',
            'keyword':u'path_digest',
            'type':'unicode',
        },
        'directory':{
            'name':u'Directory',
            'keyword':u'directory',
            'type':'unicode',
        },
        'file name':{
            'name':u'File name',
            'keyword':u'file_name',
            'type':'unicode',
        },
        'path in cache':{
            'name':u'Path in cache',
            'keyword':u'path_in_cache',
            'type':'unicode',
        },
        'exploded path':{
            'name':u'Exploded path',
            'keyword':u'exploded_path',
            'type':'unicode',
        },
        'file size':{
            'name':u'File size',
            'keyword':u'file_size',
            'type':'int',
            'format':'byte',
        },
        'preset':{
            'name':u'Preset',
            'keyword':u'Preset',
            'type':'unicode'
        },
        'profile':{
            'name':u'Profile',
            'keyword':u'profile',
            'type':'unicode'
        },
        'volume':{
            'name':u'Volume',
            'keyword':u'volume',
            'type':'unicode'
        },
        'volume path':{
            'name':u'Volume path',
            'keyword':u'volume_path',
            'type':'unicode'
        },
        'kind':{
            'name':u'Kind',
            'keyword':u'kind',
            'type':'unicode',
        },
        'tvdb tv show id':{
            'name':u'TVDb TV show ID',
            'keyword':u'tvdb_tv_show_id',
            'type':'int',
        },
        'tvdb tv season id':{
            'name':u'TVDb TV season ID',
            'keyword':u'tvdb_tv_season_id',
            'type':'int',
        },
        'tvdb tv episode id':{
            'name':u'TVDb TV episode ID',
            'keyword':u'tvdb_tv_episode_id',
            'type':'int',
        },
        'tvdb person id':{
            'name':u'TVDb person ID',
            'keyword':u'tvdb_person_id',
            'type':'int',
        },
        'tvdb image id':{
            'name':u'TVDb image ID',
            'keyword':u'tvdb_image_id',
            'type':'int',
        },
        'imdb tv show id':{
            'name':u'IMDb TV show ID',
            'keyword':u'imdb_tv_show_id',
            'type':'unicode',
        },
        'imdb tv episode id':{
            'name':u'IMDb TV episode ID',
            'keyword':u'imdb_tv_episode_id',
            'type':'unicode',
        },
        'imdb movie id':{
            'name':u'IMDb movie ID',
            'keyword':u'imdb_movie_id',
            'type':'unicode'
        },
        'trimmed imdb movie id':{
            'name':u'Trimmed IMDb movie ID',
            'keyword':u'trimmed_imdb_movie_id',
            'type':'unicode'
        },
        'tmdb movie id':{
            'name':u'TMDb movie ID',
            'keyword':u'tmdb_movie_id',
            'type':'int',
        },
        'tmdb collection id':{
            'name':u'TMDb collection ID',
            'keyword':u'tmdb_collection_id',
            'type':'int'
        },
        'tmdb person id':{
            'name':u'TMDb person ID',
            'keyword':u'tmdb_person_id',
            'type':'int',
        },
        'tmdb company id':{
            'name':u'TMDb company ID',
            'keyword':u'tmdb_company_id',
            'type':'int',
        },
        'tmdb genre id':{
            'name':u'TMDb genre ID',
            'keyword':u'tmdb_genre_id',
            'type':'int',
        },
        'tmdb keyword id':{
            'name':u'TMDb keyword ID',
            'keyword':u'tmdb_keyword_id',
            'type':'int',
        },
        'rottentomatoes movie id':{
            'name':u'Rotten tomatoes movie ID',
            'keyword':u'rottentomatoes_movie_id',
            'type':'int',
        },
        'zap2it tv show id':{
            'name':u'Zap2It TV show ID',
            'keyword':u'zap2it_tv_show_id',
            'type':'unicode',
        },
        'simple name':{
            'name':u'Simple name',
            'keyword':u'simple_name',
            'type':'unicode',
            'simplify':True,
        },
        'movie handle':{
            'name':u'Movie handle',
            'keyword':u'movie_handle',
            'type':'unicode',
            'simplify':True,
        },
        'album handle':{
            'name':u'Album handle',
            'keyword':u'album_handle',
            'type':'unicode',
            'simplify':True,
        },
        'tv show handle':{
            'name':u'TV show handle',
            'keyword':u'tv_show_handle',
            'type':'unicode',
            'simplify':True,
        },
        'keywords':{
            'name':u'Keywords',
            'keyword':u'keywords',
            'type':'unicode',
            'plural':'list',
        },
        'tv show runtime':{
            'name':u'TV show runtime',
            'keyword':u'tv_show_runtime',
            'type':'int',
        },
        'tv show status':{
            'name':u'TV show status',
            'keyword':u'tv_show_status',
            'type':'unicode',
        },
        'vote average':{
            'name':u'Vote average',
            'keyword':u'vote_average',
            'type':'float',
        },
        'vote count':{
            'name':'Vote count',
            'keyword':u'vote_count',
            'type':'int',
        },
        'language':{
            'name':u'Language',
            'keyword':u'language',
            'type':'enum',
            'enumeration':'language',
        },
        'media kind':{
            'name':u'Media kind',
            'keyword':u'media_kind',
            'type':'enum',
            'atom':'stik',
            'enumeration':'media kind',
        },
        'name':{
            'name':u'Name',
            'keyword':u'name',
            'type':'unicode',
            'atom':'©nam',
        },
        'artist':{
            'name':u'Artist',
            'keyword':u'artist',
            'type':'unicode',
            'atom':'@ART',
        },
        'composer':{
            'name':u'Composer',
            'keyword':u'composer',
            'type':'unicode',
            'atom':'©wrt',
        },
        'album artist':{
            'name':u'Album artist',
            'description':u'Artist for the whole album, if different than the individual tracks.',
            'keyword':u'album_artist',
            'type':'unicode',
            'atom':'aART',
        },
        'album':{
            'name':u'Album name',
            'keyword':u'album',
            'type':'unicode',
            'atom':'©alb',
        },
        'track number':{
            'name':u'Track number',
            'keyword':u'track_number',
            'type':'unicode',
            'atom':'trkn',
        },
        'disk number':{
            'name':u'Disk number',
            'keyword':u'disk_number',
            'type':'unicode',
            'atom':'disk',
        },
        'track position':{
            'name':u'Track position',
            'keyword':u'track_position',
            'type':'int',
        },
        'track total':{
            'name':u'Track total',
            'keyword':u'track_total',
            'type':'int',
        },
        'disk position':{
            'name':u'Disk position',
            'keyword':u'disk_position',
            'type':'int',
        },
        'disk total':{
            'name':u'Disk total',
            'keyword':u'disk_total',
            'type':'int',
        },
        'grouping':{
            'name':u'Grouping',
            'description':u'Overall work, like TIT1 in ID3',
            'keyword':u'grouping',
            'type':'unicode',
            'atom':'grup',
        },
        'comment':{
            'name':u'User comment',
            'keyword':u'comment',
            'type':'unicode',
            'atom':'©cmt',
        },
        'description':{
            'name':u'Description',
            'keyword':u'description',
            'type':'unicode',
            'atom':'desc',
        },
        'long description':{
            'name':u'Long description',
            'keyword':u'long_description',
            'type':'unicode',
            'atom':'ldes',
        },
        'biography':{
            'name':u'Biography',
            'keyword':u'biography',
            'type':'unicode',
        },
        'place of birth':{
            'name':u'Place of birth',
            'keyword':u'place_of_birth',
            'type':'unicode',
        },
        'lyrics':{
            'name':u'Lyrics',
            'keyword':u'lyrics',
            'type':'unicode',
            'atom':'©lyr',
        },
        'compilation':{
            'name':u'Compilation',
            'description':u'Is disc part of a compilation?',
            'keyword':u'compilation',
            'type':'bool',
            'atom':'cpil',
        },
        'copyright':{
            'name':u'Copyright',
            'keyword':u'copyright',
            'type':'unicode',
            'atom':'cprt',
        },
        'tempo':{
            'name':u'Beats per minute',
            'keyword':u'tempo',
            'type':'int',
            'atom':'tmpo',
        },
        'genre type':{
            'name':u'Pre-defined genre',
            'description':u'Enumerated value from ID3 tag set, plus 1',
            'keyword':u'genre_type',
            'type':'enum',
            'atom':'gnre',
            'enumeration':'genre',
        },
        'genre':{
            'name':u'User genre',
            'keyword':u'genre',
            'type':'unicode',
            'atom':'©gen',
        },
        'gapless':{
            'name':u'Gapless',
            'keyword':u'gapless',
            'type':'bool',
            'atom':'pgap',
        },
        'itunes keywords':{
            'name':u'iTunes keywords',
            'keyword':u'itunes_keywords',
            'type':'unicode',
            'atom':'keyw',
        },
        'itunes category':{
            'name':u'iTunes category',
            'keyword':u'itunes_category',
            'type':'unicode',
            'atom':'catg',
        },
        'hd video':{
            'name':u'HD video',
            'keyword':u'hd_video',
            'type':'int',
            'atom':'hdvd',
        },
        'tv show':{
            'name':u'TV show',
            'keyword':u'tv_show',
            'type':'unicode',
            'atom':'tvsh',
        },
        'track genealogy':{
            'name':u'Track genealogy',
            'keyword':u'track_genealogy',
            'type':'unicode',
        },
        'tv episode id':{
            'name':u'TV episode ID',
            'keyword':u'tv_episode_id',
            'type':'unicode',
            'atom':'tven',
        },
        'tv season':{
            'name':u'TV season',
            'keyword':u'tv_season',
            'type':'int',
            'atom':'tvsn',
        },
        'tv episode':{
            'name':u'TV episode',
            'keyword':u'tv_episode',
            'type':'int',
            'atom':'tves',
        },
        'absolute tv episode':{
            'name':u'Absolute TV episode',
            'keyword':'absolute_tv_episode',
            'type':'int',
        },
        'tv network':{
            'name':u'TV network',
            'keyword':u'tv_network',
            'type':'unicode',
            'atom':'tvnn',
        },
        'sort name':{
            'name':u'Sort name',
            'keyword':u'sort_name',
            'type':'unicode',
            'atom':'sonm',
        },
        'sort artist':{
            'name':u'Sort artist',
            'keyword':u'sort_artist',
            'type':'unicode',
            'atom':'soar',
        },
        'sort composer':{
            'name':u'Sort composer',
            'keyword':u'sort_composer',
            'type':'unicode',
            'atom':'soco',
        },
        'sort album artist':{
            'name':u'Sort album artist',
            'keyword':u'sort_album_artist',
            'type':'unicode',
            'atom':'soaa',
        },
        'sort album':{
            'name':u'Sort album',
            'keyword':u'sort_album',
            'type':'unicode',
            'atom':'soal',
        },
        'sort tv show':{
            'name':u'Sort TV show',
            'keyword':u'sort_tv_show',
            'type':'unicode',
            'atom':'sosn',
        },
        'encoding tool':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':u'Encoding tool',
            'description':u'Software which encoded the recording',
            'keyword':u'encoding_tool',
            'type':'unicode',
            'atom':'©too',
        },
        'encoded by':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':u'Encoded by',
            'description':u'Person or company that encoded the recording',
            'keyword':u'encoded_by',
            'type':'unicode',
            'atom':'@enc',
        },
        'modified date':{
            'name':u'Modified date',
            'keyword':u'modified_date',
            'type':'date',
        },
        'tag date':{
            'name':u'Tag date',
            'keyword':u'tag_date',
            'type':'date',
        },
        'birthday':{
            'name':u'Birthday',
            'keyword':u'birthday',
            'type':'date',
        },
        'deathday':{
            'name':u'Deathday',
            'keyword':u'deathday',
            'type':'date',
        },
        'release date':{
            'name':u'Release date',
            'keyword':u'release_date',
            'type':'date',
            'atom':'©day',
        },
        'purchase date':{
            'name':u'Purchase date',
            'keyword':u'purchase_date',
            'type':'date',
            'atom':'purd',
        },
        'encoded date':{
            'name':u'Encoded date',
            'keyword':u'encoded_date',
            'type':'date',
        },
        'xid':{
            'name':u'iTunes extra ID',
            'keyword':u'xid',
            'type':'unicode',
            'atom':'xid',
        },
        'itunes content id':{
            'name':u'iTunes content ID',
            'keyword':u'itunes_content_id',
            'type':'int',
            'atom':'cnID',
        },
        'itunes account':{
            'name':u'iTunes account ID',
            'keyword':u'itunes_account_id',
            'type':'unicode',
            'atom':'apID',
        },
        'itunes artist id':{
            'name':u'iTunes artist ID',
            'keyword':u'itunes_artist_id',
            'type':'int',
            'atom':'atID',
        },
        'itunes composer id':{
            'name':u'iTunes composer ID',
            'keyword':u'itunes_composer_id',
            'type':'int',
            'atom':'cmID',
        },
        'itunes playlist id':{
            'name':u'iTunes playlist ID',
            'keyword':u'itunes_playlist_id',
            'type':'int',
            'atom':'plID',
        },
        'itunes genre id':{
            'name':u'iTunes genre ID',
            'keyword':u'itunes_genre_id',
            'type':'int',
            'atom':'geID',
        },
        'itunes country id':{
            'name':u'iTunes country ID',
            'keyword':u'itunes_country_id',
            'type':'enum',
            'atom':'sfID',
            'enumeration':'country',
        },
        'itunes account type':{
            'name':u'iTunes account type',
            'keyword':u'itunes_account_type',
            'type':'enum',
            'atom':'akID',
            'enumeration':'itunes account type',
        },
        'itunes episode global id':{
            'name':u'Episode global ID',
            'keyword':u'episode_global_id',
            'type':'int',
            'atom':'egid',
        },
        'podcast':{
            'name':u'Podcast',
            'keyword':u'podcast',
            'type':'bool',
            'atom':'pcst',
        },
        'podcast url':{
            'name':u'Podcast URL',
            'keyword':u'podcast_url',
            'type':'unicode',
            'atom':'purl',
        },
        'content rating':{
            'name':u'Content rating',
            'description':u'Does song have explicit content?',
            'keyword':u'content_rating',
            'type':'enum',
            'atom':'rtng',
            'enumeration':'content rating',
        },
        'itunnorm':{
            'name':u'iTunNORM',
            'description':'Sound Check analysis info',
            'keyword':u'itunnorm',
            'type':'unicode',
            'atom':'iTunNORM',
        },
        'itunextc':{
            'name':u'iTunEXTC',
            'keyword':u'itunextc',
            'type':'unicode',
            'atom':'iTunEXTC',
        },
        'itunmovi':{
            'name':u'iTunMOVI',
            'keyword':u'itunmovi',
            'type':'plist',
            'atom':'iTunMOVI',
        },
        'cast':{
            'name':u'Cast',
            'type':'unicode',
            'keyword':u'cast',
            'plural':'list',
        },
        'directors':{
            'name':u'Directors',
            'keyword':u'directors',
            'type':'unicode',
            'plural':'list',
        },
        'codirectors':{
            'name':u'Codirectors',
            'keyword':u'codirectors',
            'type':'unicode',
            'plural':'list',
        },
        'producers':{
            'name':u'Producers',
            'keyword':u'producers',
            'type':'unicode',
            'plural':'list',
        },
        'screenwriters':{
            'name':u'Screenwriters',
            'keyword':u'screenwriters',
            'type':'unicode',
            'plural':'list',
        },
        'studio':{
            'name':u'Studio',
            'keyword':u'studio',
            'type':'unicode',
            'plural':'list',
        },
        'rating standard':{
            'name':u'Rating standard',
            'keyword':u'rating_standard',
            'type':'unicode',
        },
        'rating':{
            'name':u'Rating',
            'keyword':u'rating',
            'type':'unicode',
        },
        'rating score':{
            'name':u'Rating score',
            'keyword':u'rating_score',
            'type':'int',
        },
        'rating annotation':{
            'name':u'Rating annotation',
            'keyword':u'rating_annotation',
            'type':'unicode',
        },
        'cover':{
            'name':u'Cover art',
            'description':u'One or more cover art images',
            'keyword':u'cover_pieces',
            'type':'int',
            'atom':'covr',
            'auto cast':False,
        },
        'stream name':{
            'name':u'Stream name',
            'keyword':u'stream_name',
            'type':'unicode',
        },
        'stream type':{
            'name':u'Stream type',
            'keyword':u'stream_type',
            'type':'enum',
            'enumeration':'mediainfo stream type',
        },
        'stream kind':{
            'name':u'Stream kind',
            'keyword':u'stream_kind',
            'type':'enum',
            'enumeration':'stream kind',
        },
        'format':{
            'name':u'Format',
            'keyword':u'format',
            'type':'unicode',
        },
        'format profile':{
            'name':u'Format profile',
            'type':'unicode',
            'plural':'list',
        },
        'channel count':{
            'name':u'Channel count',
            'keyword':u'channel_count',
            'type':'int',
            'plural':'list',
        },
        'channel position':{
            'name':u'Channel position',
            'keyword':u'channel_position',
            'type':'unicode',
            'plural':'list',
        },
        'stream id':{
            'name':u'Stream ID',
            'keyword':u'stream_id',
            'type':'int',
        },
        'stream kind position':{
            'name':u'Stream position',
            'keyword':u'stream_kind_position',
            'type':'int',
        },
        'stream size':{
            'name':u'Stream size',
            'keyword':u'stream_size',
            'type':'int',
            'format':'byte',
        },
        'stream portion':{
            'name':u'Stream portion',
            'keyword':u'stream_portion',
            'type':'float',
        },
        'default':{
            'name':u'Default',
            'keyword':u'default',
            'type':'bool',
        },
        'primary':{
            'name':u'Primary',
            'keyword':u'primary',
            'type':'bool',
        },
        'delay':{
            'name':u'Delay',
            'keyword':u'delay',
            'type':'int',
        },
        'bit rate':{
            'name':u'Bit rate',
            'keyword':u'bit_rate',
            'type':'int',
            'format':'bitrate',
        },
        'bit rate mode':{
            'name':u'Bit rate mode',
            'keyword':u'bit_rate_mode',
            'type':'unicode',
        },
        'bit depth':{
            'name':u'Bit depth',
            'keyword':u'bit_depth',
            'type':'int',
            'format':'bit',
        },
        'sample rate':{
            'name':u'Sample rate',
            'keyword':u'sample_rate',
            'type':'int',
            'format':'frequency',
        },
        'sample count':{
            'name':u'Sample count',
            'keyword':u'sample_count',
            'type':'int',
        },
        'frame rate':{
            'name':u'Frame rate',
            'keyword':u'frame_rate',
            'type':'float',
            'format':'framerate',
        },
        'frame rate mode':{
            'name':u'Frame rate mode',
            'keyword':u'frame_rate_mode',
            'type':'unicode',
        },
        'frame rate minimum':{
            'name':u'Frame rate minimum',
            'keyword':u'frame_rate_minimum',
            'type':'float',
            'format':'framerate',
        },
        'frame rate maximum':{
            'name':u'Frame rate maximum',
            'keyword':u'frame_rate_maximum',
            'type':'float',
            'format':'framerate',
        },
        'frame count':{
            'name':u'Frame count',
            'keyword':u'frame_count',
            'type':'int',
        },
        'duration':{
            'name':u'Duration',
            'keyword':u'duration',
            'type':'int',
            'format':'millisecond',
        },
        'width':{
            'name':u'Width',
            'keyword':u'width',
            'type':'int',
            'format':'pixel',
        },
        'height':{
            'name':u'Height',
            'keyword':u'height',
            'type':'int',
            'format':'pixel',
        },
        'pixel aspect ratio':{
            'name':u'Pixel aspect ratio',
            'keyword':u'pixel_aspect_ratio',
            'type':'float',
        },
        'display aspect ratio':{
            'name':u'Display aspect ratio',
            'keyword':u'display_aspect_ratio',
            'type':'float',
        },
        'color space':{
            'name':u'Color space',
            'keyword':u'color_space',
            'type':'unicode',
        },
        'channels':{
            'name':u'Channels',
            'keyword':u'channels',
            'type':'int',
        },
        'dialnorm':{
            'name':u'Dialnorm',
            'keyword':u'dialnorm',
            'type':'int',
        },
        'bpf':{
            'name':u'Bits / Pixel * Frame',
            'keyword':u'bpf',
            'type':'float',
        },
        'encoder':{
            'name':u'Encoder',
            'keyword':u'encoder',
            'type':'unicode',
        },
        'encoder settings':{
            'name':u'Encoder settings',
            'keyword':u'encoder_settings',
            'type':'unicode',
            'plural':'dict',
        },
        'character':{
            'name':u'Character',
            'keyword':u'character',
            'type':'unicode',
        },
        'image url':{
            'name':u'Image URL',
            'keyword':u'image_url',
            'type':'unicode',
        },
        'poster url':{
            'name':u'Poster URL',
            'keyword':u'poster_url',
            'type':'unicode',
        },
        'backdrop url':{
            'name':u'Backdrop URL',
            'keyword':u'backdrop_url',
            'type':'unicode',
        },
        'database':{
            'name':u'Database',
            'keyword':u'database',
            'type':'unicode',
        },
        'username':{
            'name':u'Username',
            'keyword':u'username',
            'type':'unicode',
        },
        'password':{
            'name':u'Password',
            'keyword':u'password',
            'type':'unicode',
        },
        'mongodb url':{
            'name':u'MongoDB URL',
            'keyword':u'mongodb_url',
            'type':'unicode',
        },
        'home id':{
            'name':u'Home ID',
            'keyword':u'home_id',
            'type':'int',
        },
        'album id':{
            'name':u'Album ID',
            'keyword':u'album_id',
            'type':'int',
        },
        'disk id':{
            'name':u'Disk ID',
            'keyword':u'disk_id',
            'type':'int',
        },
        'track id':{
            'name':u'Track ID',
            'keyword':u'track_id',
            'type':'int',
        },
        
        'movie id':{
            'name':u'Movie ID',
            'keyword':u'movie_id',
            'type':'int',
        },
        'collection id':{
            'name':u'Collection ID',
            'keyword':u'collection_id',
            'type':'int',
        },
        'tv show id':{
            'name':u'TV show ID',
            'keyword':u'tv_show_id',
            'type':'int',
        },
        'person id':{
            'name':u'Person ID',
            'keyword':u'person_id',
            'type':'int',
        },
        'company id':{
            'name':u'Company ID',
            'keyword':u'company_id',
            'type':'int',
        },
        'network id':{
            'name':u'Network ID',
            'keyword':u'network_id',
            'type':'int',
        },
        'studio id':{
            'name':u'Studio ID',
            'keyword':u'studio_id',
            'type':'int',
        },
        'job id':{
            'name':u'Job ID',
            'keyword':u'job_id',
            'type':'int',
        },
        'department id':{
            'name':u'Department ID',
            'keyword':u'department_id',
            'type':'int',
        },
        'keyword id':{
            'name':u'Keyword ID',
            'keyword':u'keyword_id',
            'type':'int',
        },
        'genre id':{
            'name':u'Genre ID',
            'keyword':u'genre_id',
            'type':'int',
        },
        'sort order':{
            'name':u'Sort order',
            'keyword':u'sort_order',
            'type':'int',
        },
        'tv show air day':{
            'name':u'TV show air day',
            'keyword':u'tv_show_air_day',
            'type':'unicode',
        },
        'tv show air time':{
            'name':u'TV show air time',
            'keyword':u'tv_show_air_time',
            'type':'time',
        },
        'track subtitle':{
            'name':'Track subtitle',
            'keyword':'track_subtitle',
            'type':'unicode',
            'atom':'@st3',
            'enable':False,
        },
        'art director':{
            'name':u'Art director',
            'description':'Person responsible for non-photographic artwork used with content',
            'keyword':u'art_director',
            'type':'unicode',
            'atom':'@ard',
            'enable':False,
        },
        'arranger':{
            'name':u'Arranger',
            'description':'Person responsible for particular adaptation of composition',
            'keyword':u'arranger',
            'type':'unicode',
            'atom':'@arg',
            'enable':False,
        },
        'lyricist':{
            'name':u'Lyricist',
            'description':u'Writer of the song lyrics',
            'keyword':'lyricist',
            'type':'unicode',
            'atom':'©aut',
            'enable':False,
        },
        'copyright acknowledgement':{
            'name':u'Copyright acknowledgement',
            'description':u'Ackowledgements of those granting permission to use copyrighted material',
            'keyword':'copyright_acknowledgement',
            'type':'unicode',
            'atom':'©cak',
            'enable':False,
        },
        'conductor':{
            'name':u'Conductor',
            'description':u'Name of the person who directed the orchestra',
            'keyword':'conductor',
            'type':'unicode',
            'atom':'©con',
            'enable':False,
        },
        'song description':{
            'name':u'Song description',
            'description':u'Explanation of the song',
            'keyword':'song_description',
            'type':'unicode',
            'atom':'©des',
            'enable':False,
        },
        'equalization preset name':{
            'name':u'Equalization preset name',
            'description':u'Setting for equalization of content',
            'keyword':'equalization_preset_name',
            'type':'unicode',
            'atom':'©equ',
            'enable':False,
        },
        'liner notes':{
            'name':u'Liner notes',
            'description':u'Explanatory notes about a record album, included on the jacket or in the packaging',
            'keyword':'liner_notes',
            'type':'unicode',
            'atom':'©lnt',
            'enable':False,
        },
        'record company':{
            'name':u'Record company',
            'description':u'Company releasing the song',
            'keyword':'record_company',
            'type':'unicode',
            'atom':'©mak',
            'enable':False,
        },
        'original artist':{
            'name':u'Original artist',
            'description':u'Name of artist originally attributed with content',
            'keyword':'original_artist',
            'type':'unicode',
            'atom':'©ope',
            'enable':False,
        },
        'phonogram rights':{
            'name':u'Phonogram rights',
            'description':u'Like a copyright, but using the circled P symbol, for audio rights',
            'keyword':'phonogram_rights',
            'type':'unicode',
            'atom':'©phg',
            'enable':False,
        },
        'performer':{
            'name':u'Performer',
            'description':u'Name or URL of the individual primary members of the band or group',
            'keyword':'Performer',
            'type':'unicode',
            'atom':'©prf',
            'enable':False,
        },
        'publisher':{
            'name':u'Publisher',
            'description':u'Company publishing the song',
            'keyword':'publisher',
            'type':'unicode',
            'atom':'©pub',
            'enable':False,
        },
        'sound engineer':{
            'name':u'Sound engineer',
            'description':u'The name of the person doing soundengineering',
            'keyword':'sound_engineer',
            'type':'unicode',
            'atom':'©sne',
            'enable':False,
        },
        'soloist':{
            'name':u'Soloist',
            'description':u'Name of the musician who performs the solo',
            'keyword':'soloist',
            'type':'unicode',
            'atom':'©sol',
            'enable':False,
        },
        'credits':{
            'name':u'Credits',
            'description':u'Credits for those who provided source content',
            'keyword':'credits',
            'type':'unicode',
            'atom':'©src',
            'enable':False,
        },
        'thanks':{
            'name':u'Thanks and dedications',
            'description':u'Notes of acknowledgement or recognition from the artist',
            'keyword':'thanks',
            'type':'unicode',
            'atom':'©thx',
            'enable':False,
        },
        'online extras':{
            'name':u'Online extras',
            'description':u'Links to content that can only be accessed when connected to the internet',
            'keyword':'online_extras',
            'type':'unicode',
            'atom':'©url',
            'enable':False,
        },
        'executive producer':{
            'name':u'Executive producer',
            'description':u'Person responsible for creating or supervising the song',
            'keyword':'executive_producer',
            'type':'unicode',
            'atom':'©xpd',
            'enable':False,
        },
        'producer':{
            'name':u'Producer',
            'description':u'Person responsible for creating or supervising the song',
            'keyword':'producer',
            'type':'unicode',
            'atom':'©prd',
            'enable':False,
        },
        'director':{
            'name':u'Director',
            'description':u'Name of director for movie',
            'keyword':'director',
            'type':'unicode',
            'atom':'©dir',
            'enable':False,
        },
        
        'homepage':{
            'name':u'Homepage',
            'keyword':u'homepage',
            'type':'unicode',
        },
        'title':{
            'name':u'Title',
            'keyword':u'title',
            'type':'unicode',
        },
        'original title':{
            'name':u'Original title',
            'keyword':u'original title',
            'type':'unicode',
        },
        'tagline':{
            'name':u'Tagline',
            'keyword':u'tagline',
            'type':'unicode',
        },
        'budget':{
            'name':u'Budget',
            'keyword':u'budget',
            'type':'int',
        },
        'runtime':{
            'name':u'Runtime',
            'keyword':u'runtime',
            'type':'int',
        },
        'revenue':{
            'name':u'Revenue',
            'keyword':u'revenue',
            'type':'int',
        },
        
        'recursive':{
            'name':u'Recursive',
            'keyword':u'recursive',
            'type':'bool',
        },
        'sync':{
            'name':u'Synchronize',
            'keyword':u'sync',
            'type':'bool',
        },
        'crawl':{
            'name':u'Crawl',
            'keyword':u'crawl',
            'type':'bool',
        },
        'download':{
            'name':u'Download',
            'keyword':u'download',
            'type':'bool',
        },
        'overwrite':{
            'name':u'Overwrite',
            'keyword':u'overwrite',
            'type':'bool',
        },
        'debug':{
            'name':u'Debug',
            'keyword':u'debug',
            'type':'bool',
        },
        'verbosity':{
            'name':u'Verbosity',
            'keyword':u'verbosity',
            'type':'enum',
            'enumeration':'verbosity',
        },
        'configuration path':{
            'name':u'Configuration path',
            'keyword':u'configuration_path',
            'type':'unicode',
        },
        'inclusion':{
            'name':u'Inclusion filter',
            'keyword':u'inclusion',
            'type':'unicode',
        },
        'exclusion':{
            'name':u'Exclusion filter',
            'keyword':u'exclusion',
            'type':'unicode',
        },
        'scan path':{
            'name':u'Scan path',
            'keyword':u'scan_path',
            'type':'unicode',
            'plural':'list',
        },
        'uris':{
            'name':u'URIs',
            'keyword':u'uris',
            'type':'unicode',
            'plural':'list',
        },
        'quantizer':{
            'name':u'Quantizer',
            'keyword':u'quantizer',
            'type':'float',
        },
        'crop':{
            'name':u'Crop',
            'keyword':u'crop',
            'type':'unicode',
        },
        'time shift':{
            'name':u'Time shift',
            'keyword':u'shift',
            'type':'int',
        },
        'source frame rate':{
            'name':u'Source frame rate',
            'keyword':u'source_frame_rate',
            'type':'enum',
            'enumeration':'frame rate',
        },
        'target frame rate':{
            'name':u'Target frame rate',
            'keyword':u'target_frame_rate',
            'type':'enum',
            'enumeration':'frame rate',
        },
        'action':{
            'name':u'Action',
            'keyword':u'action',
            'type':'unicode',
        },
        'handbrake parameters':{
            'name':u'HandBrake parameters',
            'keyword':u'handbrake_parameters',
            'type':'unicode',
            'plural':'dict',
        },
        'handbrake x264 settings':{
            'name':u'HandBrake x264 settings',
            'keyword':u'handbrake_x264_settings',
            'type':'unicode',
            'plural':'dict',
        },
        'handbrake audio encoder settings':{
            'name':u'HandBrake audio encoder settings',
            'keyword':u'handbrake_audio_encoder_settings',
            'type':'unicode',
            'plural':'dict',
        },
        'home uri':{
            'name':u'Home URI',
            'keyword':'home_uri',
            'type':'unicode',
        },
        'asset uri':{
            'name':u'Asset URI',
            'keyword':'asset_uri',
            'type':'unicode',
        },
        'resource uri':{
            'name':u'Resource URI',
            'keyword':'resource_uri',
            'type':'unicode',
        },
    },
}
