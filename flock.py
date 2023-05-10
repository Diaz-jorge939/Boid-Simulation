import pygame
import random
import math 

# Initialize Pygame
pygame.init()

#getting the screen width and height of device currently running the program
device_screen = pygame.display.Info()

SCREEN_WIDTH, SCREEN_HEIGHT = device_screen.current_w-100, device_screen.current_h-100

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# # Update the display
# pygame.display.update()

# two-dimensional vector class
class vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
            
        self.angle = None
    
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def random2D(self):
        angle = random.uniform(0.0, 2.0 * math.pi)
        x = 1 * math.cos(angle)
        y = 1 * math.sin(angle)

        return vector(x, y)

    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def sub(vector1, vector2):
        return vector(vector1.x - vector2.x , vector1.y - vector2.y)

    def add(self, vector):
        if self.y != None and self.x != None:
            self.x += vector.x
            self.y += vector.y
        else:
            self.x = vector.x
            self.y = vector.y

    def dist(self, vector):
        return math.sqrt(math.pow(vector.x - self.x, 2) + math.pow(vector.y - self.y, 2))
    
    # static method
    def dist(vector1, vector2):
        return math.sqrt(math.pow(vector2.position.x - vector1.position.x, 2) + math.pow(vector2.position.y - vector1.position.y, 2))

    def div(self, scalar):
        self.x = self.x / scalar
        self.y = self.y / scalar

    # unit vector * magnitude = desired magnitude 
    def setMag(self, magnitude):
        pass 

    def calc_magnitude(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
    
    # scale vector to have a magnitude of 1 
    def normalize(self):
        if self.x != None or self.y != None:
            self.x = self.x / self.calc_magnitude()
            self.y = self.y / self.calc_magnitude()
        else:
            self.x = 1
            self.y = 1
    
    def limit(self, limit):
        pass
    

class Boid:
    def __init__(self):

        self.position = vector(random.randrange(0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT)) 
        self.velocity = vector(random.randrange(1,4),random.randrange(1,4))         #vector(random.randrange(1, 5),  random.randrange(1, 5))
        self.acceleration = vector(0,0)


        # self.angle = random.uniform(0.0, 2.0 * math.pi)
    
        self.img = pygame.transform.scale(pygame.image.load('Penguins/TenderBud/idle/0.png'), (40,40))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
        self.maxspeed = 4
        self.maxforce = 0.1

    def applyForce(self, force):
        self.acceleration.x = force
        self.acceleration.y = force
    
    def draw(self):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0 :
            self.position.y = SCREEN_HEIGHT

        
        SCREEN.blit(self.img ,(self.position.x, self.position.y))

    def update(self):
        self.position.add(self.velocity)
        self.velocity.add(self.acceleration)

    def align(self, boids):
        perception = 100
        steering = vector()
        total = 0 

        for boid in boids:
            distance = vector.dist(self, boid)

            if distance > 0 and distance < perception:
                steering.add(boid.velocity)
                total += 1
        
        if total > 0:

            steering.div(total)
            steering.setMag(self.maxspeed)
            steering.sub(self.velocity)
            steering.limit(self.maxforce)

        return steering

    def flock(self, boids):
        alignment = self.align(boids)
        self.acceleration = alignment

        print(self.acceleration.x)

def main():

    clock = pygame.time.Clock()
    FPS = 25
    run = True 

    boids = []
    for boid in range(25):
        boids.append(Boid())

    while run:
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        SCREEN.fill((255,255,255))
        # keys_pressed = pygame.key.get_pressed()

        # put the image onto the screen
        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.draw()

        clock.tick(FPS)
        pygame.display.update()

main()
