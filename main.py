import pygame
import pygame_gui
import time
import pygame.freetype
#innit
pygame.init()
starttime = time.time()
pygame.mixer.init()
bigfont = pygame.freetype.Font("font.ttf", 75)
font = pygame.freetype.Font("font.ttf", 24)

'''
TODO

put in doors
put in elevators 
make objects like paper work or hard drives yk
make playing
make saving
make loading


'''

#window
originalscreenheight = 1920/2
originalscreenwidth = 1080/2

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Synapse')
scrx, scry = screen.get_size()

running = True

#images
maintitle, rect = bigfont.render("Synapse", (0, 0, 0))
mainbackround = pygame.image.load("backround.png")




scene = 1


#UI
manager = pygame_gui.UIManager((scrx, scry), theme_path="main.json")

#main
singleplayer_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2-125, scry/2-35), (250, 70)),text='Singleplayer',manager=manager)
multiplayer_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2-125, scry/2+35), (250, 70)),text='Multiplayer',manager=manager)
settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2-125, scry/2+175), (250, 70)),text='Settings',manager=manager)
levelbuilder_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2-125, scry/2+105), (250, 70)),text='Level Builder',manager=manager)
close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, scry - 70), (100, 70)),text='Close',manager=manager)
#settings
volume_slider =  pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((scrx/2+ 40, scry/2), (250, 30)),start_value=0,value_range=[0,100],manager=manager)
volume_slider.hide()
volume_text, rect = font.render("Volume", (0,0,0))
fullscreen_text, rect = font.render("Fullscreen", (0,0,0))
fullscreen_button_on =pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2+50, scry/2-50), (100, 40)),text='On',manager=manager)
fullscreen_button_off =pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2+150, scry/2-50), (100, 40)),text='Off',manager=manager)
settings_back = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2-100, scry/2 + 100), (180, 70)),text='Back',manager=manager)
fullscreen_button_on.hide()
fullscreen_button_off.hide()
settings_back.hide()
newlevel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2-125, scry/2-35), (250, 70)),text='New Level',manager=manager)
loadfile_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx/2-125, scry/2+35), (250, 70)),text='Load File',manager=manager)
newlevel_button.hide()
loadfile_button.hide()

#level building
rooms = []
rooms.append(pygame.image.load("room0.png"))
rooms.append(pygame.image.load("room1.png"))
rooms_buttons = []
selected_room = 0
for i in range(len(rooms)):
	rooms_buttons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((70 * i)+20,scry-90), (70, 70)),text='',manager=manager))
	rooms_buttons[i].hide()
def show_roombuttons():
	for i in range(len(rooms)):
		rooms_buttons[i].show()
camx = 0
camy = 0
roomtype = []
roomx = []
roomy = []
roomwidth = []
roomheight = []
roomdir = []

wallx = []
wally = []
wallx1 = []
wally1 = []

doorx = []
doory = []
doorrot = []
doorclosed = pygame.image.load("doorclosed.png")
dooropen = pygame.image.load("dooropen.png")
doorshadow = pygame.image.load("doorshadow.png")

placewalls_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx-700,scry-90), (140, 70)),text='Place Walls',manager=manager)
placedoors_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx-560,scry-90), (140, 70)),text='Place Doors',manager=manager)
playlevel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx-140,scry-90), (140, 70)),text='Play Level',manager=manager)
savelevel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx-280,scry-90), (140, 70)),text='Save Level',manager=manager)
togglehitboxes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx-420,scry-90), (140, 70)),text='Show Hitboxes',manager=manager)
delete_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scrx-800,scry-90), (100, 70)),text='Delete',manager=manager)

placewalls_button.hide()
placedoors_button.hide()
playlevel_button.hide()
savelevel_button.hide()
togglehitboxes_button.hide()
delete_button.hide()
makewallx = 0
makewally = 0 
show_hitboxes = False
objrot = 360
zoom = 1
mouseup = True
def updateui():
	singleplayer_button.set_position((scrx/2-125,scry/2-35))
	multiplayer_button.set_position((scrx/2-125, scry/2+35))
	settings_button.set_position((scrx/2-125, scry/2+175))
	levelbuilder_button.set_position((scrx/2-125, scry/2+105))
	volume_slider.set_position((scrx/2+ 40, scry/2))
	fullscreen_button_on.set_position((scrx/2+50, scry/2-50))
	fullscreen_button_off.set_position((scrx/2+150, scry/2-50))
	settings_back.set_position((scrx/2-90, scry/2+140))
	close_button.set_position((0, scry - 70))
	newlevel_button.set_position((scrx/2-125,scry/2-35))
	loadfile_button.set_position((scrx/2-125, scry/2+35))
	for i in range(len(rooms)):
		rooms_buttons[i].set_position(((70 * i)+20,scry-90))
	placewalls_button.set_position((scrx-700,scry-90))
	placedoors_button.set_position((scrx-560,scry-90))
	playlevel_button.set_position((scrx-140,scry-90))
	savelevel_button.set_position((scrx-280,scry-90))
	togglehitboxes_button.set_position((scrx-420,scry-90))
	delete_button.set_position((scrx-800,scry-90))

def hideui():
	singleplayer_button.hide()
	multiplayer_button.hide()
	settings_button.hide()
	levelbuilder_button.hide()
	volume_slider.hide()
	fullscreen_button_on.hide()
	fullscreen_button_off.hide()
	settings_back.hide()
	close_button.hide()
	newlevel_button.hide()
	loadfile_button.hide()
	for i in range(len(rooms)):
		rooms_buttons[i].hide()
	placewalls_button.hide()
	placedoors_button.hide()
	playlevel_button.hide()
	savelevel_button.hide()
	togglehitboxes_button.hide()
	delete_button.hide()

def inwall(rect):
	#pygame.Rect.colliderect(rect1, rect)
	for i in range(len(wallx)):
		if wallx[i] == wallx1[i]:
			if wally[i] < wally1[i]:
				if pygame.Rect.colliderect(pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom),8*zoom,abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom)))), rect):
					return True
								
			elif wally[i] > wally1[i]:
				if pygame.Rect.colliderect(pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom)-abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom))),8*zoom,abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom)))), rect):
					return True		
		else:
			if wallx[i] < wallx1[i]:
				if pygame.Rect.colliderect(pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom),abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))),8*zoom), rect):
					return True
			elif wallx[i] > wallx1[i]:
				if pygame.Rect.colliderect(pygame.Rect((wallx[i]*(50*zoom))+camx-abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))), (wally[i]*(50*zoom))+camy-(4*zoom),abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))),8*zoom), rect):
					return True


def indoor(rect):
	pygame.draw.rect(screen, (0,0,0), rect)
	indoor = False
	for i in range(len(doorx)):
		if doorrot[i] == 270 or doorrot[i] == 180 and pygame.Rect.colliderect(pygame.Rect((doorx[i]*50*zoom)+camx+10,(doory[i]*50*zoom)+camy+10,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-30   ,  pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-25), rect):
			indoor = True
		elif doorrot[i] == 90 and pygame.Rect.colliderect(pygame.Rect((doorx[i]*50*zoom)+20+camx+(pygame.transform.scale(doorclosed,(doorclosed.get_width()*zoom,doorclosed.get_height()*zoom)).get_height()) - pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width(),(doory[i]*50*zoom)+10+camy,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-20,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-30), rect):
			indoor = True
		elif doorrot[i] == 360 and pygame.Rect.colliderect(pygame.Rect((doorx[i]*50*zoom)+10+camx,(doory[i]*50*zoom)+camy+10+(10*zoom)+(pygame.transform.scale(doorclosed,(doorclosed.get_width()*zoom,doorclosed.get_height()*zoom)).get_height()) - pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()+10   ,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-30,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-20), rect):
			indoor = True
	return indoor




screen = pygame.display.set_mode([originalscreenheight, originalscreenwidth])
scrx, scry = screen.get_size()
updateui()

clock = pygame.time.Clock()
volume_slider.set_current_value(100)


while running:
	
	scrx, scry = screen.get_size()
	screen.fill((0,0,0))
	time_delta = clock.tick(60)/1000.0
	mx,my = pygame.mouse.get_pos()



	#scaling
	mainbackround = pygame.transform.scale(mainbackround, (scrx,scry))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				camy += 100
			if event.key == pygame.K_a:
				camx += 100
			if event.key == pygame.K_s:
				camy -= 100
			if event.key == pygame.K_d:
				camx -= 100
			if event.key == pygame.K_r and scene == 5.1:
				objrot -= 90
				if objrot <= 0:
					objrot = 360
		manager.process_events(event)
		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == singleplayer_button:
				print("hella")
			if event.ui_element == multiplayer_button:
				print("hella")
			if event.ui_element == settings_button:
				scene = 2
				hideui()
				volume_slider.show()
			if event.ui_element == fullscreen_button_on:
				screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
				scrx, scry = screen.get_size()
				updateui()
				
			if event.ui_element == fullscreen_button_off:
				screen = pygame.display.set_mode([originalscreenheight, originalscreenwidth])
				scrx, scry = screen.get_size()
				updateui()
			if event.ui_element == settings_back:
				scene = 1
				hideui()
			if event.ui_element == close_button:
				running = False
			if event.ui_element == levelbuilder_button:
				scene = 5
				hideui()
			if event.ui_element == newlevel_button:
				scene = 5.1
				hideui()
			if event.ui_element == loadfile_button:
				scene = 5.1
				hideui()
			for i in range(len(rooms)):
				if event.ui_element == rooms_buttons[i]:
					selected_room = i
			if event.ui_element == togglehitboxes_button:
				show_hitboxes = not show_hitboxes
			if event.ui_element == delete_button:
				selected_room = -1
			if event.ui_element == placewalls_button:
				selected_room = -2
			if event.ui_element == placedoors_button:
				selected_room = -3

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4 and scene == 5.1:
				zoom += 0.1
			if event.button == 5 and scene == 5.1:
				zoom -= 0.1
			if zoom >= 1.9:
				zoom = 1.8
			elif zoom <= 0.5:
				zoom = 0.6

	if scene == 1:
		singleplayer_button.show()
		multiplayer_button.show()
		levelbuilder_button.show()
		settings_button.show()
		close_button.show()
		screen.fill((255,255,255))
		screen.blit(mainbackround, (0,0))
		
		screen.blit(maintitle, ((scrx/2)-160,scry/10))
	if scene == 2:
		screen.blit(mainbackround, (0,0))
		pygame.draw.rect(screen, (100,100,100), pygame.Rect(scrx/2-120, scry/2 -70, 440, 120))
		screen.blit(maintitle, ((scrx/2)-160,scry/10))
		volume_slider.show()
		settings_back.show()
		
		pygame.mixer.music.set_volume(volume_slider.get_current_value()/100)
		screen.blit(volume_text,(scrx/2-100,scry/2 + 5))

		fullscreen_button_on.show()
		fullscreen_button_off.show()
		screen.blit(fullscreen_text,(scrx/2-100,scry/2 -40))
	if scene == 5:
		settings_back.show()
		newlevel_button.show()
		loadfile_button.show()
	if scene == 5.1:
		
		if camy >=1500:
			camy = 1400
		elif camy <= -1500:
			camy = -1400
		if camx >=1500:
			camx = 1400
		elif camx <= -1500:
			camx = -1400


		show_roombuttons()
		placewalls_button.show()
		placedoors_button.show()
		playlevel_button.show()
		savelevel_button.show()
		togglehitboxes_button.show()
		delete_button.show()
		touchingroom = False			
		if len(roomtype) > 0 and selected_room >= 0:
			for i in range(len(roomtype)):
				if pygame.Rect.colliderect(pygame.Rect(roomx[i]*zoom*50+camx+5,roomy[i]*zoom*50+camy+5,(roomwidth[i]*zoom)-10,(roomheight[i]*zoom)-10), pygame.Rect((((mx+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_width()/2)-camx)//(50*zoom))*(50*zoom))+camx, (((my+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_height()/2)-camy)//(50*zoom))*(50*zoom))+camy, rooms[selected_room].get_width()/2*zoom, rooms[selected_room].get_height()/2*zoom)):
					touchingroom = True
		
		screen.fill((150,150,150))

		for i in range (int(round(-2500*zoom)),int(round(2500*zoom)), int(round(50*zoom))):
			pygame.draw.line(screen, (0,0,0),((i)+camx,2500+camy),((i)+camx,-2500+camy),width=round(5*zoom))
		for i in range (int(round(-2500*zoom)),int(round(2500*zoom)), int(round(50*zoom))):
			pygame.draw.line(screen, (0,0,0),(2500+camx,(i)+camy),(-2500+camx,(i)+camy),width=round(5*zoom))

		pygame.draw.line(screen, (255,0,0),(-100+camx,camy),(100+camx,camy),width=round(5*zoom))
		pygame.draw.line(screen, (255,0,0),(camx,-100+camy),(camx,100+camy),width=round(5*zoom))

		if event.type == pygame.MOUSEBUTTONUP:
			mouseup = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			if selected_room >= 0 and not pygame.Rect(0, scry-100, scrx, 100).collidepoint(mx,my) and touchingroom == False :
				print("block placed")
				roomtype.append(selected_room)
				roomx.append((mx+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_width()/2)-camx)//(50*zoom))
				roomy.append((my+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_height()/2)-camy)//(50*zoom))
				roomwidth.append(rooms[selected_room].get_width()/2)
				roomheight.append(rooms[selected_room].get_height()/2)
				roomdir.append(objrot)

			elif selected_room == -1 and not pygame.Rect(0, scry-100, scrx, 100).collidepoint(mx,my) and mouseup:
				mouseup = False
				deleted = False
				for i in range(len(wallx)-1):
					if wallx[i] == wallx1[i]:
						if wally[i] < wally1[i]:
							if pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom),8*zoom,abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom)))).collidepoint(mx, my):
								del wallx[i]
								del wally[i]
								del wallx1[i]
								del wally1[i]
								deleted = True
								
						elif wally[i] > wally1[i]:
							if pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom)-abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom))),8*zoom,abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom)))).collidepoint(mx, my):
								del wallx[i]
								del wally[i]
								del wallx1[i]
								del wally1[i]
								deleted = True		
					else:
						if wallx[i] < wallx1[i]:
							if pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom),abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))),8*zoom).collidepoint(mx, my):
								del wallx[i]
								del wally[i]
								del wallx1[i]
								del wally1[i]
								deleted = True
						elif wallx[i] > wallx1[i]:
							if pygame.Rect((wallx[i]*(50*zoom))+camx-abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))), (wally[i]*(50*zoom))+camy-(4*zoom),abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))),8*zoom).collidepoint(mx, my):
								del wallx[i]
								del wally[i]
								del wallx1[i]
								del wally1[i]
								deleted = True
				if not deleted:
					for i in range(len(roomtype)):
						if pygame.Rect(roomx[i]*zoom*50+camx+5,roomy[i]*zoom*50+camy+5,(roomwidth[i]*zoom)-10,(roomheight[i]*zoom)-10).collidepoint(mx, my):
							del roomtype[i]
							del roomx[i]
							del roomy[i]
							del roomwidth[i]
							del roomheight[i]
							del roomdir[i]
							break
							deleted = True


			elif selected_room == -2 and not pygame.Rect(0, scry-100, scrx, 100).collidepoint(mx,my):

				if makewallx == 0 and mouseup and not indoor(pygame.Rect(((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom),((my+(25*zoom)-camy)//(50*zoom))*(50*zoom),5,5)):
					makewallx =	((mx+(25*zoom)-camx)//(50*zoom))
					makewally = ((my+(25*zoom)-camy)//(50*zoom))
				elif mouseup and not (makewallx in wallx and makewally in wally and ((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom)+camx in wallx1 and ((my+(25*zoom)-camy)//(50*zoom))*(50*zoom)+camy in wally1) and not indoor(pygame.Rect(((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom),((my+(25*zoom)-camy)//(50*zoom))*(50*zoom),5,5)):
						#if (makewallx == ((mx+(25*zoom)-camx)//(50*zoom)) and (makewally < ((my+(25*zoom)-camy)//(50*zoom)) and indoor(pygame.Rect((makewallx*(50*zoom))+camx, (makewally*(50*zoom))+camy-(4*zoom),8*zoom,abs((((my+(25*zoom)-camy)//(50*zoom))*(50*zoom))-(makewally*(50*zoom)))))))    or   (makewally > ((my+(25*zoom)-camy)//(50*zoom)) and indoor(   pygame.Rect((makewallx*(50*zoom))+camx, (makewally*(50*zoom))+camy-(4*zoom)-abs((((my+(25*zoom)-camy)//(50*zoom))*(50*zoom))-(makewally*(50*zoom))),8*zoom,abs((((my+(25*zoom)-camy)//(50*zoom))*(50*zoom))-(makewally*(50*zoom)))    ))) or (makewallx < ((mx+(25*zoom)-camx)//(50*zoom)) and indoor(pygame.Rect((makewallx*(50*zoom))+camx, (makewally*(50*zoom))+camy-(4*zoom),abs((((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom))-(makewallx*(50*zoom))),8*zoom))) or (makewallx > ((mx+(25*zoom)-camx)//(50*zoom)) and indoor(pygame.Rect((makewallx*(50*zoom))+camx-abs((((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom))-(makewallx*(50*zoom))), (makewally*(50*zoom))+camy-(4*zoom),abs((((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom))-(makewallx*(50*zoom)))))):
					tsfine = True
					for i in range(len(doorx)):
						time.sleep(0.2)
						if doorrot[i] == 270 or doorrot[i] == 180 and pygame.Rect((doorx[i]*50*zoom)+camx+10,(doory[i]*50*zoom)+camy+10,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-30   ,  pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-25).clipline(((makewallx-camx)*(50*zoom),(makewally-camy)*(50*zoom)),(((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom),((my+(25*zoom)-camy)//(50*zoom))*(50*zoom))):
							tsfine = False
						elif doorrot[i] == 90 and pygame.Rect((doorx[i]*50*zoom)+20+camx+(pygame.transform.scale(doorclosed,(doorclosed.get_width()*zoom,doorclosed.get_height()*zoom)).get_height()) - pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width(),(doory[i]*50*zoom)+10+camy,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-20,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-30).clipline(((makewallx-camx)*(50*zoom),(makewally-camy)*(50*zoom)),(((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom),((my+(25*zoom)-camy)//(50*zoom))*(50*zoom))):
							tsfine = False
						elif doorrot[i] == 360 and pygame.Rect((doorx[i]*50*zoom)+10+camx,(doory[i]*50*zoom)+camy+10+(10*zoom)+(pygame.transform.scale(doorclosed,(doorclosed.get_width()*zoom,doorclosed.get_height()*zoom)).get_height()) - pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()+10   ,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-30,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-20).clipline(((makewallx-camx)*(50*zoom),(makewally-camy)*(50*zoom)),(((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom),((my+(25*zoom)-camy)//(50*zoom))*(50*zoom))):
							tsfine = False
						pygame.draw.rect(screen,(0,0,0),pygame.Rect((doorx[i]*50*zoom)+10+camx,(doory[i]*50*zoom)+camy+10+(10*zoom)+(pygame.transform.scale(doorclosed,(doorclosed.get_width()*zoom,doorclosed.get_height()*zoom)).get_height()) - pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()+10   ,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-30,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-20))
						pygame.draw.line(screen,(255,255,255), ((makewallx-camx)*(50*zoom),(makewally-camy)*(50*zoom)),(((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom),((my+(25*zoom)-camy)//(50*zoom))*(50*zoom)),10)
						pygame.display.flip()
					print(i)
					print(tsfine)
					if tsfine:
						wallx.append(makewallx)
						wally.append(makewally)
						wallx1.append(((mx+(25*zoom)-camx)//(50*zoom)))
						wally1.append(((my+(25*zoom)-camy)//(50*zoom)))
					makewallx = 0
					makewally = 0


				


				mouseup = False
			elif selected_room == -3 and not pygame.Rect(0, scry-100, scrx, 100).collidepoint(mx,my):
				if not inwall(pygame.Rect(((mx-(doorshadow.get_width()/2))//(50*zoom))*(50*zoom)+10,((my-(doorshadow.get_height()/2))//(50*zoom))*(50*zoom)+10,doorshadow.get_width()-20,doorshadow.get_height()-20)):
					if objrot == 360:
						doorx.append(((mx-camx-(doorshadow.get_width()/2)))//(50*zoom))
						doory.append(((my-camy-(doorshadow.get_height()/2)))//(50*zoom)+1)
						doorrot.append(objrot)
					elif objrot == 270 or objrot == 180:
						doorx.append(((mx-camx-(doorshadow.get_width()/2)))//(50*zoom))
						doory.append(((my-camy-(doorshadow.get_height()/2)))//(50*zoom))
						doorrot.append(objrot)
					elif objrot == 90:
						doorx.append(((mx-camx-(doorshadow.get_width()/2)))//(50*zoom)+1)
						doory.append(((my-camy-(doorshadow.get_height()/2)))//(50*zoom))
						doorrot.append(objrot)


		for i in range(len(roomtype)):
			screen.blit(pygame.transform.rotate(pygame.transform.scale(rooms[roomtype[i]], (250*zoom,250*zoom)),roomdir[i]),(((roomx[i])*(50*zoom))+camx,((roomy[i])*(50*zoom))+camy))


		if selected_room >= 0 and touchingroom == False:
			screen.blit(pygame.transform.rotate(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)), objrot),((((mx+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_width()/2)-camx)//(50*zoom))*(50*zoom))+camx,(((my+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_height()/2)-camy)//(50*zoom))*(50*zoom))+camy))
		elif selected_room >= 0:
			screen.blit(pygame.transform.rotate(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)), objrot),((((mx+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_width()/2)-camx)//(50*zoom))*(50*zoom))+camx,(((my+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_height()/2)-camy)//(50*zoom))*(50*zoom))+camy))

			redsurf = (pygame.Surface((rooms[selected_room].get_height() / 2 * zoom, rooms[selected_room].get_width() / 2 * zoom), pygame.SRCALPHA))
			redsurf.fill((255, 0, 0, 128))
			screen.blit(redsurf, (((((mx+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_width()/2)-camx)//(50*zoom))*(50*zoom))+camx),((((my+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_height()/2)-camy)//(50*zoom))*(50*zoom))+camy)))

		for i in range(len(wallx)):
			pygame.draw.line(screen,(0,255,0), (wallx[i]*(50*zoom)+camx,wally[i]*(50*zoom)+camy),(wallx1[i]*(50*zoom)+camx,wally1[i]*(50*zoom)+camy), width=int(4*zoom))
		if selected_room == -2 and not makewallx == 0:
			if makewallx == ((mx+(25*zoom)-camx)//(50*zoom)) or makewally == ((my+(25*zoom)-camy)//(50*zoom)):
				pygame.draw.line(screen,(0,255,0), (makewallx*(50*zoom)+camx,makewally*(50*zoom)+camy),(((mx+(25*zoom)-camx)//(50*zoom))*(50*zoom)+camx,((my+(25*zoom)-camy)//(50*zoom))*(50*zoom)+camy), width=int(4*zoom))
		elif selected_room == -3:
			if not inwall(pygame.Rect(((mx-(doorshadow.get_width()/2))//(50*zoom))*(50*zoom)+10,((my-(doorshadow.get_height()/2))//(50*zoom))*(50*zoom)+10,doorshadow.get_width()-20,doorshadow.get_height()-20)):
				screen.blit(pygame.transform.scale(pygame.transform.rotate(doorshadow, objrot),(doorshadow.get_width()*zoom,doorshadow.get_height()*zoom)), (((((mx-camx-(doorshadow.get_width()/2)))//(50*zoom)))*(50*zoom)+camx,((((my-camy-(doorshadow.get_height()/2)))//(50*zoom)))*(50*zoom)+camy))


		for i in range(len(doorx)):
			screen.blit(pygame.transform.scale(pygame.transform.rotate(doorclosed,doorrot[i]),(pygame.transform.rotate(doorclosed,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorclosed,doorrot[i]).get_height()*zoom)), ((doorx[i]*50*zoom)+camx, (doory[i]*50*zoom)+camy))


		#show hitboxes
		if show_hitboxes:		
			for i in range(len(roomtype)):
				pygame.draw.rect(screen, (255,0,0),pygame.Rect(roomx[i]*zoom*50+camx+5,roomy[i]*zoom*50+camy+5,(roomwidth[i]*zoom)-10,(roomheight[i]*zoom)-10), 3)
			if selected_room >= 0:
				pygame.draw.rect(screen, (0,0,255),pygame.Rect((((mx+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_width()/2)-camx)//(50*zoom))*(50*zoom))+camx, (((my+(25*zoom)-(pygame.transform.scale(rooms[selected_room], (250*zoom,250*zoom)).get_height()/2)-camy)//(50*zoom))*(50*zoom))+camy, rooms[selected_room].get_width()/2*zoom, rooms[selected_room].get_height()/2*zoom),3)

			for i in range(len(wallx)):
				if wallx[i] == wallx1[i]:
					if wally[i] < wally1[i]:
						pygame.draw.rect(screen,(255,165,0),pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom),8*zoom,abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom)))), int(2*zoom))
					elif wally[i] > wally1[i]:
						pygame.draw.rect(screen,(255,165,0),pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom)-abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom))),8*zoom,abs((wally1[i]*(50*zoom))-(wally[i]*(50*zoom)))), int(2*zoom))
				else:
					if wallx[i] < wallx1[i]:
						pygame.draw.rect(screen,(255,165,0),pygame.Rect((wallx[i]*(50*zoom))+camx, (wally[i]*(50*zoom))+camy-(4*zoom),abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))),8*zoom), int(2*zoom))
					elif wallx[i] > wallx1[i]:
						pygame.draw.rect(screen,(255,165,0),pygame.Rect((wallx[i]*(50*zoom))+camx-abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))), (wally[i]*(50*zoom))+camy-(4*zoom),abs((wallx1[i]*(50*zoom))-(wallx[i]*(50*zoom))),8*zoom), int(2*zoom))

			for i in range(len(doorx)):
				if doorrot[i] == 270 or doorrot[i] == 180:
					pygame.draw.rect(screen,(144,42,0),pygame.Rect((doorx[i]*50*zoom)+camx+10,(doory[i]*50*zoom)+camy+10,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-30   ,  pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-25), 3)
				elif doorrot[i] == 90:
					pygame.draw.rect(screen,(144,42,0),pygame.Rect((doorx[i]*50*zoom)+20+camx+(pygame.transform.scale(doorclosed,(doorclosed.get_width()*zoom,doorclosed.get_height()*zoom)).get_height()) - pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width(),(doory[i]*50*zoom)+10+camy,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-20,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-30), 3)
				elif doorrot[i] == 360:
					pygame.draw.rect(screen,(144,42,0),pygame.Rect((doorx[i]*50*zoom)+10+camx,(doory[i]*50*zoom)+camy+10+(10*zoom)+(pygame.transform.scale(doorclosed,(doorclosed.get_width()*zoom,doorclosed.get_height()*zoom)).get_height()) - pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()+10   ,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_width()-30,pygame.transform.scale(pygame.transform.rotate(doorshadow,doorrot[i]),(pygame.transform.rotate(doorshadow,doorrot[i]).get_width()*zoom,pygame.transform.rotate(doorshadow,doorrot[i]).get_height()*zoom)).get_height()-20), 3)

		pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, scry-100, scrx, 100))
		manager.draw_ui(screen)
		for i in range(len(rooms)):
			screen.blit(pygame.transform.scale(rooms[i], (50,50)),((70 * i)+30,scry-80))






	manager.update(time_delta) 
	if scene != 5.1:
		manager.draw_ui(screen)
	pygame.display.update()
pygame.quit()