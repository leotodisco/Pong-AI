import pygame 
import paddle
import ball 

pygame.init()
WIDTH = 700
HEIGHT =  500
FPS = 60
WHITE = (255,255,255)
BLACK = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5
pygame.display.set_caption("Pong")


def handle_collision(ball:ball.Ball, leftPaddle:paddle.Paddle, rightPaddle:paddle.Paddle):
    if ball.y + ball.RADIUS >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.RADIUS <= 0:
        ball.y_vel *= -1
    
    
    if ball.x_vel < 0:
        #left paddle
        if ball.y >= leftPaddle.y and ball.y <= leftPaddle.y+leftPaddle.HEIGHT:
            if ball.x - ball.RADIUS <= leftPaddle.x + leftPaddle.WIDTH:
                ball.x_vel *= -1
                
                middle_y = leftPaddle.y + leftPaddle.HEIGHT / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (leftPaddle.HEIGHT / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= rightPaddle.y and ball.y <= rightPaddle.y+rightPaddle.HEIGHT:
            if ball.x + ball.RADIUS >= rightPaddle.x:
                ball.x_vel *= -1

                middle_y = rightPaddle.y + rightPaddle.HEIGHT / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (rightPaddle.HEIGHT / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    
    
    
def draw(win, leftPaddle, rightPaddle, ball):
    win.fill(BLACK)
    leftPaddle.draw(win)
    rightPaddle.draw(win)
    ball.draw(win)
    pygame.display.update()

def main():
    run = True  
    clock = pygame.time.Clock()
    
    left_paddle = paddle.Paddle(10, HEIGHT // 2 - paddle.Paddle.HEIGHT // 2)
    right_paddle = paddle.Paddle(WIDTH - 10 - paddle.Paddle.WIDTH, HEIGHT // 2 - paddle.Paddle.HEIGHT//2)
    palla = ball.Ball(WIDTH // 2, HEIGHT // 2)
    
    score_paddle_sinistra = 0
    score_paddle_destra = 0

    
    while run:
        clock.tick(FPS)
        draw(WIN, left_paddle, right_paddle, palla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 1:
            left_paddle.move(True)
        elif keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.HEIGHT <= HEIGHT-1: # sommo anche altezza della paddle perche y coincide con il primo punto del paddle
            left_paddle.move(False)
            
        palla.move()
        handle_collision(palla, left_paddle, rightPaddle=right_paddle)
        
        if palla.x < 0:
            score_paddle_destra += 1
            palla.reset()
        elif palla.x > WIDTH:
            score_paddle_sinistra += 1
            palla.reset()
        
        won = False
        if score_paddle_sinistra >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif score_paddle_destra >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            handle_vittoria(left_paddle, right_paddle, palla, win_text)


    pygame.quit()

def handle_vittoria(left_paddle, right_paddle, palla, win_text):
    text = SCORE_FONT.render(win_text, 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width() //
                            2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    palla.reset()
    left_paddle.reset()
    right_paddle.reset()
    score_paddle_sinistra = 0
    score_paddle_destra = 0

if __name__ == '__main__':
    main()