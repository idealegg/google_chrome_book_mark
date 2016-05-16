# -*- coding: utf-8 -*-
import re
import pprint


type_list = ('                    <DT><A HREF',
'            </DL><p>',
'            <DL><p>',
'            <DT><A HREF',
'            <DT><H3 ADD_DATE',
'        </DL><p>',
'        <DL><p>',
'        <DT><H3 ADD_DATE',
'    </DL><p>',
'    <DL><p>',
'    <DT><H3 ADD_DATE',
None
)

class BookMark:
    __doc__ = ('\n'
               '                    <DT><A HREF\n'
               '            </DL><p>\n'
               '            <DL><p>\n'
               '            <DT><A HREF\n'
               '            <DT><H3 ADD_DATE\n'
               '        </DL><p>\n'
               '        <DL><p>\n'
               '        <DT><H3 ADD_DATE\n'
               '     DO NOT EDIT! -->\n'
               '     It will be read and overwritten.\n'
               '    </DL><p>\n'
               '    <DL><p>\n'
               '    <DT><H3 ADD_DATE\n'
               '<!-- This is an automatically generated file.\n'
               '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n'
               '</DL><p>\n'
               '<DL><p>\n'
               '<H1>Bookmarks</H1>\n'
               '<META HTTP-EQUIV\n'
               '<TITLE>Bookmarks</TITLE>\n'
               '    ')

    def __init__(self, line_no, content):
        self.type = None
        self.line_no = line_no
        self.content = content
        self.key = None
        self.child_list = []
        self.parent = None
        self.to_inserted_behind = []
        self.checked = False

    def initialize(self):
        global type_list
        for t_type in type_list:
            if t_type:
                if self.content[:len(t_type)] == t_type:
                    self.type = t_type
                    break
        re_result = re.search(r'>([\w+]+)</H3>', self.content)
        if re_result:
            self.key = re_result.group(1)
        else:
            re_result = re.search(r'<DT><A HREF="([^"]+)"', self.content)
            if re_result:
                self.key = re_result.group(1)

    def is_child(self, t_type):
        if not self.type:
            return False
        if self.type[:4] != '    ':
            return False
        if self.type[-16:] != '<DT><H3 ADD_DATE':
            return False
        ret_list = []
        ret_list.append(''.join(['    ', self.type]))
        ret_list.append(''.join(['    ', self.type[:-16], '<DT><A HREF']))
        if t_type in ret_list:
            return True
        return False

    def is_grandchild(self, t_type):
        if not self.type or not t_type or self.type[:4] != '    ' or self.type[-16:] != '<DT><H3 ADD_DATE':
            return False
        if t_type.find(''.join(['        ', self.type])) != -1 or t_type.find(''.join(['        ', self.type[:-16], '<DT><A HREF'])) != -1:
            return True
        return False

    def is_p(self):
        if self.type and self.type.find('<p>') != -1:
            return True
        return False

    def is_ahref(self):
        if self.type and self.type.find('<DT><A HREF=') != -1:
            return True
        return False

    def is_directory(self):
        if self.type and self.type.find('<DT><H3 ADD_DATE=') != -1:
            return True
        return False

    def is_in(self, a_href):
        if self.key and self.key == a_href:
            return True
        return False

    def get_parent_and_inserted_lines(self):
        if self.is_ahref():
            pass

    def checked(self):
        self.checked = True
        for c_item in self.child_list:
            c_item.checked()

    def get_domain(self):
        domain = self.line_no
        if self.child_list:
            domain = self.child_list[-1].get_domain() + 1
        return domain

    def print_bookmark(self):
        if self.key:
            print self.key+"\n"
        else:
            print "CONTENT: {0} LENGTH {1}".format(self.content, len(self.content))
        if self.type:
            print "type: {0}".format(self.type)
        else:
            print "type: None"
        pprint.pprint(self.child_list)
        pprint.pprint(self.parent)
