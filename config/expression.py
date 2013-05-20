# -*- coding: utf-8 -*-

{
    'expression':[
        {
            'name':'srt time line', 
            'definition':u'^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$', 
            'flags':32,
        },
        {
            'name':'ass timecode', 
            'definition':ur'([0-9]):([0-9]{2}):([0-9]{2}).([0-9]{2})', 
            'flags':32,
        },
        {
            'name':'ass subtitle line', 
            'definition':ur'^Dialogue\s*:\s*(.*)$', 
            'flags':32,
        },
        {
            'name':'ass formation line', 
            'definition':ur'^Format\s*:\s*(.*)$', 
            'flags':32,
        },
        {
            'name':'ass condense line breaks', 
            'definition':ur'(\\N)+', 
            'flags':32,
        },
        {
            'name':'ass event command', 
            'definition':ur'\{\\[^\}]+\}', 
            'flags':32,
        },
        {
            'name':'whitespace',
            'definition':ur'\s+',
            'flags':32,
        },
        {
            'name':'characters to exclude from filename',
            'definition':ur'[\\\/?<>:*|\'"^\.]',
            'flags':32,
        },
        {
            'name':'sentence end',
            'definition':ur'[.!?]',
            'flags':32,
        },
        {
            'name':'mediainfo value list',
            'definition':ur'^[^/]+(?:\s*/\s*[^/]+)*$',
            'flags':32,
        },
        {
            'name':'tvdb list separators',
            'definition':ur'\||,',
            'flags':32,
        },
        {
            'name':'space around tvdb list item',
            'definition':ur'\s*\|\s*',
            'flags':32,
        },
        {
            'name':'clean xml',
            'definition':ur'\s+/\s+(?:\t)*',
            'flags':32,
        },
        {
            'name':'true value',
            'definition':ur'yes|true|1',
            'flags':34,
        },
        {
            'name':'full utc datetime',
            'definition':ur'(?:(?P<tzinfo>[A-Za-z/]+) )?(?P<year>[0-9]{4})(?:-(?P<month>[0-9]{2})(?:-(?P<day>[0-9]{2})(?:(?: |T)(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2}))?)?)?',
            'flags':32,
        },
    ],
    'constant':{
        'empty string':u'',
        'hd threshold':720,
        'playback aspect ration':1920.0/1080.0,
        'space':u' ',
        'dot':u'.',
    },
}
