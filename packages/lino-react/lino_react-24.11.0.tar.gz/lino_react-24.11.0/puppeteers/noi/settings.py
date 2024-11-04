# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_book.projects.noi1r.settings import *

class Site(Site):
    default_ui = 'lino_react.react'
    title = "Noi React demo"

SITE = Site(globals())
