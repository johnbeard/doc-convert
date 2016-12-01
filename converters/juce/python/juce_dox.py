#! /usr/bin/env python

import pydevhelp.devhelp as devhelp
import pydevhelp.dox_tagfile

import os
import argparse

import lxml.html as HTML

def getModules(fileList):
    """
    These aren't in the tag file, and they don't even come out properly
    in Doxygen XML, just just manually mess with the files
    """

    modList = {}

    for d in fileList:
        readModuleCrumbs(d, modList)

    mod = devhelp.Subsection("Modules", modList['modules']['href'])

    addModules(mod, modList['modules'])

    return mod

def addModules(parent, module):

    for m in module['sub']:
        submod = module['sub'][m]
        s = devhelp.Subsection(m, submod['href'])
        parent.addSub(s)

        addModules(s, submod)

def readModuleCrumbs(file, modList):
    html = HTML.parse(file)

    # <li class="navelem"><a class="el" href="dir_e05d7e2b1ecd646af5bb94391405f3b5.html">modules</a></li><li class="navelem"><a class="el" href="dir_fd421517ec8f709274e931dda731313f.html">juce_core</a></li><li class="navelem"><a class="el" href="dir_0d31e411142695dc4add552e9ff0c68a.html">streams</a></li>  </ul>

    crumbs = html.iterfind("//li[@class='navelem']/a[@class='el']")

    currMod = modList

    # add the crumbs to the module list, adding each level if not
    # there already
    for c in crumbs:

        name = c.text

        if name not in currMod:
            currMod[name] = {'name':name, 'href': c.attrib['href'], "sub": {}}

        currMod = currMod[name]["sub"]

class JuceDoc(object):

    def __init__(self, doc_src, doc_root):
        self.dsrc = doc_src

        self.db = devhelp.DevhelpBook(title = "JUCE 4.3.0 Reference Manual",
            name = "juce-doc",
            base = doc_root,
            link = "index.html",
            language = "c++")

        mods = self.getModules()
        self.db.addChapter(mods)

        tf = pydevhelp.dox_tagfile.DoxygenTagFile(os.path.join(self.dsrc, 'juce.tag'), filterFunc=self.filterTags)

        tf.extractKeywords( lambda kw: self.db.addKeyword(kw))

        nsChap = devhelp.Subsection('Namespaces', 'index.html')
        tf.extractNamespaces(lambda ns: nsChap.addSub(ns))
        self.db.addChapter(nsChap)

        classChap = devhelp.Subsection('Classes', 'classes.html')
        tf.extractClasses(None, lambda s: classChap.addSub(s))
        self.db.addChapter(classChap)

    def filterTags(self, tree):

        # the juce namespace is a bit wierd and just duplicates a subset of the classes
        for remove in tree.xpath("/tagfile/compound[@kind='namespace' and name = 'juce']"):
            remove.getparent().remove(remove)

        # get rid of one of the duplicate littlfoot namespaces
        for remove in tree.xpath("/tagfile/compound[@kind='namespace' and name = 'juce::littlefoot']"):
            remove.getparent().remove(remove)


    def getModules(self):
        """
        These aren't in the tag file, and they don't even come out properly
        in Doxygen XML, just just manually mess with the files
        """

        fileList = [os.path.join(self.dsrc, d) for d in os.listdir(self.dsrc) if d.startswith('dir_')];
        mod = getModules(fileList)

        return mod


    def output(self, fn):
        data = self.db.write(fn)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert JUCE Doxygen documentation into devhelp documentation')

    parser.add_argument('-d', '--doc-src', metavar='DOCSRC',
                            type=str, required=True,
                            help='the root of existing generated JUCE Doxygen documentation (e.g. "doxygen/doc" under your JUCE path, or an installed location in /usr/share/doc)')
    parser.add_argument('-r', '--doc-root', metavar='DOCROOT',
                            type=str, required=True,
                            help='the root of the documentation when installed (probably an installed location in /usr/share/doc)')
    parser.add_argument('-o', '--output', metavar='OUTFILE',
                            type=str, default='juce-doc.devhelp2',
                            help='output devhelp2 file, default is current dir file called juce-doc.devhelp2')
    args = parser.parse_args()

    jd = JuceDoc(args.doc_src, args.doc_root)

    jd.output(args.output)
