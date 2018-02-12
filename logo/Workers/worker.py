# @author   huizhan

import os

from logo import Logo

if __name__ == '__main__':

    store_root = './Logos/'

    logo = Logo()

    content = 'curme'

    # get fonts
    fonts = os.listdir('./Fonts/')
    fonts = [font for font in fonts \
        if len(font.split('.'))==1]

    # get colors
    colors = os.listdir('./Colors/')
    colors = [color.split('.')[0] for color in \
        colors if color.split('.')[-1]=='jpg']


    for font in fonts:
        logo.set_font(font)
        logo.set_content(content)

        for color in colors:
            logo.set_colors(color)

            logo_img = logo.draw()            
            save_path = store_root + content + '/'
            save_path+= font + '/'
            img_name = color + '.bmp'
            if not os.path.exists(save_path): os.makedirs(save_path)
            logo_img.save(save_path + img_name)
