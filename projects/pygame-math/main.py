import random
import sys
import pygame

def make_question(rng=random):
    a,b=rng.randint(1,12),rng.randint(1,12)
    return a,b,a+b

def main():
    pygame.init()
    screen=pygame.display.set_mode((640,380))
    pygame.display.set_caption("Math Sprint")
    font=pygame.font.SysFont(None,52)
    small=pygame.font.SysFont(None,30)
    a,b,answer=make_question()
    typed=""
    score=0
    clock=pygame.time.Clock()
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:running=False
                elif event.key==pygame.K_BACKSPACE:typed=typed[:-1]
                elif event.key==pygame.K_RETURN:
                    if typed and int(typed)==answer:score+=1
                    else:score=max(0,score-1)
                    a,b,answer=make_question()
                    typed=""
                elif event.unicode.isascii() and event.unicode.isdigit() and len(typed)<4:
                    typed+=event.unicode
        screen.fill((12,21,38))
        for message,y,f in [(f"{a} + {b} = ?",110,font),(typed or "Type an answer and press Enter",190,small),(f"Score: {score}   |   Esc: quit",300,small)]:
            screen.blit(f.render(message,True,(222,240,255)),(45,y))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
if __name__=="__main__":main()
