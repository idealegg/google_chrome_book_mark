# -*- coding: utf-8 -*-

import bookmark.bookmark

class BookMarkManager:
    def __init__(self, file):
        self.file = file
        self.bookmark_list = []

    def initialize(self):
        lines = open(file, 'r').readlines()
        num = 0
        type_stack = []
        for line in lines:
            num += 1
            line = line[:-1]
            bm = bookmark.bookmark.BookMark(num, line)
            bm.init_type()
            cur_type = bm.type
            if len(type_stack):
                last_type = type_stack[-1]


