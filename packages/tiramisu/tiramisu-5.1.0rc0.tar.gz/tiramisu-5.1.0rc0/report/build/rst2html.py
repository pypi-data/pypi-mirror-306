#!/usr/bin/python
# unproudly borrowed from David Goodger's rst2html.py

""" A minimal front end to the Docutils Publisher, producing HTML with a 
`config` role 
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description
# ____________________________________________________________
from docutils import nodes, utils
from docutils.parsers.rst import roles

# ____________________________________________________________
#register a :config: ReST link role for use in documentation    
def config_reference_role(role, rawtext, text, lineno, inliner,
                    options={}, content=[]):
    basename = text
    refuri = "report/build" + basename + '.html'
    roles.set_classes(options)
    node = nodes.reference(rawtext, utils.unescape(text), refuri=refuri,
                        **options)
    return [node], []

roles.register_local_role('config', config_reference_role)
# ____________________________________________________________


description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)

publish_cmdline(writer_name='html', description=description)

