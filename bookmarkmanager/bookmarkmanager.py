# -*- coding: utf-8 -*-

import bookmark.bookmark
import pprint


class BookMarkManager:
    def __init__(self, file):
        self.file = file
        self.bookmark_list = []
        self.lines = None

    def initialize(self):
        t_file_o = open(self.file, 'r')
        self.lines = t_file_o.readlines()
        t_file_o.close()
        num = 0
        #type_stack = []
        for line in self.lines:
            num += 1
            line = line[:-1]
            bm = bookmark.bookmark.BookMark(num, line)
            bm.initialize()
            #cur_type = bm.type
            #if len(type_stack):
            #    last_type = type_stack[-1]
            self.bookmark_list.append(bm)
        num = 0
        for bm_item in self.bookmark_list:
            c_num = 0
            for child_item in self.bookmark_list[num+1:]:
                if not child_item.is_p():
                    if bm_item.is_child(child_item.type):
                        self.bookmark_list[num].child_list.append(child_item)
                        self.bookmark_list[c_num].parent = self.bookmark_list[num]
                    else:
                        if bm_item.is_grandchild(child_item.type):
                            continue
                        else:
                            break
                c_num += 1
            num += 1

    def find_item(self, item):
        for bm_item in self.bookmark_list:
            if item.type == bm_item.type and item.key == bm_item.key:
                return bm_item
        return None

    def get_inserted_item(self, i_bmm):
        for i_item in i_bmm.bookmark_list:
            # if is a a href link, to judge if insert.
            if i_item.is_ahref():
                o_item = self.find_item(i_item)
                # if not found, insert
                to_insert = None
                while not o_item:
                    to_insert = i_item
                    i_item = i_item.parent
                    o_item = self.find_item(i_item)
                if not to_insert.checked:
                    o_item.child_list[-1].to_inserted_behind.append(to_insert)
                    i_item.checked()

    def get_merge_lines(self, i_bmm):
        t_lines = []
        for m_item in self.bookmark_list:
            t_lines.append(m_item.content)
            for n_item in m_item.to_inserted_behind:
                t_lines.extend(i_bmm.bookmark_list[n_item.line_no:n_item.get_domain()+1])
        return t_lines

if __name__ == '__main__':
    import os
    import sys
    import re
    tmp_file_list = os.listdir(os.path.dirname(sys.path[0]))
    src_file = ""
    for t_file in tmp_file_list:
        if re.search(r'^bookmarks_\d+', t_file):
            src_file = t_file
            break
    bmm1 = BookMarkManager('../bookmarks.html')
    bmm1.initialize()
    bmm2 = BookMarkManager(''.join(['../', src_file]))
    bmm2.initialize()
    bmm1.get_inserted_item(bmm2)
    final_lines = bmm1.get_merge_lines(bmm2)
    file_o = open('../bookmarks_output.html', 'w')
    file_o.writelines(map(lambda x: ''.join([x, "\n"]), final_lines))
    file_o.close()

