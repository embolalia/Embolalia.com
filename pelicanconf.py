#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Edward Powell'
SITENAME = u'Embolalia.com'
SITEURL = 'https://embolalia.com'
FEED_DOMAIN = 'https://embolalia.com'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Blogroll
LINKS =  (('Nerdfighteria Network', 'http://dftba.net'),
          ('Willie IRC Bot', 'http://willie.dftba.net'),)

# Social widget
SOCIAL = (('GitHub', 'https://github.com/embolalia'),)

DEFAULT_PAGINATION = 10

EXTRA_PATH_METADATA = {
    '*/resume.md': {
        'Title': 'Resume',
    },
}

#TEMPLATE_PAGES = {
#    'resume/resume.md': 'content/pages/resume.md'
#}
