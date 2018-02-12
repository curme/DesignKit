# @author   huizhan

'''
    A tool to generate letter logo for given logo content(letters only).
    Fonts come from some font designer webpages.
    Colors come from the website: https://uigradients.com/
    Thanks a lot. 

    Mode auto

        set content, font and color.
        the program would generate layout automatically.
        e.g. worker.py

    Mode manual

        set layout and color.
        the program would use the layout you design.
        e.g. worker_pea6.py & pea6.logo

    --
    Apologize for the ugly codes.
'''

from itertools import product

import numpy
from PIL import Image, ImageDraw


# @brief    decorator
#           used to check if the font has been set
def _check_font(func):
    def wrap(self, *args, **kargs):
        if self.font == None or self.letters == {}:
            print('font has not been set.')
            return False
        return func(self, *args, **kargs)
    return wrap


# @brief    decorator
#           used to check if the layout has been generated
def _check_layout(func):
    def wrap(self, *args, **kargs):
        if self.layout == None:
            print('layout has not been created.')
            return False
        return func(self, *args, **kargs)
    return wrap


# @brief    decorator
#           used to check if the color has been set
def _check_color(func):
    def wrap(self, *args, **kargs):
        if 'bg_name' not in self.color.keys():
            print('color has not been set.')
            return False
        return func(self, *args, **kargs)
    return wrap


# @brief    generate logo layout automatically
#           should be given the logo content and font
class Layoutor:


    # @brief    generate cubic layout
    def cubic(self, count):

        cube_side = int(count ** 0.5)
        cube_side+= 0 if cube_side**2 == count else 1

        # get diagonal first and the fining it
        lines = [i+1 for i in range(cube_side)][::-1]
        count-= sum(lines)

        # drop overfill chars
        empty_lines = len([line for line \
            in lines if line == 0])
        line_offset = cube_side - empty_lines
        while count < 0:
            count += 1
            lines[line_offset-1] -= 1
            line_offset -= 1
            if line_offset < 1:
                empty_lines += 1
                line_offset = cube_side - empty_lines

        # fill vacancy
        full_lines = len([line for line \
            in lines if line == cube_side])
        line_offset = full_lines + 1
        while count > 0:
            count -= 1
            lines[line_offset-1] += 1
            line_offset += 1
            if line_offset > cube_side:
                full_lines += 1
                line_offset = full_lines + 1

        return lines


    # @brief    revise the cubic layout by decrease lines
    #           because cubic layout's height almostly 
    #           greater than width
    def merge_line(self, cubic, merge_lines):

        merge_chars = sum(cubic[len(cubic)-merge_lines:])
        lines = cubic[:len(cubic)-merge_lines]

        # fill the rest lines of the cubic layout
        while merge_chars is not 0:

            merge_chars -= 1
            minist = min(lines)
            min_index = lines.index(minist)
            lines[min_index] += 1

        return lines


    # @brief    calculate the difference between the 
    #           height and width of the given layout
    def diff_wh(self, lines, content, letters):


        # calculate the width of the layout
        # is the maximium width among the lines exactly
        line_widths = [[] for _ in range(len(lines))]
        
        line_offset = 0
        for line_index, line_chars in enumerate(lines):
            for char_index in range(1, line_chars+1):
                index = line_offset + char_index
                char = content[index-1]
                char_width = len(letters[char][0])
                line_widths[line_index].append(char_width)
            line_offset += line_chars

        for line_width in line_widths:
            line_width.append(len(line_width)-1)
        layout_width = max([sum(line) for \
            line in line_widths])

        # calculate the height of the layout
        lines_count = len(lines)
        layout_height = len(letters['a']) * \
            lines_count + lines_count - 1

        # the difference
        diff = abs(layout_height - layout_width)
        return diff
        
    
    # @brief    a default layout mode
    #           would generate the layout automatically, 
    #           with aligning the logo content top and left
    def left_top(self, content, letters):

        cubic = self.cubic(len(content))
        best_lines = cubic
        best_wh_diff = self.diff_wh(cubic, content, letters)

        # revise lines
        merge_lines = 0
        while 1:
            merge_lines += 1
            new_lines = self.merge_line(cubic, merge_lines)
            new_wh_diff = self.diff_wh(new_lines, content, letters)
            if new_wh_diff <= best_wh_diff:
                best_wh_diff = new_wh_diff
                best_lines = new_lines
            else: break
        best_lines = [item for item in best_lines if item is not 0]

        # generate layout
        layout = None
        line_char_offset = 0
        for line_chars in best_lines:
            node_lines = None
            for line_char_index in range(1, line_chars+1):
                index = line_char_index + line_char_offset
                char = content[index-1]
                char_node_lines = letters[char]
                # print(char, char_node_lines)
                if node_lines is None: node_lines = letters[char]
                else:
                    node_lines = [line+'0' for line in node_lines]
                    for nl_index in range(len(char_node_lines)):
                        node_lines[nl_index] += char_node_lines[nl_index]
                # print(char, node_lines)
            if layout is None: layout = node_lines
            else:
                layout += ['seperate']
                layout += node_lines
            line_char_offset += line_chars

        # fill vacancy
        max_width = max([len(line) for line in layout])
        replace = lambda x: '0'*max_width if x=='seperate' else x
        fill = lambda x: x + '0'*(max_width-len(x))
        layout = [fill(replace(line)) for line in layout]
        # fill border
        layout = ['0'*max_width]*3 + layout
        layout = layout + ['0'*max_width]*3
        layout = ['000'+line+'000' for line in layout]

        return layout


# @brief    logo class
class Logo:


    def __init__(self):

        self.content = None
        self.font = None
        self.letters = {}
        self.node_cubes = None
        self.cube_side = None
        self.color = {}
        self.layout = None
        self.layoutor = Layoutor()


    # @brief    set font
    def set_font(self, font):

        self.font = font

        # read letters' code
        letters = 'abcdefghijklmnopqrstuvwxyz'
        with open('./Fonts/%s'%font, 'r+') as f:
            codes = f.read().split('\n')
        for i, letter in zip(range(26), letters):
            width = int(codes[i][0])
            code = codes[i][1:]
            code = [code[i*width:(i+1)*width] for \
                i in range(int(len(code)/width))]
            self.letters[letter] = code


    # @brief    set color
    def set_colors(self, color_bg=None, color_fg=None):
    
        # read background color
        if color_bg is not None:
            bg = Image.open('./Colors/%s.jpg' % color_bg)
            w, h = bg.size
            w, h = w-1, h-1
            bg_pix = bg.load()
            bg_start = numpy.array(list(bg_pix[0,0])[:3])
            bg_end = numpy.array(list(bg_pix[w,h])[:3])
            self.color['bg_name'] = color_bg
            self.color['bg_start'] = bg_start
            self.color['bg_end'] = bg_end
        else:
            self.color['bg_name'] = 'bg default'
            self.color['bg_start'] = numpy.array([0,0,0])
            self.color['bg_end'] = numpy.array([0,0,0])

        # read foreground color
        if color_fg is not None:
            fg = Image.open('./Colors/%s.jpg' % color_fg)
            w, h = fg.size
            w, h = w-1, h-1
            fg_pix = fg.load()
            fg_start = numpy.array(list(fg_pix[0,0])[:3])
            fg_end = numpy.array(list(fg_pix[w, h])[:3])
            self.color['fg_name'] = color_fg
            self.color['fg_start'] = fg_start
            self.color['fg_end'] = fg_end
        else:
            self.color['fg_name'] = 'fg default'
            self.color['fg_start'] = numpy.array([255,255,255])
            self.color['fg_end'] = numpy.array([255,255,255])


    # @brief    set content
    @_check_font
    def set_content(self, content):

        self.content = content.lower()

        # generate layout
        self.layout = self.layoutor.left_top(\
            self.content, self.letters)


    # @brief    set content
    def set_layout(self, layout):
        self.layout = layout


    # @brief    draw logo
    @_check_layout
    @_check_color
    def draw(self, node_cubes=10, cube_side=1):

        # get logo board
        # the digit in the layout is named as NODE
        # and each NODE comsists of several cubes
        y_nodes = len(self.layout)
        x_nodes = len(self.layout[0])
        y_cubes = y_nodes * node_cubes
        x_cubes = x_nodes * node_cubes
        board_height = cube_side * y_cubes
        board_width  = cube_side * x_cubes
        board_size   = (board_width, board_height)
        board = Image.new('RGB', board_size, (255,255,255))
        draw  = ImageDraw.Draw(board)

        # get color for the logo board
        color_bged = self.color['bg_end']
        color_fged = self.color['fg_end']
        color_bgst = self.color['bg_start']
        color_fgst = self.color['fg_start']
        # calculate the color gap between the conjunct cubes
        color_bg_step = color_bged - color_bgst
        color_fg_step = color_fged - color_fgst
        color_bg_step = numpy.divide(color_bg_step, y_cubes + x_cubes - 1)
        color_fg_step = numpy.divide(color_fg_step, y_cubes + x_cubes - 1)

        # draw logo
        y_axis, x_axis = range(y_cubes), range(x_cubes)
        for y, x in product(y_axis, x_axis):

            # generate the area for current position
            y_s, x_s = y * cube_side, x * cube_side
            y_e, x_e = y_s+cube_side, x_s+cube_side
            area = [x_s, y_s, x_e, y_e]

            # generate the color for current position
            if self.layout[int(y/node_cubes)][int(x/node_cubes)] == '1':
                color = color_fgst+color_fg_step*(x+y)
                color = [int(item) for item in color]
                color = tuple(color)
            else: 
                color = color_bgst+color_bg_step*(x+y)
                color = [int(item) for item in color]
                color = tuple(color)

            draw.rectangle(area, fill=color)

        return board
