# -*- coding: utf-8 -*-

{
    'service':{
        'home':{
            'match':ur'^/h/.*$',
            'key generator':'knowledge',
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
                        'movie handle',
                        'rottentomatoes movie id',
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
                            'depend':ur'/c/{language}/tvdb/show/{tvdb tv show id}',
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
                        'tv show handle',
                        'tvdb tv show id',
                        'imdb tv show id',
                    ],
                },
                'service.home.tv.season':{
                    'match':[
                        {
                            'filter':ur'^/h/tv/season/(?P<disk_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/season/tvdb/(?P<tvdb_tv_season_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/season/{tvdb tv season id}',
                        },
                        {
                            'filter':ur'^/h/tv/season/tvdb/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/season/{tvdb tv show id}/{disk position}',
                        },
                        {
                            'filter':ur'^/h/tv/season/imdb/(?P<imdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
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
                            'name':u'season home by disk id',
                            'format':ur'/h/tv/season/{disk id}',
                        },
                        {
                            'name':u'season home by tv show id',
                            'format':ur'/h/tv/season/{tv show id}/{disk position}',
                        },
                        {
                            'name':u'season home by tvdb tv season id',
                            'format':ur'/h/tv/season/tvdb/{tvdb tv season id}',
                        },
                        {
                            'name':u'season home by tvdb tv show id',
                            'format':ur'/h/tv/season/tvdb/{tvdb tv show id}/{disk position}',
                        },
                        {
                            'name':u'season home by imdb tv show id',
                            'format':ur'/h/tv/season/imdb/{imdb tv show id}/{disk position}',
                        },
                    ],
                    'collection':'home',
                    'key':'disk id',
                    'index':[
                        'tv show id',
                        'disk id',
                        'disk position',
                        'tvdb tv show id',
                        'imdb tv show id',
                        'tvdb tv season id',
                    ],
                },
                'service.home.tv.episode':{
                    'match':[
                        {
                            'filter':ur'^/h/tv/episode/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/(?P<disk_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/~/(?P<tv_show_handle>[^/]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/tvdb/(?P<tvdb_tv_episode_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/episode/{tvdb tv episode id}',
                        },
                        {
                            'filter':ur'^/h/tv/episode/tvdb/(?P<tvdb_tv_season_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/episode/{tvdb tv season id}/{track position}',
                        },
                        {
                            'filter':ur'^/h/tv/episode/tvdb/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/episode/{tvdb tv show id}/{disk position}/{track position}',
                        },
                        {
                            'filter':ur'^/h/tv/episode/imdb/(?P<imdb_tv_episode_id>tt[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tv/episode/imdb/(?P<imdb_tv_show_id>tt[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'collect':[
                        ur'/h/tv/season/tvdb/{tvdb tv show id}/{disk position}',
                        ur'/h/tv/season/tvdb/{tvdb tv season id}',
                    ],
                    'resolvable':[
                        {
                            'name':u'episode home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'episode home by track id',
                            'format':ur'/h/tv/episode/{track id}',
                        },
                        {
                            'name':u'episode home by disk id',
                            'format':ur'/h/tv/episode/{disk id}/{track position}',
                        },
                        {
                            'name':u'episode home by tv show id',
                            'format':ur'/h/tv/episode/{tv show id}/{disk position}/{track position}',
                        },
                        {
                            'name':u'episode home by tv show handle',
                            'format':ur'/h/tv/episode/~/{tv show handle}/{disk position}/{track position}',
                        },
                        {
                            'name':u'episode home by tvdb tv episode id',
                            'format':ur'/h/tv/episode/tvdb/{tvdb tv episode id}',
                        },
                        {
                            'name':u'episode home by tvdb tv season id',
                            'format':ur'/h/tv/episode/tvdb/{tvdb tv season id}/{track position}',
                        },
                        {
                            'name':u'episode home by tvdb tv show id',
                            'format':ur'/h/tv/episode/tvdb/{tvdb tv show id}/{disk position}/{track position}',
                        },
                        {
                            'name':u'episode home by imdb tv episode id',
                            'format':ur'/h/tv/episode/imdb/{imdb tv episode id}',
                        },
                        {
                            'name':u'episode home by imdb tv show id',
                            'format':ur'/h/tv/episode/imdb/{imdb tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'collection':'home',
                    'key':'track id',
                    'index':[
                        'tv show id',
                        'disk id',
                        'track id',
                        'disk position',
                        'track position'
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'tvdb tv episode id',
                        'imdb tv show id',
                        'imdb tv episode id',
                    ],
                },
                'service.home.music.album':{
                    'match':[
                        {
                            'filter':ur'^/h/music/album/(?P<album_id>[0-9]+)$',
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
                            'name':u'music album home by album handle',
                            'format':ur'/h/music/album/~/{album handle}',
                        },
                    ],
                    'collection':'home',
                    'key':'album id',
                    'index':['album id', 'album handle'],
                },
                'service.home.music.disk':{
                    'match':[
                        {
                            'filter':ur'^/h/music/disk/(?P<disk_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/disk/(?P<album_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/disk/~/(?P<album_handle>[^/]+)/(?P<disk_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music disk home by home id',
                            'format':ur'/h/{home id}',
                            'canonical':True,
                        },
                        {
                            'name':u'music disk home by disk id',
                            'format':ur'/h/music/disk/{disk id}',
                        },
                        {
                            'name':u'music disk home by album id',
                            'format':ur'/h/music/disk/{album id}/{disk position}',
                        },
                        {
                            'name':u'music disk home by album handle',
                            'format':ur'/h/music/disk/~/{album handle}/{disk position}',
                        },
                    ],
                    'collection':'home',
                    'key':'disk id',
                    'index':['album id', 'disk id', 'disk position', 'album handle'],
                },
                'service.home.music.track':{
                    'match':[
                        {
                            'filter':ur'^/h/music/track/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/track/(?P<disk_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/track/(?P<album_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/music/track/~/(?P<album_handle>[^/]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
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
                            'name':u'music track home by disk id',
                            'format':ur'/h/music/track/{disk id}/{track position}',
                        },
                        {
                            'name':u'music track home by album id',
                            'format':ur'/h/music/track/{album id}/{disk position}/{track position}',
                        },
                        {
                            'name':u'music track home by album handle',
                            'format':ur'/h/music/track/~/{album handle}/{disk position}/{track position}',
                        },
                    ],
                    'collection':'home',
                    'key':'track id',
                    'index':['album id', 'disk id', 'track id', 'disk position', 'track position', 'album handle'],
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
                    ],
                    'collection':'home',
                    'key':'person id',
                    'index':['person id', 'tmdb person id'],
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
                    'index':['company id', 'tmdb company id'],
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
                    ],
                    'collection':'home',
                    'key':'genre id',
                    'index':['genre id', 'tmdb genre id'],
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
                'service.knowledge.music.disk':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/disk/(?P<disk_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/disk/(?P<album_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music disk by disk id',
                            'format':ur'/k/{language}/music/disk/{disk id}',
                        },
                        {
                            'name':u'music disk by album id',
                            'format':ur'/k/{language}/music/disk/{album id}/{disk position}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_music_disk',
                    'namespace':'knowledge.music.disk',
                    'index':['album id', 'disk id', 'disk position', 'language'],
                },
                'service.knowledge.music.track':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/track/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/track/(?P<disk_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/music/track/(?P<album_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music track by track id',
                            'format':ur'/k/{language}/music/track/{track id}',
                        },
                        {
                            'name':u'music track by disk id',
                            'format':ur'/k/{language}/music/track/{disk id}/{track position}',
                        },
                        {
                            'name':u'music track by album id',
                            'format':ur'/k/{language}/music/track/{album id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_music_track',
                    'namespace':'knowledge.music.track',
                    'index':['album id', 'disk id', 'track id', 'disk position', 'track position', 'language'],
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
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/season/(?P<disk_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'season knowledge by disk id',
                            'format':ur'/k/{language}/tv/season/{disk id}',
                        },
                        {
                            'name':u'season knowledge by tv show id and position',
                            'format':ur'/k/{language}/tv/season/{tv show id}/{disk position}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season',
                    'namespace':'ns.knowledge.tv.season',
                    'index':['tv show id', 'disk id', 'disk position'],
                },
                'service.knowledge.tv.season.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show season image',
                            'format':ur'/k/tv/season/{tv show id}/{disk position}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season_image',
                    'namespace':'knowledge.tv.season.image',
                },
                'service.knowledge.tv.season.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show season image',
                            'format':ur'/k/tv/season/{tv show id}/{disk position}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season_credit',
                    'namespace':'knowledge.tv.season.credit',
                },
                'service.knowledge.tv.episode':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/episode/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/episode/(?P<disk_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'episode knowledge by track id',
                            'format':ur'/k/{language}/tv/episode/{track id}',
                        },
                        {
                            'name':u'episode knowledge by disk id',
                            'format':ur'/k/{language}/tv/episode/{disk id}/{track position}',
                        },
                        {
                            'name':u'episode knowledge by tv show id',
                            'format':ur'/k/{language}/tv/episode/{tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode',
                    'namespace':'ns.knowledge.tv.episode',
                    'index':['tv show id', 'track id', 'disk id', 'disk position', 'track position', 'language'],
                },
                'service.knowledge.tv.episode.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode image',
                            'format':ur'/k/tv/episode/{tv show id}/{disk position}/{track position}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode_image',
                    'namespace':'knowledge.tv.episode.image',
                },
                'service.knowledge.tv.episode.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tv/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode credit',
                            'format':ur'/k/tv/episode/{tv show id}/{disk position}/{track position}/credit',
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
                            'name':u'genre',
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
                'service.remote.tmdb.configuration':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/configuration$',
                            'remote':ur'configuration?api_key={api key}',
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
                    'type':'json',
                },
                'service.remote.tmdb.genre':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/genre/(?P<tmdb_genre_id>[0-9]+)$',
                            'remote':ur'genre/{tmdb genre id}?language={language}&api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb genre id'],
                },
                'service.remote.tmdb.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)$',
                            'remote':ur'movie/{tmdb movie id}?language={language}&api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/imdb/(?P<imdb_movie_id>tt[0-9]+)$',
                            'remote':ur'movie/{imdb movie id}?language={language}&api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id', 'language', 'imdb movie id'],
                },
                'service.remote.tmdb.movie.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/cast$',
                            'remote':ur'movie/{tmdb movie id}/casts?api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'service.remote.tmdb.movie.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/image$',
                            'remote':ur'movie/{tmdb movie id}/images?api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'service.remote.tmdb.movie.keyword':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/keyword$',
                            'remote':ur'movie/{tmdb movie id}/keywords?api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'service.remote.tmdb.movie.rating':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/rating$',
                            'remote':ur'movie/{tmdb movie id}/releases?api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'service.remote.tmdb.movie.clip':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/clip$',
                            'remote':ur'movie/{tmdb movie id}/trailers?api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'service.remote.tmdb.movie.translation':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/translation$',
                            'remote':ur'movie/{tmdb movie id}/translations?api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'service.remote.tmdb.movie.alternative':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/alternative$',
                            'remote':ur'movie/{tmdb movie id}/alternative_titles?api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'service.remote.tmdb.collection':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/collection/(?P<tmdb_collection_id>[0-9]+)$',
                            'remote':ur'collection/{tmdb collection id}?language={language}&api_key={api key}',
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
                    'type':'json',
                    'index':['tmdb collection id', 'language'],
                },
                'service.remote.tmdb.person':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)$',
                            'remote':ur'person/{tmdb person id}?api_key={api key}',
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
                    'type':'json',
                },
                'service.remote.tmdb.person.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/image$',
                            'remote':ur'person/{tmdb person id}/images?api_key={api key}',
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
                    'type':'json',
                },
                'service.remote.tmdb.person.credit':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/credit$',
                            'remote':ur'person/{tmdb person id}/credits?api_key={api key}',
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
                    'type':'json',
                },
                'service.remote.tmdb.company':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/company/(?P<tmdb_company_id>[0-9]+)$',
                            'remote':ur'company/{tmdb company id}?api_key={api key}',
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
                    'type':'json',
                },
                'service.remote.tmdb.company.credit':{
                    # There is the issue of paging... page={page}&
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/company/(?P<tmdb_company_id>[0-9]+)/credit$',
                            'remote':ur'company/{tmdb company id}/movies?api_key={api key}',
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
                    'type':'json',
                },
            },
        },
        'tvdb':{
            'api key':u'7B3B400B0146EA83',
            'remote base':u'http://www.thetvdb.com/api',
            'match':ur'^/c(?:/[a-z]{2})?/tvdb/.*$',
            'branch':{
                'service.remote.tvdb.show':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/{language}.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show by tvdb show id',
                            'format':ur'/c/{language}/tvdb/show/{tvdb tv show id}',
                            'canonical':True,
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Series',
                            'reference':'service.remote.tvdb.show',
                            'coalesce':False,
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'imdb tv show id',
                    ],
                    'collection':'tvdb_tv_show',
                    'namespace':'ns.knowledge.tv.show',
                    'type':'xml',
                },
                'service.remote.tvdb.show.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/cast$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/actors.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show cast by tvdb show id',
                            'format':ur'/c/tvdb/show/{tvdb tv show id}/cast',
                            'canonical':True,
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Actor',
                            'reference':'service.remote.tvdb.show.cast',
                            'coalesce':True,
                        },
                    ],
                    'collection':'tvdb_tv_show_cast',
                    'namespace':'ns.knowledge.cast',
                    'type':'xml',
                },
                'service.remote.tvdb.show.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/image$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/banners.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show image by tvdb show id',
                            'format':ur'/c/tvdb/show/{tvdb tv show id}/image',
                            'canonical':True,
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Banner',
                            'reference':'service.remote.tvdb.show.image',
                            'coalesce':True,
                        },
                    ],
                    'collection':'tvdb_tv_show_image',
                    'namespace':'ns.knowledge.image',
                    'type':'xml',
                },
                'service.remote.tvdb.season':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/season/(?P<tvdb_tv_season_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/season/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb season by tvdb season id',
                            'format':ur'/c/{language}/tvdb/season/{tvdb tv season id}',
                            'canonical':True,
                        },
                        {
                            'name':u'tvdb season by tvdb show id',
                            'format':ur'/c/{language}/tvdb/season/{tvdb tv show id}/{disk position}',
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'imdb tv show id',
                        'disk position',
                    ],
                    'collection':'tvdb_tv_season',
                    'namespace':'ns.knowledge.tv.season',
                    'type':'xml',
                },
                'service.remote.tvdb.episode':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/episode/(?P<tvdb_tv_episode_id>[0-9]+)$',
                            'remote':ur'{api key}/episodes/{tvdb tv episode id}/{language}.xml',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/episode/(?P<tvdb_tv_season_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/episode/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/default/{disk position}/{track position}/{language}.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb episode by tvdb episode id',
                            'format':ur'/c/{language}/tvdb/episode/{tvdb tv episode id}',
                            'canonical':True,
                        },
                        {
                            'name':u'tvdb episode by tvdb season id',
                            'format':ur'/c/{language}/tvdb/episode/{tvdb tv season id}/{track position}',
                        },
                        {
                            'name':u'tvdb episode by tvdb show id',
                            'format':ur'/c/{language}/tvdb/episode/{tvdb tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Episode',
                            'reference':'service.remote.tvdb.episode',
                            'coalesce':False,
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'tvdb tv episode id',
                        'imdb tv show id',
                        'imdb tv episode id',
                        'disk position',
                        'track position',
                    ],
                    'collection':'tvdb_tv_episode',
                    'namespace':'ns.knowledge.tv.episode',
                    'type':'xml',
                },
                'service.remote.tvdb.show.complete':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/complete$',
                            'remote':ur'{api key}/series/{tvdb tv show id}/all/{language}.zip',
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Series',
                            'reference':'service.remote.tvdb.show',
                            'coalesce':False,
                        },
                        {
                            'tag':u'Episode',
                            'reference':'service.remote.tvdb.episode',
                            'coalesce':False,
                        },
                        {
                            'tag':u'Banner',
                            'reference':'service.remote.tvdb.show.image',
                            'coalesce':True,
                        },
                        {
                            'tag':u'Actor',
                            'reference':'service.remote.tvdb.show.cast',
                            'coalesce':True,
                        },
                    ],
                    'type':'zip',
                },
                'service.remote.tvdb.update.daily':{
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
                    'type':'zip',
                },
                'service.remote.tvdb.update.weekly':{
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
                    'type':'zip',
                },
                'service.remote.tvdb.update.monthly':{
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
                    'type':'zip',
                },
            },
        },
        'itunes':{
            'remote base':u'http://itunes.apple.com',
            'match':ur'^/c(?:/[a-z]{2})?/itunes/.*$',
            'branch':{
                'service.remote.itunes.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/movie/(?P<itunes_movie_id>[0-9]+)$',
                            'remote':ur'lookup?id={itunes movie id}&entity=movie',
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
                    'index':['itunes movie id'],
                },
                'service.remote.itunes.person':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/person/(?P<itunes_person_id>[0-9]+)$',
                            'remote':ur'lookup?id={itunes person id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'itunes person by itunes id',
                            'format':ur'/c/itunes/person/{itunes movie id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'itunes_person',
                    'namespace':'ns.knowledge.person',
                    'type':'json',
                    'index':['itunes person id'],
                },
                'service.remote.itunes.show':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/show/(?P<itunes_tv_show_id>[0-9]+)$',
                            'remote':ur'lookup?id={itunes tv show id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes tv show by itunes id',
                            'format':ur'/c/itunes/show/{itunes tv show id}',
                            'canonical':True,
                        },
                    ],
                    'collection':'itunes_tv_show',
                    'namespace':'ns.knowledge.tv.show',
                    'type':'json',
                    'index':['itunes tv show id'],
                },
                'service.remote.itunes.season':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/season/(?P<itunes_tv_season_id>[0-9]+)$',
                            'remote':ur'lookup?id={itunes tv season id}',
                        },
                        {
                            'filter':ur'^/c/itunes/season/(?P<itunes_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes tv season by itunes id',
                            'format':ur'/c/itunes/season/{itunes tv season id}',
                            'canonical':True,
                        },
                        {
                            'name':'itunes tv season by itunes show id',
                            'format':ur'/c/itunes/season/{itunes tv show id}/{disk position}',
                        },
                    ],
                    'collection':'itunes_tv_season',
                    'namespace':'ns.knowledge.tv.season',
                    'type':'json',
                    'index':['itunes tv show id', 'itunes tv season id', 'disk position'],
                },
                'service.remote.itunes.episode':{
                    'match':[
                        {
                            'filter':ur'^/c/itunes/episode/(?P<itunes_tv_episode_id>[0-9]+)$',
                            'remote':ur'lookup?id={itunes tv episode id}',
                        },
                        {
                            'filter':ur'^/c/itunes/episode/(?P<itunes_tv_season_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/c/itunes/episode/(?P<itunes_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':'itunes tv episode by itunes id',
                            'format':ur'/c/itunes/episode/{itunes tv episode id}',
                            'canonical':True,
                        },
                        {
                            'name':'itunes tv episode by itunes season id',
                            'format':ur'/c/itunes/episode/{itunes tv season id}/{track position}',
                        },
                        {
                            'name':'itunes tv episode by itunes show id',
                            'format':ur'/c/itunes/episode/{itunes tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'collection':'itunes_tv_episode',
                    'namespace':'ns.knowledge.tv.episode',
                    'type':'json',
                    'index':['itunes tv show id', 'itunes tv season id', 'itunes tv episode id', 'disk position', 'track position'],
                },
            },
        },
        'rottentomatoes':{
            'api key':u'wyeeuz4yjjqvyjgtju68c6p3',
            'remote base':u'http://api.rottentomatoes.com/api/public/v1.0',
            'match':ur'^/c(?:/[a-z]{2})?/rottentomatoes/.*$',
            'branch':{
                'service.remote.rottentomatoes.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)$',
                            'remote':ur'movies/{rottentomatoes movie id}.json?apikey={api key}',
                        },
                        {
                            'filter':ur'^/c/rottentomatoes/movie/imdb/(?P<imdb_movie_id>tt[0-9]+)$',
                            'remote':ur'movie_alias.json?apikey={api key}&type=imdb&id={trimmed imdb movie id}',
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
                    'index':['rottentomatoes movie id', 'imdb movie id'],
                },
                'service.remote.rottentomatoes.movie.review':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/review$',
                            'remote':ur'movies/{rottentomatoes movie id}/reviews.json?review_type=top_critic&apikey={api key}',
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
                'service.remote.rottentomatoes.movie.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/cast$',
                            'remote':ur'movies/{rottentomatoes movie id}/cast.json?apikey={api key}',
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
                
                'service.remote.rottentomatoes.movie.similar':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/similar$',
                            'remote':ur'movies/{rottentomatoes movie id}/similar.json?apikey={api key}',
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
                'service.remote.rottentomatoes.movie.clip':{
                    'match':[
                        {
                            'filter':ur'^/c/rottentomatoes/movie/(?P<rottentomatoes_movie_id>[0-9]+)/clip$',
                            'remote':ur'movies/{rottentomatoes movie id}/clips.json?apikey={api key}',
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
