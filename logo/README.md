## Brief
A tool to generate letter logo for given logo content(letters only).  
Fonts come from some font designer webpages.  
Colors come from the website: [UI Gradients](https://uigradients.com/)  
Thanks a lot.   

## Mode

### Mode Auto

Set content, font and color.  
The program would generate layout automatically.  
e.g. `worker.py`

	logo = Logo()
	logo.set_font('typography')
	logo.set_colors('Noon to Dusk')
	logo.set_content('curme')
	img = logo.draw()
	# example1.bmp
	
	>>> python ./Workers/worker.py

> ![example1.bmp](./Logos/example1.bmp)  
> example1.bmp  
  
 ***
  
### Mode Manual

Set layout and color.  
The program would use the layout you design.  
e.g. `worker_pea6.py` & `pea6.logo`

	logo = Logo()
	with open('./pea6.logo', 'r+') as f: 
		layout = f.read().split('\n')
	logo.set_layout(layout)
	logo.set_colors('Sea Blue')
	img = logo.draw()
	# example2.bmp
	
	>>> python ./Workers/worker_pea6.py
	
>![example2.bmp](./Logos/example2.bmp)  
> example2.bmp