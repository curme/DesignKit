# @author   huizhan

import os

from logo import Logo

if __name__ == '__main__':

    store_root = './Logos/'

    logo = Logo()

    content = 'gea6'
    with open('./Workers/gea6.logo', 'r+') as f:
        layout = f.read().split('\n')
    logo.set_layout(layout)

    # get colors
    colors = os.listdir('./Colors/')
    colors = [color.split('.')[0] for color in \
        colors if color.split('.')[-1]=='jpg']

    for color in colors:
        logo.set_colors(color)

        logo_img = logo.draw()            
        save_path = store_root + content + '/'
        img_name = color + '.bmp'
        if not os.path.exists(save_path): os.makedirs(save_path)
        logo_img.save(save_path + img_name)
