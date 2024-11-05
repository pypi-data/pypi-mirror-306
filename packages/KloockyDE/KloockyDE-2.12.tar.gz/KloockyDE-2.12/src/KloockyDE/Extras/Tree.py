from os.path import join, isfile, isdir, getsize, basename, abspath
from os import listdir
from KloockyDE.numberstuff import cap_float
from KloockyDE.helpers import merge_list


class Tree:
    def __init__(self, dirpath=None, **kwargs):
        if dirpath is None:
            dirpath = abspath('.')
        self.dirpath = dirpath
        self.perm_errors = []
        self.t_list = []
        self.m_depth = -1
        if 'max_depth' in kwargs:
            self.m_depth = kwargs['max_depth']
        self.filesize = False
        if 'show_filesize' in kwargs:
            self.filesize = kwargs['show_filesize']
        self.filecount = False
        if 'show_filecount' in kwargs:
            self.filecount = kwargs['show_filecount']
        self.show_empty = True
        if 'show_empty' in kwargs:
            self.show_empty = kwargs['show_empty']
        self.do_sort = True
        if 'sort_by_size' in kwargs:
            self.do_sort = kwargs['sort_by_size']
        self.print_progress = True
        if 'print_progress' in kwargs:
            self.print_progress = kwargs['print_progress']
        self._run()


    def _run(self):
        p = self.dirpath
        '''
        Generate tree from directory 'p'. Calculates size of directories
            files/directories as tuples:    (name, path, size in Bytes)
            [_dir_, [subdir1, [subdir1_1, subfile1_1_1], [subdir1_2], subfile1_1, subfile1_2], [subdir2], subfile]
            unaccessible files/directories will have size 0 and additionally collected in perm_errors
        :return: list   tree as list
        '''
        def rek(p_):
            try:
                f_ = [[f, join(p_[1], f)] for f in listdir(p_[1]) if isfile(join(p_[1], f))]
            except PermissionError:
                self.perm_errors.append(str(p_))
                return [tuple(list(p_) + [0])]
            f_ = [tuple(f + [getsize(f[1])]) for f in f_]
            d_ = [(d, join(p_[1], d)) for d in listdir(p_[1]) if isdir(join(p_[1], d))]
            x = 0
            for i_ in range(len(f_)):
                x += f_[i_][2]
            ans = []
            fc_ = len(f_)
            for i_ in range(len(d_)):
                if self.print_progress:
                    print(f'Now checking: {d_[i_][1]} ({i_ + 1}/{len(d_)} => {cap_float((i_ / len(d_)) * 100, 2)}% done)')
                ans.append(rek(d_[i_]))
                x += ans[-1][0][2]
                fc_ += ans[-1][0][3]
            x = tuple(list(p_) + [x, fc_])
            ans = [x] + ans + f_
            return ans

        files = [[f, join(p, f)] for f in listdir(p) if isfile(join(p, f))]
        files = [tuple(f + [getsize(f[1])]) for f in files]
        dirs = [(d, join(p, d)) for d in listdir(p) if isdir(join(p, d)) and d not in ['$RECYCLE.BIN']]
        foo = []
        size = 0
        fc = len(files)
        for i in range(len(dirs)):
            if self.print_progress:
                print(f'Now checking: {dirs[i][1]} ({i + 1}/{len(dirs)} => {cap_float((i / len(dirs)) * 100, 2)}% done)')
            foo.append(rek(dirs[i]))
            size += foo[-1][0][2]
            try:
                fc += foo[-1][0][3]
            except IndexError:
                print(foo[-1])
        for i in range(len(files)):
            foo.append(files[i])
            size += files[i][2]
        foo = [(basename(p), p, size, fc)] + foo
        self.t_list = foo
        if self.do_sort:
            self._sort()


    def _sort(self):
        tree_list = list(self.t_list)
        dirs, files = [], []
        for i in range(len(tree_list)):
            if i == 0:
                pass
            elif type(tree_list[i]) == list:
                dirs.append(tree_list[i])
            elif type(tree_list[i]) == tuple:
                files.append(tree_list[i])
        res = [tree_list[0]]
        for l in [dirs, files]:
            index = {}
            for i in range(len(l)):
                if type(l[i]) == tuple:
                    size = l[i][2]
                else:
                    size = l[i][0][2]
                if size in list(index.keys()):
                    index[size].append(l[i])
                else:
                    index[size] = [l[i]]
            order = sorted(list(index.keys()))[::-1]
            for size in order:
                for x in index[size]:
                    res.append(x)
        self.t_list = res


    def __str__(self):
        def tree_str(tree_list, offset=0, depth=0, vlines=''):
            '''
            Generate string from tree as generated in tree()
            :param tree_list: list  as generated in tree()
            :param max_depth: int   how many layers do you want to be shown? if -1, all will be shown
            :param offset:    int   internal use
            :param depth:     int   internal use
            :param filesize:  bool  do you want to show sizes of files?
            :param vlines:    str   internal use
            :return: str    printable tree
            '''

            def size(foo):  # return size as str
                n = foo
                l = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
                j = 0
                while n >= 1024:
                    j += 1
                    n = n / 1024
                n = cap_float(n, 2, False)
                if n == int(n):
                    n = int(n)
                n = str(n) + ' ' + l[j]
                # if (not self.show_empty) and n == '0 B':
                #     n = ''
                return n

            t, o = tree_list, offset
            if not self.show_empty:
                # print(t)
                t_ = []
                for i in range(len(t)):
                    if (type(t[i]) == list and t[i][0][2] == 0) or (i != 0 and type(t[i]) == tuple and t[i][2] == 0):
                        pass
                    else:
                        t_.append(t[i])
                t = t_
                del t_
            spacer = '  │ '
            spacing = vlines.replace('0', '    ').replace('1', spacer)
            dir_offset1 = '  └─'
            dir_offset2 = '  ├─'
            file_offset = spacing + '    '
            if self.m_depth != -1 and self.m_depth <= depth:  # max depth reached
                return t[0][0] + '\t' + size(t[0][2]) + (f'\t({t[0][3]} Files)' * int(self.filecount)) + '\n'
            res = ''
            for i in range(len(t)):  # for item in tree list
                if i == 0:  # this dir
                    try:
                        res += t[i][0] + '\t' + size(t[i][2]) + (f'\t({t[i][3]} Files)' * int(self.filecount)) + '\n'
                    except IndexError:
                        print('t', t)
                        print('t[i]', t[i])
                elif type(t[i]) == tuple:  # files
                    if self.filesize:
                        res += file_offset + t[i][0] + '\t' + size(t[i][2]) + '\n'
                    else:
                        res += file_offset + t[i][0] + '\n'
                elif type(t[i]) == list:  # directories
                    v = vlines + '1'
                    if (i == (len(t) - 1)) or type(t[i + 1]) != list:
                        v = v[:-1] + '0'
                    sub = tree_str(tree_list=t[i], offset=offset + 1, depth=depth + 1, vlines=v)
                    if (i == (len(t) - 1)) or type(t[i + 1]) != list:
                        sub = dir_offset1 + sub
                    else:
                        sub = dir_offset2 + sub
                    res += spacing + sub
            return res
        ret = ''
        if len(self.perm_errors) != 0:
            ret += 'PermissionErrors:\n'
            ret += merge_list(self.perm_errors, '\n')
            ret += '\nPermissionErrors Ende\n'
        ret += tree_str(self.t_list)
        return ret