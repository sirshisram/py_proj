# For cycling through a list (in this case, we use a list of hex colour values)
import itertools as it

import math as m
import matplotlib.pyplot as plt

from star_sys_vectors import vectors

class Sys:
    
    # Initializer
    # We initialize the 2D projection to False
    def __init__(self, size, proj_2d=False):
        
        self.size = size
        self.bodies = []
        
        # plt.subplots() is called to render a set of axes (which is 3D in our case) and the values are assigned to fig and ax.
        self.fig, self.ax = plt.subplots(#1, 1 are to create a single set of axes in the final rendered figure
                                         1, 
                                         1,
                                         # subplot_kw has an argument "projection":"3d", which is responsible in projecting the set of axes in 3D.
                                         subplot_kw={"projection": "3d"}, 
                                         # figsize sets the overall size of the output figure.
                                         figsize=(self.size / 50, self.size / 50))  
        
        # line 25 - 30 enable/disable the 2D projection planes which helps us visualize the star system in 3D.
        self.proj_2d = proj_2d
        
        if self.proj_2d:
            self.ax.view_init(10, 0) # 2D projection is turned on. (Floor plane is visible) (10 deg of tilt can help us visualize the plane)
        else:
            self.ax.view_init(0, 0) # 2D projection is turned off.
        
        # Reduces margins at the edge of the simulation window
        self.fig.tight_layout() # Automatically adjusts the subplot params so as to optimize the figure area.
        # self.ax.set_facecolor("black")

    # Adds bodies into the system
    def add_body(self, body):
        
        self.bodies.append(body)
        
    # Updates the rendered body's motion
    def update_all(self):
        
        # Helps to show bodies behind other bodies for better 3D visualization
        self.bodies.sort(key=lambda item: item.position[0]) # Sorts the bodies[] via lambda
        
        # Calls motion() and render() so as to update the body's motion.
        for body in self.bodies:
            body.motion()
            body.render()
          
    # Updates the rendered plot via pause() function
    # Limits the rendered axes using the system's size.
    def render_all(self):
        # line 55 - 57 helps us eliminate the axes and grids so as to visualize the simulation better
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        
        # line 61 - 66 helps us to eliminate the 2d plane projections so we can get an empty space
        # Removes the ticklables of each axis.
        if self.proj_2d:
            self.ax.xaxis.set_ticklabels([]) 
            self.ax.yaxis.set_ticklabels([])
            self.ax.zaxis.set_ticklabels([])
        else:
            self.ax.axis('off') # Removes all axes
            
        plt.pause(0.001) # Helps in visualizing the motion of the body by pausing every 1 ms.
        self.ax.clear()  # Clears all the rendered axes
    
    # Accounts interaction for all the bodies in the system
    def calc_interxn(self):
        bodies_copy = self.bodies.copy() 
        for index, first_body in enumerate(bodies_copy): # enumerate() adds counter to an iterable and returns it in a form of enumerating object. This is later used for loops
            for second_body in bodies_copy[index + 1:]: # index + 1 is useful to avoid to account the interactions between two same bodies twice
                first_body.gravity_effects(second_body) # Calls the gravity_effects() for the first body and uses the second body as an argument

class Sys_Body:
    
    # This attribute is to set the minimum size of the marker so that the small planets don't look too small.
    min_disp_size = 10 
    
    # This is to convert from mass to the marker size.    
    disp_log_base = 1.3 
    
    # Initializer
    # Setting up the star_sys body. mass, position and velocity are attributes of the body
    def __init__(self,
                 system,
                 mass,
                 position=(0, 0, 0),
                 velocity=(0, 0, 0)):
        
        self.system = system # Links the defined body to the system
        self.mass = mass #int/float
        self.position = position
        self.velocity = vectors(*velocity) # Velocity of the rendered body
        
        #display_size helps us to choose between the calculated size of the marker and the minimum marker size so that the marker won't be too small or too large.
        self.display_size = max(m.log(self.mass, self.disp_log_base),
                                self.min_disp_size)
        self.colour = "black" # Default colour of the body (This is an attribute of the body.)

        self.system.add_body(self)

    # Re-defines the position attribute with the velocity attribute of the system class
    # Responsible for the motion of the rendered bodies.
    def motion(self):
        self.position = (self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1],
                         self.position[2] + self.velocity[2])
    
    # Renders a body based on given arguments
    def render(self):
        
        # Renders star/planet body
        self.system.ax.plot(*self.position,
                                  marker="o",
                                  # Line 115 helps the 3D visualization by chaning the size of the marker depending on its location on the x-axis.
                                  # self.position[0] represents the position of the object on the x-axis. 30 is just an arbitrary value.
                                  # Closer objects appear larger while farther objects appear smaller.
                                  markersize = self.display_size + self.position[0] / 30,
                                  color=self.colour)
       
        # Improvising 3D visualization
        if self.system.proj_2d:
            # A second plot is added when 2D projection is True
            self.system.ax.plot(self.position[0], # position of the bodies on x-axis
                                self.position[1], # position of the bodies on y-axis
                               -self.system.size / 2, # Minimum value of z-axis which represents the floor plane
                                marker = "o",
                                markersize = self.display_size / 2,
                                color=(.5, .5, .5))

    # Accounts gravitational interaction of the bodies in the system
    def gravity_effects(self, other):
        
        dist = vectors(*other.position) - vectors(*self.position) # *args helps us pass a variable no. of arguments to the function
        dist_mag = dist.__mag__()
        
        # Instead of using F = G*m1*m2/r_12**2, we ignore the gravitational constant G since we're using arbitrary units in this syntax. We use F= m1*m2/r_12**2
        f_mag = self.mass * other.mass / (dist_mag ** 2)
        f = dist.__norm__()*f_mag
        
        # Calculates the acceleration for each interaction
        rev = 1 # Reverse is a parameter that ensures the opposite acceleration is applied to the second body since the two bodies when interacting are being pulled towards each other.
        for body in self, other:
            acc = f/body.mass
            body.velocity += acc*rev
            rev = -1

# Defining a Star body
class Star_Body(Sys_Body):
    
    # Initializer
    def __init__(self,
                 system,
                 mass=100000,
                 position=(0, 0, 0),
                 velocity=(0, 0, 0)):
        
        # Calls the parent class Sys_Body for overriding attributes in the Star_Body.__init__()
        super(Star_Body, self).__init__(system, mass, position, velocity)
        self.colour = "orange" 

# Defining a Planet body
class Planet_Body(Sys_Body):
    
    # Cycling through a list (Useful for multi-planet star systems). Cycle changes for every runtime
    colour_set = ['#3b3838', 
                  '#8c5606', 
                  '#1336d4', 
                  '#ad401f', 
                  '#ff7e57', 
                  '#916a47', 
                  '#37ada9', 
                  '#3338a3']
    colours = it.cycle(colour_set)

    # Initializer
    def __init__(self,
                 system,
                 mass=10,
                 position=(0, 0, 0),
                 velocity=(0, 0, 0)):
        
        # Calls the parent class Sys_Body for overriding attributes in the Planet_Body.__init__()
        super(Planet_Body, self).__init__(system, mass, position, velocity)
        self.colour = next(Planet_Body.colours)