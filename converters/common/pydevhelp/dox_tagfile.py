"""
Doxygen Tag File converter
"""

from . import devhelp

import lxml.etree as ET

class DoxygenTagFile(object):

    def __init__(self, f, filterFunc):

        self.tags = ET.parse(f)

        filterFunc(self.tags)

    def _getLink(self, elem):

        link = elem.find('anchorfile').text

        anchor = elem.find('anchor').text

        if anchor:
            link += '#' + anchor

        return link

    def extractKeywords(self, handler):

        functions = self.tags.iterfind("//compound/member")

        for f in functions:

            # there are the kinds of members that get keyword entries
            if f.attrib['kind'] not in ['function', 'enumvalue', 'typedef', 'define']:
                continue

            link = self._getLink(f)

            kw = devhelp.Keyword(f.find('name').text, link, f.attrib['kind'])

            handler(kw)

    def extractNamespaces(self, handler):

        ns = self.tags.iterfind("/compound[@kind='namespace']")

        for n in ns:

            name = n.find('name').text

            s = devhelp.Subsection(name, n.find('filename').text)
            handler(s)

    def extractClasses(self, elem, handler):

        if elem is None:
            cs = self.tags.iterfind("./compound")
        else:
            cs = elem.iterfind("./member")

        for c in cs:

            kind = c.attrib['kind']

            # this should be in the xpath, but it says's 'or' is an invalid predicate
            # these are the element types that get subentries under 'classes'
            if kind not in ['class', 'struct', 'enumeration']:
                continue;

            name = c.find('name').text

            # we don't want template classes
            if name.endswith('>') and '<' in name:
                continue;

            try:
                fn = c.find('filename').text
            except AttributeError:
                fn = self._getLink(c)

            s = devhelp.Subsection(name, fn)
            handler(s)

            # add add sub elements in the same way
            self.extractClasses(c, lambda sub: s.addSub(sub))
