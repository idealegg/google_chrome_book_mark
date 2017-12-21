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
            line = line.replace('\t', '    ')
            bm = bookmark.bookmark.BookMark(num, line)
            bm.initialize()
            #cur_type = bm.type
            #if len(type_stack):
            #    last_type = type_stack[-1]
            self.bookmark_list.append(bm)
        num = 0
        for bm_item in self.bookmark_list:
            c_num = num+1
            for child_item in self.bookmark_list[num+1:]:
                if not child_item.is_p():
                    if bm_item.is_child(child_item.type):
                        self.bookmark_list[num].child_list.append(child_item)
                        self.bookmark_list[c_num].parent = self.bookmark_list[num]
                    else:
                        if not bm_item.is_grandchild(child_item.type):
                            break
                c_num += 1
            num += 1

    def find_item(self, item):
        if item:
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
                if to_insert and not to_insert.checked:
                    o_item.child_list[-1].to_inserted_behind.append(to_insert)
                    to_insert.has_checked()


def get_merge_lines(offset, o_bmm_bm, i_bmm_bml):
    t_lines = []
    for m_item in o_bmm_bm:
        if not m_item.checked:
            if not m_item.is_directory():
                t_lines.append(m_item.content)
            else:
                t_lines.append(m_item.content)
                for l_item in o_bmm_bm[m_item.line_no - offset:m_item.get_domain() - offset]:
                    t_lines.extend(get_merge_lines(l_item.line_no - 1, o_bmm_bm[l_item.line_no -1  - offset:l_item.get_domain() - offset], i_bmm_bml))
            m_item.has_checked()
            for n_item in m_item.to_inserted_behind:
                for k_item in i_bmm_bml[n_item.line_no-1:n_item.get_domain()]:
                    t_lines.append(k_item.content)
    return t_lines


def open_src():
    import os
    import sys
    import re
    tmp_file_list = os.listdir(os.path.dirname(sys.path[0]))
    src_file = ""
    for t_file in tmp_file_list:
        if re.search(r'^bookmarks_\d+', t_file):
            src_file = t_file
            break


def merge_bookmark(file1, file2, output_file):
    bmm1 = BookMarkManager(file1)
    bmm1.initialize()
    bmm2 = BookMarkManager(file2)
    bmm2.initialize()
    bmm1.get_inserted_item(bmm2)
    final_lines = get_merge_lines(0, bmm1.bookmark_list, bmm2.bookmark_list)
    #print len(bmm1.bookmark_list)
    #for item in bmm1.bookmark_list:
    #    if item.to_inserted_behind:
    #        item.print_bookmark()
    file_o = open(output_file, 'w')
    file_o.writelines(map(lambda x: ''.join([x, "\n"]), final_lines))
    file_o.close()

if __name__ == '__main__':
    #merge_bookmark('../tmp1.txt', '../tmp2.txt', '../tmpfile')
    #merge_bookmark('../bookmarks.html', '../bookmarks_16_5_16_1.html', '../tmpfile')
    #merge_bookmark('../tmpfile', '../bookmarks_16_5_16_2.html', '../bookmarks_output.html')
    #merge_bookmark('../bookmarks_output.html', '../bookmarks_16_11_5.html', '../bookmarks_output2.html')
    merge_bookmark('../bookmarks_output2.html', '../bookmarks_2017_12_21.html', '../bookmarks_output3.html')