import pygame
import math
import inputbox
import random
import os
import socket, pickle


# Call this function so the Pygame library can initialize itself
pygame.init()

# -- music --

file = 'Tetris.mp3'
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
GREY = (186, 192, 194)

PI = math.pi

# Set the width and height of each snake segment
segment_width = 5
segment_height = 5

# Set angel
angel = 0
radius = 1000


#set game
gameover = False
score = 0
play = False

# set screen
singleplayer = False
multiplayer = False

#sat server
create_game = False
join_game = False
select_server = False
connecting_to_server = True
connected = False
disconnected = False
host = False
connected_joining_screen = False
startgame = False
hit_apple = False
placement = 0
score_print = []
printing_score = False
give_score = True

# Default name
change_player_name = True

#set count imte
time_count = 0
n = 1
k = 1

#Set background images
bg = pygame.image.load("menu_bg.png")


# Placing button that is clickable.
def button(msg,x,y,w,h,ic,ac,action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    smallText = pygame.font.SysFont("comicsansms",20)
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        textSurf, textRect = text_objects(msg, smallText, ac)
        if click[0] == 1 and action == True:
            action = False
        elif click[0] == 1:
            action = True
            
            
    else:
        textSurf, textRect = text_objects(msg, smallText, ic)

    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    
    screen.blit(textSurf, textRect)
    return action
    

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y,sprite_image, width, height):
        # Call the parent's constructor
        super().__init__()

        self.image = pygame.image.load(sprite_image).convert()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.image.set_colorkey(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y      
    
    def opposite_pos (self):
        if self.rect.x < 1:
            self.rect.x = screen_width
        if self.rect.x > screen_width:
            self.rect.x = 1

        if self.rect.y > screen_height:
            self.rect.y = 1
        if self.rect.y < 1:
            self.rect.y = screen_height

class Eat_segment(Segment):

    def reset_pos_con(self, con_x, con_y):
        self.rect.x = con_x
        self.rect.y = con_y

    def reset_pos (self):
        self.rect.x = random.randrange(0, screen_width-15)
        self.rect.y = random.randrange(0, screen_height-15)    
    

# Set text
font1 = pygame.font.SysFont("comicsansms", 20)
font2 = pygame.font.SysFont("comicsansms", 50)
 
# Create an 800x600 sized screen
screen_width = 960
screen_height = 640
screen = pygame.display.set_mode([screen_width, screen_height])
 
# Set the title of the window
pygame.display.set_caption('Heaven Snake')

allspriteslist = pygame.sprite.Group()
 
# Create an initial snake
snake_segments = []
first_snake_segment = []
three_snake_segment = []
for i in range(10):
    x = 450 - (segment_width)/5 * i
    y = 500
    if i == 0:
        player = Segment(x, y, "snake_head.png", segment_width, segment_height)
        first_snake_segment.append(player)
        allspriteslist.add(player)
        
    else:
        
        if i > 0 and i <4:
            three_segment = Segment(x, y, "snake_head.png", segment_width, segment_height)
            three_snake_segment.append(three_segment)
            allspriteslist.add(three_segment)
        else:
            segment = Segment(x-10, y, "snake_head.png", segment_width, segment_height)
            snake_segments.append(segment)
            allspriteslist.add(segment)

# Create an snake eat object
snake_eat_segments = []
for i in range(1):
    x = 846
    y = 140
    eat_segment = Eat_segment(x, y, "apple.png", 15, 15)
    snake_eat_segments.append(eat_segment)
    allspriteslist.add(eat_segment)


clock = pygame.time.Clock()
done = False

while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # -- Draw everything -- #
    # Clear screen
    screen.fill(BLACK)
    screen.blit(bg, (0,0))
    
    if singleplayer:
        
        allspriteslist.draw(screen)
        if not connected:
            scoreText = font1.render("Score " + str(score), 1, WHITE)
            screen.blit(scoreText,(20,10))
        else:

            for i in range (len(playerlist)):
                if printing_score:
                    gameoverText = font1.render(playerlist[i].decode("utf-8") + " Score " + score_print[i].decode("utf-8"), 1, WHITE)
                    screen.blit(gameoverText,(20,10 + i * 50))
            

    elif multiplayer:

        if change_player_name:
            player_name = inputbox.ask(screen, 'Name: ')
            if len(player_name) <= 0:
                player_name = "player"
            print("PlayerName: "+player_name)
            change_player_name = False
        
        if create_game:
            
            os.system('pythonw server.py')
            
        if select_server:
            if connecting_to_server:
                host = inputbox.ask(screen, 'Ip: ')
                port = inputbox.ask(screen, 'port: ')
                
                if len(port) <= 0:
                    port = 9000
                if len(host) <= 0:
                    print("s")
                    host ="localhost"
                    
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect((host,int(port)))
                print("conected!")
                
                connecting_to_server = False
                connected_joining_screen = True
                
                data_player_name = player_name
                data_player_name = pickle.dumps(b"playername=" + bytes(data_player_name, 'UTF-8'))
                server.send(data_player_name)
                
                data_welcome = server.recv(1024)
                data_welcome = pickle.loads(data_welcome)
                data_welcome = data_welcome.decode("utf-8")
                if data_welcome[0] == "W":
                    print(data_welcome)

                data_host = server.recv(1024)
                data_host = pickle.loads(data_host)
                if data_host == b"1":
                    print ("host")
                    host = True
                    placement = data_host.decode("utf-8")
                else:
                    host = False
                    placement = data_host.decode("utf-8")
                print(placement)
                    
            if connected_joining_screen:
                if host:
                    startgame = button("Start Game",(screen_width)-210,10,250,50,WHITE,GREY,startgame)
                    if startgame:
                        data_start = pickle.dumps(b"startgame=True")
                        server.send(data_start)


                data_status = pickle.dumps(b"connected=True")
                server.send(data_status)
            
                data = server.recv(1024)
                data = pickle.loads(data)

                if data[0] == b'playername=':
                    playerlist = data[1]
                    for i in range (len(data[1])):                  
                        gameoverText = font1.render(data[1][i], 1, WHITE)
                        screen.blit(gameoverText,((screen_width/2) - 150,((screen_height/2) - 200) + i * 50))

                
                if data == b'startgame':
                    connected_joining_screen = False
                    multiplayer = False
                    singleplayer = True
                    select_server = False
                    connected = True
                    
                
        else:
            multiplayer = button("return",(screen_width/2)-110,50,250,50,WHITE,GREY,multiplayer)
            select_server = button("Join Game",(screen_width/2)-40,280,120,50,WHITE,GREY,select_server)
            create_game = button("Create Game",(screen_width/2)-40,340,120,50,WHITE,GREY,create_game)
            change_player_name = button("Change name",(screen_width/2)-40,400,120,50,WHITE,GREY,change_player_name)
        
        
    elif not singleplayer and not multiplayer:
        
        singleplayer = button("Singleplayer",(screen_width/2)-40,150,120,50,WHITE,GREY,singleplayer)
        multiplayer = button("Multiplayer",(screen_width/2)-40,220,120,50,WHITE,GREY,multiplayer)
        done = button("Quit",(screen_width/2)-40,280,120,50,WHITE,GREY,done)

    # -- Game Logic -- #
    if singleplayer:
            
        
        if not gameover:

            #change angel for direction      
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                angel -= 0.05 * n * (180/PI)

                time_count += 1
                if time_count == 10:
                    n += 1
                
            else:
                n = 1
                
            if pressed[pygame.K_RIGHT]:
                angel += 0.05 * k * (180/PI)
                time_count += 1
                if time_count == 10:
                    k += 1
                
            else:
                k = 1
                
            if time_count == 30:
                time_count = 0
            if n >= 6:
                n = 6
            if k >= 6:
                k = 6

            
            segment.opposite_pos()
            player.opposite_pos()
            three_segment.opposite_pos()

            player_hit_list = pygame.sprite.spritecollide(player, snake_segments, False)
            
            
            for playerhit_segment in player_hit_list:
                print ("hiting")
                gameover = True
            
            # See if the player block has collided with block.
            snake_hit_list = pygame.sprite.spritecollide(player, snake_eat_segments, False)
            
            for eat in snake_hit_list:
                
                # Reset position
                if connected:
                    hit_apple = True
                    # generate pos
                    data_generate_pos = pickle.dumps(b'generate_pos')
                    server.send(data_generate_pos)
                    
                    
                    

                else:
                    eat.reset_pos()
                    score += 1
                    for i in range (3):
                        snake_segments.insert(0, segment)
                        allspriteslist.add(segment)
            

            # Set initial speed
            x_change = math.cos(math.radians(angel)) * radius
            y_change = math.sin(math.radians(angel)) * radius
         
            # Figure out where new segment will be
            x = (first_snake_segment[0].rect.x + x_change/200)
            y = (first_snake_segment[0].rect.y + y_change/200)
            player = Segment(x, y, "snake_head.png", segment_width, segment_height)

            three_segment = Segment(x, y, "snake_head.png", segment_width, segment_height)
            
            x = three_snake_segment[2].rect.x
            y = three_snake_segment[2].rect.y
            segment = Segment(x, y, "snake_head.png", segment_width, segment_height)

        
         
            # Insert new segment into the list
            first_snake_segment.insert(0, player)
            allspriteslist.add(player)

            three_snake_segment.insert(0, three_segment)
            allspriteslist.add(three_segment)

            snake_segments.insert(0, segment)
            allspriteslist.add(segment)
            
            

            # Get rid of last segment of the snake
            # .pop() command removes last item in list
            old_segment = first_snake_segment.pop()
            allspriteslist.remove(old_segment)
            
            old_segment = three_snake_segment.pop()
            allspriteslist.remove(old_segment)

            old_segment = snake_segments.pop()
            allspriteslist.remove(old_segment)

            # -- Server Logic -- #
            if connected:
                
                if player.rect.x < 0:
                    player.rect.x = 0
                    
                if player.rect.y < 0:
                    player.rect.y = 0


                data_score = pickle.dumps(b"score=" + bytes(str(score), "utf-8") + b"=" + bytes(placement, "utf-8"))
                server.send(data_score)
                    
                #data_snake_pos_x = player.rect.x
                #data_snake_pos_y = player.rect.y
                #data_snake_pos = b'snake_pos'
                #data_snake_pos = pickle.dumps(data_snake_pos)
                #server.send(data_snake_pos)
                
                data = server.recv(1024)
                data = pickle.loads(data)



                #-- Get apple pos --#
                if data[0] == b'applepos':
                    print("change applepos")
                    apple_pos_y = data[2]
                    apple_pos_x = data[1]
                    
                    eat_segment.reset_pos_con(apple_pos_x, apple_pos_y)
                    if hit_apple:
                        give_score = True
                    hit_apple = False

                elif data[0] == b'score':
                    score_print = data[1]
                    printing_score = True


                
                if hit_apple:
                    
                    data_snake_hit_apple = pickle.dumps(b'hitapple')
                    server.send(data_snake_hit_apple)
                    print("hit")

                    if give_score:
                        score += 1

                        for i in range (3):
                            snake_segments.insert(0, segment)
                            allspriteslist.add(segment)
                        
                        give_score = False

                
                
                
            
        
        elif gameover:
            if not connected:
                gameoverText = font2.render("GAME OVER!", 1, WHITE)
                screen.blit(gameoverText,((screen_width/2) - 150,(screen_height/2) - 200))
                
                
                gameover = button("Restart",(screen_width/2)-30,200,100,30,WHITE,GREY,gameover)
                    
                # -- Reseting -- #
                if not gameover:
                    score = 0
                    allspriteslist.empty()
                    snake_eat_segments = []
                    snake_segments = []
                    first_snake_segment = []
                    three_snake_segment = []
                    angel = 0
                    
                    for i in range(10):
                        x = 450 - (segment_width)/5 * i
                        y = 500
                        if i == 0:
                            player = Segment(x, y, "snake_head.png", segment_width, segment_height)
                            first_snake_segment.append(player)
                            allspriteslist.add(player)
                            
                        else:
                            
                            if i > 0 and i <4:
                                three_segment = Segment(x, y, "snake_head.png", segment_width, segment_height)
                                three_snake_segment.append(three_segment)
                                allspriteslist.add(three_segment)
                            else:
                                segment = Segment(x-10, y, "snake_head.png", segment_width, segment_height)
                                snake_segments.append(segment)
                                allspriteslist.add(segment)

                    # Create an snake eat object
                    for i in range(1):
                        x = random.randrange(0, screen_width-15)
                        y = random.randrange(0, screen_height-15)
                        eat_segment = Eat_segment(x, y, "apple.png", 15, 15)
                        snake_eat_segments.append(eat_segment)
                        allspriteslist.add(eat_segment)
        else:
            gameoverText = font2.render("GAME OVER!", 1, WHITE)
            screen.blit(gameoverText,((screen_width/2) - 150,(screen_height/2) - 200))
                
            disconnected = button("disconnected",(screen_width/2)-30,200,100,30,WHITE,GREY,disconnected)
            if disconnected:
                server.close()
            
        
     
    # Flip screen
    pygame.display.flip()
 
    # Pause
    clock.tick(30)
 
pygame.quit()
