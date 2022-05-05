import math

# This class is used to carry out vector related operations in 3D.
class vectors:
    
    def __init__(self, x=0, y=0, z=0):
        
        # This method is the initializer. 
        # It is called everytime an object is created from a class and it allows the class to initialize the attributes of this class.
        
        self.x = x # 'self.x' is an attribute of the class, whereas 'x' is the argument that's passed to the class.
        self.y = y
        self.z = z

    def __repr__(self):
        
        # This function is responsible for displaying of the object.
        
        return f"Vector({self.x}, {self.y}, {self.z})" # f strings are useful in simplifying string interpolation

    def __str__(self):
        
        # This function is responsible for printing the object as a string.
        
        return f"{self.x}i + {self.y}j + {self.z}k"

    def __getitem__(self, item):
        
        # This function allows the calling class to index the variables of this class.
        
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise IndexError("Only 3D Vectors!") # Raises an index error.

    def __add__(self, other):
        
        # Vector Addition
        
        return vectors(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)

    def __sub__(self, other):
        
        # Vector Subtraction
        
        return vectors(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)

    def __mul__(self, other):
        
        if isinstance(other, vectors): #isinstance returns a boolean if the object is of the specified type
            
            # Vector Dot product
            
            return (self.x * other.x
                    + self.y * other.y
                    + self.z * other.z)
        
        elif isinstance(other, (int, float)):  
            
            # Scalar product
            
            return vectors(self.x * other,
                           self.y * other,
                           self.z * other)
        else:
            raise TypeError("Accepted Datatypes: vector, int, float")

    def __truediv__(self, other):
        
        # Division
        
        if isinstance(other, (int, float)):
            
            return vectors(self.x / other,
                           self.y / other,
                           self.z / other)
        else:
            
            raise TypeError("Accepted Datatypes: int, float")

    def __mag__(self):
        
        # Magnitude of the vector
        
        return math.sqrt(self.x ** 2 + 
                         self.y ** 2 + 
                         self.z ** 2)

    def __norm__(self):
        
        # Normalization of the vector
        
        mag = self.__mag__()
        return vectors(self.x / mag,
                       self.y / mag,
                       self.z / mag)