import pygame
import random
pygame.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    GREY = 128,128,128
    BACKGROUND_COLOR = WHITE
    GRADIENT = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]
    FONT = pygame.font.SysFont("comicsans", 20)
    LARGE_FONT = pygame.font.SysFont("comicsans", 30)
    SIDE_PAD = 100
    TOP_PAD = 150
    
    def __init__(self,width,height,lst):
        self.width = width
        self.height = height
        
        self.window = pygame.display.set_mode((width,height)) # Set the window size
        pygame.display.set_caption("Sorting Algorithm and Visvulizer")
        self.set_lst(lst)
    
    def set_lst(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        
        self.block_width = round(self.width - self.SIDE_PAD )/ len(lst)
        self.block_height = ((self.height - self.TOP_PAD) / (self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD//2

def draw(Draw_info):
    Draw_info.window.fill(Draw_info.BACKGROUND_COLOR)
    controls = Draw_info.FONT.render("R - RESET | SPACE - START | A - ASCENDING | D - DESCENDING", 1, Draw_info.BLACK)
    Draw_info.window.blit(controls, (Draw_info.width/2-controls.get_width()/2, 5))
    controls = Draw_info.FONT.render("I - INSERTION SORT | B - BUBBLE SORT ", 1, Draw_info.BLACK)
    Draw_info.window.blit(controls, (Draw_info.width/2-controls.get_width()/2, 35))
    draw_list(Draw_info)
    pygame.display.update()
    
def draw_list(draw_info,color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect) 
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIENT[i % 3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()  
        
def generate_starting_list(n,min_val,max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
        
    return lst  
        
def bubble_sort(draw_info,ascending = True): 
    Lst = draw_info.lst
    for i in range (len(Lst)-1):
        for j in range(len(Lst)-i-1):
            num1 = Lst[j]
            num2 = Lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                Lst[j], Lst[j+1] = Lst[j+1], Lst[j]
                draw_list(draw_info,{j:draw_info.RED,j+1:draw_info.GREEN},True)
                yield True
    return Lst

    
def main():
    
    run = True
    sorting = False
    ascending = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n,min_val,max_val)
    draw_info = DrawInformation(800,600,lst)
    
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None
    while run:
        clock.tick(60) # FPS
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_lst(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True  
                sorting_algo_generator = sorting_algorithm(draw_info,ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True  
            elif event.key == pygame.K_d and not sorting:
                ascending = False 
    pygame.quit()   

if __name__ == "__main__":
    main()
    
    