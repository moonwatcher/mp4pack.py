# -*- coding: utf-8 -*-

# album id
# track id
# album > disc > track

# tv show id
# tv season id
# tv episode
# tv show > tv season > tv episode

# movie id
# movie version id
 
{
    'service':{
        'home':{
            'match':ur'^/h/.*$',
            'key generator':{'space':'knowledge', 'element':u'home id' },
            'branch':{
                'service.home':{
                    'match':[
                        {
                            'filter':ur'^/h/(?P<home_id>[0-9]+)$',
                        },
                    ],
                    'collection':'home',
                },
                'service.home.movie':{
                    'match':[
                        {
                            'filter':ur'^/h/movie/(?P<movie_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/movie/~/(?P<movie_handle>[^/]+)$',
                        },
                        {
                            'filter':ur'^/h/movie/tmdb/(?P<tmdb_movie_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tmdb/movie/{tmdb movie id}',
                        },
                        {
                            'filter':ur'^/h/movie/imdb/(?P<imdb_movie_id>tt[0-9]+)$',
                            'depend':ur'/c/{language}/tmdb/movie/imdb/{imdb movie id}',
                        },
                        {
                            'filter':ur'^/h/movie/rottentomatoes/(?P<rottentomatoes_movie_id>[0-9]+)$',
                            'depend':ur'/c/rottentomatoes/movie/{rottentomatoes movie id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'movie home by id',
                            'format':ur'/h/movie/{movie id}',
                        },
                        {
                            'name':u'movie home by handle',
                            'format':ur'/h/movie/~/{movie handle}',
                        },
                        {
                            'name':u'movie home by tmdb id',
                            'format':ur'/h/movie/tmdb/{tmdb movie id}',
                        },
                        {
                            'name':u'movie home by imdb id',
                            'format':ur'/h/movie/imdb/{imdb movie id}',
                        },
                        {
                            'name':u'movie home by rottentomatoes movie id',
                            'format':ur'/h/movie/rottentomatoes/{rottentomatoes movie id}',
                        },
                    ],
                    'collection':'home',
                    'key':'movie id',
                    'index':[
                        'movie id',
                        'tmdb movie id',
                        'imdb movie id',
                        'itunes movie id',
                        'rottentomatoes movie id',
                        'movie title',
                        'simple movie title',
                        'movie handle',
                    ],
                },
                'service.home.tv.show':{
                    'match':[
                        {
                            'filter':ur'^/h/tv/show/(?P<tv_show_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/show/~/(?P<tv_show_handle>[^/]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/show/tvdb/(?P<tvdb_tv_show_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/tv/show/{tvdb tv show id}',
                        },
                        {
                            'filter':ur'^/h/tv/show/imdb/(?P<imdb_tv_show_id>tt[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'show home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'show home by tv show id',
                            'format':ur'/h/tv/show/{tv show id}',
                        },
                        {
                            'name':u'show home by tv show handle',
                            'format':ur'/h/tv/show/~/{tv show handle}',
                        },
                        {
                            'name':u'show home by tvdb tv show id',
                            'format':ur'/h/tv/show/tvdb/{tvdb tv show id}',
                        },
                        {
                            'name':u'show home by imdb tv show id',
                            'format':ur'/h/tv/show/imdb/{imdb tv show id}'
                        },
                    ],
                    'collection':'home',
                    'key':'tv show id',
                    'index':[
                        'tv show id',
                        'tvdb tv show id',
                        'imdb tv show id',
                        'itunes tv show id',
                        'tv show name',
                        'simple tv show name',
                        'tv show handle',
                    ],
                },
                'service.home.tv.season':{
                    'match':[
                        {
                            'filter':ur'^/h/tv/season/(?P<tv_season_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/season/tvdb/(?P<tvdb_tv_season_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/tv/season/{tvdb tv season id}',
                        },
                        {
                            'filter':ur'^/h/tv/season/tvdb/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/tv/season/{tvdb tv show id}/{disc number}',
                        },
                        {
                            'filter':ur'^/h/tv/season/imdb/(?P<imdb_tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)$',
                        },
                    ],
                    'collect':[
                        ur'/h/tv/show/tvdb/{tvdb tv show id}',
                    ],
                    'resolvable':[
                        {
                            'name':u'season home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'season home by tv season id',
                            'format':ur'/h/tv/season/{tv season id}',
                        },
                        {
                            'name':u'season home by tv show id',
                            'format':ur'/h/tv/season/{tv show id}/{disc number}',
                        },
                        {
                            'name':u'season home by tvdb tv season id',
                            'format':ur'/h/tv/season/tvdb/{tvdb tv season id}',
                        },
                        {
                            'name':u'season home by tvdb tv show id',
                            'format':ur'/h/tv/season/tvdb/{tvdb tv show id}/{disc number}',
                        },
                        {
                            'name':u'season home by imdb tv show id',
                            'format':ur'/h/tv/season/imdb/{imdb tv show id}/{disc number}',
                        },
                    ],
                    'collection':'home',
                    'key':'tv season id',
                    'index':[
                        'tv show id',
                        'tv season id',
                        'disc number',
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'imdb tv show id',
                        'itunes tv show id',
                        'itunes tv season id',
                        'tv show name',
                        'simple tv show name',
                    ],
                },
                'service.home.tv.episode':{
                    'match':[
                        {
                            'filter':ur'^/h/tv/episode/(?P<tv_episode_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/(?P<tv_season_id>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/~/(?P<tv_show_handle>[^/]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/tvdb/(?P<tvdb_tv_episode_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/tv/episode/{tvdb tv episode id}',
                        },
                        {
                            'filter':ur'^/h/tv/episode/tvdb/(?P<tvdb_tv_season_id>[0-9]+)/(?P<track_number>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/tv/episode/{tvdb tv season id}/{track number}',
                        },
                        {
                            'filter':ur'^/h/tv/episode/tvdb/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/tv/episode/{tvdb tv show id}/{disc number}/{track number}',
                        },
                        {
                            'filter':ur'^/h/tv/episode/imdb/(?P<imdb_tv_episode_id>tt[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/imdb/(?P<imdb_tv_show_id>tt[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                    ],
                    'collect':[
                        ur'/h/tv/season/tvdb/{tvdb tv show id}/{disc number}',
                        ur'/h/tv/season/tvdb/{tvdb tv season id}',
                    ],
                    'resolvable':[
                        {
                            'name':u'episode home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'episode home by tv episode id',
                            'format':ur'/h/tv/episode/{tv episode id}',
                        },
                        {
                            'name':u'episode home by tv season id',
                            'format':ur'/h/tv/episode/{tv season id}/{track number}',
                        },
                        {
                            'name':u'episode home by tv show id',
                            'format':ur'/h/tv/episode/{tv show id}/{disc number}/{track number}',
                        },
                        {
                            'name':u'episode home by tv show handle',
                            'format':ur'/h/tv/episode/~/{tv show handle}/{disc number}/{track number}',
                        },
                        {
                            'name':u'episode home by tvdb tv episode id',
                            'format':ur'/h/tv/episode/tvdb/{tvdb tv episode id}',
                        },
                        {
                            'name':u'episode home by tvdb tv season id',
                            'format':ur'/h/tv/episode/tvdb/{tvdb tv season id}/{track number}',
                        },
                        {
                            'name':u'episode home by tvdb tv show id',
                            'format':ur'/h/tv/episode/tvdb/{tvdb tv show id}/{disc number}/{track number}',
                        },
                        {
                            'name':u'episode home by imdb tv episode id',
                            'format':ur'/h/tv/episode/imdb/{imdb tv episode id}',
                        },
                        {
                            'name':u'episode home by imdb tv show id',
                            'format':ur'/h/tv/episode/imdb/{imdb tv show id}/{disc number}/{track number}',
                        },
                    ],
                    'collection':'home',
                    'key':'tv episode id',
                    'index':[
                        'tv show id',
                        'tv season id',
                        'tv episode id',
                        'disc number',
                        'track number'
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'tvdb tv episode id',
                        'imdb tv show id',
                        'imdb tv episode id',
                        'itunes tv show id',
                        'itunes tv season id',
                        'itunes tv episode id',
                        'tv show name',
                        'tv episode name',
                        'simple tv show name',
                        'simple tv episode name',
                    ],
                },
                'service.home.music.album':{
                    'match':[
                        {
                            'filter':ur'^/h/music/album/(?P<album_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/album/itunes/(?P<itunes_music_album_id>[0-9]+)$',
                            'depend':ur'/c/itunes/music/album/{itunes music album id}',
                        },
                        {
                            'filter':ur'^/h/music/album/~/(?P<album_handle>[^/]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music album home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'music album home by album id',
                            'format':ur'/h/music/album/{album id}',
                        },
                        {
                            'name':u'music album home by itunes music album id',
                            'format':ur'/h/music/album/itunes/{itunes music album id}',
                        },
                        {
                            'name':u'music album home by album handle',
                            'format':ur'/h/music/album/~/{album handle}',
                        },
                    ],
                    'collection':'home',
                    'key':'album id',
                    'index':[
                        'album id',
                        'itunes music album id',
                        'music album name',
                        'simple music album name',
                        'album handle'
                    ],
                },
                'service.home.music.track':{
                    'match':[
                        {
                            'filter':ur'^/h/music/track/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/track/(?P<album_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/track/itunes/(?P<itunes_music_track_id>[0-9]+)$',
                            'depend':ur'/c/itunes/music/track/{itunes music track id}',
                        },
                        {
                            'filter':ur'^/h/music/track/itunes/(?P<itunes_music_album_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                            'depend':ur'/c/itunes/music/track/{itunes music album id}/{disc number}/{track number}',
                        },
                        {
                            'filter':ur'^/h/music/track/~/(?P<album_handle>[^/]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music track home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'music track home by track id',
                            'format':ur'/h/music/track/{track id}',
                        },
                        {
                            'name':u'music track home by album id',
                            'format':ur'/h/music/track/{album id}/{disc number}/{track number}',
                        },
                        {
                            'name':u'music track home by itunes music track id',
                            'format':ur'/h/music/track/itunes/{itunes music track id}',
                        },
                        {
                            'name':u'music track home by itunes music album id',
                            'format':ur'/h/music/track/itunes/{itunes music album id}/{disc number}/{track number}',
                        },
                        {
                            'name':u'music track home by album handle',
                            'format':ur'/h/music/track/~/{album handle}/{disc number}/{track number}',
                        },
                    ],
                    'collection':'home',
                    'key':'track id',
                    'index':[
                        'album id',
                        'track id',
                        'disc number',
                        'track number',
                        'itunes music track id',
                        'itunes music album id',
                        'music album name',
                        'music track name',
                        'simple music album name',
                        'simple music track name',
                        'album handle',
                    ],
                },
                'service.home.person':{
                    'match':[
                        {
                            'filter':ur'^/h/person/(?P<person_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/person/tmdb/(?P<tmdb_person_id>[0-9]+)$',
                            'depend':ur'/c/tmdb/person/{tmdb person id}',
                        },
                        {
                            'filter':ur'^/h/person/itunes/(?P<itunes_person_id>[0-9]+)$',
                            'depend':ur'/c/itunes/person/{itunes person id}',
                        },
                        {
                            'filter':ur'^/h/person/imdb/(?P<imdb_person_id>nm[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'person home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'person home by person id',
                            'format':ur'/h/person/{person id}',
                        },
                        {
                            'name':u'person home by tmdb person id',
                            'format':ur'/h/person/tmdb/{tmdb person id}',
                        },
                        {
                            'name':u'person home by itunes person id',
                            'format':ur'/h/person/itunes/{itunes person id}',
                        },
                    ],
                    'collection':'home',
                    'key':'person id',
                    'index':[
                        'person id',
                        'tmdb person id',
                        'itunes person id',
                        'person name',
                        'simple person name',
                    ],
                },
                'service.home.company':{
                    'match':[
                        {
                            'filter':ur'^/h/company/(?P<company_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/company/tmdb/(?P<tmdb_company_id>[0-9]+)$',
                            'depend':ur'/c/tmdb/company/{tmdb company id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'company home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'company home by company id',
                            'format':ur'/h/company/{company id}',
                        },
                        {
                            'name':u'company home by tmdb company id',
                            'format':ur'/h/company/tmdb/{tmdb company id}',
                        },
                    ],
                    'collection':'home',
                    'key':'company id',
                    'index':[
                        'company id',
                        'tmdb company id',
                        'company name',
                        'simple company name',                        
                    ],
                },
                'service.home.genre':{
                    'match':[
                        {
                            'filter':ur'^/h/genre/(?P<genre_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/genre/tmdb/(?P<tmdb_genre_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tmdb/genre/{tmdb genre id}',
                        },
                        {
                            'filter':ur'^/h/genre/itunes/(?P<itunes_genre_id>[0-9]+)$',
                            'depend':ur'/c/itunes/genre/{itunes genre id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'genre home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'genre home by genre id',
                            'format':ur'/h/genre/{genre id}',
                        },
                        {
                            'name':u'genre home by tmdb genre id',
                            'format':ur'/h/genre/tmdb/{tmdb genre id}',
                        },
                        {
                            'name':u'genre home by itunes genre id',
                            'format':ur'/h/genre/itunes/{itunes genre id}',
                        },
                    ],
                    'collection':'home',
                    'key':'genre id',
                    'index':[
                        'genre id',
                        'tmdb genre id',
                        'itunes genre id',
                        'genre name',
                        'simple genre name',
                    ],
                },
                'service.home.job':{
                    'match':[
                        {
                            'filter':ur'^/h/job/(?P<job_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'job home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'job home by job id',
                            'format':ur'/h/job/{job id}',
                        },
                    ],
                    'collection':'home',
                    'key':'job id',
                },
                'service.home.department':{
                    'match':[
                        {
                            'filter':ur'^/h/department/(?P<department_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'department home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'department home by department id',
                            'format':ur'/h/department/{department id}',
                        },
                    ],
                    'collection':'home',
                    'key':'department id',
                },
            },
        },
        'medium':{
            'match':ur'^/m/.*$',
            'branch':{
                'service.medium.asset':{
                    'match':[
                        {
                            'filter':ur'^/m/asset/(?P<home_id>[0-9]+)$',
                            'depend':ur'/h/{home id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'asset by home id',
                            'format':ur'/m/asset/{home id}',
                            'canonical':True,
                        },
                    ],
                    'type':'reference',
                    'collection':'medium_asset',
                },
                'service.medium.resource':{
                    'match':[
                        {
                            'filter':ur'^/m/resource/sha1/(?P<path_digest>[0-9a-f]{40})$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'resource',
                            'format':ur'/m/resource/sha1/{path digest}',
                            'canonical':True,
                        },
                    ],
                    'type':'crawl',
                    'collection':'medium_resource',
                },
            }
        },
        'knowledge':{
            'match':ur'^/k/.*$',
            'branch':{
                'service.knowledge.configuration':{
                    'match':[
                        {
                            'filter':ur'^/k/configuration$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'knowledge configuration',
                            'format':ur'/k/configuration',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_configuration',
                },

                'service.knowledge.playlist':{
                    'match':[
                        {
                            'filter':ur'^/k/playlist/(?P<playlist_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'playlist knowledge',
                            'format':ur'/k/{language}/playlist/{playlist id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_playlist',
                    'namespace':'knowledge.playlist',
                },

                'service.knowledge.movie':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/movie/(?P<movie_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie knowledge by id',
                            'format':ur'/k/{language}/movie/{movie id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie',
                    'namespace':'ns.knowledge.movie',
                    'index':['movie id', 'language'],
                },
                'service.knowledge.movie.cast':{
                    'match':[
                        {
                            'filter':ur'^/k/movie/(?P<movie_id>[0-9]+)/cast$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie cast knowledge',
                            'format':ur'/k/movie/{movie id}/cast',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie_cast',
                    'namespace':'knowledge.movie.cast',
                },
                'service.knowledge.movie.image':{
                    'match':[
                        {
                            'filter':ur'^/k/movie/(?P<movie_id>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie image knowledge',
                            'format':ur'/k/movie/{movie id}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie_image',
                    'namespace':'knowledge.movie.image',
                },
                'service.knowledge.movie.keyword':{
                    'match':[
                        {
                            'filter':ur'^/k/movie/(?P<movie_id>[0-9]+)/keyword$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie keyword knowledge',
                            'format':ur'/k/movie/{movie id}/keyword',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie_keyword',
                    'namespace':'knowledge.movie.keyword',
                },
                'service.knowledge.movie.release':{
                    'match':[
                        {
                            'filter':ur'^/k/movie/(?P<movie_id>[0-9]+)/release$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie release knowledge',
                            'format':ur'/k/movie/{movie id}/release',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie_release',
                    'namespace':'knowledge.movie.release',
                },
                'service.knowledge.movie.clip':{
                    'match':[
                        {
                            'filter':ur'^/k/movie/(?P<movie_id>[0-9]+)/clip$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie clip knowledge',
                            'format':ur'/k/movie/{movie id}/clip',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie_clip',
                    'namespace':'knowledge.movie.clip',
                },
                'service.knowledge.movie.translation':{
                    'match':[
                        {
                            'filter':ur'^/k/movie/(?P<movie_id>[0-9]+)/translation$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie translation knowledge',
                            'format':ur'/k/movie/{movie id}/translation',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie_translation',
                    'namespace':'knowledge.movie.translation',
                },
                'service.knowledge.movie.alternative':{
                    'match':[
                        {
                            'filter':ur'^/k/movie/(?P<movie_id>[0-9]+)/alternative$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie alternative knowledge',
                            'format':ur'/k/movie/{movie id}/alternative',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_movie_alternative',
                    'namespace':'knowledge.movie.alternative',
                },

                'service.knowledge.music.album':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/album/(?P<album_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music album',
                            'format':ur'/k/{language}/music/album/{album id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_music_album',
                    'namespace':'knowledge.music.album',
                    'index':['album id', 'language'],
                },
                'service.knowledge.music.album.image':{
                    'match':[
                        {
                            'filter':ur'^/k/music/album/(?P<album_id>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music album image',
                            'format':ur'/k/music/album/{album id}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_music_album_image',
                    'namespace':'knowledge.music.album.image',
                },
                'service.knowledge.music.track':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/track/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/track/(?P<album_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music track by track id',
                            'format':ur'/k/{language}/music/track/{track id}',
                        },
                        {
                            'name':u'music track by album id',
                            'format':ur'/k/{language}/music/track/{album id}/{disc number}/{track number}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_music_track',
                    'namespace':'knowledge.music.track',
                    'index':['album id', 'track id', 'disc number', 'track number', 'language'],
                },

                'service.knowledge.tv.show':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/show/(?P<tv_show_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'show knowledge by tv show id',
                            'format':ur'/k/{language}/tv/show/{tv show id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_show',
                    'namespace':'ns.knowledge.tv.show',
                    'index':['tv show id', 'language'],
                },
                'service.knowledge.tv.show.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/show/(?P<tv_show_id>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show image',
                            'format':ur'/k/tv/show/{tv show id}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_show_image',
                    'namespace':'knowledge.tv.show.image',
                },
                'service.knowledge.tv.show.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/show/(?P<tv_show_id>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show credit',
                            'format':ur'/k/tv/show/{tv show id}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_show_credit',
                    'namespace':'knowledge.tv.show.credit',
                },
                'service.knowledge.tv.season':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/season/(?P<tv_season_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'season knowledge by tv season id',
                            'format':ur'/k/{language}/tv/season/{tv season id}',
                        },
                        {
                            'name':u'season knowledge by tv show id and position',
                            'format':ur'/k/{language}/tv/season/{tv show id}/{disc number}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season',
                    'namespace':'ns.knowledge.tv.season',
                    'index':[
                        'tv show id',
                        'tv season id',
                        'disc number',
                    ],
                },
                'service.knowledge.tv.season.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show season image',
                            'format':ur'/k/tv/season/{tv show id}/{disc number}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season_image',
                    'namespace':'knowledge.tv.season.image',
                },
                'service.knowledge.tv.season.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show season image',
                            'format':ur'/k/tv/season/{tv show id}/{disc number}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season_credit',
                    'namespace':'knowledge.tv.season.credit',
                },
                'service.knowledge.tv.episode':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/episode/(?P<tv_episode_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/episode/(?P<tv_season_id>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'episode knowledge by tv episode id',
                            'format':ur'/k/{language}/tv/episode/{tv episode id}',
                        },
                        {
                            'name':u'episode knowledge by tv season id',
                            'format':ur'/k/{language}/tv/episode/{tv season id}/{track number}',
                        },
                        {
                            'name':u'episode knowledge by tv show id',
                            'format':ur'/k/{language}/tv/episode/{tv show id}/{disc number}/{track number}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode',
                    'namespace':'ns.knowledge.tv.episode',
                    'index':[
                        'tv show id',
                        'tv season id',
                        'tv episode id',
                        'disc number',
                        'track number',
                        'language',
                    ],
                },
                'service.knowledge.tv.episode.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode image',
                            'format':ur'/k/tv/episode/{tv show id}/{disc number}/{track number}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode_image',
                    'namespace':'knowledge.tv.episode.image',
                },
                'service.knowledge.tv.episode.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode credit',
                            'format':ur'/k/tv/episode/{tv show id}/{disc number}/{track number}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode_credit',
                    'namespace':'knowledge.tv.episode.credit',
                },

                'service.knowledge.person':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/person/(?P<person_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'person by knowledge id',
                            'format':ur'/k/{language}/person/{person id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_person',
                    'namespace':'ns.knowledge.person',
                },
                'service.knowledge.person.image':{
                    'match':[
                        {
                            'filter':ur'^/k/person/(?P<person_id>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'person image',
                            'format':ur'/k/person/{person id}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_person_image',
                    'namespace':'knowledge.person.image',
                },
                'service.knowledge.person.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/person/(?P<person_id>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'person credit',
                            'format':ur'/k/person/{person id}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_person_credit',
                    'namespace':'knowledge.person.credit',
                },
                'service.knowledge.company':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/company/(?P<company_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'company by knowledge id',
                            'format':ur'/k/{language}/company/{company id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_company',
                    'namespace':'ns.knowledge.company',
                },
                'service.knowledge.company.image':{
                    'match':[
                        {
                            'filter':ur'^/k/company/(?P<company_id>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'company image',
                            'format':ur'/k/company/{company id}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_company_image',
                    'namespace':'knowledge.company.image',
                },
                'service.knowledge.company.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/company/(?P<company_id>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'company credit',
                            'format':ur'/k/company/{company id}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_company_credit',
                    'namespace':'knowledge.company.credit',
                },
                'service.knowledge.genre':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/genre/(?P<genre_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'genre by genre id',
                            'format':ur'/k/{language}/genre/{genre id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_genre',
                    'namespace':'ns.knowledge.genre',
                },
                'service.knowledge.job':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/job/(?P<job_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'job',
                            'format':ur'/k/{language}/job/{job id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_job',
                    'namespace':'ns.knowledge.job',
                },
                'service.knowledge.department':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/department/(?P<department_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'department',
                            'format':ur'/k/{language}/department/{department id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_department',
                    'namespace':'ns.knowledge.department',
                },
            },
        },

        'tmdb':{
            'api key':u'a8b9f96dde091408a03cb4c78477bd14',
            'remote base':u'http://api.themoviedb.org/3',
            'match':ur'^/c(?:/[a-z]{2})?/tmdb/.*$',
            'branch':{
                'service.search.tmdb.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/search$',
                            'query parameter':set(('api key', 'term', 'release year', 'language', 'page')),
                            'remote':ur'search/movie',
                        },
                    ],
                    'trigger':[
                        {
                            'namespace':'ns.knowledge.movie',
                            'format':ur'/c/{language}/tmdb/movie/{tmdb movie id}',
                        },
                    ],
                    'parse type':'search',
                },
                'service.search.tmdb.person':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/search$',
                            'query parameter':set(('api key', 'term', 'page')),
                            'remote':'search/person',
                        },
                    ],
                    'trigger':[
                        {
                            'namespace':'ns.knowledge.person',
                            'format':ur'/c/tmdb/person/{tmdb person id}',
                        },
                    ],
                    'parse type':'search',
                },
                'service.search.tmdb.company':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/search$',
                            'query parameter':set(('api key', 'term', 'page')),
                            'remote':'search/company',
                        },
                    ],
                    'trigger':[
                        {
                            'namespace':'ns.knowledge.company',
                            'format':ur'/c/tmdb/company/{tmdb company id}',
                        },
                    ],
                    'parse type':'search',
                },
                'service.document.tmdb.configuration':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/configuration$',
                            'query parameter':set(('api key',)),
                            'remote':ur'configuration',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb configuration',
                            'format':ur'/c/tmdb/configuration',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_configuration',
                    'parse type':'document',
                },
                'service.document.tmdb.genre':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/genre/(?P<tmdb_genre_id>[0-9]+)$',
                            'query parameter':set(('api key', 'language')),
                            'remote':ur'genre/{tmdb genre id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb genre by tmdb id',
                            'format':ur'/c/{language}/tmdb/genre/{tmdb genre id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_genre',
                    'namespace':'ns.knowledge.genre',
                    'parse type':'document',
                    'index':[
                        'tmdb genre id',
                        'genre name',
                        'simple genre name',
                        'language',
                    ],
                },
                'service.document.tmdb.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)$',
                            'query parameter':set(('api key', 'language')),
                            'remote':ur'movie/{tmdb movie id}',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/imdb/(?P<imdb_movie_id>tt[0-9]+)$',
                            'query parameter':set(('api key', 'language')),
                            'remote':ur'movie/{imdb movie id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie by tmdb id',
                            'format':ur'/c/{language}/tmdb/movie/{tmdb movie id}',
                            'canonical':True,
                        },
                        {
                            'name':u'tmdb movie by imdb id',
                            'format':ur'/c/{language}/tmdb/movie/imdb/{imdb movie id}',
                        }
                    ],
                    'collection':'tmdb_movie',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':[
                        'tmdb movie id',
                        'language',
                        'imdb movie id',
                        'movie title',
                        'simple movie title',
                    ],
                },
                'service.document.tmdb.movie.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/cast$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movie/{tmdb movie id}/casts',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie cast by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/cast',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_movie_cast',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':['tmdb movie id'],
                },
                'service.document.tmdb.movie.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/image$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movie/{tmdb movie id}/images',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie image by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/image',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_movie_image',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':['tmdb movie id'],
                },
                'service.document.tmdb.movie.keyword':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/keyword$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movie/{tmdb movie id}/keywords',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie keyword by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/keyword',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_movie_keyword',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':['tmdb movie id'],
                },
                'service.document.tmdb.movie.rating':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/rating$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movie/{tmdb movie id}/releases',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie release by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/rating',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_movie_rating',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':['tmdb movie id'],
                },
                'service.document.tmdb.movie.clip':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/clip$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movie/{tmdb movie id}/trailers',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie clip by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/clip',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_movie_clip',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':['tmdb movie id'],
                },
                'service.document.tmdb.movie.translation':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/translation$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movie/{tmdb movie id}/translations',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie translation by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/translation',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_movie_translation',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':['tmdb movie id'],
                },
                'service.document.tmdb.movie.alternative':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/alternative$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movie/{tmdb movie id}/alternative_titles',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie alternative by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/alternative',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_movie_alternative',
                    'namespace':'ns.knowledge.movie',
                    'parse type':'document',
                    'index':['tmdb movie id'],
                },
                'service.document.tmdb.collection':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/collection/(?P<tmdb_collection_id>[0-9]+)$',
                            'query parameter':set(('api key', 'language')),
                            'remote':ur'collection/{tmdb collection id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb collection by tmdb id',
                            'format':ur'/c/{language}/tmdb/collection/{tmdb collection id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_collection',
                    'namespace':'ns.knowledge.collection',
                    'parse type':'document',
                    'index':['tmdb collection id', 'language'],
                },
                'service.document.tmdb.person':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)$',
                            'query parameter':set(('api key',)),
                            'remote':ur'person/{tmdb person id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_person',
                    'namespace':'ns.knowledge.person',
                    'parse type':'document',
                    'index':[
                        'tmdb person id',
                        'person name',
                        'simple person name',
                    ],
                },
                'service.document.tmdb.person.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/image$',
                            'query parameter':set(('api key',)),
                            'remote':ur'person/{tmdb person id}/images',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person image by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}/image',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_person_image',
                    'namespace':'ns.knowledge.person',
                    'parse type':'document',
                },
                'service.document.tmdb.person.credit':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/credit$',
                            'query parameter':set(('api key',)),
                            'remote':ur'person/{tmdb person id}/credits',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person credit by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}/credit',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_person_credit',
                    'namespace':'ns.knowledge.person',
                    'parse type':'document',
                },
                'service.document.tmdb.company':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/company/(?P<tmdb_company_id>[0-9]+)$',
                            'query parameter':set(('api key',)),
                            'remote':ur'company/{tmdb company id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb company by tmdb id',
                            'format':ur'/c/tmdb/company/{tmdb company id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_company',
                    'namespace':'ns.knowledge.company',
                    'parse type':'document',
                    'index':[
                        'tmdb company id',
                        'company name',
                        'simple company name',
                    ],
                },
                'service.document.tmdb.company.credit':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/company/(?P<tmdb_company_id>[0-9]+)/credit$',
                            'query parameter':set(('api key',)),
                            'remote':ur'company/{tmdb company id}/movies',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb company credit by tmdb id',
                            'format':ur'/c/tmdb/company/{tmdb company id}/credit',
                            'canonical':True,
                        },
                    ],
                    'collection':'tmdb_company_credit',
                    'namespace':'ns.knowledge.company',
                    'parse type':'document',
                },
            },
        },
        'tvdb':{
            'api key':u'7B3B400B0146EA83',
            'remote base':u'http://www.thetvdb.com/api',
            'match':ur'^/c(?:/[a-z]{2})?/tvdb/.*$',
            'branch':{
                'service.search.tvdb.tv.show':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/show/search$',
                            'query parameter':set(('tv show name', 'language',)),
                            'remote':ur'GetSeries.php',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/show/search/imdb/(?P<imdb_tv_show_id>tt[0-9]+)$',
                            'query parameter':set(('imdb tv show id', 'language',)),
                            'remote':ur'GetSeriesByRemoteID.php',
                        },
                    ],
                    'trigger':[
                        {
                            'tag':u'Series',
                            'namespace':'ns.knowledge.tv.show',
                            'format':ur'/c/{language}/tvdb/tv/show/{tvdb tv show id}',
                        },
                    ],
                    'parse type':'search',
                    'type':'xml',
                },
                'service.document.tvdb.tv.show':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/show/(?P<tvdb_tv_show_id>[0-9]+)$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/{language}.xml',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/show/imdb/(?P<imdb_tv_show_id>tt[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show by tvdb show id',
                            'format':ur'/c/{language}/tvdb/tv/show/{tvdb tv show id}',
                            'canonical':True,
                        },
                        {
                            'name':u'tvdb show by imdb show id',
                            'format':ur'/c/{language}/tvdb/tv/show/imdb/{imdb tv show id}',
                        },
                    ],
                    'collect':[
                        ur'/c/{language}/tvdb/tv/show/search/imdb/{imdb tv show id}',
                    ],
                    'produce':[
                        {
                            'tag':u'Series',
                            'reference':'service.document.tvdb.tv.show',
                            'coalesce':False,
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'imdb tv show id',
                        'tv show name',
                        'simple tv show name',
                    ],
                    'collection':'tvdb_tv_show',
                    'namespace':'ns.knowledge.tv.show',
                    'parse type':'document',
                    'type':'xml',
                },
                'service.document.tvdb.tv.show.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/tv/show/(?P<tvdb_tv_show_id>[0-9]+)/cast$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/actors.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show cast by tvdb show id',
                            'format':ur'/c/tvdb/tv/show/{tvdb tv show id}/cast',
                            'canonical':True,
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Actor',
                            'reference':'service.document.tvdb.tv.show.cast',
                            'coalesce':True,
                        },
                    ],
                    'collection':'tvdb_tv_show_cast',
                    'namespace':'ns.knowledge.tv.show',
                    'parse type':'document',
                    'type':'xml',
                },
                'service.document.tvdb.tv.show.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/tv/show/(?P<tvdb_tv_show_id>[0-9]+)/image$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/banners.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show image by tvdb show id',
                            'format':ur'/c/tvdb/tv/show/{tvdb tv show id}/image',
                            'canonical':True,
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Banner',
                            'reference':'service.document.tvdb.tv.show.image',
                            'coalesce':True,
                        },
                    ],
                    'collection':'tvdb_tv_show_image',
                    'namespace':'ns.knowledge.tv.show',
                    'parse type':'document',
                    'type':'xml',
                },
                'service.document.tvdb.tv.season':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/season/(?P<tvdb_tv_season_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/season/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)$',
                        },
                    ],
                    'collect':[
                        ur'/c/{language}/tvdb/tv/show/{tvdb tv show id}',
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb season by tvdb season id',
                            'format':ur'/c/{language}/tvdb/tv/season/{tvdb tv season id}',
                            'canonical':True,
                        },
                        {
                            'name':u'tvdb season by tvdb show id',
                            'format':ur'/c/{language}/tvdb/tv/season/{tvdb tv show id}/{disc number}',
                        },
                        {
                            'name':u'tvdb season by imdb show id',
                            'format':ur'/c/{language}/tvdb/tv/season/imdb/{imdb tv show id}/{disc number}',
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'imdb tv show id',
                        'disc number',
                        'tv show name',
                        'simple tv show name',
                    ],
                    'collection':'tvdb_tv_season',
                    'namespace':'ns.knowledge.tv.season',
                    'parse type':'document',
                    'type':'xml',
                },
                'service.document.tvdb.tv.episode':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/episode/(?P<tvdb_tv_episode_id>[0-9]+)$',
                            'remote':ur'{api key}/episodes/{tvdb tv episode id}/{language}.xml',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/episode/(?P<tvdb_tv_season_id>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/episode/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/default/{disc number}/{track number}/{language}.xml',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/episode/imdb/(?P<imdb_tv_episode_id>tt[0-9]+)$',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/episode/imdb/(?P<imdb_tv_show_id>tt[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                        },
                    ],
                    'collect':[
                        ur'/c/{language}/tvdb/tv/show/{tvdb tv show id}',
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb episode by tvdb episode id',
                            'format':ur'/c/{language}/tvdb/tv/episode/{tvdb tv episode id}',
                            'canonical':True,
                        },
                        {
                            'name':u'tvdb episode by tvdb season id',
                            'format':ur'/c/{language}/tvdb/tv/episode/{tvdb tv season id}/{track number}',
                        },
                        {
                            'name':u'tvdb episode by tvdb show id',
                            'format':ur'/c/{language}/tvdb/tv/episode/{tvdb tv show id}/{disc number}/{track number}',
                        },
                        {
                            'name':u'tvdb episode by imdb episode id',
                            'format':ur'/c/{language}/tvdb/tv/episode/imdb/{imdb tv episode id}',
                        },
                        {
                            'name':u'tvdb episode by imdb show id',
                            'format':ur'/c/{language}/tvdb/tv/episode/imdb/{imdb tv show id}/{disc number}/{track number}',
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Episode',
                            'reference':'service.document.tvdb.tv.episode',
                            'coalesce':False,
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'tvdb tv episode id',
                        'imdb tv show id',
                        'imdb tv episode id',
                        'disc number',
                        'track number',
                        'tv show name',
                        'tv episode name',
                        'simple tv show name',
                        'simple tv episode name',
                        'tv episode production code',
                    ],
                    'collection':'tvdb_tv_episode',
                    'namespace':'ns.knowledge.tv.episode',
                    'parse type':'document',
                    'type':'xml',
                },
                'service.document.tvdb.tv.show.complete':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/tv/show/(?P<tvdb_tv_show_id>[0-9]+)/complete$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/all/{language}.zip',
                        },
                    ],
                    'collect':[
                        ur'/c/{language}/tvdb/tv/show/{tvdb tv show id}',
                    ],
                    'produce':[
                        {
                            'tag':u'Series',
                            'reference':'service.document.tvdb.tv.show',
                            'coalesce':False,
                        },
                        {
                            'tag':u'Episode',
                            'reference':'service.document.tvdb.tv.episode',
                            'coalesce':False,
                        },
                        {
                            'tag':u'Banner',
                            'reference':'service.document.tvdb.tv.show.image',
                            'coalesce':True,
                        },
                        {
                            'tag':u'Actor',
                            'reference':'service.document.tvdb.tv.show.cast',
                            'coalesce':True,
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'imdb tv show id',
                    ],
                    'parse type':'document',
                    'type':'zip',
                },
                'service.document.tvdb.update.daily':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/day$',
                            'remote':ur'{api key}/updates/updates_day.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb daily update',
                            'format':ur'/c/tvdb/update/day',
                            'canonical':True,
                        },
                    ],
                    'parse type':'update',
                    'type':'zip',
                },
                'service.document.tvdb.update.weekly':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/week$',
                            'remote':ur'{api key}/updates/updates_week.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb weekly update',
                            'format':ur'/c/tvdb/update/week',
                            'canonical':True,
                        },
                    ],
                    'parse type':'update',
                    'type':'zip',
                },
                'service.document.tvdb.update.monthly':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/month$',
                            'remote':ur'{api key}/updates/updates_month.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb monthly update',
                            'format':ur'/c/tvdb/update/month',
                            'canonical':True,
                        },
                    ],
                    'parse type':'update',
                    'type':'zip',
                },
            },
        },
        'itunes':{
            'remote base':u'http://itunes.apple.com',
            'match':ur'^/c(?:/[a-z]{2})?/itunes/.*$',
            'branch':{
                'service.document.itunes.genre':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/genre/(?P<itunes_genre_id>[0-9]+)$',
                            'query parameter':set(('itunes genre id',)),
                            'remote':'WebObjects/MZStoreServices.woa/ws/genres',
                        },
                    ],
                    'process':'parse_itunes_genres',
                    'produce':[
                        {
                            'reference':'service.document.itunes.genre',
                            'condition':{'kind': 'genre'},
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes genre by itunes id',
                            'format':ur'/c/itunes/genre/{itunes genre id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'itunes_genre',
                    'namespace':'ns.knowledge.genre',
                    'type':'json',
                    'index':[
                        'itunes genre id',
                        'genre name',
                        'simple genre name',
                    ],
                },
                'service.document.itunes.person':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/person/(?P<itunes_person_id>[0-9]+)$',
                            'query parameter':set(('itunes person id',)),
                            'remote':ur'lookup',
                        },
                        {
                            'filter':ur'^/c/itunes/person/search$',
                            'query parameter':set(('term',)),
                            'remote':ur'search?entity=movieArtist&attribute=artistTerm',
                        },
                    ],
                    'produce':[
                        {
                            'reference':'service.document.itunes.person',
                            'condition':{'wrapperType':'artist', 'artistType':'Movie Artist'}
                        },
                        {
                            'reference':'service.document.itunes.person',
                            'condition':{'wrapperType':'artist', 'artistType':'Artist'}
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'itunes person by itunes id',
                            'format':ur'/c/itunes/person/{itunes person id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'itunes_person',
                    'namespace':'ns.knowledge.person',
                    'type':'json',
                    'index':[
                        'itunes person id',
                        'person name',
                        'simple person name',
                    ],
                },
                'service.document.itunes.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/movie/(?P<itunes_movie_id>[0-9]+)$',
                            'query parameter':set(('itunes movie id',)),
                            'remote':ur'lookup?entity=movie',
                        },
                        {
                            'filter':ur'^/c/itunes/movie/search$',
                            'query parameter':set(('term',)),
                            'remote':ur'search?entity=movie&attribute=movieTerm',
                        },
                    ],
                    'produce':[
                        {
                            'reference':'service.document.itunes.movie',
                            'condition':{'wrapperType':'track', 'kind': 'feature-movie'},
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes movie by itunes id',
                            'format':ur'/c/itunes/movie/{itunes movie id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'itunes_movie',
                    'namespace':'ns.knowledge.movie',
                    'type':'json',
                    'index':[
                        'itunes movie id',
                        'movie title',
                        'simple movie title',
                    ],
                },
                'service.document.itunes.tv.show':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/tv/show/(?P<itunes_tv_show_id>[0-9]+)$',
                            'query parameter':set(('itunes tv show id',)),
                            'remote':ur'lookup?entity=tvShow',
                        },
                        {
                            'filter':ur'^/c/itunes/tv/show/search$',
                            'query parameter':set(('term',)),
                            'remote':ur'search?entity=tvShow&attribute=showTerm',
                        },
                    ],
                    'produce':[
                        {
                            'reference':'service.document.itunes.tv.show',
                            'condition':{'wrapperType':'artist', 'artistType':'TV Show'},
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes tv show by itunes id',
                            'format':ur'/c/itunes/tv/show/{itunes tv show id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'itunes_tv_show',
                    'namespace':'ns.knowledge.tv.show',
                    'type':'json',
                    'index':[
                        'itunes tv show id',
                        'tv show name',
                        'simple tv show name',
                    ],
                },
                'service.document.itunes.tv.season':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/tv/season/(?P<itunes_tv_season_id>[0-9]+)$',
                            'query parameter':set(('itunes tv season id',)),
                            'remote':ur'lookup?entity=tvSeason',
                        },
                        {
                            'filter':ur'^/c/itunes/tv/season/(?P<itunes_tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)$',
                            'query parameter':set(('itunes tv show id',)),
                            'remote':ur'lookup?entity=tvSeason&limit=500',
                        },
                    ],
                    'produce':[
                        {
                            'reference':'service.document.itunes.tv.show',
                            'condition':{'wrapperType':'artist', 'artistType':'TV Show'},
                        },
                        {
                            'reference':'service.document.itunes.tv.season',
                            'condition':{'wrapperType':'collection', 'collectionType':'TV Season'},
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes tv season by itunes id',
                            'format':ur'/c/itunes/tv/season/{itunes tv season id}',
                            'canonical':True,
                        },
                        {
                            'name':'itunes tv season by itunes show id',
                            'format':ur'/c/itunes/tv/season/{itunes tv show id}/{disc number}',
                        },
                    ],
                    'collection':'itunes_tv_season',
                    'namespace':'ns.knowledge.tv.season',
                    'type':'json',
                    'index':[
                        'itunes tv show id',
                        'itunes tv season id',
                        'disc number',
                        'tv show name',
                        'simple tv show name',
                    ],
                },
                'service.document.itunes.tv.episode':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/tv/episode/(?P<itunes_tv_episode_id>[0-9]+)$',
                            'query parameter':set(('itunes tv episode id',)),
                            'remote':ur'lookup?entity=tvEpisode',
                        },
                        {
                            'filter':ur'^/c/itunes/tv/episode/(?P<itunes_tv_season_id>[0-9]+)/(?P<track_number>[0-9]+)$',
                            'query parameter':set(('itunes tv season id',)),
                            'remote':ur'lookup?entity=tvEpisode&limit=500',
                        },
                        {
                            'filter':ur'^/c/itunes/tv/episode/(?P<itunes_tv_show_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                            'query parameter':set(('itunes tv show id',)),
                            'remote':ur'lookup?entity=tvEpisode&limit=500',
                        },
                    ],
                    'produce':[
                        {
                            'reference':'service.document.itunes.tv.show',
                            'condition':{'wrapperType':'artist', 'artistType':'TV Show'},
                        },
                        {
                            'reference':'service.document.itunes.tv.season',
                            'condition':{'wrapperType':'collection', 'collectionType':'TV Season'},
                        },
                        {
                            'reference':'service.document.itunes.tv.episode',
                            'condition':{'wrapperType':'track', 'kind':'tv-episode'},
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes tv episode by itunes id',
                            'format':ur'/c/itunes/tv/episode/{itunes tv episode id}',
                            'canonical':True,
                        },
                        {
                            'name':'itunes tv episode by itunes season id',
                            'format':ur'/c/itunes/tv/episode/{itunes tv season id}/{track number}',
                        },
                        {
                            'name':'itunes tv episode by itunes show id',
                            'format':ur'/c/itunes/tv/episode/{itunes tv show id}/{disc number}/{track number}',
                        },
                    ],
                    'collection':'itunes_tv_episode',
                    'namespace':'ns.knowledge.tv.episode',
                    'type':'json',
                    'index':[
                        'itunes tv show id',
                        'itunes tv season id',
                        'itunes tv episode id',
                        'disc number',
                        'track number',
                        'tv show name',
                        'tv episode name',
                        'simple tv show name',
                        'simple tv episode name',
                    ],
                },
                'service.document.itunes.music.album':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/music/album/(?P<itunes_music_album_id>[0-9]+)$',
                            'query parameter':set(('itunes music album id',)),
                            'remote':ur'lookup?entity=album',
                        },
                        {
                            'filter':ur'^/c/itunes/music/album/search$',
                            'query parameter':set(('term',)),
                            'remote':ur'search?entity=album&attribute=albumTerm',
                        },
                    ],
                    'produce':[
                        {
                            'reference':'service.document.itunes.music.album',
                            'condition':{'wrapperType':'collection', 'collectionType':'Album'},
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes album by itunes id',
                            'format':ur'/c/itunes/music/album/{itunes music album id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'itunes_music_album',
                    'namespace':'ns.knowledge.music.album',
                    'type':'json',
                    'index':[
                        'itunes music album id',
                        'music album name',
                        'simple music album name',
                    ],
                },
                'service.document.itunes.music.track':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/music/track/(?P<itunes_music_track_id>[0-9]+)$',
                            'query parameter':set(('itunes music track id',)),
                            'remote':ur'lookup?entity=song',
                        },
                        {
                            'filter':ur'^/c/itunes/music/track/(?P<itunes_music_album_id>[0-9]+)/(?P<disc_number>[0-9]+)/(?P<track_number>[0-9]+)$',
                            'query parameter':set(('itunes music album id',)),
                            'remote':ur'lookup?entity=song&limit=500',
                        },
                    ],
                    'produce':[
                        {
                            'reference':'service.document.itunes.music.track',
                            'condition':{'wrapperType':'track', 'kind':'song'},
                        },
                        {
                            'reference':'service.document.itunes.music.album',
                            'condition':{'wrapperType':'collection', 'collectionType':'Album'},
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes music track by itunes id',
                            'format':ur'/c/itunes/music/track/{itunes music track id}',
                            'canonical':True,
                        },
                        {
                            'name':'itunes music track by itunes album id',
                            'format':ur'/c/itunes/music/track/{itunes music album id}/{disc number}/{track number}',
                        },
                    ],
                    'collection':'itunes_music_track',
                    'namespace':'ns.knowledge.music.track',
                    'type':'json',
                    'index':[
                        'itunes music track id',
                        'itunes music album id',
                        'disc number',
                        'track number',
                        'music album name',
                        'music track name',
                        'simple music album name',
                        'simple music track name',
                    ],
                },
                'service.document.itunes.genre.complete':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/genre/complete',
                            'remote':'WebObjects/MZStoreServices.woa/ws/genres',
                        },
                    ],
                    'process':'parse_itunes_genres',
                    'produce':[
                        {
                            'reference':'service.document.itunes.genre',
                            'condition':{'kind': 'genre'},
                        },
                    ],
                    'namespace':'ns.knowledge.genre',
                    'type':'json',
                    'index':['itunes genre id'],
                },
            },
        },
        'rottentomatoes':{
            'api key':u'wyeeuz4yjjqvyjgtju68c6p3',
            'remote base':u'http://api.rottentomatoes.com/api/public/v1.0',
            'match':ur'^/c(?:/[a-z]{2})?/rottentomatoes/.*$',
            'branch':{
                'service.document.rottentomatoes.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movies/{rottentomatoes movie id}.json',
                        },
                        {
                            'filter':ur'^/c/rottentomatoes/movie/imdb/(?P<imdb_movie_id>tt[0-9]+)$',
                            'query parameter':set(('api key', 'trimmed imdb movie id')),
                            'remote':ur'movie_alias.json?type=imdb',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'rotten tomatoes movie by rottentomatoes movie id',
                            'format':ur'/c/rottentomatoes/movie/{rottentomatoes movie id}',
                            'canonical':True,
                        },
                        {
                            'name':u'rotten tomatoes movie by imdb id',
                            'format':ur'/c/rottentomatoes/movie/imdb/{imdb movie id}',
                        }
                    ],
                    'collection':'rottentomatoes_movie',
                    'namespace':'ns.knowledge.movie',
                    'type':'json',
                    'index':[
                        'rottentomatoes movie id',
                        'imdb movie id',
                        'movie title',
                        'simple movie title',
                    ],
                },
                'service.document.rottentomatoes.movie.review':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/review$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movies/{rottentomatoes movie id}/reviews.json?review_type=top_critic',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'rotten tomatoes movie review by rottentomatoes movie id',
                            'format':ur'/c/rottentomatoes/movie/{rottentomatoes movie id}/review',
                            'canonical':True,
                        },
                    ],
                    'collection':'rottentomatoes_movie_review',
                    'namespace':'ns.knowledge.movie',
                    'type':'json',
                    'index':['rottentomatoes movie id'],
                },
                'service.document.rottentomatoes.movie.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/cast$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movies/{rottentomatoes movie id}/cast.json',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'rotten tomatoes movie cast by rottentomatoes movie id',
                            'format':ur'/c/rottentomatoes/movie/{rottentomatoes movie id}/cast',
                            'canonical':True,
                        },
                    ],
                    'collection':'rottentomatoes_movie_cast',
                    'namespace':'ns.knowledge.movie',
                    'type':'json',
                    'index':['rottentomatoes movie id'],
                },

                'service.document.rottentomatoes.movie.similar':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/similar$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movies/{rottentomatoes movie id}/similar.json',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'rotten tomatoes similar movies by rottentomatoes movie id',
                            'format':ur'/c/rottentomatoes/movie/{rottentomatoes movie id}/similar',
                            'canonical':True,
                        },
                    ],
                    'collection':'rottentomatoes_movie_similar',
                    'namespace':'ns.knowledge.movie',
                    'type':'json',
                    'index':['rottentomatoes movie id'],
                },
                'service.document.rottentomatoes.movie.clip':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/clip$',
                            'query parameter':set(('api key',)),
                            'remote':ur'movies/{rottentomatoes movie id}/clips.json',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'rotten tomatoes movie clip by rottentomatoes movie id',
                            'format':ur'/c/rottentomatoes/movie/{rottentomatoes movie id}/clip',
                            'canonical':True,
                        },
                    ],
                    'collection':'rottentomatoes_movie_clip',
                    'namespace':'ns.knowledge.movie',
                    'type':'json',
                    'index':['rottentomatoes movie id'],
                },
            },
        },
        'facebook':{
            'match':ur'^/c/facebook/.*$',
            'remote base':u'http://graph.facebook.com',
            'branch':{
                'facebook.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/facebook/movie/(?P<facebook_movie_id>[0-9]+)$',
                            'remote':ur'{facebook movie id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'facebook movie by facebook id',
                            'format':ur'/c/facebook/movie/{facebook movie id}',
                        }
                    ],
                    'collection':'facebook_movie',
                    'namespace':'ns.facebook.movie',
                    'type':'json',
                    'index':['facebook movie id'],
                },
            },
        },
        'wikipedia':{
            'match':ur'^/c(?:/[a-z]{2})?/wikipedia/.*$',
            'branch':{
                'wikipedia.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/wikipedia/movie/(?P<wikipedia_movie_id>[0-9]+)$',
                            'remote':ur'',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'wikipedia movie by wikipedia id',
                            'format':ur'/c/wikipedia/movie/{wikipedia movie id}',
                        }
                    ],
                    'collection':'wikipedia_movie',
                    'namespace':'ns.wikipedia.movie',
                    'type':'json',
                    'index':['wikipedia movie id'],
                },
                'wikipedia.person':{
                },
                'wikipedia.company':{
                },
                'wikipedia.tvshow.show':{
                },
            },
        },
    },
}
