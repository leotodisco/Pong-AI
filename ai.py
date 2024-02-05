import pygame
from pong import Game
import neat
import os
import pickle

class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball
        
    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        WIDTH  = 700
        HEIGHT = 500

        window = pygame.display.set_mode((WIDTH, HEIGHT))

        game = Game(window, WIDTH, HEIGHT)
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)
                
            output = net.activate(
                (self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()
        
        
    def train_ai(self, genome1, genome2, config):
        nn1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        nn2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        
        
        run = True
        #clock = pygame.time.Clock()
        while run:
            #clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    
            outpu1 = nn1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision1 = outpu1.index(max(outpu1))
            outpu2 = nn2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision2 = outpu2.index(max(outpu2))
            
            if decision1==0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)
            
                        
            if decision2==0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=False)
            else:
                self.game.move_paddle(left=False, up=False)
            
            
            
            info = self.game.loop()
            self.game.draw(draw_hits=True, draw_score=False)

            
            #se un paddle missa la palla non vogliamo portarlo avanti nelle generazioni e non vogliamo ripetere n volte l'esecuzione, meglio buttare via
            if info.left_score >= 1 or info.right_score >= 1 or info.left_hits > 50: #se player colpisce troppe volte ma il match non termina, meglio chiudere la partita per non sprecare tempo
                self.calculate_fitness(genome1, genome2, info)
                break
            
            pygame.display.update()
            
            
            
    def calculate_fitness(self, genome1, genome2, info):
        genome1.fitness += info.left_hits
        genome2.fitness += info.right_hits


def eval_genomes(genomes, config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    
    for i, (genome_id1, genome1) in enumerate(genomes): #facciamo giocare un gene contro un altro per valutare le prestazioni
        
        if i==len(genomes)-1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]: 
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config)
            
    

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-17')
    #p = neat.Population(config) #configura la popolazione iniziale 
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(2))
    
    winner = p.run(eval_genomes, 50) 
    with open("best.pickle", 'wb') as f:
        pickle.dump(winner, f)
        
        
def test_ai(config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    
    with open("best.pickle", 'rb') as f:
        winner = pickle.load(f)
        
    game = PongGame(window=window, width=width, height=height)
    game.test_ai(winner, config)
        
        


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)    
    run_neat(config=config)
    #test_ai(config=config)
    
