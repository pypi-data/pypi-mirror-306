""" 


                                ___                      ___
                |\  /|   /\    /   \  |\  /|   /\       |   \ \  /  
                | \/ |  /__\  |   ___ | \/ |  /__\   _  |___/  \/
                |    | /    \  \___/| |    | /    \ |_| |      /



====================================================================================================================================
~ Magmas Package 
====================================================================================================================================


& Creator:      Skylar Korf 
& Created:      May 2024 - ??? 
& Assisted By:  Codeium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


? Table of Contents 
? -----------------------------------------------------------------------------------------------------------------------------------
    ? General Methods 
        ^ Vector Addition 
        ^ Vector Subtraction 
        ^ Scalar Multiplication
        ^ Dot Product 
        ^ Cross Product 
        ? Matrix Multiplication 
        ? Determinant 
        ? Trace 
        ? Subset 
        ? Equivalence Relations 
        ? Counting (Combinatorics) 
    
    ? Magma Properties Checker (Script) **
        ^ Properties 
            * Associativity 
            * Commutativity 
            ? Distributivity (?)
            * Inverses 
            * Identity 
            * Potency 
            ? Bol 
            ? Moufang 
            ? Flexible 
            ? Left / Right - Alternative 
            ? Nuclear 
            * Structure
            ? etc.  
    
    ? Primary Objects 
        * Magma 
            ^ Properties 
                * Associativity 
                * Commutativity 
                ? Distributivity (?) 
                * Inverses 
                * Identity 
                * Potency 
                * Medial 
                * Left-Semimedial 
                * Right-Semimedial
                * Semimedial 
                * Left-Distributive
                * Right-Distributive
                * Autodistributive
                * Left-Cancellative
                * Right-Cancellative
                * Cancellative
                ? Bol (Loop)
                ? Moufang (Loop)
                ? Bruck (Loop)
                ? Paige (Loop)
                * Flexible 
                * Left / Right - Alternative 
                ? Power Associative 
                ? Nuclear (Left, Right, Middle) 
                ? Commutant 
                ? Associator 
                ? Nucleus 
                ? Center 
                ? Normality 
                ? Substructures 
                ? Quotient Structures 
                ? etc. 
                * Structure 
        * Dual Magma 
        ? Substructures 
        ? Equivalence Classes 
        * Unital Magma 
        * Semigroup 
        * Monoid
        * Quasigroup 
        * Loop 
        * Group 
        * Abelian Group 
        ^ Morphism 
            ? Homotopy 
            ? Isotopy 
            * Homomorphism 
            * Isomorphism 
            ? Automorphism 
            ? Endomorphism 
            ? Epimorphism 
            ? Endomorphism 
        ? Ring (?)
        ? Module (?)
        ? Field (?)
        ? Vector Space (?)
        ? Algebra (?)
    
    ? Supplementary Objects 
        ? Vector 
        ? Zorn Matrix 
            ! Zorn Matrix Multiplication 
            * Zorn Matrix Determinant 
            ? Zorn Matrix Trace 
        ? Kroncker Product 
    

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


To Do (Timeline):  
! Top Priority:  
    * Figure out try/except to raise errors if instance of subclasses doesn't meet property requirements 
    * Add __eq__ function to Magma class for equality 
    ^ Finish Morphism class
        - Add homotopies, isotopies, monomorphisms, epimorphisms, endomorphisms, & automorphisms 
    - Add progress bar with computation time (estimated time to complete?) 
    - Organize table of contents & to-do lists 
    - Finish Math Documentation 
    - Coding Documentation 
    - Thesis Writeup (Math & Code Documentation) 

^ Mild Priority: 
    - Add more properties to check for; 
        - Bol 
        - Moufang 
        - Paige 
        - Bruck 
        - etc. 
    * Add attribute to Magma.__str__ to change letter of set for output based on object type 
    - Fix vector functions 
        - Implement SymPy for this? 
    - Fix Zorn Matrix class and methods 

* Beta Release! 

? Next Steps: 
    - Abstract algorithm for property checker functions and reimplement
    - Add rings, modules, fields, vector spaces, & algebras 
    - Add octonion / split-octonion stuff (Additions to Zorn's Vector Matrix Algebra)
    - Add more properties to check for 
        - Associator 
        - Commutant 
        - Nucleus 
        - Center 
        - Alternative, Jordan, Lie, etc. 
    
    
! More To Do: 
    ! Fix Inverses checker: Remove duplicate outputs 
        ! Add internal function to return Cayley Table(s) of inverses 
            ! Add version of this to Quasigroup, Loop & Group classes 
    
    ! Recreate general methods (vector operations) 
    
    ! Fix Zorn Multiplication calculator 
        ? Add simplificationfor variable form 
        ? Reconstruct with single functions to take str / int / both  
    
    ! Derived Classes 
        * Add Try/Except to throw errors for classing if input doesn't have the right properties (Only for substructures - Magmas auto-reclassed)
        * Magma inputs automatically forced to be class that corresponds to the magma's properties 
        * Unital Magma 
        * Semigroup 
        * Quasigroup (Left, Right, Two-Sided) 
        * Loop (Left, Right, Two-Sided)
        * Monoid 
        * Group 
        * Abelian Group 
        * Commutative version of all structures 
    
    ! Add more properties to check for 
        * Left/Right Alternativity 
        * Flexibility 
        ! Nuclear 
        ! Middle 
        ! Bol, Moufang & Bol-Moufang 
        ! Paige, Frute, etc. (Loops)
        ! Normality 
        ! Sub-Structures 
        ! Quotient Structures 
    
    ! Add more to Morphism class 
        ! Add way to compose multiple functions? 
        ! Add check for homo/iso-topies between two objects. 
    
    ! Decorators for stuff? 
    
    ! Parallelize computations (if there are many computations to perform) 
    
    ! Time Function(s)  
        - Allow users to see how long computations took 
        - Allow users to see a progress bar for computation progress 
        - Have progress bar show number of computations completed/total needed to perform 
            - Calculate number of computations needed in each property checker, then add together 
            in progress bar
        - Have progress bar change color depending on progression
            - Umbre from red -> orange -> yellow -> yellow-green -> green 
            - Animated in some cool way? 



~ -------------------------------------------------------------------------------------------------------------------
"""

#& Le Code
# -------------------------------------------------------------------------------------------------------------------


#^ Imports 
# -------------------------------------------------------------------------------------------------------------------
import sys 
import itertools 
from typing import Type 
from collections import Counter 
import re 



#^ General Methods 
# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------------------------

"""
* Magma Class 
- This class is the base class for all the basic structures. 
- It automatically reformats input for calculations, and has methods for property extraction. 
- It will also automatically re-classify an object if certain properties are met. 
"""
class Magma: 
    
    higherstructure = "Magma" 
    set_letter = "M" 
    dual_count = 0 
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative: bool = None, associative: bool = None, identity: bool | str = None, inverse: bool | str = None, potency: str = None, left_alternative: bool = None, right_alternative: bool = None, flexible: bool = None, medial: bool = None, left_semimedial: bool = None, right_semimedial: bool = None, semimedial: bool = None, left_distributive: bool = None, right_distributive: bool = None, autodistributive: bool = None, left_cancellative: bool = None, right_cancellative: bool = None, cancellative: bool = None, structure: str = None): 
        
        # The set of elements the magma is generated from 
        self.set = magma_set
        
        # Array as list of lists; sublists are rows of the Cayley Table representation of the magma
        self.magma = magma 
        
        # The properties of the magma -> bool | str
        self.commutative = commutative 
        self.associative = associative 
        self.identity = identity 
        self.inverse = inverse 
        self.potency = potency 
        self.left_alternative = left_alternative 
        self.right_alternative = right_alternative
        self.flexible = flexible 
        self.medial = medial 
        self.left_semimedial = left_semimedial
        self.right_semimedial = right_semimedial 
        self.semimedial = semimedial 
        self.left_distributive = left_distributive 
        self.right_distributive = right_distributive 
        self.autodistributive = autodistributive 
        self.left_cancellative = left_cancellative 
        self.right_cancellative = right_cancellative 
        self.cancellative = cancellative
        
        self.selfdual: bool 
        
        # Automatically reformat magma input for calculations 
        self.final_magma = self.magma_format(magma_set, magma) 
        
        # Overall structure of the magma -> str 
        self.structure = structure 
        structure = self.struct().structure 
    
    
    # Check that the input for the magma set is a list of strings, and that each row (sublist) in the magma array is of equal length
    def input_checker(self, magma_set: list[str], magma: list[list]): 
        
        # Check that the input for the magma set is a list of strings
        try: 
            for element in magma_set: 
                type(element) == str 
        except ValueError: 
            # print("ValueError: Magma set must be a list of strings. ")
            # sys.exit()
            raise ValueError("Magma set must be a list of strings. ")
        
        # Check that each row (sublist) in the magma array is of equal length
        try: 
            length = len(magma[0]) 
            
            for row in magma: 
                if len(row) != length: 
                    print("ValueError: Magma must be a list of sublists of equal length. ")
                    sys.exit() 
        
        except IndexError: 
            raise ValueError("Magma entry is empty. ")
    
    
    # Subclasses of Magma stored in the higher_structures dictionary
    higher_structures = {} 
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs) 
        cls.higher_structures["Magma"] = Magma 
        cls.higher_structures[cls.higherstructure] = cls 
    
    
    # Automatically re-class objects based on their input (structure) 
    def __new__(cls, magma_set: list[str], magma: list[list], commutative=None, associative=None, identity=None, inverse=None, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure=None):
        
        cls.set = magma_set 
        cls.magma = magma
        
        # Check the input for magma set and magma are correct
        cls.input = cls.input_checker(cls, magma_set, magma)
        
        # Automatically reformat magma input for calculations
        cls.final_magma = cls.magma_format(magma_set, magma) 
        
        # Run the structure check (associativity, inverses and identity) for determining higher structure (if any)
        structure = cls.struct(cls).structure 
        
        # Re-classing of object if properties are met
        if structure in cls.higher_structures: 
            new_cls = cls.higher_structures[structure]
            instance = object.__new__(new_cls) 
            instance.__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure) 
            
            # If object is a subclass of Magma & doesn't match the structure of the input, raises a ValueError 
            try:
                if cls != Magma:
                    raise ValueError("Incorrect class type")
            except ValueError as e:
                if cls.higherstructure != cls.structure: 
                    print(f"ValueError: {e} \nThis is not a {cls.higherstructure}, this is a {cls.structure}. ")
                    sys.exit() 
        
        # If no properties are met, returns the original object (Magma)
        else:
            instance = super().__new__(cls)
            instance.__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
        
        return instance
    
    
    # Developer representation of the object -> dict[index: str, value: str]
    def __repr__(self):
        return f"Magma: {self.final_magma} "
    
    
    # String representation of the object; prints the Cayley table
    def __str__(self): 
        # if self.dual_count == 0: 
        if self.dual_count > 0 and self.commutative == True: 
            print(f"This {self.structure} is self-dual. ")
        set_with_binop = f"({self.set_letter}{'*'*self.dual_count}, ∘)"
        magma = self.magma
        string = '\n'
        for i in magma:
            i = [str(j).rjust(len(str(magma[-1][-1]))+1) for j in i]
            string += ''.join(i)
            string += '\n'
        return f"{self.structure}, {set_with_binop} \n{string}"
    
    
    # Equality method to check if two objects are equal 
    def __eq__(self, other) -> bool:
        if not isinstance(other, Magma):
            return False
        else: 
            if self.magma == other.magma: 
                return True 
            else: 
                return False
    
    
    # Reformat magma input for calculations: list[list] -> list[dict{index: str, value: str}]
    @classmethod
    def magma_format(self, magma_set, magma) -> list[dict[str, str]]: 
        
        set_column, set_row = magma_set, magma_set
        
        global set_size 
        set_size = len(magma_set) 
        
        # Create magma as list with each list element being a dictionary of the index and value of that index 
        # global self.final_magma
        self.final_format = []
        for i in set_column: 
            for j in set_row: 
                element = {
                    "index": f"{i}{j}" 
                }
                self.final_format.append(element) 
        
        counter = 0
        for i, magma_row in enumerate(magma): 
            for j, product in enumerate(magma_row): 
                self.final_format[counter].update({"value": product}) 
                counter += 1 
        
        # print(self.final_magma) 
        return self.final_format 
    
    
    # Check for commutativity 
    # Commutative Law: xy = yx ∀ x,y ∈ M 
    # For a set of size n, ∃ = n²-n checks for commutativity 
    def commutativity_check(self) -> bool: 
        
        non_comm = 0 
        non_comm_list = []
        commutativity_check_list = []
        # print(self.final_magma)
        for element_1 in self.final_magma: 
            for element_2 in self.final_magma: 
                index_1, index_2 = element_1["index"], element_2["index"]
                value_1, value_2 = element_1["value"], element_2["value"]
                # print(index_1, value_1, index_2, value_2)
                
                # Checks for expressions that palindromes & not identical 
                if index_1 == index_2[::-1] and index_1 != index_2: 
                    if value_1 == value_2: 
                        product_value_list = [index_1, value_1, index_2, value_2] 
                        commutativity_check_list.append(product_value_list) 
                        
                        # Remove duplicates from commutativity check list 
                        for product_1 in commutativity_check_list: 
                            for product_2 in commutativity_check_list: 
                                if product_2[2] == product_1[0]: 
                                    commutativity_check_list.remove(product_2) 
                        # print(commutativity_check_list)
                    else: 
                        non_comm += 1 
                        
                        # Make list of non-commutative expressions without duplicates
                        non_comm_expression = f"{index_1[0]}{index_1[1]} = {value_1} ≠ {value_2} = {index_2[0]}{index_2[1]}"   
                        non_comm_list.append(non_comm_expression) 
                        for bad_expression_1 in non_comm_list: 
                            for bad_expression_2 in non_comm_list: 
                                if bad_expression_1[0:2] == bad_expression_2[0:2][::-1]:  
                                    non_comm_list.remove(bad_expression_2) 
                    # print(commutativity_check_list)
        
        if non_comm > 0: 
            self.commutative = False 
        else: 
            self.commutative = True 
        
        # This is equivalent to "if len(commutativity_check_list) != ((magma_size - set_size)/2)", which is the number of cases that must be checked for a magma (divided by 2 because palindromes are paired together)
        def show() -> str: 
            
            if non_comm > 0: 
                print("This magma is non-commutative: ") 
                # Show non-commutative expressions 
                for bad_expression in non_comm_list: 
                    print(f"    {bad_expression}") 
            else: 
                print("This magma is commutative. ") 
            return self 
        
        self.show = show
        
        return self 
    
    # Alias
    comm = commutativity_check
    
    
    # Check for associativty 
    # Law of Associativity: (xy)z = x(yz) ∀ x,y,z ∈ M 
    # For a set of size n, ∃ n³ checks for associativity
    def associativity_check(self) -> bool: 
        
        # Initialize variables/lists for calculation
        non_assoc = 0 
        associativity_check_list = [] 
        new_asso_list = [] 
        simplified_asso_list = []
        non_asso_list = []
        
        # Grab 3 elements from the magma
        for element_1 in self.set: 
            for element_2 in self.set: 
                for element_3 in self.set: 
                    
                    # Assign indices and values from magma entries to variables 
                    # index_1, index_2, index_3 = element_1["index"], element_2["index"], element_3["index"] 
                    # value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"] 
                    
                    # Left & right side of associativity expression 
                    left_side, right_side = f"({element_1}{element_2}){element_3}", f"{element_1}({element_2}{element_3})" 
                    
                    # Develop list of all expressions to check; len(list) = n^3 for a set of size n 
                    assoc_expression = f"{left_side} = {right_side}" 
                    associativity_check_list.append(assoc_expression) 
        
        
        # Remove duplicates from associativity check list 
        associativity_check_list = list(set(associativity_check_list)) 
        
        # Simplify expressions (portions in parentheses) from triples to doubles (without parentheses)
        for expression in associativity_check_list:
            
            # Split expressions into left and right sides 
            split_expression = expression.split(" = ")
            left_side = split_expression[0]
            right_side = split_expression[1]
            
            for element in self.final_magma:
                
                # Simplify left side 
                if left_side[1:3] == element["index"]:
                    simplified_left_side = left_side.replace(left_side[1:3], element["value"], 1).replace('(', '').replace(')', '')
                    left_side = simplified_left_side
                
                # Simplify right side
                if right_side[2:4] == element["index"]:
                    simplified_right_side = right_side.replace(right_side[2:4], element["value"], 1).replace('(', '').replace(')', '')
                    right_side = simplified_right_side
            
            # Reattach simplified left and right sides 
            new_asso_list.append(f"{left_side} = {right_side}") 
        
        # Simplify expressions from doubles to singles 
        for expression in new_asso_list: 
            
            # Split expressions into left and right (again)
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"])
                    left = simplified_left 
                
                # Simplify right side
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"]) 
                    right = simplified_right 
                
            # Reattach fully simplified left and right sides
            simplified_asso_list.append(f"{left} = {right}") 
        
        # Final list of associative expressions with their simplifications
        final_asso_check_list = [f"{i} => {j} => {k}" for i, j, k in zip(associativity_check_list, new_asso_list, simplified_asso_list)]
        
        # Create list of non-associative expressions (if any) 
        for expression in final_asso_check_list: 
            if expression[-5] != expression[-1]: 
                non_assoc += 1 
                non_asso_list.append(f"{expression[0:29]} ≠{expression[31:]}") 
        
        if non_assoc> 0: 
            self.associative = False 
        else: 
            self.associative = True 
        
        
        # Prints whether magma is associative or not
        # If magma is non-associative, non-associative expression(s) are shown 
        def show() -> str: 
            
            if non_assoc > 0: 
                print("This magma is non-associative: ") 
                for bad_expression in non_asso_list: 
                    print(f"    {bad_expression}") 
            else: 
                print("This magma is associative. ") 
            
            return self 
        
        self.show = show 
        
        return self
    
    # Alias
    asso = associativity_check
    
    
    # Identity element checker 
    def identity_check(self) -> bool | str:
        
        # Left identity element
        # ex = x ∀ x ∈ M
        
        # Right identity element 
        # xe = x ∀ x ∈ M
        
        # Two-sided identity element
        # ex = xe = x ∀ x ∈ M 
        
        not_left_identity = set()
        not_right_identity = set() 
        
        # Check for left-identity elements
        left_identity_check_list = list(set([element_2["index"][0] for element_1 in self.final_magma for element_2 in self.final_magma if element_1["index"] != element_2["index"]]))
        for left_variable in left_identity_check_list: 
            for element in self.final_magma: 
                if left_variable == element["index"][0]: 
                    if element["index"][1] == element["value"]: 
                        left_identity = left_variable 
                    elif element["index"][1] != element["value"]: 
                        not_left_identity.add(left_variable)
        left_identity_list = [element for element in left_identity_check_list if element not in not_left_identity]
        
        # Check for right-identity elements
        right_identity_check_list = list(set([element_2["index"][1] for element_1 in self.final_magma for element_2 in self.final_magma if element_1["index"] != element_2["index"]]))
        for right_variable in right_identity_check_list: 
            for element in self.final_magma: 
                if right_variable == element["index"][1]: 
                    if element["index"][0] == element["value"]: 
                        right_identity = right_variable 
                    elif element["index"][0] != element["value"]: 
                        not_right_identity.add(right_variable) 
        right_identity_list = [element for element in right_identity_check_list if element not in not_right_identity]
        
        # Check for two-sided identity element(s)
        two_sided_identity_list = [left_id for left_id in left_identity_list for right_id in right_identity_list if left_id == right_id ]
        
        # Set value of 'identity' attribute 
        if len(two_sided_identity_list) > 0: 
            self.identity = True 
        elif len(left_identity_list) > 0: 
            self.identity = "Left" 
        elif len(right_identity_list) > 0: 
            self.identity = "Right" 
        else: 
            self.identity = False 
        
        
        # Show results of calculations 
        def show() -> str: 
            # Print out identity element(s)
            
            # Two-Sided Identity 
            if len(two_sided_identity_list) > 0: 
                print("Two-sided identity element: ") 
                for identity in two_sided_identity_list: 
                    print(f"    {identity}") 
            
            # Left-Identity 
            elif len(left_identity_list) > 0: 
                print("Left-sided identity element(s): ") 
                for identity in left_identity_list: 
                    print(f"    {identity}")
            
            # Right-Identity 
            elif len(right_identity_list) > 0: 
                print("Right-sided identity element(s): ") 
                for identity in right_identity_list: 
                    print(f"    {identity}") 
            
            # No identity element(s) 
            else: 
                print("This magma does not have an identity element. ") 
            
            return self 
        
        self.show = show 
        
        return self  
    
    # Alias
    iden = identity_check 
    
    # ! Fix: Sometimes still has a duplicate in the output 
    # Inverse element checker 
    def inverse_check(self) -> bool | str: 
        
        # -----------------------------
        # Right Quasigroup, (Q, ∗, /)
        # y = (y / x) ∗ x
        # y = (y ∗ x) / x
        
        # Left Quasigroup, (Q, ∗, \) 
        # y = x ∗ (x \ y)
        # y = x \ (x ∗ y)
        
        # Quasigroup, (Q, *, \, /)
        # y = (y / x) ∗ x
        # y = (y ∗ x) / x
        # y = x ∗ (x \ y)
        # y = x \ (x ∗ y)
        # -----------------------------
        
        # Check for right inverses -> Right Quasigroup
        # Check for left inverses -> Left Quasigroup
        # If it has both left & right inverses -> Quasigroup 
        
        
        # Create lists of left and right inverses elements
        right_inverses = [{"index": f"{element['index'][0]}\\{element['value']}", "value": f"{element['index'][1]}"} for element in self.final_magma]
        left_inverses = [{"index": f"{element['value']}/{element['index'][1]}", "value": f"{element['index'][0]}"} for element in self.final_magma]
        
        
        # Look for right inverse elements with multiple values (i.e., not inverse elements)
        bad_right_expressions = []
        for element_1 in right_inverses: 
            for element_2 in right_inverses: 
                if element_1["index"] == element_2["index"] and element_1["value"] != element_2["value"]: 
                    bad_right_expressions.append([element_1, element_2]) 
        # print(bad_right_expressions)
        
        # Remove duplicates from bad right expressions
        for bad_expression_1 in bad_right_expressions: 
            for bad_expression_2 in bad_right_expressions: 
                if bad_expression_1[0:3] == bad_expression_2[0:3]: 
                    bad_right_expressions.remove(bad_expression_2) 
        
        # Look for left inverse elements with multiple values (i.e., not inverse elements)
        bad_left_expressions = []
        for element_1 in left_inverses: 
            for element_2 in left_inverses: 
                if element_1["index"] == element_2["index"] and element_1["value"] != element_2["value"]: 
                    bad_left_expressions.append([element_1, element_2]) 
        
        # # Remove duplicates from bad left expressions
        for bad_expression_1 in bad_left_expressions: 
            for bad_expression_2 in bad_left_expressions: 
                if bad_expression_1[0:3] == bad_expression_2[0:3]: 
                    bad_left_expressions.remove(bad_expression_2)
        
        # Determine if the magma has right inverses or not
        if len(bad_right_expressions) > 0: 
            right_invs = False 
        else: 
            right_invs = True
        
        # Determine if the magma has left inverses or not
        if len(bad_left_expressions) > 0: 
            left_invs = False 
        else: 
            left_invs = True
        
        # Set value of attribute 'inverse' 
        if right_invs == True and left_invs == True: 
            self.inverse = True 
        elif right_invs == True and left_invs == False: 
            self.inverse = "Right" 
        elif left_invs == True and right_invs == False: 
            self.inverse = "Left" 
        elif left_invs == False and right_invs == False:
            self.inverse = False 
        
        
        
        def show() -> str: 
            # Display whether the magma has left and right inverses
            if right_invs == True and left_invs == True: 
                print("This magma has left and right inverses. ") 
            # Display whether the magma has right inverses but not left inverses
            elif right_invs == True and left_invs == False: 
                print("This magma has right inverses, but not left inverses: ")
                for expression in bad_left_expressions: 
                    print(f"    {expression[0]['index']} = {expression[0]['value']} ≠ {expression[1]['value']} = {expression[1]['index']}") 
            # Display whether the magma has left inverses but not right inverses
            elif left_invs == True and right_invs == False: 
                print("This magma has left inverses but not right inverses: ")
                for expression in bad_right_expressions: 
                    print(f"    {expression[0]['index']} = {expression[0]['value']} ≠ {expression[1]['value']} = {expression[1]['index']}")
            # Display if magma has no inverses, and all the instances that break the property of having inverses 
            elif left_invs == False and right_invs == False: 
                print("This magma does not have inverses: ")
                for expression in bad_left_expressions: 
                    print(f"    {expression[0]['index']} = {expression[0]['value']} ≠ {expression[1]['value']} = {expression[1]['index']}")
                for expression in bad_right_expressions: 
                    print(f"    {expression[0]['index']} = {expression[0]['value']} ≠ {expression[1]['value']} = {expression[1]['index']}")
            
            return self 
        
        self.show = show 
        
        return self
    
    # Alias
    inv = inverse_check 
    
    
    # Check for idempotency and unipotency 
    def potency_check(self) -> str: 
        
        # A single element is idempotent under a binary operation if composition with 
        # itself returns itself, i.e., a ∘ a = a 
        
        # A magma is idempotent if every element squares to itself i.e., x ∘ x = x ∀ x ∈ M
        
        # A magma is unipotent under a binary operation if every element squares to the same element 
        # i.e., a ∘ a , b ∘ b, c ∘ c, etc. = a 
        
        # A magma is zeropotent under a binary operation if every element squares to zero 
        # i.e., (xx) ∘ y = xx = y ∘ (xx) ∀ x, y ∈ M
        
        
        idempotent_elements = []
        unipotent_elements = []
        
        # Generate list of elements on diagonal of Cayley table
        for element in self.final_magma: 
            if element["index"] == element["index"][::-1]: 
                unipotent_elements.append(element["value"]) 
                # List of diagonal elements if x ∘ x = x
                if element["value"] == element["index"][0]: 
                    idempotent_elements.append(element["value"]) 
        
        if len(list(set(unipotent_elements))) == 1:
            self.potency = "Unipotent"
        elif len(list(set(idempotent_elements))) == len(idempotent_elements) == set_size: 
            self.potency = "Idempotent" 
        elif 0 < len(list(set(idempotent_elements))) < set_size: 
            self.potency = "Idempotent Element(s)"
        
        def show() -> str: 
            # Determine & output whether the magma has idempotent element(s), 
            # is an idempotent or unipotent magma. 
            if len(list(set(unipotent_elements))) == 1: 
                    print("This is a unipotent magma. ") 
            # Check that all potent elements are different 
            elif len(list(set(idempotent_elements))) == len(idempotent_elements) == set_size: 
                print("This is an idempotent magma. ")
            elif 0 < len(list(set(idempotent_elements))) < set_size: 
                print("This magma has idempotent element(s): ") 
                for potent_elems in list(set(idempotent_elements)): 
                    print(f"    {potent_elems}") 
            
            return self 
        
        self.show = show
        
        return self 
    
    # Alias 
    potent = potency_check
    
    
    # Check for left alternativity
    def left_alternative_check(self) -> bool: 
        
        # Left-Alternativity
        # (xx)y = x(xy) ∀ x,y ∈ M
        
        # Initialize variables/lists for calculation
        non_la = 0 
        la_check_list = [] 
        new_la_list = [] 
        simplified_la_list = []
        non_la_list = []
        
        
        # Grab 2 elements from the magma
        for element_1 in self.set: 
            for element_2 in self.set: 
                
                # Assign indices and values from magma entries to variables 
                # index_1, index_2, index_3 = element_1["index"], element_2["index"], element_3["index"] 
                # value_1, value_2 = element_1["value"], element_2["value"]
                
                # Left & right side of associativity expression 
                left_side, right_side = f"({element_1}{element_1}){element_2}", f"{element_1}({element_1}{element_2})" 
                
                # Develop list of all expressions to check; len(list) = n^3 for a set of size n 
                la_expression = f"{left_side} = {right_side}" 
                la_check_list.append(la_expression) 
        
        # Remove duplicates from associativity check list 
        la_check_list = list(set(la_check_list)) 
        
        # Simplify expressions (portions in parentheses) from triples to doubles (without parentheses)
        for expression in la_check_list:
            
            # Split expressions into left and right sides 
            split_expression = expression.split(" = ")
            left_side = split_expression[0]
            right_side = split_expression[1]
            
            for element in self.final_magma:
                
                # Simplify left side 
                if left_side[1:3] == element["index"]:
                    simplified_left_side = left_side.replace(left_side[1:3], element["value"], 1).replace('(', '').replace(')', '')
                    left_side = simplified_left_side
                
                # Simplify right side
                if right_side[2:4] == element["index"]:
                    simplified_right_side = right_side.replace(right_side[2:4], element["value"], 1).replace('(', '').replace(')', '')
                    right_side = simplified_right_side
            
            # Reattach simplified left and right sides 
            new_la_list.append(f"{left_side} = {right_side}") 
        
        # Simplify expressions from doubles to singles 
        for expression in new_la_list: 
            
            # Split expressions into left and right (again)
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"])
                    left = simplified_left 
                
                # Simplify right side
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"]) 
                    right = simplified_right 
                
            # Reattach fully simplified left and right sides
            simplified_la_list.append(f"{left} = {right}") 
        
        # Final list of associative expressions with their simplifications
        final_la_check_list = [f"{i} => {j} => {k}" for i, j, k in zip(la_check_list, new_la_list, simplified_la_list)]
        
        # Create list of non-associative expressions (if any) 
        for expression in final_la_check_list: 
            if expression[-5] != expression[-1]: 
                non_la += 1 
                non_la_list.append(f"{expression[0:29]} ≠{expression[31:]}") 
        
        if non_la > 0: 
            self.left_alternative = False 
        else: 
            self.left_alternative = True 
        
        
        # Prints whether magma is associative or not
        # If magma is non-associative, non-associative expression(s) are shown 
        def show() -> str: 
            
            if non_la > 0: 
                print("This magma is not left-alternative: ") 
                for bad_expression in non_la_list: 
                    print(f"    {bad_expression}") 
            else: 
                print("This magma is left-alternative. ") 
            
            return self 
        
        self.show = show 
        
        return self
    
    # Alias 
    la = left_alternative_check
    
    
    # Check for right alternativity
    def right_alternative_check(self) -> bool:
        
        # Right Alternativity 
        # (xy)y = x(yy) ∀ x,y ∈ M
        
        # Initialize variables/lists for calculation
        non_ra = 0 
        ra_check_list = [] 
        new_ra_list = [] 
        simplified_ra_list = []
        non_ra_list = []
        
        
        # Grab 3 elements from the magma
        for element_1 in self.set: 
            for element_2 in self.set:  
                    
                # Assign indices and values from magma entries to variables 
                # index_1, index_2, index_3 = element_1["index"], element_2["index"], element_3["index"] 
                # value_1, value_2 = element_1["value"], element_2["value"]
                
                # Left & right side of associativity expression 
                left_side, right_side = f"({element_1}{element_2}){element_2}", f"{element_1}({element_2}{element_2})" 
                
                # Develop list of all expressions to check; len(list) = n^3 for a set of size n 
                ra_expression = f"{left_side} = {right_side}" 
                ra_check_list.append(ra_expression) 
        
        # Remove duplicates from associativity check list 
        ra_check_list = list(set(ra_check_list)) 
        
        # Simplify expressions (portions in parentheses) from triples to doubles (without parentheses)
        for expression in ra_check_list:
            
            # Split expressions into left and right sides 
            split_expression = expression.split(" = ")
            left_side = split_expression[0]
            right_side = split_expression[1]
            
            for element in self.final_magma:
                
                # Simplify left side 
                if left_side[1:3] == element["index"]:
                    simplified_left_side = left_side.replace(left_side[1:3], element["value"], 1).replace('(', '').replace(')', '')
                    left_side = simplified_left_side
                
                # Simplify right side
                if right_side[2:4] == element["index"]:
                    simplified_right_side = right_side.replace(right_side[2:4], element["value"], 1).replace('(', '').replace(')', '')
                    right_side = simplified_right_side
            
            # Reattach simplified left and right sides 
            new_ra_list.append(f"{left_side} = {right_side}") 
        
        # Simplify expressions from doubles to singles 
        for expression in new_ra_list: 
            
            # Split expressions into left and right (again)
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"])
                    left = simplified_left 
                
                # Simplify right side
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"]) 
                    right = simplified_right 
                
            # Reattach fully simplified left and right sides
            simplified_ra_list.append(f"{left} = {right}") 
        
        # Final list of associative expressions with their simplifications
        final_ra_check_list = [f"{i} => {j} => {k}" for i, j, k in zip(ra_check_list, new_ra_list, simplified_ra_list)]
        
        # Create list of non-associative expressions (if any) 
        for expression in final_ra_check_list: 
            if expression[-5] != expression[-1]: 
                non_ra += 1 
                non_ra_list.append(f"{expression[0:29]} ≠{expression[31:]}") 
        
        if non_ra > 0: 
            self.right_alternative = False 
        else: 
            self.right_alternative = True 
        
        
        # Prints whether magma is associative or not
        # If magma is non-associative, non-associative expression(s) are shown 
        def show() -> str: 
            
            if non_ra > 0: 
                print("This magma is not right-alternative: ") 
                for bad_expression in non_ra_list: 
                    print(f"    {bad_expression}") 
            else: 
                print("This magma is right-alternative. ") 
            
            return self 
        
        self.show = show 
        
        return self
    
    # Alias 
    ra = right_alternative_check
    
    
    # Check for flexibility
    def flexible_check(self) -> bool: 
        
        # Flexibility
        # (xy)x = x(yx) ∀ x,y ∈ M
        
        # Initialize variables/lists for calculation
        non_flex = 0 
        flex_check_list = [] 
        new_flex_list = [] 
        simplified_flex_list = []
        non_flex_list = []
        
        
        # Grab 3 elements from the magma
        for element_1 in self.set: 
            for element_2 in self.set: 
                    
                # Assign indices and values from magma entries to variables 
                # index_1, index_2, index_3 = element_1["index"], element_2["index"], element_3["index"] 
                # value_1, value_2 = element_1["value"], element_2["value"]
                
                # Left & right side of associativity expression 
                left_side, right_side = f"({element_1}{element_2}){element_1}", f"{element_1}({element_2}{element_1})" 
                
                # Develop list of all expressions to check; len(list) = n^3 for a set of size n 
                flex_expression = f"{left_side} = {right_side}" 
                flex_check_list.append(flex_expression) 
        
        # Remove duplicates from associativity check list 
        flex_check_list = list(set(flex_check_list)) 
        
        # Simplify expressions (portions in parentheses) from triples to doubles (without parentheses)
        for expression in flex_check_list:
            
            # Split expressions into left and right sides 
            split_expression = expression.split(" = ")
            left_side = split_expression[0]
            right_side = split_expression[1]
            
            for element in self.final_magma:
                
                # Simplify left side 
                if left_side[1:3] == element["index"]:
                    simplified_left_side = left_side.replace(left_side[1:3], element["value"], 1).replace('(', '').replace(')', '')
                    left_side = simplified_left_side
                
                # Simplify right side
                if right_side[2:4] == element["index"]:
                    simplified_right_side = right_side.replace(right_side[2:4], element["value"], 1).replace('(', '').replace(')', '')
                    right_side = simplified_right_side
            
            # Reattach simplified left and right sides 
            new_flex_list.append(f"{left_side} = {right_side}") 
        
        # Simplify expressions from doubles to singles 
        for expression in new_flex_list: 
            
            # Split expressions into left and right (again)
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"])
                    left = simplified_left 
                
                # Simplify right side
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"]) 
                    right = simplified_right 
                
            # Reattach fully simplified left and right sides
            simplified_flex_list.append(f"{left} = {right}") 
        
        # Final list of associative expressions with their simplifications
        final_flex_check_list = [f"{i} => {j} => {k}" for i, j, k in zip(flex_check_list, new_flex_list, simplified_flex_list)]
        
        # Create list of non-associative expressions (if any) 
        for expression in final_flex_check_list: 
            if expression[-5] != expression[-1]: 
                non_flex += 1 
                non_flex_list.append(f"{expression[0:29]} ≠{expression[31:]}") 
        
        if non_flex > 0: 
            self.flexible = False 
        else: 
            self.flexible = True 
        
        
        # Prints whether magma is associative or not
        # If magma is non-associative, non-associative expression(s) are shown 
        def show() -> str: 
            
            if non_flex > 0: 
                print("This magma is not flexible: ") 
                for bad_expression in non_flex_list: 
                    print(f"    {bad_expression}") 
            else: 
                print("This magma is flexible. ") 
            
            return self 
        
        self.show = show 
        
        return self
    
    # Alias 
    flex = flexible_check
    
    
    # Check for mediality (a.k.a. entropic) 
    def mediality_check(self) -> bool: 
        
        # (xy) ∘ (uz) = (xu) ∘ (yz) ∀ u, x, y, z ∈ M
        
        # Initialize variables/lists for calculation
        non_medial = 0 
        medial_check_list = [] 
        new_medial_list = [] 
        doubles_medial_list = []
        simplified_medial_list = []
        non_medial_list = []
        
        # Grab 4 elements from the magma 
        for element_1 in self.set: # x
            for element_2 in self.set: # y
                for element_3 in self.set: # u 
                    for element_4 in self.set: # z 
                        
                        # Assign indices and values from magma entries to variables 
                        # value_1, value_2, value_3, value_4 = element_1["value"], element_2["value"], element_3["value"], element_4["value"] 
                        
                        # Left & right side of medial expression 
                        left_side, right_side = f"({element_1}{element_2})({element_3}{element_4})", f"({element_1}{element_3})({element_2}{element_4})" 
                        
                        # Create full expression 
                        expression = f"{left_side} = {right_side}" 
                        
                        # Add expression to list
                        medial_check_list.append(expression) 
        
        # Remove duplicates from medial check list
        medial_check_list = list(set(medial_check_list)) 
        
        # Simplify expressions from quadruples to triples 
        for expression in medial_check_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split[1:3] == element["index"]: 
                    simplified_left = left_split.replace(left_split[1:3], element["value"], 1) 
                    left = simplified_left 
                    
                if right_split[1:3] == element["index"]: 
                    simplified_right = right_split.replace(right_split[1:3], element["value"], 1) 
                    right = simplified_right 
                
            # Reattach half simplified left and right sides 
            new_medial_list.append(f"{left} = {right}") 
        
        # Simplify expressions from triples to doubles
        for expression in new_medial_list: 
        
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            half_simp_left = split_expression[0] 
            half_simp_right = split_expression[1] 
            
            for element in self.final_magma: 
                if half_simp_left[4:6] == element["index"]: 
                    simp_left = half_simp_left.replace(half_simp_left[4:6], element["value"], 1).replace('(', '').replace(')', '')
                    left = simp_left
                
                if half_simp_right[4:6] == element["index"]: 
                    simp_right = half_simp_right.replace(half_simp_right[4:6], element["value"], 1).replace('(', '').replace(')', '')
                    right = simp_right
            
            doubles_medial_list.append(f"{left} = {right}") 
        
        # Simplify expressions from doubles to singles
        for expression in doubles_medial_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"])
                    left = simplified_left 
                
                # Simplify right side
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"]) 
                    right = simplified_right 
            
            # Reattach fully simplified left and right sides
            simplified_medial_list.append(f"{left} = {right}")
        
        final_medial_list = [f"{i} => {j} => {k}" for i, j, k in zip(medial_check_list, doubles_medial_list, simplified_medial_list)]
        
        # Generate list of non-medial expressions 
        for expression in final_medial_list: 
            if expression[-5] != expression[-1]: 
                non_medial += 1 
                non_medial_list.append(f"{expression[0:35]} ≠ {expression[38:]}")
        
        # Set value of medial attribute 
        if non_medial > 0: 
            self.medial = False
        else: 
            self.medial = True 
        
        
        # Internal show (print) function 
        def show() -> str: 
            
            if non_medial > 0: 
                print("This magma is non-medial: ") 
                for bad_expression in non_medial_list:
                    print(f"    {bad_expression}")
            else: 
                print("This magma is medial. ") 
            
            return self 
        
        self.show = show
        
        return self 
    
    # Alias 
    med = mediality_check
    
    
    # Check for left semimediality 
    def left_semimediality_check(self) -> bool: 
        
        # (xx) ∘ (yz) = (xy) ∘ (xz) ∀ x, y, z ∈ M
        
        # Initialize variables/lists for calculation
        non_left_semimedial = 0 
        left_semimedial_check_list = [] 
        new_left_semimedial_list = [] 
        doubles_left_semimedial_list = []
        simplified_left_semimedial_list = []
        non_left_semimedial_list = []
        
        # Grab 3 elements from the magma 
        for element_1 in self.set: # x
            for element_2 in self.set: # y
                for element_3 in self.set: # z 
                    
                    # Assign indices and values from magma entries to variables 
                    # value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"]
                    
                    # Left & right side of left-semimedial expression 
                    left_side, right_side = f"({element_1}{element_1})({element_2}{element_3})", f"({element_1}{element_2})({element_1}{element_3})" 
                    
                    # Create full expression 
                    expression = f"{left_side} = {right_side}" 
                    
                    # Add expression to list
                    left_semimedial_check_list.append(expression) 
        
        # Remove duplicates from medial check list
        left_semimedial_check_list = list(set(left_semimedial_check_list)) 
        
        # Simplify expressions from quadruples to triples 
        for expression in left_semimedial_check_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split[1:3] == element["index"]: 
                    simplified_left = left_split.replace(left_split[1:3], element["value"], 1) 
                    left = simplified_left 
                    
                if right_split[1:3] == element["index"]: 
                    simplified_right = right_split.replace(right_split[1:3], element["value"], 1) 
                    right = simplified_right 
                
            # Reattach half simplified left and right sides 
            new_left_semimedial_list.append(f"{left} = {right}") 
        
        # Simplify expressions from triples to doubles
        for expression in new_left_semimedial_list: 
        
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            half_simp_left = split_expression[0] 
            half_simp_right = split_expression[1] 
            
            for element in self.final_magma: 
                if half_simp_left[4:6] == element["index"]: 
                    simp_left = half_simp_left.replace(half_simp_left[4:6], element["value"], 1).replace('(', '').replace(')', '')
                    left = simp_left
                
                if half_simp_right[4:6] == element["index"]: 
                    simp_right = half_simp_right.replace(half_simp_right[4:6], element["value"], 1).replace('(', '').replace(')', '')
                    right = simp_right
            
            doubles_left_semimedial_list.append(f"{left} = {right}") 
        
        # Simplify expressions from doubles to singles
        for expression in doubles_left_semimedial_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"])
                    left = simplified_left 
                
                # Simplify right side
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"]) 
                    right = simplified_right 
            
            # Reattach fully simplified left and right sides
            simplified_left_semimedial_list.append(f"{left} = {right}")
        
        final_left_semimedial_list = [f"{i} => {j} => {k}" for i, j, k in zip(left_semimedial_check_list, doubles_left_semimedial_list, simplified_left_semimedial_list)]
        
        # Generate list of non-medial expressions 
        for expression in final_left_semimedial_list: 
            if expression[-5] != expression[-1]: 
                non_left_semimedial += 1 
                non_left_semimedial_list.append(f"{expression[0:35]} ≠ {expression[38:]}")
        
        # Set value of medial attribute 
        if non_left_semimedial > 0: 
            self.left_semimedial = False
        else: 
            self.left_semimedial = True 
        
        
        # Internal show (print) function 
        def show() -> str: 
            
            if non_left_semimedial > 0: 
                print("This magma is not left-semimedial: ") 
                for bad_expression in non_left_semimedial_list:
                    print(f"    {bad_expression}")
            else: 
                print("This magma is left-semimedial. ") 
            
            return self 
        
        self.show = show
        
        return self 
    
    # Alias 
    lsem = left_semimediality_check
    
    
    # Check for right semimediality 
    def right_semimediality_check(self) -> bool: 
        
        # (yz) ∘ (xx) = (yx) ∘ (zx) ∀ x, y, z ∈ M
        
        # Initialize variables/lists for calculation
        non_right_semimedial = 0 
        right_semimedial_check_list = [] 
        new_right_semimedial_list = [] 
        doubles_right_semimedial_list = []
        simplified_right_semimedial_list = []
        non_right_semimedial_list = []
        
        # Grab 3 elements from the magma 
        for element_1 in self.set: # x
            for element_2 in self.set: # y
                for element_3 in self.set: # z 
                    
                    # Assign indices and values from magma entries to variables 
                    # value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"]
                    
                    # Left & right side of right-semimedial expression 
                    left_side, right_side = f"({element_2}{element_3})({element_1}{element_1})", f"({element_2}{element_1})({element_3}{element_1})" 
                    
                    # Create full expression 
                    expression = f"{left_side} = {right_side}" 
                    
                    # Add expression to list
                    right_semimedial_check_list.append(expression) 
        
        # Remove duplicates from medial check list
            right_semimedial_check_list = list(set(right_semimedial_check_list)) 
        
        # Simplify expressions from quadruples to triples 
        for expression in right_semimedial_check_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split[1:3] == element["index"]: 
                    simplified_left = left_split.replace(left_split[1:3], element["value"], 1) 
                    left = simplified_left 
                    
                if right_split[1:3] == element["index"]: 
                    simplified_right = right_split.replace(right_split[1:3], element["value"], 1) 
                    right = simplified_right 
                
            # Reattach half simplified left and right sides 
            new_right_semimedial_list.append(f"{left} = {right}") 
        
        # Simplify expressions from triples to doubles
        for expression in new_right_semimedial_list: 
        
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            half_simp_left = split_expression[0] 
            half_simp_right = split_expression[1] 
            
            for element in self.final_magma: 
                if half_simp_left[4:6] == element["index"]: 
                    simp_left = half_simp_left.replace(half_simp_left[4:6], element["value"], 1).replace('(', '').replace(')', '')
                    left = simp_left
                
                if half_simp_right[4:6] == element["index"]: 
                    simp_right = half_simp_right.replace(half_simp_right[4:6], element["value"], 1).replace('(', '').replace(')', '')
                    right = simp_right
            
            doubles_right_semimedial_list.append(f"{left} = {right}") 
        
        # Simplify expressions from doubles to singles
        for expression in doubles_right_semimedial_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"])
                    left = simplified_left 
                
                # Simplify right side
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"]) 
                    right = simplified_right 
            
            # Reattach fully simplified left and right sides
            simplified_right_semimedial_list.append(f"{left} = {right}")
        
        final_right_semimedial_list = [f"{i} => {j} => {k}" for i, j, k in zip(right_semimedial_check_list, doubles_right_semimedial_list, simplified_right_semimedial_list)]
        
        # Generate list of non-medial expressions 
        for expression in final_right_semimedial_list: 
            if expression[-5] != expression[-1]: 
                non_right_semimedial += 1 
                non_right_semimedial_list.append(f"{expression[0:35]} ≠ {expression[38:]}")
        
        # Set value of medial attribute 
        if non_right_semimedial > 0: 
            self.right_semimedial = False
        else: 
            self.right_semimedial = True 
        
        
        # Internal show (print) function 
        def show() -> str: 
            
            if non_right_semimedial > 0: 
                print("This magma is not right-semimedial: ") 
                for bad_expression in non_right_semimedial_list:
                    print(f"    {bad_expression}")
            else: 
                print("This magma is right-semimedial. ") 
            
            return self 
        
        self.show = show
        
        return self 
    
    # Alias 
    rsem = right_semimediality_check
    
    
    # Check for semimediality 
    def semimediality_check(self) -> bool: 
        
        # (xx) ∘ (yz) = (xy) ∘ (xz) & (yz) ∘ (xx) = (yx) ∘ (zx) ∀ x, y, z ∈ M
        # Semimedial iff M is left and right semimedial 
        
        # Run left & right semimediality checks 
        Magma.lsem(self) 
        Magma.rsem(self) 
        
        if self.left_semimedial == True and self.right_semimedial == True: 
            self.semimedial = True 
        else: 
            self.semimedial = False 
        
        
        def show() -> str: 
            
            if self.semimedial == True: 
                print("This magma is semimedial. ") 
            else: 
                print("This magma is not semimedial. ") 
                Magma.lsem(self).show() 
                Magma.rsem(self).show()
            
            return self 
        
        self.show = show
        
        
        
        return self 
    
    # Alias 
    sem = semimediality_check
    
    
    # Check for left distributivity 
    def left_distributivity_check(self) -> bool: 
        
        # x ∘ (yz) = (xy) ∘ (xz) ∀ x, y, z ∈ M
        
        # Initialize variables/lists for calculation
        non_left_dist = 0 
        left_dist_check_list = [] 
        new_left_dist_list = [] 
        doubles_left_dist_list = []
        simplified_left_dist_list = [] 
        non_left_dist_list = []
        
        # Grab 3 elements from the magma 
        for element_1 in self.set: # x
            for element_2 in self.set: # y
                for element_3 in self.set: # z 
                    
                    # Assign indices and values from magma entries to variables 
                    # value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"]
                    
                    # Left & right side of left-distributive expression 
                    left_side, right_side = f"{element_1}({element_2}{element_3})", f"({element_1}{element_2})({element_1}{element_3})" 
                    
                    # Create full expression 
                    expression = f"{left_side} = {right_side}" 
                    
                    # Add expression to list
                    left_dist_check_list.append(expression) 
        
        # Remove duplicates from left-distributive check list
        left_dist_check_list = list(set(left_dist_check_list)) 
        
        # Simplify left side from triples to doubles & right side from quadruples to triples
        for expression in left_dist_check_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split[2:4] == element["index"]: 
                    simplified_left = left_split.replace(left_split[2:4], element["value"], 1).replace('(', '').replace(')', '') 
                    left = simplified_left 
                
                # Simplify right-left side 
                if right_split[1:3] == element["index"]: 
                    simplified_right = right_split.replace(right_split[1:3], element["value"], 1) 
                    right = simplified_right 
            
            new_left_dist_list.append(f"{left} = {right}")
        
        # Simplify right side from triples to doubles 
        for expression in new_left_dist_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                left = left_split
                
                # Simplify right-right side 
                if right_split[4:6] == element["index"]: 
                    simplified_right = right_split.replace(right_split[4:6], element["value"], 1).replace('(', '').replace(')', '') 
                    right = simplified_right
                    
            doubles_left_dist_list.append(f"{left} = {right}") 
        
        # Simplify expressions from doubles to singles 
        for expression in doubles_left_dist_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"], 1) 
                    left = simplified_left
                
                # Simplify right-right side 
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"], 1) 
                    right = simplified_right
            
            # Reattach fully simplified left and right sides
            simplified_left_dist_list.append(f"{left} = {right}") 
        
        # Generate list of left-distributive expressions with simplifications 
        final_left_dist_list = [f"{i} => {j} => {k}" for i, j, k in zip(left_dist_check_list, doubles_left_dist_list, simplified_left_dist_list)]
        
        # Generate list of non-left-distributive expressions 
        for expression in final_left_dist_list: 
            if expression[-5] != expression[-1]: 
                non_left_dist += 1 
                non_left_dist_list.append(f"{expression[0:32]} ≠ {expression[35:]}")
        
        # Set value of left-distributive attribute 
        if non_left_dist > 0: 
            self.left_distributive = False
        else: 
            self.left_distributive = True 
        
        
        # Internal show (print) function 
        def show() -> str: 
            
            if non_left_dist > 0: 
                print("This magma is not left-distributive: ") 
                for bad_expression in non_left_dist_list:
                    print(f"    {bad_expression}")
            else: 
                print("This magma is left-distributive. ") 
            
            return self 
        
        self.show = show
        
        return self 
    
    # Alias 
    ldis = left_distributivity_check
    
    
    # Check for right distributivity 
    def right_distributivity_check(self) -> bool: 
        
        # (yz) ∘ x = (yx) ∘ (zx) ∀ x, y, z ∈ M
        
        # Initialize variables/lists for calculation
        non_right_dist = 0 
        right_dist_check_list = [] 
        new_right_dist_list = [] 
        doubles_right_dist_list = []
        simplified_right_dist_list = [] 
        non_right_dist_list = []
        
        # Grab 3 elements from the magma 
        for element_1 in self.set: # x
            for element_2 in self.set: # y
                for element_3 in self.set: # z 
                    
                    # Assign indices and values from magma entries to variables 
                    # value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"]
                    
                    # Left & right side of right-distributive expression 
                    left_side, right_side = f"({element_2}{element_3}){element_1}", f"({element_2}{element_1})({element_3}{element_1})" 
                    
                    # Create full expression 
                    expression = f"{left_side} = {right_side}" 
                    
                    # Add expression to list
                    right_dist_check_list.append(expression) 
        
        # Remove duplicates from right-distributive check list
        right_dist_check_list = list(set(right_dist_check_list)) 
        
        # Simplify left side from triples to doubles & right side from quadruples to triples
        for expression in right_dist_check_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split[1:3] == element["index"]: 
                    simplified_left = left_split.replace(left_split[1:3], element["value"], 1).replace('(', '').replace(')', '') 
                    left = simplified_left 
                
                # Simplify right-left side 
                if right_split[1:3] == element["index"]: 
                    simplified_right = right_split.replace(right_split[1:3], element["value"], 1) 
                    right = simplified_right 
            
            new_right_dist_list.append(f"{left} = {right}") 
        
        # Simplify right side from triples to doubles 
        for expression in new_right_dist_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                left = left_split
                
                # Simplify right-right side 
                if right_split[4:6] == element["index"]: 
                    simplified_right = right_split.replace(right_split[4:6], element["value"], 1).replace('(', '').replace(')', '') 
                    right = simplified_right
            
            doubles_right_dist_list.append(f"{left} = {right}") 
        
        # Simplify expressions from doubles to singles 
        for expression in doubles_right_dist_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"], 1) 
                    left = simplified_left
                
                # Simplify right-right side 
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"], 1) 
                    right = simplified_right
            
            # Reattach fully simplified left and right sides
            simplified_right_dist_list.append(f"{left} = {right}") 
        
        # Generate list of right-distributive expressions with simplifications 
        final_right_dist_list = [f"{i} => {j} => {k}" for i, j, k in zip(right_dist_check_list, doubles_right_dist_list, simplified_right_dist_list)]
        
        # Generate list of non-right-distributive expressions 
        for expression in final_right_dist_list: 
            if expression[-5] != expression[-1]: 
                non_right_dist += 1 
                non_right_dist_list.append(f"{expression[0:32]} ≠ {expression[35:]}")
        
        # Set value of right-distributive attribute 
        if non_right_dist > 0: 
            self.right_distributive = False
        else: 
            self.right_distributive = True 
        
        
        # Internal show (print) function 
        def show() -> str: 
            
            if non_right_dist > 0: 
                print("This magma is not right-distributive: ") 
                for bad_expression in non_right_dist_list:
                    print(f"    {bad_expression}")
            else: 
                print("This magma is right-distributive. ") 
            
            return self 
        
        self.show = show
        
        return self 
    
    # Alias 
    rdis = right_distributivity_check
    
    
    # Check for autodistributivity 
    def autodistributivity_check(self) -> bool: 
        
        # x ∘ (yz) = (xy) ∘ (xz) & (yz) ∘ x = (yx) ∘ (zx) ∀ x, y, z ∈ M 
        # Autodistributive iff M is left and right distributive 
        
        Magma.ldis(self)
        Magma.rdis(self)  
        
        if self.left_distributive == True and self.right_distributive == True: 
            self.autodistributive = True 
        else: 
            self.autodistributive = False 
        
        def show() -> str: 
            
            if self.autodistributive == True: 
                print("This magma is autodistributive. ") 
            else: 
                print("This magma is not autodistributive. ") 
                Magma.ldis(self).show() 
                Magma.rdis(self).show() 
            
            return self 
        
        self.show = show
        
        return self  
    
    # Alias 
    autodis = autodistributivity_check
    
    
    # Check for left cancellativity 
    def left_cancellativity_check(self) -> bool: 
        
        # xy = xz ∀ x, y, z ∈ M => y = z
        
        # Initialize variables/lists for calculation
        non_left_cancel = 0 
        left_cancel_check_list = [] 
        simplified_left_cancel_list = [] 
        non_left_cancel_list = []
        
        # Grab 3 elements from the magma 
        for element_1 in self.set: # x
            for element_2 in self.set: # y
                for element_3 in self.set: # z 
                    
                    # Assign indices and values from magma entries to variables 
                    # value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"]
                    
                    # Left & right side of left-cancellative expression 
                    left_side, right_side = f"{element_1}{element_2}", f"{element_1}{element_3}" 
                    
                    # Create full expression 
                    expression = f"{left_side} = {right_side}" 
                    
                    # Add expression to list
                    left_cancel_check_list.append(expression) 
        
        # Remove duplicates from medial check list
        left_cancel_check_list = list(set(left_cancel_check_list)) 
        # print(left_cancel_check_list)
        # print(len(left_cancel_check_list))
        
        # Simplify expressions from doubles to singles 
        for expression in left_cancel_check_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"], 1)
                    left = simplified_left 
                
                # Simplify right side 
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"], 1) 
                    right = simplified_right 
            
            simplified_left_cancel_list.append(f"{left} = {right}")
        
        # Generate list of left-cancellative expressions with simplifications 
        final_left_cancel_list = [f"{i} => {j}" for i, j in zip(left_cancel_check_list, simplified_left_cancel_list)] 
        
        # Generate list of non-left-cancellative expressions 
        for expression in final_left_cancel_list: 
            if expression[-5] != expression[-1]: 
                non_left_cancel += 1 
                non_left_cancel_list.append(f"{expression[0:12]} ≠ {expression[15:]}")
        
        # Set value of left-cancellative attribute 
        if non_left_cancel > 0: 
            self.left_cancellative = False
        else: 
            self.left_cancellative = True 
        
        
        # Internal show (print) function 
        def show() -> str: 
            
            if non_left_cancel > 0: 
                print("This magma is not left-cancellative: ") 
                for bad_expression in non_left_cancel_list:
                    print(f"    {bad_expression}")
            else: 
                print("This magma is left-cancellative. ") 
            
            return self 
        
        self.show = show
        
        return self 
    
    # Alias 
    lcanc = left_cancellativity_check
    
    
    # Check for right cancellativity 
    def right_cancellativity_check(self) -> bool: 
        
        # yx = zx ∀ x, y, z ∈ M => y = z
        
        # Initialize variables/lists for calculation
        non_right_cancel = 0 
        right_cancel_check_list = [] 
        simplified_right_cancel_list = [] 
        non_right_cancel_list = []
        
        # Grab 3 elements from the magma 
        for element_1 in self.set: # x
            for element_2 in self.set: # y
                for element_3 in self.set: # z 
                    
                    # Assign indices and values from magma entries to variables 
                    # value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"]
                    
                    # Left & right side of right-cancellative expression 
                    left_side, right_side = f"{element_2}{element_1}", f"{element_3}{element_1}" 
                    
                    # Create full expression 
                    expression = f"{left_side} = {right_side}" 
                    
                    # Add expression to list
                    right_cancel_check_list.append(expression) 
        
        # Remove duplicates from right-cancellative check list
        right_cancel_check_list = list(set(right_cancel_check_list)) 
        # print(left_cancel_check_list)
        # print(len(left_cancel_check_list))
        
        # Simplify expressions from doubles to singles
        for expression in right_cancel_check_list: 
            
            # Split expressions into left and right 
            split_expression = expression.split(" = ") 
            left_split = split_expression[0] 
            right_split = split_expression[1] 
            
            for element in self.final_magma: 
                
                # Simplify left side 
                if left_split == element["index"]: 
                    simplified_left = left_split.replace(left_split, element["value"], 1)
                    left = simplified_left 
                
                # Simplify right side 
                if right_split == element["index"]: 
                    simplified_right = right_split.replace(right_split, element["value"], 1) 
                    right = simplified_right 
            
            simplified_right_cancel_list.append(f"{left} = {right}")
        
        # Generate list of right-cancellative expressions with simplifications 
        final_right_cancel_list = [f"{i} => {j}" for i, j in zip(right_cancel_check_list, simplified_right_cancel_list)] 
        
        # Generate list of non-right-cancellative expressions 
        for expression in final_right_cancel_list: 
            if expression[-5] != expression[-1]: 
                non_right_cancel += 1 
                non_right_cancel_list.append(f"{expression[0:12]} ≠ {expression[15:]}")
        
        # Set value of right-cancellative attribute 
        if non_right_cancel > 0: 
            self.right_cancellative = False
        else: 
            self.right_cancellative = True 
        
        
        # Internal show (print) function 
        def show() -> str: 
            
            if non_right_cancel > 0: 
                print("This magma is not right-cancellative: ") 
                for bad_expression in non_right_cancel_list:
                    print(f"    {bad_expression}")
            else: 
                print("This magma is right-cancellative. ") 
            
            return self 
        
        self.show = show 
        
        return self
    
    # Alias 
    rcanc = right_cancellativity_check
    
    
    # Check for cancellativity 
    def cancellativity_check(self) -> bool: 
        
        # xy = xz & yx = zx ∀ x, y, z ∈ M => y = z
        # Cancellative iff M is left and right cancellative 
        
        Magma.lcanc(self)
        Magma.rcanc(self) 
        
        if self.left_cancellative == True and self.right_cancellative == True: 
            self.cancellative = True 
        else: 
            self.cancellative = False
        
        def show() -> str: 
            
            if self.cancellative == True: 
                print("This magma is cancellative. ") 
            else: 
                print("This magma is not cancellative. ") 
                Magma.lcanc(self).show() 
                Magma.rcanc(self).show() 
            
            return self 
        
        self.show = show
        
        return self  
    
    # Alias 
    canc = cancellativity_check
    
    
    # Check what the overall structure of the magma input is 
    def structure_check(self) -> str: 
        
        # Run muted functions to get values of variables without printing their outputs 
        Magma.comm(self) 
        Magma.asso(self) 
        Magma.iden(self) 
        Magma.inv(self)  
        Magma.potent(self) 
        Magma.rdis(self)
        
        
        if self.associative == True and self.identity == True and self.inverse == True: 
            if self.commutative == True:
                self.structure = "Abelian Group" 
            else: 
                self.structure = "Group"
                
        elif self.associative == True and self.identity == True and self.inverse != True: 
            self.structure = "Monoid"
            
        elif self.associative == True and self.identity != True and self.inverse != True: 
            self.structure = "Semigroup"
        
        elif self.associative == False and self.identity != False and self.inverse == True: 
            if self.identity == "Left": 
                self.structure = "Left Loop"
            elif self.identity == "Right": 
                self.structure = "Right Loop"
            else: 
                self.structure = "Loop"
        
        elif self.associative == False and self.identity != True and self.inverse != False: 
            if self.inverse == "Left": 
                if self.right_distributive == True and self.potency == "Idempotent": 
                    self.structure = "Quandle" 
                elif self.right_distributive == True and self.potency != "Idempotent": 
                    self.structure = "Rack" 
                else: 
                    self.structure = "Left Quasigroup" 
            elif self.inverse == "Right": 
                self.structure = "Right Quasigroup"
            else: 
                self.structure = "Quasigroup"
        
        elif self.associative == False and self.identity == True and self.inverse == False: 
            self.structure = "Unital Magma"
        
        else:
            self.structure = "Magma"
        
        
        def show(): 
            
            print(f"This magma is a {self.structure}")
            
            return self 
        
        self.show = show 
        
        return self
    
    # Alias 
    struct = structure_check 
    
    # Quick summary of the properties of the input 
    def properties_check(self) -> None: 
        
        # Run muted functions to get values of variables without printing their outputs 
        Magma.struct(self) 
        Magma.potent(self) 
        Magma.la(self) 
        Magma.ra(self) 
        Magma.flex(self) 
        Magma.med(self)
        Magma.lsem(self) 
        Magma.rsem(self) 
        Magma.sem(self)
        Magma.lcanc(self) 
        Magma.rcanc(self) 
        Magma.canc(self)
        Magma.ldis(self)
        Magma.rdis(self)
        Magma.autodis(self)
        
        def show() -> str: 
            
            print(f"Commutative: {self.commutative} \nAssociative: {self.associative} \nInverses: {self.inverse} \nIdentity: {self.identity} \nPotency: {self.potency} \nLeft-Alternativity: {self.left_alternative} \nRight-Alternativity: {self.right_alternative} \nFlexibility: {self.flexible} \nMedial: {self.medial} \nLeft-Semimedial: {self.left_semimedial} \nRight-Semimedial: {self.right_semimedial} \nSemimedial: {self.semimedial} \nLeft-Cancellative: {self.left_cancellative} \nRight-Cancellative: {self.right_cancellative} \nCancellative: {self.cancellative} \nLeft-Distributive: {self.left_distributive} \nRight-Distributive: {self.right_distributive} \nAutodistributive: {self.autodistributive} \nStructure: {self.structure} \n")
            
            return self 
        
        self.show = show 
        
        return self 
    
    # Alias
    props = properties_check
    


# ---------------------------------------------------------------------------------------------------------------- 

# Subclasses (higher structures) of the Magma class

# Unital Magma subclass 
class UnitalMagma(Magma):
    higherstructure = "Unital Magma" 
    set_letter = "U"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=False, identity=True, inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Unital Magma"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure) 
    
    def __repr__(self): 
        return f"Unital Magma: {self.final_magma} " 


# Commutative Unital Magma subclass
class CommutativeUnitalMagma(Magma): 
    higherstructure = "Commutative Unital Magma"
    set_letter = "U"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=True, associative=False, identity=True, inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Commutative Unital Magma"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Commutative Unital Magma: {self.final_magma} "


# Commutative Magma subclass 
class CommutativeMagma(Magma): 
    higherstructure = "Commutative Magma"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=True, associative=False, identity=False, inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Commutative Magma"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Commutative Magma: {self.final_magma} "


# Semigroup subclass 
class Semigroup(Magma): 
    higherstructure = "Semigroup"
    set_letter = "S"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=True, identity=False, inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Semigroup"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Semigroup: {self.final_magma} " 
    
    
    # Check for null semigroup 
    def null_semigroup_check(self) -> bool: 
        
        # xy = uv ∀ x, y, u, v ∈ M 
        
        pass 
    
    
    # Check for left zeros 
    def left_zeros_check(self) -> bool:
        
        # xy = x ∀ x, y ∈ M 
        
        pass
    
    # Alias
    lzeros = left_zeros_check
    
    
    # Check for right zeros 
    def right_zeros_check(self) -> bool:
        
        # yx = x ∀ x, y ∈ M 
        
        pass
    
    # Alias
    rzeros = right_zeros_check


# Commutative Semigroup subclass
class CommutativeSemigroup(Semigroup): 
    higherstructure = "Commutative Semigroup"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=True, associative=True, identity=False, inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Commutative Semigroup"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Commutative Semigroup: {self.final_magma} "


# Monoid subclass
class Monoid(Magma): 
    higherstructure = "Monoid"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=True, identity=True, inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Monoid"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Monoid: {self.final_magma} "


# Left Monoid subclass
class LeftMonoid(Monoid): 
    higherstructure = "Left Monoid"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=True, identity="Left", inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Left Monoid"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Left Monoid: {self.final_magma} "


# Right Monoid subclass
class RightMonoid(Monoid): 
    higherstructure = "Right Monoid"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=True, identity="Right", inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Right Monoid"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Right Monoid: {self.final_magma} "


# Commutative Monoid subclass
class CommutativeMonoid(Monoid): 
    higherstructure = "Commutative Monoid"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=True, associative=True, identity=True, inverse=False, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Commutative Monoid"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Commutative Monoid: {self.final_magma} "


# Quasigroup subclass
class Quasigroup(Magma): 
    higherstructure = "Quasigroup"
    set_letter = "Q"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=False, identity=False, inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, autodistributivity = None, structure="Quasigroup"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, autodistributivity,structure) 
    
    def __repr__(self): 
        return f"Quasigroup: {self.final_magma} "


# Left Quasigroup subclass
class LeftQuasigroup(Quasigroup): 
    higherstructure = "Left Quasigroup"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=False, identity=False, inverse="Left", potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Left Quasigroup"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure) 
    
    def __repr__(self): 
        return f"Left Quasigroup: {self.final_magma} "


# Right Quasigroup subclass
class RightQuasigroup(Quasigroup): 
    higherstructure = "Right Quasigroup"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=False, identity=False, inverse="Right", potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Right Quasigroup"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Right Quasigroup: {self.final_magma} "


# Commutative Quasigroup subclass
class CommutativeQuasigroup(Quasigroup): 
    higherstructure = "Commutative Quasigroup"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=True, associative=False, identity=False, inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Commutative Quasigroup"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Commutative Quasigroup: {self.final_magma} "


# Rack subclass (Quasigroup with autodistributivity & flexibility)
class Rack(Quasigroup): 
    higherstructure = "Rack"
    set_letter = "R"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=False, associative=False, identity=False, inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = True, autodistributivity = True, structure = "Rack"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, autodistributivity, structure)

    def __repr__(self): 
        return f"Rack: {self.final_magma} "


# Quandle subclass (Idempotent Rack)
class Quandle(Rack): 
    higherstructure = "Quandle"
    set_letter = "Q"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=False, associative=False, identity=False, inverse=True, potency="Idempotent", left_alternative = None, right_alternative = None, flexible = True, autodistributivity = True, structure = "Quandle"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, autodistributivity, structure)

    def __repr__(self):
        return f"Quandle: {self.final_magma} "


# Loop subclass
class Loop(Magma): 
    higherstructure = "Loop"
    set_letter = "L"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=False, identity=True, inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Loop"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Loop: {self.final_magma} "


# Left Loop subclass
class LeftLoop(Loop): 
    higherstructure = "Left Loop"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=False, identity="Left", inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Left Loop"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Left Loop: {self.final_magma} "


# Right Loop subclass
class RightLoop(Loop): 
    higherstructure = "Right Loop"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=False, identity="Right", inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Right Loop"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Right Loop: {self.final_magma} "


# Commutative Loop subclass
class CommutativeLoop(Loop): 
    higherstructure = "Commutative Loop"
    def __init__(self, magma_set: list[str], magma: list[list], commutative=True, associative=False, identity=True, inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Commutative Loop"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Commutative Loop: {self.final_magma} "


# Group subclass
class Group(Magma): 
    higherstructure = "Group"
    set_letter = "G"
    
    def __init__(self, magma_set: list[str], magma: list[list], commutative=None, associative=True, identity=True, inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Group"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure) 
    
    def __repr__(self): 
        return f"Group: {self.final_magma} "


# Abelian Group subclass
class AbelianGroup(Group): 
    higherstructure = "Abelian Group" 
    def __init__(self, magma_set: list[str], magma: list[list], commutative=True, associative=True, identity=True, inverse=True, potency=None, left_alternative = None, right_alternative = None, flexible = None, structure="Abelian Group"):
        super().__init__(magma_set, magma, commutative, associative, identity, inverse, potency, left_alternative, right_alternative, flexible, structure)
    
    def __repr__(self): 
        return f"Abelian Group: {self.final_magma} "


# ---------------------------------------------------------------------------------------------------------------- 
    
    
    """
    
    * Dual Class 
    
    Dual doesn't inherit from Magma, but it allows the user to repeatedly take the Dual 
    of a Magma or any other structure that inherits from Magma, and returns the dual of the object, and re-classes 
    objects automatically (again) based on its input. This starts by taking a complete Magma (or higher structure) 
    as input, set the Magma.set and Magma.magma as attributes in order to re-order the Magma.magma list[list] to be 
    its Dual structure. Then, using the new dual_magma list[list] and the same set, will be able to compute all the same 
    property checks on the Dual structure. Additionally, this class will change the Magma.structure to "Dual {structure}", 
    and the Magma.set_letter to have the asterisk to notate it as a Dual structure. In the instance of taking the Dual 
    multiple times, this class will change Magma.structure to "nth Dual {structure}", and add n many asterisks to the 
    Magma.set_letter for notation. To count how many times a Dual space has been taken of a Magma and keep track of it 
    with the set and asterisk, the Magma class has a dual_counter = 0 to start, and the Dual class will increase the 
    counter and add the respective number of asterisks to the set_letter attribute to reflect how many times the Dual 
    has been taken. 
    
    """
    
class Dual: 
    
    # Automatically re-class objects as Magma or its subclasses based on their input (structure) 
    # Pretty much the same as the Magma.__new__ method.  
    def __new__(cls, magma_object: Type[Magma], *args):
        
        # OG object attributes 
        cls.set = magma_object.set                             # Same set for Dual structure  
        cls.magma = magma_object.magma 
        cls.final_magma = magma_object.final_magma 
        cls.commutative = magma_object.commutative
        
        # Dual object attributes 
        cls.final_dual_magma = cls.dual_structure(cls)         # Returns list[dict], the dual of the OG magma 
        cls.dual_magma = cls.unformat_dual(cls)                # Returns a list[list] of the dual structure  
        cls.dual_object = Magma(cls.set, cls.dual_magma)       # Returns the dual object 
        
        # Checks and such 
        cls.input = cls.dual_object.input_checker(cls.set, cls.dual_magma) 
        cls.structure = cls.dual_object.struct().structure
        
        # Run the structure check (associativity, inverses and identity) for determining higher structure (if any)
        structure = Magma.struct(cls).structure 
        
        # Re-classing of object if properties are met
        if structure in cls.higher_structures: 
            new_cls = cls.higher_structures[structure]
            instance = object.__new__(new_cls) 
            instance.__init__(magma_object.set, magma_object.magma, *args) 
            
            # If object is a subclass of Magma & doesn't match the structure of the input, raises a ValueError 
            try:
                if cls != Magma:
                    raise ValueError("Incorrect class type")
            except ValueError as e:
                if cls.higherstructure != cls.structure: 
                    print(f"ValueError: {e} \nThis is not a {cls.higherstructure}, this is a {cls.structure}. ")
                    sys.exit() 
        
        # If no properties are met, returns the original object (Magma)
        else:
            instance = Magma(cls.set, cls.dual_magma) 
            instance.dual_count = magma_object.dual_count + 1
        
        return instance
    
    
    # Initialize Dual object 
    def __init__(self, magma_object: Type[Magma], *args) -> Type[Magma]: 
        
        # OG object attributes 
        self.set = magma_object.set                               # Same set for Dual structure  
        self.magma = magma_object.magma 
        self.final_magma = magma_object.final_magma
        
        # Dual object attributes 
        self.selfdual: bool 
        self.final_dual_magma = self.dual_structure()             # Returns list[dict], the dual of the OG magma
        self.dual_magma = self.unformat_dual()                    # Returns a list[list] of the dual structure 
        self.dual_object = Magma(self.set, self.dual_magma)       # Returns the dual object 
        
        # Checks and such 
        # magma_object.dual_count += 1
        self.input = self.dual_object.input_checker(self.set, self.dual_magma) 
        self.structure = self.dual_object.struct().structure
        self.commutative = self.dual_object.comm().commutative
    
    
    # Subclasses of Magma stored in the higher_structures dictionary
    higher_structures = {} 
    def __init_subclass__(cls, **kwargs) -> None:
        Magma.__init_subclass__(**kwargs) 
    
    
    # Print the list[dict] of the dual magma 
    def __repr__(self) -> str: 
        return f"Dual {self.structure}: {self.dual_magma}" 
    
    
    # Takes [{index: xy, value: z}, ...] & reformats → [[z, z, z], [z, z, z], [z, z, z]]
    def unformat_dual(self) -> list[list]: 
        dual_rows = []
        dual_list = [] 
        
        for element in self.final_dual_magma: 
            value = element["value"] 
            dual_list.append(value) 
        
        for i in range(0, len(dual_list), len(self.set)): 
            x = i 
            dual_rows.append(dual_list[x:x+len(self.set)])
        
        return dual_rows 
    
    
    # Create Dual Structures (Magmas); (M, ∘) → (M*, ∘)
    # If (M, ∘) is commutative, then (M, ∘) is self-dual, i.e., (M, ∘) ≡ (M*, ∘)
    # Takes Magma.self.final_magma (list[dict]) and returns final_dual_magma (list[dict]) 
    def dual_structure(self) -> list[dict]: 
        self.dual_final_magma = []
        if self.commutative == True: 
            self.dual_final_magma = self.final_magma 
            self.selfdual = True 
        else: 
            self.selfdual = False
            for element_1 in self.final_magma: 
                for element_2 in self.final_magma: 
                    # Check for xy = yx  
                    value_1, value_2 = element_1["value"], element_2["value"]
                    if element_1["index"] == element_2["index"][::-1]:  
                        # Swap values, create new {"index": index_1, "value": value_2} dictionary, and create dual magma list
                        dual = {"index": element_1["index"], "value": value_2}
                        self.dual_final_magma.append(dual)
        
        return self.dual_final_magma 


# ---------------------------------------------------------------------------------------------------------------- 

"""

! Substructure Class  

The Substructure class will take a single object of type Magma (or its subclasses) and check for any substructures 
via looking for subsets of the object that are closed under the binary operation. The substructures will be returned as 
new objects of type Magma or its substructures. 


"""

class Substructure: 
    pass


# ---------------------------------------------------------------------------------------------------------------- 

"""

! Quotient Structures Class 

The Quotient Structures class will take a single object of type Magma (or its subclasses) and check for any 
quotient structures via implementing an equivalence class on the object and categorizing the elements of the 
object based on which equivalence class they belong to. 

"""

class QuotientStructure: 
    pass


# ---------------------------------------------------------------------------------------------------------------- 

"""

^ Morphism Class 

The Morphism class takes two magmas (or higher structures/subclasses) as parameters, then generates all functions 
between the two objects. The two objects are not required to be of the same size. 
After generating all the functions between the two objects, the functions are sorted into their respective 
categories, consisting of injective, surjective, bijective and constant functions, then the functions will 
also be categorized as monomorphisms, epimorphisms, homomorphisms, isomorphisms, endomorphisms, and automorphisms. 

Equal, Homotopy, Isotopy, Homomorphism, Isomorphism, Automorphism, Endomorphism, Epimorphism, Monomorphism 
    For two magmaas (M, ∘) and (M', ∗); 
    Equal: Identical objects; M = M' 
    Homotopy: Ψ = (f, g, h): M → M' s.t. f(x ∘ y) = g(x) ∗ h(y) ∀ x, y ∈ M, M' 
    Isotopy: Homotopy where f, g, h are all invertible functions 
    Homomorphism: f: M → M' s.t. f(x ∘ y) = f(x) ∗ f(y) ∀ x, y ∈ M, M'
    Anti-Homomorphism: f: M → M' s.t. f(x ∘ y) = f(y) ∗ f(x) ∀ x, y ∈ M, M' 
    Isomorphism: Homomorphism where f is invertible 
    Anti-Isomorphism: Anti-Homomorphism where f is invertible 
    Endomorphism: f: M → M s.t. f(x ∘ y) = f(x) ∘ f(y) ∀ x, y ∈ M
    Automorphism: Endomorphism where f is invertible 

All functions from smaller to larger magma that hit all elements in the larger magma will be an injective function 
    If |Set A| < |Set B|, ̸∃ surjective functions 
All functions from larger to smaller magma that hit all elements in the smaller magma will be a surjective function 
    If |Set A| > |Set B|, ̸∃ injective functions
All functions between magmas of the same size where all elements are hit are bijective functions 

"""

# Morphisms class 
#! Note: For endo & automorphisms, check if magmas are the same, and if they are, 
    #! run the homo and isomorphism checks and change the name of the output 
class Morphism:
    
    # Initialize Morphism class 
    def __init__(self, magma1: Type[Magma], magma2: Type[Magma]):
        
        # Initialize the two magmas 
        self.magma1 = magma1
        self.magma2 = magma2 
        
        # Set up the final format (dictionary) of the magmas 
        self.final_magma1 = magma1.magma_format(magma1.set, magma1.magma)
        self.final_magma2 = magma2.magma_format(magma2.set, magma2.magma)  
        
        # Lists to categorize functions as a type of morphism 
        self.endomorphisms = []
        self.automorphisms = []
        self.monomorphisms = []
        self.epimorphisms = []
        
        # Genereate list[dict] of all possible functions from set A to set B
        self.functions = self.generate_functions() 
        
        # Genreate list of all homomorphism/isomorphism expressions 
        self.expressions = [f"f({element_1} ∘ {element_2}) = f({element_1}) ∗ f({element_2})" for element_1 in self.magma1.set for element_2 in self.magma1.set] 
        
        # Run constant, injective, surjective, bijective, homomorphism and isomorphism methods to classify functions 
        self.cnstf().inj().surj().bij().homo().iso() 
        
        
    
    # Generate all functions between two objects, then categorize all the functions 
    # as their respective type of morphism. 
    # Generates |B|^|A| funtions 
    def generate_functions(self) -> list[dict[str: str]]:
        
        all_functions = []
        # larger_set = max([self.magma1.set, self.magma2.set], key=len)
        for func_tuple in itertools.product(self.magma2.set, repeat=len(self.magma1.set)):
            function_dict = {self.magma1.set[i]: func_tuple[i] for i in range(len(self.magma1.set))}
            all_functions.append(function_dict)
        
        return all_functions 
    
    def display_map(self, mappings): 
        
        for map in mappings: 
            pretty_map = [f"{x} → {y}" for x, y in map.items()]
            # for x, y in map.items(): 
            #     print(f"{x} → {y}")
            print(', '.join(pretty_map))
            
        return
    
    
    
    # Categorize all constant functions, i.e., ones that map all of Set A to one element in Set B
    # |{Constant Functions}| = |Set B| 
    def constant_functions(self):
        
        self.constant_functions = []
        for mapping in self.functions: 
            first_value = next(iter(mapping.values())) 
            if all(value == first_value for value in mapping.values()): 
                self.constant_functions.append(mapping) 
        
        def show() -> str: 
            print(f"Constant Functions: {len(self.constant_functions)}")
            print(self.constant_functions) 
            return self 
        
        self.show = show 
        
        return self
    
    cnstf = constant_functions 
    
    
    # Injective / One-to-one functions: Elements in set B mapped to by at most one element in set A
    # Generates all k!/(k-n)! functions between two magmas for |Set A| = n & |Set B| = k 
    # If ∃ injective f:A → B, => |A| ≤ |B|
    def injective_functions(self): 
        
        self.injective_functions = []
        for mapping in self.functions: 
            mapped_values = [value for value in mapping.values()] 
            mapped_values.sort() 
            maps = Counter(mapped_values)
            injective = all(value == 1 for value in maps.values())
            if injective == True:     
                self.injective_functions.append(mapping) 
        
        def show() -> str:
            print(f"Injective Functions: {len(self.injective_functions)}")
            print(self.injective_functions) 
            return self 
        
        self.show = show
        
        return self 
    
    inj = injective_functions
    
    
    # Surjective / Onto functions: All elements in set B mapped to by at least one element in set A 
    # If ∃ surjective f:A → B, => |B| ≤ |A|
    def surjective_functions(self):  
        
        self.surjective_functions = [] 
        for mapping in self.functions: 
            mapped_values = list(set([value for value in mapping.values()])) 
            mapped_values.sort() 
            if mapped_values == self.magma2.set: 
                self.surjective_functions.append(mapping) 
        
        def show() -> str:
            print(f"Surjective Functions: {len(self.surjective_functions)}")
            print(self.surjective_functions) 
            return self 
        
        self.show = show
        
        return self 
    
    surj = surjective_functions
    
    
    # Bijective functions: All elements in set B are mapped to, by exactly one element in set A 
    # Injective & Surjective 
    def bijective_functions(self):
        
        self.bijective_functions = []
        for mapping in self.functions: 
            if mapping in self.injective_functions and mapping in self.surjective_functions: 
                self.bijective_functions.append(mapping) 
        
        def show() -> str: 
            print(f"Bijective Functions: {len(self.bijective_functions)}")
            print(self.bijective_functions) 
            return self
        
        self.show = show
        
        return self
    
    bij = bijective_functions
    
    
    # Homomorphism: f(x ∘ y) = f(x) ∗ f(y) 
    # For each function between two sets, ∃ n² checks to verify it's a homomorphism 
    # If ∃ an idempotent element, i.e., ∃ x ∈ A s.t. x² = x, then the constant function 
        # f(x) = x is a homomorphism. 
    def homomorphism(self):
        
        self.homomorphisms = []
        
        semi_simplified_expressions = []
        simplified_expressions = []
        
        # Determine which magma is generated from a smaller set 
        smaller_set = min(self.magma1.set, self.magma2.set, key=len) 
        
        # Generate final format of magmas to use for homomorphism check 
        final_magma1 = self.magma1.magma_format(self.magma1.set, self.magma1.magma)
        final_magma2 = self.magma2.magma_format(self.magma2.set, self.magma2.magma)
        
        # Generate list of homomorphic expressions: f(x ∘ y) = f(x) ∗ f(y)
        homomorphism_expressions = [f"f({element_1} ∘ {element_2}) = f({element_1}) ∗ f({element_2})" for element_1 in smaller_set for element_2 in smaller_set]
        # print(homomorphism_expressions)
        
        # Simplify left side: f(x ∘ y) = f(x) ∗ f(y) → f(z) = f(x) ∗ f(y)
        # via Cayley Table 
        for expression in homomorphism_expressions: 
            for element in final_magma1: 
                if f"{expression[2]}{expression[6]}" == element["index"]: 
                    expression = expression.replace(f"{expression[2:7]}", element["value"], 1) 
                    semi_simplified_expressions.append(expression) 
        # print(semi_simplified_expressions)
        
        
        # Function mapping (substitution): Grab each expression, and loop through all functions, and simplify f(x) → y 
        # f(z) = f(x) ∗ f(y) → x = y ∗ z        
        new_expressions = []
        for function in self.functions:
            for expression in semi_simplified_expressions:
                new_expression = expression
                for key, value in function.items():
                    new_expression = new_expression.replace(f"f({key})", str(value))
                new_expressions.append(new_expression)
        
        # Check the length of the new expressions list
        assert len(new_expressions) == len(semi_simplified_expressions) * len(self.functions) 
        
        
        # Finish simplifying the right side: z = x ∗ y → z = z 
        for expression in new_expressions: 
            for element in final_magma2: 
                if f"{expression[4]}{expression[-1]}" == element["index"]: 
                    simp_expression = expression.replace(f"{expression[4:]}", element["value"], 1) 
            simplified_expressions.append(simp_expression)
        
        # Group and reformat expressions 
        
        # Sublist new_expressions and simplified_expressions, then zip them together with semi_simplified_expressions 
        # and the corresponding functions from self.functions 
        grouped_new_expressions = [new_expressions[i:i+9] for i in range(0, len(new_expressions), 9)]
        grouped_simplified_expressions = [simplified_expressions[i:i+9] for i in range(0, len(simplified_expressions), 9)]
        
        
        # Zip together the expressions f(x ∘ y) = f(x) ∗ f(y) → f(z) = f(x) ∗ f(y)
        stitched_homomorphism_expressions = list(map(list, zip(homomorphism_expressions, semi_simplified_expressions)))
        
        # Zip together the simplified expressions z = x ∗ y → z = z
        stitched_simplified_expressions = [list(map(list, zip(expression, simplified_expression))) for expression, simplified_expression in zip(grouped_new_expressions, grouped_simplified_expressions)]
        
        # Zip it all together: [[f(x ∘ y) = f(x) ∗ f(y), f(z) = f(x) ∗ f(y)], [z = x ∗ y, z = z]]
        # Grouped together by all 9 expressions per function 
        full_stitched_expressions = [list(map(list, zip(stitched_homomorphism_expressions, simplified_expressions))) for simplified_expressions in stitched_simplified_expressions]
        
        
        # Reformat sublists to be of the form: [f(x ∘ y) = f(x) ∗ f(y) → f(z) = f(x) ∗ f(y) → z = x ∗ y → z = z]
        reformatted_expressions = [' → '.join([f'({expression[0]} → {expression[1]})' for expression in subsublist]) for sublist in full_stitched_expressions for subsublist in sublist]
        grouped_reformatted_expressions = [reformatted_expressions[i:i+9] for i in range(0, len(reformatted_expressions), 9)] 
        
        # Remove parentheses separating expressions in simplifications 
        final_expressions_list = []
        for simplification in grouped_reformatted_expressions: 
            for expression in simplification: 
                final_expression = expression.replace(") → (", " → ", 1).replace(expression[0], '', 1)
                final_expressions_list.append(final_expression) 
        
        # Remove ")" at the end 
        final_expressions = [re.sub(r'\)$', '', expression) for expression in final_expressions_list]
        # Regroup every 9 expressions (again) 
        self.grouped_final_expressions = [final_expressions[i:i+9] for i in range(0, len(final_expressions), 9)]
        self.grouped_final_expressions = list(map(list, zip(self.functions, self.grouped_final_expressions))) 
        
        
        # Add functions to self.homomorphisms or bad_homo_expressions 
        bad_homo_list = [] 
        for group in self.grouped_final_expressions: 
            all_equal = True 
            for expression in group[1]: 
                if expression[-5] != expression[-1]: 
                    expression = re.sub(r'\=$', '≠', expression)
                    all_equal = False 
                    break
            if all_equal: 
                self.homomorphisms.append(group)  
            else: 
                bad_homo_list.append(group) 
        
        
        # Translate homomorphisms from dictionaries {a: c, b: a, c: b} to cycle notation, (1 3 2) 
        # for homomorphism in self.homomorphisms: 
        #     for items in homomorphism[0].items(): 
        
        
        def show() -> str:
            print(f"Homomorphisms: {len(self.homomorphisms)}")
            for morphism in self.homomorphisms: 
                print(morphism[0]) 
                for simplification in morphism[1]: 
                    print(f"    {simplification}")  
            return self 
        
        self.show = show
        
        return self 
    
    homo = homomorphism
    
    
    # Homomorphism where f is invertible
    # For finite structures, if f is a surjective homomorphism, then f is an isomorphism. 
    def isomorphism(self):
        
        self.isomorphisms = []
        for function in self.functions: 
            if function in self.surjective_functions and function in self.homomorphisms[0]: 
                self.isomorphisms.append(function)
        
        def show() -> str:
            print(f"Isomorphisms: {len(self.isomorphisms)}")
            for morphism in self.isomorphisms: 
                print(morphism)  
            return self 
        
        self.show = show
        
        return self 
    
    iso = isomorphism
    
    
    def endomorphism(self):
        # Implement your endomorphism check logic here
        pass
    
    endo = endomorphism
    
    
    def automorphism(self):
        # Implement your automorphism check logic here
        pass
    
    auto = automorphism
    
    
    def monomorphism(self):
        # Implement your monomorphism check logic here
        pass
    
    mono = monomorphism 
    
    
    def epimorphism(self):
        # Implement your epimorphism check logic here
        pass
    
    epi = epimorphism
    
    
    def homotopy(self): 
        pass 
    
    
    def isotopy(self): 
        pass 
    
    
    def morphisms(self) -> str: 
        
        if self.magma1 == self.magma2: 
            print("These magmas are the same. ")
        
        if len(self.constant_functions) > 0: 
            print(f"There are {len(self.constant_functions)} constant functions. ") 
            for function in self.constant_functions: 
                print(function)
                # self.display_map(self.constant_functions)
        
        if len(self.injective_functions) > 0: 
            print(f"There are {len(self.injective_functions)} injective functions. ") 
            for function in self.injective_functions: 
                print(function)
                # self.display_map(self.injective_functions)
        
        if len(self.surjective_functions) > 0: 
            print(f"There are {len(self.surjective_functions)} surjective functions. ") 
            for function in self.surjective_functions: 
                print(function)
                # self.display_map(self.surjective_functions)
        
        if len(self.bijective_functions) > 0: 
            print(f"There are {len(self.bijective_functions)} bijective functions. ") 
            for function in self.bijective_functions: 
                print(function)
                # self.display_map(self.bijective_functions)
        
        if len(self.homomorphisms) > 0: 
            print(f"There are {len(self.homomorphisms)} homomorphisms. ") 
            for function in self.homomorphisms: 
                print(function[0])
                # self.display_map(self.homomorphisms)
        
        if len(self.isomorphisms) > 0: 
            print(f"There are {len(self.isomorphisms)} isomorphisms. ") 
            for function in self.isomorphisms: 
                print(function)
                # self.display_map(self.isomorphisms)
        
        return self
    

# ---------------------------------------------------------------------------------------------------------------- 






