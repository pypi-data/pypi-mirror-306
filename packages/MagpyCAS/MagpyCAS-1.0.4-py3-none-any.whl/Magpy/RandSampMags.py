
# Imports 
from .Magmas import * 
from iteration_utilities import random_product 
import time
import string 


class MagmaSampler: 
    
    """
    Purpose: 
        Helps to find a specific structure of a certain size without having to generate and 
        perform calculations on all n^n^2 magmas. 
    
    Description: 
        Parse through a random sample of magmas of a specified size and structure, and display them. 
    
    Parameters: 
        size: An integer to define the size of the magmas to generate. 
        structure: A string to define the structure of the magmas to search for. 
            Default: "All" 
            Options: Any structure (class) defined in the package. 
        sample_size: An integer to define the number of magmas to generate. 
            Default: 1000 
        exclude: A list of strings to define the structures to exclude from the search. 
            Default: None 
            Options: Any structure (class) defined in the package, inside of a list, and separated by commas. 
    
    Use: 
        Call the MagmaSampler() function; the only required parameter is the `size` of the magmas to generate and parse through. 
    
    Example:
        MagmaSampler(4) 
        MagmaSampler(4, structure = "All", sample_size = 5000, exclude = ["Magma"]) 
    """
    
    def __init__(self, size: int, structure: str = "All", sample_size: int = 1000, exclude: list[str] = "None"): 
        
        # Initalize parameters 
        self.size = size
        self.structure = structure
        self.sample_size = sample_size
        self.exclude = exclude 
        
        # Storage for magmas
        self.magmas = []
        
        # Define usuable variables
        self.variables = [letter for letter in string.ascii_lowercase] 
        
        # Grab number of variables as defined by the `size` parameter 
        self.mset = self.variables[0:size] 
        
        # Table size 
        self.table_size = self.size**2
        
        # Random sampling list: Magma set repeated size^2 times 
        self.sampling_list = [self.mset] * self.table_size  
        
        # Generate random sample of magmas 
        self.randmags = list(random_product(*self.sampling_list, repeat = self.sample_size)) 
        self.randmags = [self.randmags[i:i+self.table_size] for i in range(0, len(self.randmags), self.table_size)] 
        
        # Initialize counter 
        self.counter = 0
        
        # Set timer 
        self.execution_time = 0 
        
        # Exclusion list 
        if self.exclude != "None": 
            if len(self.exclude) == 1: 
                self.exclusion_list = self.exclude[0] 
            else: 
                last = self.exclude[-1]
                rest_of_list = [struct + "s" for struct in self.exclude[:-1]]
                rest_of_list = ", ".join(self.exclude[:-1])
                self.exclusion_list = f"{rest_of_list} or {last}"
    
    
    def __generate_and_parse(self):
        
        # Start timer 
        start = time.time() 
        
        # Parse random sample 
        for magma in self.randmags: 
            
            # Format tables: Split up lists into list of sublists  
            magma = [magma[i:i+self.size] for i in range(0, len(magma), self.size)] 
            
            # Create magma object 
            final_magma = Magma(self.mset, magma) 
            
            # Print magmas of desired structure 
            if self.structure == "All":
                if self.exclude == "None":
                    self.counter += 1
                    self.magmas.append(final_magma)
                
                elif self.structure == "All" and self.exclude != "None": 
                    if final_magma.structure not in self.exclude:
                        self.counter += 1
                        self.magmas.append(final_magma)
            
            else: 
                if final_magma.structure == self.structure: 
                    self.counter += 1
                    self.magmas.append(final_magma)
                    break 
                
        # Message for no specific examples found 
        if self.counter == 0: 
            if self.structure == "All": 
                print(f"No non-{self.exclusion_list}s found. Please run again.")
            else: 
                print(f"No {self.structure}s found. Please run again.")
        
        # End timer 
        end = time.time() 
        
        # Calculate execution time 
        self.execution_time = end - start
        
        return self
    
    def run(self, time = False, show = False): 
        
        self.__generate_and_parse() 
        
        if show == True: 
            return [print(mag) for mag in self.magmas]
        
        if time == True: 
            print(f"Execution time: {self.execution_time}")
    


