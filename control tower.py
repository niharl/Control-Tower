#CONTROL TOWER
#by Nihar Lohan
#Based on the Android/iOS game by the same name
#https://play.google.com/store/apps/details?id=com.momcina.ctower_free&hl=en_GB
#Images snipped from original game
#Pygame 2.0 & Python 3.8.2

#Instructions:
    #Guide planes and helicopters to land by clicking on them and drawing pathways to the start of their runway/helipad
    #Planes can only land on runways and helicopters only at the helipad
    #Different types of aircraft have different speeds
    #If 2 aircraft collide midair you lose
    #Press P or SPACE to pause the game at any time

#Issues:
    #Planes don't always follow the centerline of the drawn path when at an angle
    #Rotation is quite sudden & discontinuous


import pygame
import random
import math

# Graphics window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PLANE_DIMENSION = 50
LANDED_PLANE_DIMENSION = 26
PLANE_SIZE = (PLANE_DIMENSION,PLANE_DIMENSION)
LANDED_PLANE_SIZE = [LANDED_PLANE_DIMENSION,LANDED_PLANE_DIMENSION]
NUMBER_OF_PLANES = 4
HELIPAD_TARGET_SIZE = 60
RUNWAY_TARGET_SIZE = 45
SAMPLING_RATE = 3
LANDING_DISTANCE = 10
high_score = 0

# Pygame initialisation
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Control Tower")
clock = pygame.time.Clock()
medium_font = pygame.font.SysFont("Comic Sans MS", 30)
major_info_font = pygame.font.SysFont("Comic Sans MS", 60)
major_font = pygame.font.SysFont("Comic Sans MS", 100)
instruction_font = pygame.font.SysFont("Comic Sans MS", 40)


#Loading Images
plane_images = []
for i in range(NUMBER_OF_PLANES):
    plane_images.append(pygame.transform.scale(pygame.image.load('Plane'+str(i+1)+'.png').convert_alpha(), (PLANE_SIZE)))
background = pygame.image.load('Background.png').convert_alpha()
explosion = pygame.transform.scale(pygame.image.load('Explosion.png').convert_alpha(),(100,100))
homepage = pygame.image.load('Home_Page.png').convert_alpha()
distances = [1.5,2,1.2,1]
landing_distances = [10,10,10,3]


class Runway:
    def __init__(self,startpoint,endpoint,helipad):
        if helipad: self.radius = HELIPAD_TARGET_SIZE
        else: self.radius = RUNWAY_TARGET_SIZE
        self.startpoint = startpoint
        self.endpoint = endpoint
    
    def check_if_landed(self,x,y):
        if math.hypot(abs(x-self.startpoint[0]),abs(y-self.startpoint[1])) <= RUNWAY_TARGET_SIZE: return True
        else: return False

class Landed_Plane:
    def __init__(self,start,runway,game,type,bearing):
        self.x = start[0] - LANDED_PLANE_DIMENSION//2
        self.y = start[1] - LANDED_PLANE_DIMENSION//2
        self.runway = runway
        self.waypoints = [game.runways[self.runway].endpoint]
        self.original = pygame.transform.scale(plane_images[type],LANDED_PLANE_SIZE)
        self.bearing = bearing
        self.distance = landing_distances[type]

    def draw_on(self,surface):
        self.img = pygame.transform.rotate(self.original,-self.bearing)
        surface.blit(self.img,(round(self.x),round(self.y)))

    def move_on(self,game,i):
        self.check_if_path_over(game,i)
        self.calculate_move()
        self.x += self.move_x
        self.y += self.move_y

    def check_if_path_over(self,game,i):
        if (abs(int(self.x)-self.waypoints[0][0]) <= 5 and abs(int(self.y)-self.waypoints[0][1]) <= 5):
            game.landed_planes.remove(i)
            game.planes[i] = None
            game.score += 1

    def calculate_move(self):
        distance_x = self.waypoints[0][0] - self.x
        distance_y = self.waypoints[0][1] - self.y
        total_distance = math.hypot(abs(distance_x),abs(distance_y))
        factor = total_distance/self.distance
        angle = math.degrees(math.atan(abs(distance_y/distance_x)))
        if distance_x >= 0 and distance_y >= 0:
            self.bearing = 90 + angle
        elif distance_x >= 0 and distance_y < 0:
            self.bearing = 90 - angle
        elif distance_x < 0 and distance_y < 0:
            self.bearing = 270 + angle
        else:
            self.bearing = 270 - angle
        self.move_x = distance_x/factor
        self.move_y = distance_y/factor


class Plane:
    def __init__(self,plane_images):
        self.type = random.randint(0,3)
        self.side = random.randint(0,3)
        self.next_side = self.side
        self.generate_next_side()
        self.x, self.y = self.generate_waypoint(self.side)
        if self.side == 0: self.y -= PLANE_DIMENSION
        elif self.side == 2: self.y += PLANE_DIMENSION
        elif self.side == 1: self.x += PLANE_DIMENSION
        elif self.side == 3: self.x -= PLANE_DIMENSION
        self.waypoints = [self.generate_waypoint(self.next_side)]
        while (self.side == 0 and self.waypoints[0][1] <= 200) or (self.side == 1 and self.waypoints[0][0] >= SCREEN_HEIGHT-200) or (self.side == 2 and self.waypoints[0][1] >= SCREEN_HEIGHT - 200) or (self.side == 3 and self.waypoints[0][0] <= 200) or (math.hypot(abs(self.waypoints[0][0] - self.x),abs(self.waypoints[0][1] - self.y)) <= 400):
            self.waypoints = [self.generate_waypoint(self.next_side)]
        self.original = plane_images[self.type]        
        self.line_drawn = False
        self.line_being_drawn = False
        self.distance = distances[self.type]
        self.centre_x = self.x + PLANE_DIMENSION/2
        self.centre_y = self.y + PLANE_DIMENSION/2
        if self.type <= 2: self.allowed_runways = [0,1]
        else: self.allowed_runways = [2]
        self.line_to_runway = False
        self.landing_runway = -1
        self.bearing = 0
        


    def generate_next_side(self):
        self.side = self.next_side
        self.next_side = random.randint(0,3)
        while self.next_side == self.side:
            self.next_side = random.randint(0,3)

    def generate_waypoint(self,side):
        if side == 0:
            return [random.randint(0,SCREEN_WIDTH-PLANE_DIMENSION),0]
        elif side == 1:
            return [SCREEN_WIDTH-PLANE_DIMENSION,random.randint(0,SCREEN_HEIGHT-PLANE_DIMENSION)]
        elif side == 2:
            return [random.randint(0,SCREEN_WIDTH-PLANE_DIMENSION),SCREEN_HEIGHT-PLANE_DIMENSION]
        elif side == 3:
            return [0,random.randint(0,SCREEN_HEIGHT-PLANE_DIMENSION)]

    def draw_on(self,surface):
        self.img = pygame.transform.rotate(self.original,(-self.bearing))#Alternative: -5*round(self.bearing/5))) #-this changes the accuracy of the bearing: the more accurate the more frequently tiny changes are made, the less accurate the more sudden the changes
        surface.blit(self.img,(round(self.x),round(self.y)))
    
    def check_if_path_over(self,game,i):
        check = True
        if (abs(int(self.x)-self.waypoints[0][0]) <= 2 and abs(int(self.y)-self.waypoints[0][1]) <= 2):
            if self.line_drawn == False and self.line_being_drawn == False:
                self.generate_next_side()
                self.waypoints = [self.generate_waypoint(self.next_side)]
                check = False

        while check and (abs(int(self.x)-self.waypoints[0][0]) <= 7 and abs(int(self.y)-self.waypoints[0][1]) <= 7):
            if (self.line_drawn) or (len(self.waypoints) > 1 and self.line_being_drawn) :
                j = self.waypoints.pop(0)
                if self.line_being_drawn and len(self.waypoints) == 1:
                    check = False
                if self.line_drawn:
                    if self.line_to_runway and len(self.waypoints) <= 1:
                            if len(self.waypoints) == 0: self.waypoints.append(j)
                            if (abs(int(self.x)-self.waypoints[0][0]) <= 3 and abs(int(self.y)-self.waypoints[0][1]) <= 3):
                                game.planes[i] = Landed_Plane([self.centre_x,self.centre_y],self.landing_runway,game,self.type,self.bearing)
                                game.landed_planes.append(i)
                                game.active_planes.remove(i)
                                game.line_drawn_planes.remove(i)
                            check = False
                    if len(self.waypoints) == 0:
                        self.calculate_straight_line_destination(game,i,j)
            else:
                check = False

    def calculate_straight_line_destination(self,game,i,j):
        destination_x = j[0]
        destination_y = j[1]
        while (0 <= destination_x + self.move_x <= SCREEN_WIDTH - PLANE_DIMENSION) and (0 <= destination_y + self.move_y <= SCREEN_HEIGHT - PLANE_DIMENSION):
            destination_x += self.move_x
            destination_y += self.move_y
        self.waypoints = [[destination_x,destination_y]]
        self.line_drawn = False
        self.line_to_runway = False
        if i in game.line_drawn_planes:
            game.line_drawn_planes.remove(i)

    def move_on(self,game,i):
        if not self.waypoints:
            print()
        self.check_if_path_over(game,i)
        self.calculate_move()
        self.x += self.move_x
        self.y += self.move_y
        self.centre_x += self.move_x
        self.centre_y += self.move_y

    def calculate_move(self):
        distance_x = self.waypoints[0][0] - self.x
        distance_y = self.waypoints[0][1] - self.y
        total_distance = math.hypot(abs(distance_x),abs(distance_y))
        factor = total_distance/self.distance
        if distance_x != 0:
            angle = math.degrees(math.atan(abs(distance_y/distance_x)))
        elif distance_x == 0 and distance_y >= 0:
            self.bearing = 0
        elif distance_x == 0 and distance_y < 0:
            self.bearing = 180
        if distance_x > 0 and distance_y >= 0:
            self.bearing = 90 + angle
        elif distance_x > 0 and distance_y < 0:
            self.bearing = 90 - angle
        elif distance_x < 0 and distance_y < 0:
            self.bearing = 270 + angle
        else:
            self.bearing = 270 - angle
        self.move_x = distance_x/factor
        self.move_y = distance_y/factor
            

    def check_for_collisions(self,start,screen,explosion,game,position):
        for i in range(start,len(game.planes)):
            check_plane = game.planes[i]
            if isinstance(check_plane,Plane):
                check_centre_x,check_centre_y = [check_plane.x + PLANE_DIMENSION/2,check_plane.y + PLANE_DIMENSION/2]
                self.centre_x,self.centre_y = [self.x + PLANE_DIMENSION/2,self.y + PLANE_DIMENSION/2]
                if math.hypot(abs(check_plane.centre_x - self.centre_x),abs(check_plane.centre_y - self.centre_y)) <= PLANE_DIMENSION:
                    if (self.x + PLANE_DIMENSION) < 10 or (self.x ) >= (SCREEN_WIDTH-10) or (self.y + PLANE_DIMENSION) < 10 or (self.y) >= (SCREEN_HEIGHT - 10):
                        game.active_planes.remove(position)
                        game.planes[position] = None
                        if position in game.line_drawn_planes:
                            game.line_drawn_planes.remove(position)
                    else:
                        location = [round((check_plane.centre_x+self.centre_x)/2)-50,round((check_plane.centre_y+self.centre_y)/2)-50]
                        screen.blit(explosion,location)
                        text = major_font.render("CRASH", 1, (255,255,255))
                        screen.blit(text, (380,250 ))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        return True
        return False

    def check_if_selected(self,event):
        x,y = pygame.mouse.get_pos()
        if math.hypot(abs(self.centre_x-x),abs(self.centre_y-y)) <= PLANE_DIMENSION/2:
            return True

    def draw_line(self,screen):
        start_x,start_y = [self.x + PLANE_DIMENSION/2,self.y + PLANE_DIMENSION/2]
        if self.line_to_runway: color = (255,255,255)
        else: color = (255,0,0)
        for j in range(len(self.waypoints)):
            end_x,end_y = self.waypoints[j]
            end_x += PLANE_DIMENSION/2
            end_y += PLANE_DIMENSION/2
            pygame.draw.line(screen,color,[start_x,start_y],[end_x,end_y],width = 5)
            start_x = end_x
            start_y = end_y


class Game:
    def __init__(self):
        self.frequency = 400
        self.planes = [Plane(plane_images)]
        self.time_since_last = 0
        self.mouse_down = False
        self.plane_selected = -1
        self.line_drawn_planes = []
        self.timer = 0
        self.runways = [Runway([728,208],[439,89],False),  
                        Runway([295,332],[537,70],False), 
                        Runway([697,520],[684,502],True)] 
        self.active_planes = [0]
        self.landed_planes = []
        self.score = 0
        self.crashed = False

    
    def add_plane(self):
        if (random.randint(0,self.frequency) == 0 and (self.time_since_last > 80 or (self.frequency < 200 and self.time_since_last > 30))) or len(self.active_planes) == 0:
            self.active_planes.append(len(self.planes))
            self.planes.append(Plane(plane_images))
            self.time_since_last = 0

    
    def move_planes(self):
        for i in self.active_planes:
            plane = self.planes[i]
            plane.move_on(self,i)
        for i in self.landed_planes:
            self.planes[i].move_on(self,i)

    def increment_time(self):
        self.time_since_last += 1
        self.timer += 1

    def collision_check(self,screen,explosion):
        for start in range(0,len(self.planes)-1):
            plane = self.planes[start]
            if isinstance(plane,Plane): self.crashed = plane.check_for_collisions(start+1,screen,explosion,self,start)
            if self.crashed: break

    def handle_mouse_click(self,event):
        for i in self.active_planes:
            plane = self.planes[i]
            if plane.check_if_selected(event):
                    self.plane_selected = i
                    self.mouse_down = True
                    self.timer = -5
                    if self.planes[i].line_drawn:
                        self.planes[i].calculate_straight_line_destination(self,i,self.planes[i].waypoints[0])
                    if self.planes[i].line_to_runway:
                        self.planes[i].line_to_runway = False
                    break

    def handle_mouse_up(self,event):
        if self.mouse_down:
            self.mouse_down = False
            self.planes[self.plane_selected].line_being_drawn = False
            self.planes[self.plane_selected].line_drawn = True
            self.planes[self.plane_selected].line_to_runway = False
            if not self.planes[self.plane_selected].waypoints:
                j = [self.planes[self.plane_selected].x + self.planes[self.plane_selected].move_x,self.planes[self.plane_selected].y + self.planes[self.plane_selected].move_y]
                self.planes[self.plane_selected].calculate_straight_line_destination(self,self.plane_selected,j)
            x,y = pygame.mouse.get_pos()
            for i in self.planes[self.plane_selected].allowed_runways:
                runway = self.runways[i]
                if runway.check_if_landed(x,y):
                    self.planes[self.plane_selected].line_to_runway = True
                    self.planes[self.plane_selected].landing_runway = i



    def reset_selected(self):
        if self.mouse_down and self.timer == -1:
                self.planes[self.plane_selected].waypoints = []
    
    def add_to_line(self):
        if self.timer == 0 and self.mouse_down:
            self.line_drawn_planes.append(self.plane_selected)
            self.planes[self.plane_selected].line_being_drawn = True
        if self.mouse_down and self.timer % SAMPLING_RATE == 0 and self.timer >= 0:
            x,y = pygame.mouse.get_pos()
            x -= PLANE_DIMENSION/2
            y -= PLANE_DIMENSION/2
            self.planes[self.plane_selected].waypoints.append([x,y]) 

    def plot_lines(self,screen):
        for i in self.line_drawn_planes:
            if self.planes[i].line_drawn or self.planes[i].line_being_drawn:
                self.planes[i].draw_line(screen)

    def draw_planes_on(self,screen):
        for i in self.landed_planes:
            self.planes[i].draw_on(screen)
        for i in self.active_planes:
            self.planes[i].draw_on(screen)
        

    def calculate_frequency(self):
        self.frequency = round(((0.8**(len(self.planes)/12)))*230) + 1

    def display_score(self,surface):    
        text = "SCORE: " + str(self.score)
        text = medium_font.render(text,1,(255,255,255))
        surface.blit(text,(10,10))

    def display_pause_icon(self,surface):
        surface.blit(home_icon, [850,30])

class Homescreen:
    def __init__(self,img):
        self.img = img
        start = major_font.render("START GAME",1,(255,255,255))
        width = start.get_width()
        height = start.get_height()
        self.start_game_position = [250,250+width,420,420+height]
    
    def display_start_button(self,surface):
        start = major_font.render("START GAME",1,(255,255,255))
        surface.blit(start,(275,420))
        width = start.get_width()
        height = start.get_height()
        self.start_game_position = [250,250+width,420,420+height]

    def display_highscore(self,surface):
        text = medium_font.render("Your highscore is " + str(high_score),1,(255,255,255))
        surface.blit(text,(407,520))

    def display_img(self,surface):
        surface.blit(self.img,(((SCREEN_WIDTH//2) - 210),40))
    
    def display_whole(self,surface):
        surface.fill((133,222,249))
        self.display_img(surface)
        self.display_start_button(surface)
        self.display_highscore(surface)
    
    def check_if_start(self,event):
        x,y = pygame.mouse.get_pos()
        if self.start_game_position[0] <= x <= self.start_game_position[1] and self.start_game_position[2] <= y <= self.start_game_position[3]:
            return True
        return False
    

def paused_message(screen):
    text = major_font.render("PAUSED", 1, (255,255,255))
    screen.blit(text, (361,250 ))
    text = instruction_font.render("Press the spacebar or P to continue playing",1,(255,255,255))
    screen.blit(text,(204,350))   
    text = instruction_font.render("Press escape or H to return home ",1,(255,255,255))
    screen.blit(text,(274,410))  

#Gameplay variables

home = Homescreen(homepage)
playing = False
paused = False
reborn = False
crashed = False

while True:
    clock.tick(40)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playing and not paused:
                game.handle_mouse_click(event)
            elif not playing:
                if home.check_if_start(event):
                    reborn = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if playing and not paused:
                game.handle_mouse_up(event)
        elif event.type == pygame.KEYDOWN:
            if not paused and playing:
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    paused = True
                    paused_message(screen)
                    pygame.display.update()
            elif paused and playing:
                if (event.key == pygame.K_ESCAPE or event.key == pygame.K_h):
                    paused = False
                    playing = False
                    if game.score > high_score:
                        high_score = game.score
                    home = Homescreen(homepage)
                elif (event.key == pygame.K_p or event.key == pygame.K_SPACE):
                    paused = False
    
    if reborn:
        playing = True
        game = Game()
        reborn = False
    
    if not playing:
        home.display_whole(screen)
        pygame.display.update()

    if playing and not paused:    
        game.add_to_line()
        
        game.add_plane()

        screen.blit(background,(0,0))

        game.move_planes()

        game.plot_lines(screen)

        game.draw_planes_on(screen)

        game.reset_selected()

        game.increment_time()

        game.calculate_frequency()

        game.display_score(screen)

        pygame.display.update()

        game.collision_check(screen,explosion)
        
        crashed = game.crashed

    if crashed:
        playing = False
        if game.score > high_score:
            high_score = game.score
        home = Homescreen(homepage)
        crashed = False