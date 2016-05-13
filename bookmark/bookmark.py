# -*- coding: utf-8 -*-

type_list = ('                    <DT><A HREF',
'            </DL><p>',
'            <DL><p>',
'            <DT><A HREF',
'            <DT><H3 ADD_DATE',
'        </DL><p>',
'        <DL><p>',
'        <DT><H3 ADD_DATE',
None
)

class BookMark:
    '''
                    <DT><A HREF
            </DL><p>
            <DL><p>
            <DT><A HREF
            <DT><H3 ADD_DATE
        </DL><p>
        <DL><p>
        <DT><H3 ADD_DATE
     DO NOT EDIT! -->
     It will be read and overwritten.
    </DL><p>
    <DL><p>
    <DT><H3 ADD_DATE
<!-- This is an automatically generated file.
<!DOCTYPE NETSCAPE-Bookmark-file-1>
</DL><p>
<DL><p>
<H1>Bookmarks</H1>
<META HTTP-EQUIV
<TITLE>Bookmarks</TITLE>
    '''

    def __init__(self, line_no, content):
        self.type = None
        self.line_no = line_no
        self.content = content
        self.child_list = []

    def init_type(self):
        global type_list
        for t_type in type_list:
            if self.content[:len(t_type)] == t_type:
                self.type = t_type


