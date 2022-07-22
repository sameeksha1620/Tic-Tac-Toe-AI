import pygame
import random
import copy
#import array as arr
win_x = 800
win_y = 600
box_size = 100
board_x = win_x/2 - 3*box_size/2
board_y = win_y/2 - 3*box_size/2

def cross(a,b):
    s = 30
    pygame.draw.line(win,(225,225,225),[a-s,b-s],[a+s,b+s],2)
    pygame.draw.line(win,(225,225,225),[a+s,b-s],[a-s,b+s],2)

def board(x,y,z):
    l = 3*z
    pygame.draw.line(win,(225,225,225),[x, y], [x + l, y], 2)
    pygame.draw.line(win,(225,225,225),[x, y+z], [x + l, y+z], 2)
    pygame.draw.line(win,(225,225,225),[x, y+2*z], [x+l, y+2*z], 2)
    pygame.draw.line(win,(225,225,225),[x, y+l], [x+l, y+l], 2)
    pygame.draw.line(win,(225,225,225),[x, y], [x, y+l],2)
    pygame.draw.line(win,(225,225,225),[x+z,y],[x+z, y+l],2)
    pygame.draw.line(win,(225,225,225),[x+2*z, y], [x+2*z, y+l],2)
    pygame.draw.line(win,(225,225,225),[x+l,y],[x+l,y+l],2)

def zero(a,b):
    s = 40
    pygame.draw.ellipse(win,(225,225,225),(a-s/2,b-(s+s/2)/2,s,s+s/2),2)

def check(game_data):
    for i in range (0,3):
        if game_data[i][0] == game_data[i][1] and game_data[i][0] == game_data[i][2]:
            if game_data[i][0] != -1:
                return True
        if game_data[0][i] == game_data[1][i] and game_data[0][i] == game_data[2][i]:
            if game_data[0][i] != -1:
                return True
    if game_data[0][0] == game_data[1][1] and game_data[0][0] == game_data[2][2]:
        if game_data[0][0] != -1:
            return True
    if game_data[0][2] == game_data[1][1] and game_data[1][1] == game_data[2][0]:
        if game_data[1][1] != -1:
            return True
    return False

def clear_scr(game_data):
    for i in range (0,3):
        for j in range (0,3):
            game_data[i][j] = -1

def random_move(game_data):
    x1 = [random.randint(0,2),random.randint(0,2)]
    if game_data[x1[0]][x1[1]] == -1:
        return x1
    else:
        return random_move(game_data)

def tie_checker(game_data):
    for i in range (0,3):
        for j in range (0,3):
            if game_data[i][j] == -1:
                return False
    return True

def AI(game_data):
    game_data_store = copy.deepcopy(game_data)
    #print("AI game data",game_data)
    #print("AI game data store",game_data_store)
    cost = [0]
    cost_val = [10000]
    cost_pr = -100000
    best_move = [-1,-1]
    for i in range (0,3):
        for j in range (0,3):
            if game_data_store[i][j] == -1:
                game_data_store[i][j] = 1
                if check(game_data_store):
                    game_data[i][j] = 1
                    print("AI Best Move")
                    return
                game_data_store[i][j] = 0
                if check(game_data_store):
                    game_data[i][j] = 1
                    print("AI Best Move")
                    return
                game_data_store[i][j] = 1


                cost_val[0] -= 1000
                AI_min(game_data_store, cost, cost_val)
                #print("Cost for i,j ",i," ",j," is",cost[0])
            if cost[0] > cost_pr:
                cost_pr = cost[0]
                best_move[0] = i
                best_move[1] = j
            cost[0] = 0
            game_data_store = copy.deepcopy(game_data)
            cost_val[0] = 10000
    if game_data[best_move[0]][best_move[1]] == -1:
        game_data[best_move[0]][best_move[1]] = 1
        print("AI Best Move")
    else:
        ran_move = random_move(game_data)
        if game_data[ran_move[0]][ran_move[1]] == -1:
            game_data[ran_move[0]][ran_move[1]] = 1
            print("AI Random Move")






def AI_max(game_data_store, cost, cost_val):
    free_place = 0
    max_game_data_store = copy.deepcopy(game_data_store)
    for i in range (0,3):
        for j in range (0,3):
            if game_data_store[i][j] == -1:
                game_data_store[i][j] = 1
                free_place += 1
                if check(game_data_store):
                    cost[0] += cost_val[0]
                else:
                    cost_val[0] -= 100
                    AI_min(game_data_store, cost, cost_val)
                    max_game_data_store = copy.deepcopy(game_data_store)
            if free_place == 0:
                return

def AI_min(game_data_store, cost, cost_val):
    free_place = 0
    min_game_data_store = copy.deepcopy(game_data_store)
    for i in range (0,3):
        for j in range (0,3):
            if game_data_store[i][j] == -1:
                game_data_store[i][j] = 0
                free_place += 1
                if check(game_data_store):
                    cost[0] -= cost_val[0]
                else:
                    cost_val[0] -= 1000
                    AI_max(game_data_store, cost, cost_val)
                    min_game_data_store = copy.deepcopy(game_data_store)
            if free_place == 0:
                return

game_data = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
win = pygame.display.set_mode((win_x,win_y))
pygame.display.set_caption("Tic-Tac")
run = True
count = 1
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if count % 2 == 1:
                    loc1 = -1
                    loc2 = -1
                    if pos[0] > 250 and pos[0] < 350:
                        loc1 = 0
                    if pos[0] > 350 and pos[0] < 450:
                        loc1 = 1
                    if pos[0] > 450 and pos[0] < 550:
                        loc1 = 2
                    if pos[1] > 150 and pos[1] < 250:
                        loc2 = 0
                    if pos[1] > 250 and pos[1] < 350:
                        loc2 = 1
                    if pos[1] > 350 and pos[1] < 450:
                        loc2 = 2
                    if loc1 >= 0 and loc2 >= 0:
                        game_data[loc1][loc2] = 0
                        print("User Move")
                        if check(game_data) :
                            print("Zero won")
                            clear_scr(game_data)
                        if tie_checker(game_data):
                            print("Game Tie")
                            clear_scr(game_data)

                        count +=1
    if count % 2 == 0:
        AI(game_data)
        if check(game_data):
            print("AI won")
            clear_scr(game_data)
        if tie_checker(game_data):
            print("Game Tie")
            clear_scr(game_data)
        count +=1
    win.fill((0,0,0))
    board(board_x,board_y,box_size)
    for i in range (0,3):
        for j in range (0,3):
            if game_data[i][j] == 0:
                zero(win_x/2 + (i-1)*box_size,win_y/2 + (j-1)*box_size)
            if game_data[i][j] == 1:
                cross(win_x/2 + (i-1)*box_size,win_y/2 + (j-1)*box_size)

    pygame.display.update()
pygame.quit()
