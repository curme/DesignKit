# @author   huizhan

import os

from PIL import Image

from logo import Logo

def save_fix_height(img, name, root='./Logos/', fixed_height=120):

    width, height = img.size
    width = int(width * fixed_height / height)
    size = (width, fixed_height)
    img = img.resize(size, Image.ANTIALIAS)           
    if not os.path.exists(root): os.makedirs(root)
    img.save(root + name +'.bmp', quality=100)


if __name__ == '__main__':
    

    logo = Logo()


    # example 1
    logo.set_font('typography')
    logo.set_colors('Noon to Dusk')
    logo.set_content('curme')
    logo_img = logo.draw()
    save_fix_height(logo_img, 'example1')


    # example 2
    with open('./Workers/pea6.logo', 'r+') as f:
        layout = f.read().split('\n')
    logo.set_layout(layout)
    logo.set_colors('Sea Blue')
    logo_img = logo.draw()
    save_fix_height(logo_img, 'example2')
