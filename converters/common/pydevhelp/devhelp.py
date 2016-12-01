"""
Classes for representation and export of devhelp books
"""

import lxml.etree as ET

class Keyword(object):

    def __init__(self, name, link, type):
        self.name = name
        self.link = link
        self.type = type

    def getXml(self):
        e = ET.Element('keyword', attrib={'name':self.name, 'link':self.link, 'type':self.type})
        return e

class Subsection(object):

    def __init__(self, name, link):
        self.name = name
        self.link = link

        self.subs = []

    def addSub(self, sub):
        self.subs.append(sub)

    def getXml(self):

        e = ET.Element('sub', attrib={'name':self.name, 'link':self.link})

        for s in self.subs:
            e.append(s.getXml());

        return e

class FunctionList(object):

    def __init__(self):

        # list of keyword items
        self.functions = []

    def addKeyword(self, kw):
        self.functions.append(kw)

    def getXml(self):

        e = ET.Element('functions')

        for f in self.functions:
            e.append(f.getXml())

        return e

class ChapterList(object):

    def __init__(self):

        # list of keyword items
        self.chapters = []

    def addChapter(self, sub):
        self.chapters.append(sub)

    def getXml(self):

        e = ET.Element('chapters')

        for f in self.chapters:
            e.append(f.getXml())

        return e

class DevhelpBook(object):

    xmlVersion = 2
    xmlns="http://www.devhelp.net/book"

    def __init__(self, name, title, base, link, language=None, author=""):
        self.name = name
        self.title = title
        self.base = base
        self.link = link
        self.language = language
        self.author = author

        self.funcs = FunctionList()
        self.chaps = ChapterList()

    def getXml(self):

        tree = ET.Element('book', attrib= {
            'language':self.language,
            'author':self.author,
            'name':self.name,
            'title':self.title,
            'base':self.base,
            'link':self.link,
            'version':str(self.xmlVersion)
            })

        tree.append(self.chaps.getXml())
        tree.append(self.funcs.getXml())

        return ET.ElementTree(tree)

    def addChapter(self, sub):
        self.chaps.addChapter(sub)

    def addKeyword(self, kw):
        self.funcs.addKeyword(kw)

    def write(self, fn):
        tree = self.getXml()
        tree.write(fn, encoding='utf-8', standalone=False, pretty_print=True)
