# -*- coding: utf-8 -*-

configuration = {
    'service':{
        'home':{
            'match':ur'^/h/.*$',
            'branch':{
                'home.movie':{
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
                    ],
                    'resolvable':[
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
                    ],
                    'type':'json',
                    'collection':'home_movie',
                    'namespace':'home.movie',
                    'generate':{'name':'knowledge', 'key':'movie id'},
                    'index':['movie id', 'tmdb movie id', 'imdb movie id', 'movie handle'],
                },
                'home.tvshow.show':{
                    'match':[
                        {
                            'filter':ur'^/h/tvshow/show/(?P<tv_show_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tvshow/show/~/(?P<tv_show_handle>[^/]+)$',
                        },
                        {
                            'filter':ur'^/h/tvshow/show/tvdb/(?P<tvdb_tv_show_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/show/{tvdb tv show id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'show home by tv show id',
                            'format':ur'/h/tvshow/show/{tv show id}',
                        },
                        {
                            'name':u'show home by tv show handle',
                            'format':ur'/h/tvshow/show/~/{tv show handle}',
                        },
                        {
                            'name':u'show home by tvdb tv show id',
                            'format':ur'/h/tvshow/show/tvdb/{tvdb tv show id}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_tvshow_show',
                    'namespace':'home.tvshow.show',
                    'generate':{'name':'knowledge', 'key':'tv show id'},
                    'index':[
                        'tv show id',
                        'tv show handle',
                        'tvdb tv show id',
                    ],
                },
                'home.tvshow.season':{
                    'match':[
                        {
                            'filter':ur'^/h/tvshow/season/(?P<disk_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tvshow/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tvshow/season/tvdb/(?P<tvdb_tv_season_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/season/{tvdb tv season id}',
                        },
                        {
                            'filter':ur'^/h/tvshow/season/tvdb/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/season/{tvdb tv show id}/{disk position}',
                        },
                    ],
                    'collect':[
                        ur'/h/tvshow/show/tvdb/{tvdb tv show id}',
                    ],
                    'resolvable':[
                        {
                            'name':u'season home by disk id',
                            'format':ur'/h/tvshow/season/{disk id}',
                        },
                        {
                            'name':u'season home by tv show id',
                            'format':ur'/h/tvshow/season/{tv show id}/{disk position}',
                        },
                        {
                            'name':u'season home by tvdb tv season id',
                            'format':ur'/h/tvshow/season/tvdb/{tvdb tv season id}',
                        },
                        {
                            'name':u'season home by tvdb tv show id',
                            'format':ur'/h/tvshow/season/tvdb/{tvdb tv show id}/{disk position}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_tvshow_season',
                    'namespace':'home.tvshow.season',
                    'generate':{'name':'knowledge', 'key':'disk id'},
                    'index':[
                        'tv show id',
                        'disk id',
                        'disk position',
                        'tvdb tv show id',
                        'tvdb tv season id',
                    ],
                },
                'home.tvshow.episode':{
                    'match':[
                        {
                            'filter':ur'^/h/tvshow/episode/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tvshow/episode/(?P<disk_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tvshow/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/tvshow/episode/tvdb/(?P<tvdb_tv_episode_id>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/episode/{tvdb tv episode id}',
                        },
                        {
                            'filter':ur'^/h/tvshow/episode/tvdb/(?P<tvdb_tv_season_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/episode/{tvdb tv season id}/{track position}',
                        },
                        {
                            'filter':ur'^/h/tvshow/episode/tvdb/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                            'depend':ur'/c/{language}/tvdb/episode/{tvdb tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'collect':[
                        ur'/h/tvshow/season/tvdb/{tvdb tv show id}/{disk position}',
                        ur'/h/tvshow/season/tvdb/{tvdb tv season id}',
                    ],
                    'resolvable':[
                        {
                            'name':u'episode home by track id',
                            'format':ur'/h/tvshow/episode/{track id}',
                        },
                        {
                            'name':u'episode home by disk id',
                            'format':ur'/h/tvshow/episode/{disk id}/{track position}',
                        },
                        {
                            'name':u'episode home by tv show id',
                            'format':ur'/h/tvshow/episode/{tv show id}/{disk position}/{track position}',
                        },
                        {
                            'name':u'episode home by tvdb tv episode id',
                            'format':ur'/h/tvshow/episode/tvdb/{tvdb tv episode id}',
                        },
                        {
                            'name':u'episode home by tvdb tv season id',
                            'format':ur'/h/tvshow/episode/tvdb/{tvdb tv season id}/{track position}',
                        },
                        {
                            'name':u'episode home by tvdb tv show id',
                            'format':ur'/h/tvshow/episode/tvdb/{tvdb tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_tvshow_episode',
                    'namespace':'home.tvshow.episode',
                    'generate':{'name':'knowledge', 'key':'track id'},
                    'index':[
                        'tv show id',
                        'disk id',
                        'track id',
                        'disk position',
                        'track position'
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'tvdb tv episode id',
                    ],
                },
                'home.music.album':{
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
                            'name':u'music home by album id',
                            'format':ur'/h/music/album/{album id}',
                        },
                        {
                            'name':u'music home by album handle',
                            'format':ur'/h/music/album/~/{album handle}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_music_album',
                    'namespace':'home.music.album',
                    'generate':{'name':'knowledge', 'key':'album id'},
                    'index':['album id', 'album handle'],
                },
                'home.music.disk':{
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
                    'type':'json',
                    'collection':'home_music_disk',
                    'namespace':'home.music.disk',
                    'generate':{'name':'knowledge', 'key':'disk id'},
                    'index':['album id', 'disk id', 'disk position', 'album handle'],
                },
                'home.music.track':{
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
                    'type':'json',
                    'collection':'home_music_track',
                    'namespace':'home.music.track',
                    'generate':{'name':'knowledge', 'key':'track id'},
                    'index':['album id', 'disk id', 'track id', 'disk position', 'track position', 'album handle'],
                },
                'home.person':{
                    'match':[
                        {
                            'filter':ur'^/h/person/(?P<person_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/person/tmdb/(?P<tmdb_person_id>[0-9]+)$',
                            'depend':ur'/c/tmdb/person/{tmdb person id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'person home by person id',
                            'format':ur'/h/person/{person id}',
                        },
                        {
                            'name':u'person home by tmdb person id',
                            'format':ur'/h/person/tmdb/{tmdb person id}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_person',
                    'namespace':'home.person',
                    'generate':{'name':'knowledge', 'key':'person id'},
                    'index':['person id', 'tmdb person id'],
                },
                'home.company':{
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
                            'name':u'company home by company id',
                            'format':ur'/h/company/{company id}',
                        },
                        {
                            'name':u'company home by tmdb company id',
                            'format':ur'/h/company/tmdb/{tmdb company id}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_company',
                    'namespace':'home.company',
                    'generate':{'name':'knowledge', 'key':'company id'},
                    'index':['company id', 'tmdb company id'],
                },
                'home.genre':{
                    'match':[
                        {
                            'filter':ur'^/h/genre/(?P<genre_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/h/genre/tmdb/(?P<tmdb_genre_id>[0-9]+)$',
                            'depend':ur'/c/tmdb/genre/{tmdb genre id}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'genre home by genre id',
                            'format':ur'/h/genre/{genre id}',
                        },
                        {
                            'name':u'genre home by tmdb genre id',
                            'format':ur'/h/genre/tmdb/{tmdb genre id}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_genre',
                    'namespace':'home.genre',
                    'generate':{'name':'knowledge', 'key':'genre id'},
                },
                'home.job':{
                    'match':[
                        {
                            'filter':ur'^/h/job/(?P<job_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'job home by job id',
                            'format':ur'/h/job/{job id}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_job',
                    'namespace':'home.job',
                    'generate':{'name':'knowledge', 'key':'job id'},
                },
                'home.department':{
                    'match':[
                        {
                            'filter':ur'^/h/department/(?P<department_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'department home by department id',
                            'format':ur'/h/department/{department id}',
                        },
                    ],
                    'type':'json',
                    'collection':'home_department',
                    'namespace':'home.department',
                    'generate':{'name':'knowledge', 'key':'department id'},
                },
            },
        },
        'knowledge':{
            'match':ur'^/k/.*$',
            'branch':{
                'knowledge.configuration':{
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
                
                'knowledge.playlist':{
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
                
                'knowledge.movie':{
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
                'knowledge.movie.cast':{
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
                'knowledge.movie.image':{
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
                'knowledge.movie.keyword':{
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
                'knowledge.movie.release':{
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
                'knowledge.movie.clip':{
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
                'knowledge.movie.translation':{
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
                'knowledge.movie.alternative':{
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
                
                'knowledge.music.album':{
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
                'knowledge.music.album.image':{
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
                'knowledge.music.disk':{
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
                'knowledge.music.track':{
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
                
                'knowledge.tvshow.show':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tvshow/show/(?P<tv_show_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'show knowledge by tv show id',
                            'format':ur'/k/{language}/tvshow/show/{tv show id}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_show',
                    'namespace':'ns.knowledge.tvshow.show',
                    'index':['tv show id', 'language'],
                },
                'knowledge.tvshow.show.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tvshow/show/(?P<tv_show_id>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show image',
                            'format':ur'/k/tvshow/show/{tv show id}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_show_image',
                    'namespace':'knowledge.tvshow.show.image',
                },
                'knowledge.tvshow.show.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tvshow/show/(?P<tv_show_id>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show credit',
                            'format':ur'/k/tvshow/show/{tv show id}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_show_credit',
                    'namespace':'knowledge.tvshow.show.credit',
                },
                'knowledge.tvshow.season':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tvshow/season/(?P<disk_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tvshow/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'season knowledge by disk id',
                            'format':ur'/k/{language}/tvshow/season/{disk id}',
                        },
                        {
                            'name':u'season knowledge by tv show id and position',
                            'format':ur'/k/{language}/tvshow/season/{tv show id}/{disk position}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season',
                    'namespace':'ns.knowledge.tvshow.season',
                    'index':['tv show id', 'disk id', 'disk position'],
                },
                'knowledge.tvshow.season.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tvshow/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show season image',
                            'format':ur'/k/tvshow/season/{tv show id}/{disk position}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season_image',
                    'namespace':'knowledge.tvshow.season.image',
                },
                'knowledge.tvshow.season.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tvshow/season/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show season image',
                            'format':ur'/k/tvshow/season/{tv show id}/{disk position}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_season_credit',
                    'namespace':'knowledge.tvshow.season.credit',
                },
                'knowledge.tvshow.episode':{
                    'match':[
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tvshow/episode/(?P<track_id>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tvshow/episode/(?P<disk_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/k/(?P<language>[a-z]{2})/tvshow/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'episode knowledge by track id',
                            'format':ur'/k/{language}/tvshow/episode/{track id}',
                        },
                        {
                            'name':u'episode knowledge by disk id',
                            'format':ur'/k/{language}/tvshow/episode/{disk id}/{track position}',
                        },
                        {
                            'name':u'episode knowledge by tv show id',
                            'format':ur'/k/{language}/tvshow/episode/{tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode',
                    'namespace':'ns.knowledge.tvshow.episode',
                    'index':['tv show id', 'track id', 'disk id', 'disk position', 'track position', 'language'],
                },
                'knowledge.tvshow.episode.image':{
                    'match':[
                        {
                            'filter':ur'^/k/tvshow/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)/image$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode image',
                            'format':ur'/k/tvshow/episode/{tv show id}/{disk position}/{track position}/image',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode_image',
                    'namespace':'knowledge.tvshow.episode.image',
                },
                'knowledge.tvshow.episode.credit':{
                    'match':[
                        {
                            'filter':ur'^/k/tvshow/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)/credit$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode credit',
                            'format':ur'/k/tvshow/episode/{tv show id}/{disk position}/{track position}/credit',
                        },
                    ],
                    'type':'json',
                    'collection':'knowledge_tvshow_episode_credit',
                    'namespace':'knowledge.tvshow.episode.credit',
                },
                
                'knowledge.person':{
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
                'knowledge.person.image':{
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
                'knowledge.person.credit':{
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
                'knowledge.company':{
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
                'knowledge.company.image':{
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
                'knowledge.company.credit':{
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
                'knowledge.genre':{
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
                'knowledge.job':{
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
                'knowledge.department':{
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
            'match':ur'^/c(?:/[a-z]{2})?/tmdb/.*$',
            'branch':{
                'tmdb.configuration':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/configuration$',
                            'remote':ur'http://api.themoviedb.org/3/configuration?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb configuration',
                            'format':ur'/c/tmdb/configuration',
                        },
                    ],
                    'collection':'tmdb_configuration',
                    'namespace':'ns.tmdb.configuration',
                    'type':'json',
                },
                'tmdb.movie':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}?language={language}&api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/movie/imdb/(?P<imdb_movie_id>tt[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}?language={language}&api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie by tmdb id',
                            'format':ur'/c/{language}/tmdb/movie/{tmdb movie id}',
                        },
                        {
                            'name':u'tmdb movie by imdb id',
                            'format':ur'/c/{language}/tmdb/movie/imdb/{imdb movie id}',
                        }
                    ],
                    'collection':'tmdb_movie',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id', 'language', 'imdb movie id'],
                },
                'tmdb.movie.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/cast$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/casts?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie cast by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/cast',
                        },
                    ],
                    'collection':'tmdb_movie_cast',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/image$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/images?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie image by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/image',
                        },
                    ],
                    'collection':'tmdb_movie_image',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.keyword':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/keyword$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/keywords?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie keyword by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/keyword',
                        },
                    ],
                    'collection':'tmdb_movie_keyword',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.release':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/release$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/releases?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie release by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/release',
                        },
                    ],
                    'collection':'tmdb_movie_release',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.trailer':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/trailer$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/trailers?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie trailer by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/trailer',
                        },
                    ],
                    'collection':'tmdb_movie_trailer',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.translation':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/translation$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/translations?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie translation by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/translation',
                        },
                    ],
                    'collection':'tmdb_movie_translation',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.alternative':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/alternative$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/alternative_titles?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie alternative by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/alternative',
                        },
                    ],
                    'collection':'tmdb_movie_alternative',
                    'namespace':'ns.tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.collection':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tmdb/collection/(?P<tmdb_collection_id>[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/collection/{tmdb collection id}?language={language}&api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb collection by tmdb id',
                            'format':ur'/c/{language}/tmdb/collection/{tmdb collection id}',
                        },
                    ],
                    'collection':'tmdb_collection',
                    'namespace':'ns.tmdb.collection',
                    'type':'json',
                    'index':['tmdb collection id', 'language'],
                },
                'tmdb.person':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/person/{tmdb person id}?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}',
                        },
                    ],
                    'collection':'tmdb_person',
                    'namespace':'ns.tmdb.person',
                    'type':'json',
                },
                'tmdb.person.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/image$',
                            'remote':ur'http://api.themoviedb.org/3/person/{tmdb person id}?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person image by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}/image',
                        },
                    ],
                    'collection':'tmdb_person_image',
                    'namespace':'ns.tmdb.person.image',
                    'type':'json',
                },
                'tmdb.person.credit':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/credit$',
                            'remote':ur'http://api.themoviedb.org/3/person/{tmdb person id}/credits?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person credit by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}/credit',
                        },
                    ],
                    'collection':'tmdb_person_credit',
                    'namespace':'ns.tmdb.person.credit',
                    'type':'json',
                },
                'tmdb.company':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/company/(?P<tmdb_company_id>[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/company/{tmdb company id}?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb company by tmdb id',
                            'format':ur'/c/tmdb/company/{tmdb company id}',
                        },
                    ],
                    'collection':'tmdb_company',
                    'namespace':'ns.tmdb.company',
                    'type':'json',
                },
                'tmdb.company.credit':{
                    #There is the issue of paging...
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/company/(?P<tmdb_company_id>[0-9]+)/credit$',
                            'remote':ur'http://api.themoviedb.org/3/company/{tmdb company id}/movies?page={page}&api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb company credit by tmdb id',
                            'format':ur'/c/tmdb/company/{tmdb company id}/credit',
                        },
                    ],
                    'collection':'tmdb_company_credit',
                    'namespace':'ns.tmdb.company.credit',
                    'type':'json',
                },
            },
            'status codes':{
                1:'Success.',
                2:'Invalid service - This service does not exist.',
                3:'Authentication failed - You do not have permissions to access the service.',
                4:'Invalid format - This service doesn\'t exist in that format.',
                5:'Invalid parameters - Your request parameters are incorrect.',
                6:'Invalid id - The pre-requisite id is invalid or not found.',
                7:'Invalid API key - You must be granted a valid key.',
                8:'Duplicate entry - The data you tried to submit already exists.',
                9:'Service offline - This service is temporarily offline. Try again later.',
                10:'Suspended API key - Access to your account has been suspended, contact TMDb.',
                11:'Internal error - Something went wrong. Contact TMDb.',
                12:'The item/record was updated successfully.',
                13:'The item/record was deleted successfully.',
                14:'Authentication failed.',
                15:'Failed.',
                16:'Device denied.',
                17:'Session denied.',
            }
        },
        'tvdb':{
            # http://www.thetvdb.com/api/7B3B400B0146EA83/series/73255/en.xml
            # http://www.thetvdb.com/api/7B3B400B0146EA83/series/73255/all/en.xml
            # http://www.thetvdb.com/api/7B3B400B0146EA83/series/73255/all/en.zip
            # http://www.thetvdb.com/api/7B3B400B0146EA83/series/73255/default/8/5/en.xml
            'api key':u'7B3B400B0146EA83',
            'match':ur'^/c(?:/[a-z]{2})?/tvdb/.*$',
            'branch':{
                'tvdb.show':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/{language}.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show by tvdb show id',
                            'format':ur'/c/{language}/tvdb/show/{tvdb tv show id}',
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Series',
                            'reference':'tvdb.show',
                            'coalesce':False,
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                    ],
                    'collection':'tvdb_tv_show',
                    'namespace':'ns.tvdb.show',
                    'type':'xml',
                },
                'tvdb.show.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/cast$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/actors.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show cast by tvdb show id',
                            'format':ur'/c/tvdb/show/{tvdb tv show id}/cast',
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Actor',
                            'reference':'tvdb.show.cast',
                            'coalesce':True,
                        },
                    ],
                    'collection':'tvdb_tv_show_cast',
                    'namespace':'ns.tvdb.show.cast',
                    'type':'xml',
                },
                'tvdb.show.image':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/image$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/banners.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show image by tvdb show id',
                            'format':ur'/c/tvdb/show/{tvdb tv show id}/image',
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Banner',
                            'reference':'tvdb.show.image',
                            'coalesce':True,
                        },
                    ],
                    'collection':'tvdb_tv_show_image',
                    'namespace':'ns.tvdb.show.image',
                    'type':'xml',
                },
                'tvdb.season':{
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
                        },
                        {
                            'name':u'tvdb season by tvdb show id',
                            'format':ur'/c/{language}/tvdb/season/{tvdb tv show id}/{disk position}',
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'disk position',
                    ],
                    'collection':'tvdb_tv_season',
                    'namespace':'tvdb.season',
                    'type':'xml',
                },
                'tvdb.episode':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/episode/(?P<tvdb_tv_episode_id>[0-9]+)$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/episodes/{tvdb tv episode id}/{language}.xml',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/episode/(?P<tvdb_tv_season_id>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/episode/(?P<tvdb_tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/default/{disk position}/{track position}/{language}.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb episode by tvdb episode id',
                            'format':ur'/c/{language}/tvdb/episode/{tvdb tv episode id}',
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
                            'reference':'tvdb.episode',
                            'coalesce':False,
                        },
                    ],
                    'index':[
                        'tvdb tv show id',
                        'tvdb tv season id',
                        'tvdb tv episode id',
                        'disk position',
                        'track position',
                    ],
                    'collection':'tvdb_tv_episode',
                    'namespace':'ns.tvdb.episode',
                    'type':'xml',
                },
                'tvdb.show.complete':{
                    'match':[
                        {
                            'filter':ur'^/c/(?P<language>[a-z]{2})/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/complete$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/all/{language}.zip',
                        },
                    ],
                    'produce':[
                        {
                            'tag':u'Series',
                            'reference':'tvdb.show',
                            'coalesce':False,
                        },
                        {
                            'tag':u'Episode',
                            'reference':'tvdb.episode',
                            'coalesce':False,
                        },
                        {
                            'tag':u'Banner',
                            'reference':'tvdb.show.image',
                            'coalesce':True,
                        },
                        {
                            'tag':u'Actor',
                            'reference':'tvdb.show.cast',
                            'coalesce':True,
                        },
                    ],
                    'type':'zip',
                },
                
                'tvdb.update.daily':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/day$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/updates/updates_day.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb daily update',
                            'format':ur'/c/tvdb/update/day',
                        },
                    ],
                    'type':'zip',
                },
                'tvdb.update.weekly':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/week$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/updates/updates_week.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb weekly update',
                            'format':ur'/c/tvdb/update/week',
                        },
                    ],
                    'type':'zip',
                },
                'tvdb.update.monthly':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/month$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/updates/updates_month.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb monthly update',
                            'format':ur'/c/tvdb/update/month',
                        },
                    ],
                    'type':'zip',
                },
            },
        },
        'medium':{
            'match':ur'^/m(?:/[a-z]{2})?/.*$',
            'branch':{
                'medium.asset.movie':{
                    'match':[
                        {
                            'filter':ur'^/m/asset/movie/(?P<movie_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie asset',
                            'format':ur'/m/asset/movie/{movie id}',
                        },
                    ],
                    'type':'reference',
                    'collection':'medium_asset_movie',
                    'collection reference':'medium_resource_movie',
                    'namespace':'medium.asset.movie',
                },
                'medium.asset.music.track':{
                    'match':[
                        {
                            'filter':ur'^/m/asset/music/track/(?P<album_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music asset',
                            'format':ur'/m/asset/music/track/{album id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'reference',
                    'collection':'medium_asset_music_track',
                    'collection reference':'medium_resource_music',
                    'namespace':'medium.asset.music.track',
                },
                'medium.asset.tvshow.episode':{
                    'match':[
                        {
                            'filter':ur'^/m/asset/tvshow/episode/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show asset',
                            'format':ur'/m/asset/tvshow/episode/{tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'reference',
                    'collection':'medium_asset_tvshow_episode',
                    'collection reference':'medium_resource_tvshow',
                    'namespace':'medium.asset.tvshow.episode',
                },
                'medium.resource.movie.language':{
                    'match':[
                        {
                            'filter':ur'^/m/resource/(?P<volume>[^/]+)/movie/(?P<kind>[^\.]{3,4})/(?P<profile>[^/]{2,})/(?P<language>[a-z]{2})/(?P<movie_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie resource with language',
                            'format':ur'/m/resource/{volume}/movie/{kind}/{profile}/{language}/{movie id}',
                        },
                    ],
                    'type':'crawl',
                    'collection':'medium_resource_movie',
                    'namespace':'medium.resource.movie',
                },
                'medium.resource.movie':{
                    'match':[
                        {
                            'filter':ur'^/m/resource/(?P<volume>[^/]+)/movie/(?P<kind>[^\.]{3,4})/(?P<profile>[^/]{2,})/(?P<movie_id>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'movie resource',
                            'format':ur'/m/resource/{volume}/movie/{kind}/{profile}/{movie id}',
                        },
                    ],
                    'type':'crawl',
                    'collection':'medium_resource_movie',
                    'namespace':'medium.resource.movie',
                },
                'medium.resource.tvshow.language':{
                    'match':[
                        {
                            'filter':ur'^/m/resource/(?P<volume>[^/]+)/tvshow/(?P<kind>[^\.]{3,4})/(?P<profile>[^/]{2,})/(?P<language>[a-z]{2})/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode resource with language',
                            'format':ur'/m/resource/{volume}/tvshow/{kind}/{profile}/{language}/{tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'crawl',
                    'collection':'medium_resource_tvshow',
                    'namespace':'medium.resource.tvshow',
                },
                'medium.resource.tvshow':{
                    'match':[
                        {
                            'filter':ur'^/m/resource/(?P<volume>[^/]+)/tvshow/(?P<kind>[^\.]{3,4})/(?P<profile>[^/]{2,})/(?P<tv_show_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tv show episode resource',
                            'format':ur'/m/resource/{volume}/tvshow/{kind}/{profile}/{tv show id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'crawl',
                    'collection':'medium_resource_tvshow',
                    'namespace':'medium.resource.tvshow',
                },
                'medium.resource.music.language':{
                    'match':[
                        {
                            'filter':ur'^/m/resource/(?P<volume>[^/]+)/music/(?P<kind>[^\.]{3,4})/(?P<profile>[^/]{2,})/(?P<language>[a-z]{2})/(?P<album_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music track resource with language',
                            'format':ur'/m/resource/{volume}/music/{kind}/{profile}/{language}/{album id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'crawl',
                    'collection':'medium_resource_music',
                    'namespace':'medium.resource.music',
                },
                'medium.resource.music':{
                    'match':[
                        {
                            'filter':ur'^/m/resource/(?P<volume>[^/]+)/music/(?P<kind>[^\.]{3,4})/(?P<profile>[^/]{2,})/(?P<album_id>[0-9]+)/(?P<disk_position>[0-9]+)/(?P<track_position>[0-9]+)$',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'music track resource',
                            'format':ur'/m/resource/{volume}/music/{kind}/{profile}/{album id}/{disk position}/{track position}',
                        },
                    ],
                    'type':'crawl',
                    'collection':'medium_resource_music',
                    'namespace':'medium.resource.music',
                },
            }
        },
    },
}
