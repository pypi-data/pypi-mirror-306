from os.path import dirname, join
from rst import Rest, Paragraph, Strong, OrderedListItem, ListItem, Title, Link, Transition
from rst import Directive, Em, Quote, Text
from tiramisu.option import *
from tiramisu.config import *
#from makerestdoc import *

docdir = join(dirname(__file__), 'build')

def make_rst_file(filename, rstcontent):
    fh = file(filename, 'w')
    fh.write(rstcontent.text())
    fh.close()

def descr_content(path, prefix, descr, root=False):
    content = Rest()
    title = Title(abovechar="", belowchar="=")
    if root:
        title.join(Text("Configuration's overview for: "), Quote(descr._name))
    else:
        title.join(Text("Group's overview for: "), Quote(descr._name))
    content.add(title)
    content.add(ListItem().join(Strong("name:"), Text(descr._name)))
    if not root:
        content.add(ListItem().join(Strong("path:"), Text(path)))
    content.add(ListItem().join(Strong("description:"), Text(descr.impl_get_information('doc'))))
    if not root:
        content.add(ListItem().join(Strong("parent config:"), Text(prefix)))
    if not root:
        content.add(ListItem().join(Strong("type:"), Text(descr._group_type)))
    if not root:
        content.add(ListItem().join(Strong("requirements:"), Text(str(descr._requires))))
    if not root:
        content.add(ListItem().join(Strong("properties"), Text(str([prop for prop in descr._properties]))))
    content.add(Transition())
    content.add(Title(abovechar="", belowchar="-").join(Text("Ordered list of childrens for:"), Text(path)))
    names, options = descr._children
    for opt in options:
        name = opt._name
        link = Link(name + ":", join(path + '.' + name + ".html"))
        # because of SympLink opt
        if hasattr(opt, 'impl_get_information'):
            doc = opt.impl_get_information('doc')
        else:
            doc = name
        content.add(OrderedListItem(link, Text(opt.impl_get_information('doc'))))
    content.add(Transition())
    content.add(Paragraph(Link("back to index", "index.html")))
    make_rst_file(join(docdir, path + '.txt'), content)
    if root:
        make_rst_file(join(docdir, 'index.txt'), content)

def opt_rst_content(path, prefix, descr, value):
    content = Rest()
    title = Title(abovechar="", belowchar="=")
    title.join(Text("Configuration's option overview for: "), Quote(descr._name))
    content.add(title)
    content.add(ListItem().join(Strong("name:"), Text(descr._name)))
    content.add(ListItem().join(Strong("type:"), Text(descr.__class__.__name__)))
    content.add(ListItem().join(Strong("current value:"), Text(str(value))))
    content.add(ListItem().join(Strong("path:"), Text(path)))
    content.add(ListItem().join(Strong("parent config:"), Text(prefix)))
    if isinstance(descr, ChoiceOption):
        content.add(ListItem().join(Strong("possible values:"), Text(str(descr.impl_get_values()))))
    if not isinstance(descr, SymLinkOption):
        content.add(ListItem().join(Strong("mime type:"), Text(str(descr.__class__.__name__))))
        content.add(ListItem().join(Strong("default value:"), Text(str(descr.impl_getdefault()))))
        content.add(ListItem().join(Strong("description:"), Text(str(descr.impl_get_information('doc')))))
        content.add(ListItem().join(Strong("requirements:"), Text(str(descr._requires))))
        content.add(ListItem().join(Strong("properties"), Text(str([prop for prop in descr._properties]))))
    else:
        content.add(ListItem().join(Strong("links to:"), Text(str(descr.path))))
    content.add(Transition())
    content.add(Paragraph(Link("back to parent config", join(prefix + ".html"))))
    make_rst_file(join(docdir, path + '.txt'), content)

def make_rest_overview(cfg, title=True):
    descr = cfg._impl_descr
    rootname = descr._name
    descr_content(rootname, rootname, descr, root=True)

    for path in descr.impl_getpaths(include_groups=True):
        child = cfg.unwrap_from_path(path)
        fullpath = rootname + '.' + path
        prefix = fullpath.rsplit(".", 1)[0]
        if isinstance(child, OptionDescription):
            descr_content(fullpath, prefix, child)
        else:
            value = getattr(cfg, path)
            opt_rst_content(fullpath, prefix, child, value)

if __name__ == '__main__':
    from sampleconfig import get_example_config
    make_rest_overview(get_example_config())
# ____________________________________________________________
