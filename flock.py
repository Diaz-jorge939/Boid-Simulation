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
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # creates Vector object with a random direction and magnitude of 1
    def random2D():
        angle = random.uniform(0.0, 2.0 * math.pi)      # generates an angle between 0 and 2pi 

        x = math.cos(angle)     # cos and sin of angle theta ensure unit vector 
        y = math.sin(angle)

        return vector(x, y)
    # difference of two vectors returned as new vector
    def subtract(vector1, vector2):
        x = vector2.x - vector1.x
        y = vector2.y - vector1.y

        return vector(x, y)
    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def add(self, vector):
            self.x += vector.x
            self.y += vector.y

    def dist(self, vector2):
        return math.sqrt((vector2.x - self.x)**2 + (vector2.y - self.y)**2)
    
    def div(self, scalar):
        self.x = self.x / scalar
        self.y = self.y / scalar

    # sets vector magnitude by specified value. calculates the unit vector * magnitude 
    def setMag(self, magnitude):

        self.x = (self.x / self.mag()) * magnitude 
        self.y = (self.y / self.mag()) * magnitude
    
    # returns the calculated magnitude of the vector
    def mag(self):
        if self.x == 0 and self.y == 0:
            return 1
        else:
            return math.sqrt(self.x**2 + self.y**2)
    
    # scale vector to have a magnitude of 1 
    def normalize(self):
        self.x = self.x / self.mag()
        self.y = self.y / self.mag()
    
    #limits the magnitude (length) of a vector to a specified maximum value.
    def limit(self, limit):
        if self.mag() > limit:
            self.setMag(limit)
    

class Boid:
    def __init__(self):

        self.position = vector(random.randrange(0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT)) 
        self.velocity = vector.random2D() #vector(random.randrange(1, 5),  random.randrange(1, 5)) 
        self.velocity.setMag(random.randrange(2,4))
        self.acceleration = vector(0,0)
    
        self.img = pygame.transform.scale(pygame.image.load('Penguins/TenderBud/idle/0.png'), (15,15))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
        self.maxspeed = 4
        self.maxforce = 0.2

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
        perception = 50
        steering = vector()
        total = 0 

        for boid in boids:
            distance = vector.dist(self.position, boid.position)
            
            if boid != self and distance < perception:
                steering.add(boid.velocity)
                total += 1
        
        if total > 0:

            steering.div(total)
            steering.setMag(self.maxspeed)
            steering.sub(self.velocity)
            steering.limit(self.maxforce)
        
        return steering

    def separation(self, boids):
        avoidance_radius = 100
        steering = vector()

        sum = vector()

        total = 0 

        for boid in boids:
            distance = vector.dist(self.position, boid.position)
            
            if distance > 0 and distance < avoidance_radius:
                
                diff = vector.subtract(boid.position,self.position )
                diff.div(distance)
                steering.add(diff)
                total += 1
        
        if total > 0:

            steering.div(total)
            steering.setMag(self.maxspeed)
            steering.sub(self.velocity)
            steering.limit(self.maxforce)     

        return steering
       
    def flock(self, boids):
        # alignment = self.align(boids)
        separation = self.separation(boids)
        self.acceleration = separation       # F = MA -> A = F

def main():

    clock = pygame.time.Clock()
    FPS = 30
    run = True 

    boids = []
    for boid in range(100):
        boids.append(Boid())

    while run:
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        SCREEN.fill((0,0,0))
        # keys_pressed = pygame.key.get_pressed()

        #put the image onto the screen
        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.draw()

        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()