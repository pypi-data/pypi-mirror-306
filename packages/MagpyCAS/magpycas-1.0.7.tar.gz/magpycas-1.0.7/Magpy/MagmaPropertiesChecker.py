
"""
This script takes a magma as input, first by taking just the set, 
then the entries of the Cayley table representation of the magma 
by row, then outputs the properties the magma does and doesn't have. 

If a property is not met by a magma, then every instance that breaks 
that property will be listed. For larger inputs, it may be recommended 
the user comments out the lines that display all the false expressions 
(instances that break the property). These would be lines 108-109 
(commutativity), 201-202 (associativity) and lines 393-394, 399-400 
and 406-409 (inverses); elements that are not identity elements will 
not be displayed. 

If there are properties that are met by a magma (beyond commutativity), 
then the name of the 'higher' structure will be displayed in the output. 
For example, if a magma is associative, the script will say that the magma 
is in fact a semigroup, or if it has inverses and identity it will be 
noted that the structure is actually a loop. 

"""

def magma_input(): 
    
    # Enter in set for magma 
    magma_set = input("Enter the set for your magma, separated by commas: ") 
    set_list = magma_set.split(",") 
    # print(set_list)
    
    # Get size of set and magma 
    set_size = len(set_list) 
    # print(set_size) 
    magma_size = set_size ** 2 
    # print(magma_size) 
    
    # Initialize variables for input & formatting 
    set_column = set_list 
    set_row = set_list 
    # print(set_column) 
    # print(set_row) 
    
    # Enter rows of magma 
    magma = [] 
    row_count = 0 
    print("Input entries of the magma by row, separated by commas")
    
    while row_count < set_size: 
        row = input("Enter row of magma: ") 
        fixed_row = row.split(",") 
        magma.append(fixed_row) 
        row_count += 1 
    # print(magma) 
    
    # Create magma as list with each list element being a dictionary of the index and value of that index 
    final_magma = []
    for i in set_column: 
        for j in set_row: 
            element = {
                "index": f"{i}{j}" 
            }
            final_magma.append(element) 
    
    counter = 0
    for i, magma_row in enumerate(magma): 
        for j, product in enumerate(magma_row): 
            # print(f"Value at {i}*{j} : {product}") 
            final_magma[counter].update({"value": product}) 
            counter += 1 
    
    # print(value) 
    # print(final_magma) 
    
    # Global variables for final structure determination
    global associative 
    associative = ""
    
    global identity 
    identity = "" 
    
    global inverse 
    inverse = "" 
    
    
    # ------------------------------------------------------------------------------------------------------------------
    
    # Check for commutativity 
    def commutativity_check(): 
        
        # Commutative Law 
        # xy = yx ∀ x,y ∈ M 
        
        non_comm = 0 
        commutative = ""
        non_comm_list = []
        commutativity_check_list = []
        
        for element_1 in final_magma: 
            for element_2 in final_magma: 
                # print(element_1["index"], element_2["index"])  
                index_1, index_2 = element_1["index"], element_2["index"]
                value_1, value_2 = element_1["value"], element_2["value"]
                
                # Checks for expressions that palindromes & not identical 
                if index_1 == index_2[::-1] and index_1 != index_2: 
                    # print("comm?: ", index_1, index_2) 
                    # print(value_1, value_2) 
                    if value_1 == value_2: 
                        # print("comm") 
                        product_value_list = [index_1, value_1, index_2, value_2] 
                        commutativity_check_list.append(product_value_list) 
                        # Remove duplicates from commutativity check list 
                        for product_1 in commutativity_check_list: 
                            for product_2 in commutativity_check_list: 
                                if product_2[2] == product_1[0]: 
                                    commutativity_check_list.remove(product_2) 
                    else: 
                        # print("non-comm") 
                        non_comm += 1 
                        # Make list of non-commutative expressions without duplicates
                        non_comm_expression = f"{index_1[0]}{index_1[1]} = {value_1} != {value_2} = {index_2[0]}{index_2[1]}"   
                        non_comm_list.append(non_comm_expression) 
                        for bad_expression_1 in non_comm_list: 
                            for bad_expression_2 in non_comm_list: 
                                if bad_expression_1[0:2] == bad_expression_2[0:2][::-1]:  
                                    non_comm_list.remove(bad_expression_2) 
                        
        # This is equivalent to "if len(commutativity_check_list) != ((magma_size - set_size)/2)", which is the number of cases that must be checked for a magma (divided by 2 because palindromes are paired together)
        if non_comm > 0: 
            commutative = False
            print("This magma is non-commutative: ") 
            # Show non-commutative expressions 
            for bad_expression in non_comm_list: 
                print(f"    {bad_expression}") 
        else: 
            print("This magma is commutative. ") 
            commutative = True 
        # print(commutativity_check_list) 
    
    commutativity_check() 
    
    # ------------------------------------------------------------------------------------------------------------------
    
    # Check for associativty 
    def associativity_check(): 
        
        # Law of Associativity 
        # (xy)z = x(yz) ∀ x,y,z ∈ M
        
        # Global associativity variable for final structure determination 
        global associative 
        
        # Initialize variables/lists for calculation
        non_assoc = 0 
        associativity_check_list = [] 
        new_asso_list = [] 
        simplified_asso_list = []
        non_asso_list = []
        
        
        # Grab 3 elements from the magma
        for element_1 in final_magma: 
            for element_2 in final_magma: 
                for element_3 in final_magma: 
                    
                    # Assign indices and values from magma entries to variables 
                    index_1, index_2, index_3 = element_1["index"], element_2["index"], element_3["index"] 
                    value_1, value_2, value_3 = element_1["value"], element_2["value"], element_3["value"] 
                    
                    # Left & right side of associativity expression 
                    left_side, right_side = f"({value_1}{value_2}){value_3}", f"{value_1}({value_2}{value_3})" 
                    
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
            
            for element in final_magma:
                
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
            
            for element in final_magma: 
                
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
                non_asso_list.append(f"{expression[0:29]} !{expression[30:]}") 
        
        # Prints whether magma is associative or not
        # If magma is non-associative, non-associative expression(s) are shown
        if non_assoc > 0: 
            print("This magma is non-associative: ") 
            for bad_expression in non_asso_list: 
                print(f"    {bad_expression}") 
            associative = False 
        else: 
            associative = True 
            print("This magma is associative. ")
    
    associativity_check() 
    
    # ------------------------------------------------------------------------------------------------------------------
    
    # Identity element checker 
    def identity_check():
        
        # Left identity element
        # ex = x ∀ x ∈ M
        
        # Right identity element 
        # xe = x ∀ x ∈ M
        
        # Two-sided identity element
        # ex = xe = x ∀ x ∈ M
        
        # Global identity variable for final structure determination
        global identity 
        # identity = ""
        
        not_left_identity = set()
        not_right_identity = set() 
        
        # Check for left-identity elements
        left_identity_check_list = list(set([element_2["index"][0] for element_1 in final_magma for element_2 in final_magma if element_1["index"] != element_2["index"]]))
        # print(left_identity_check_list) 
        for left_variable in left_identity_check_list: 
            for element in final_magma: 
                if left_variable == element["index"][0]: 
                    if element["index"][1] == element["value"]: 
                        left_identity = left_variable 
                    elif element["index"][1] != element["value"]: 
                        not_left_identity.add(left_variable)
        left_identity_list = [element for element in left_identity_check_list if element not in not_left_identity]
        # print(left_identity) 
        # print(not_left_identity)
        
        # Check for right-identity elements
        right_identity_check_list = list(set([element_2["index"][1] for element_1 in final_magma for element_2 in final_magma if element_1["index"] != element_2["index"]]))
        # print(right_identity_check_list) 
        for right_variable in right_identity_check_list: 
            for element in final_magma: 
                if right_variable == element["index"][1]: 
                    if element["index"][0] == element["value"]: 
                        right_identity = right_variable 
                    elif element["index"][0] != element["value"]: 
                        not_right_identity.add(right_variable) 
        right_identity_list = [element for element in right_identity_check_list if element not in not_right_identity]
        # not_right_identity = list(set(no))
        # print(not_right_identity)
        
        # Check for two-sided identity element(s)
        two_sided_identity_list = [left_id for left_id in left_identity_list for right_id in right_identity_list if left_id == right_id ]
        
        # Print out identity element(s)
        # Two-Sided Identity 
        if len(two_sided_identity_list) > 0: 
            print("Two-sided identity element: ") 
            for identity in two_sided_identity_list: 
                print(f"    {identity}") 
            identity = True
        
        # Left-Identity 
        elif len(left_identity_list) > 0: 
            print("Left-sided identity element(s): ") 
            for identity in left_identity_list: 
                print(f"    {identity}")
            identity = "Left"
        
        # Right-Identity 
        elif len(right_identity_list) > 0: 
            print("Right-sided identity element(s): ") 
            for identity in right_identity_list: 
                print(f"    {identity}") 
            identity = "Right"
        
        # No identity element(s) 
        else: 
            identity = False 
            print("This magma does not have an identity element. ")
    
    identity_check() 
    
    # ------------------------------------------------------------------------------------------------------------------
    
    # Inverse element checker 
    def inverse_check(): 
        
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
        
        # Global inverse variable for final structure determination
        global inverse 
        
        # Create lists of left and right inverses elements
        right_inverses = [{"index": rf"{element['index'][0]}\\{element['value']}", "value": f"{element['index'][1]}"} for element in final_magma]
        left_inverses = [{"index": f"{element['value']}/{element['index'][1]}", "value": f"{element['index'][0]}"} for element in final_magma]
        
        # Look for right inverse elements with multiple values (i.e., not inverse elements)
        bad_right_expressions = []
        for element_1 in right_inverses: 
            for element_2 in right_inverses: 
                if element_1["index"] == element_2["index"] and element_1["value"] != element_2["value"]: 
                    bad_right_expressions.append([element_1, element_2]) 
        
        # Look for left inverse elements with multiple values (i.e., not inverse elements)
        bad_left_expressions = []
        for element_1 in left_inverses: 
            for element_2 in left_inverses: 
                if element_1["index"] == element_2["index"] and element_1["value"] != element_2["value"]: 
                    bad_left_expressions.append([element_1, element_2]) 
        
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
        
        # Display whether the magma has left and right inverses
        if right_invs == True and left_invs == True: 
            # global inverse
            inverse = True 
            print("This magma has left and right inverses. ") 
        # Display whether the magma has right inverses but not left inverses
        elif right_invs == True and left_invs == False: 
            print("This magma has right inverses, but not left inverses: ")
            for expression in bad_left_expressions: 
                print(f"    {expression[0]['index']} = {expression[0]['value']} != {expression[1]['value']} = {expression[1]['index']}") 
            inverse = "Right"
        # Display whether the magma has left inverses but not right inverses
        elif left_invs == True and right_invs == False: 
            print("This magma has left inverses but not right inverses: ")
            for expression in bad_right_expressions: 
                print(f"    {expression[0]['index']} = {expression[0]['value']} != {expression[1]['value']} = {expression[1]['index']}")
            inverse = "Left" 
        # Display if magma has no inverses, and all the instances that break the property of having inverses 
        elif left_invs == False and right_invs == False: 
            
            print("This magma does not have inverses: ")
            for expression in bad_left_expressions: 
                print(f"    {expression[0]['index']} = {expression[0]['value']} != {expression[1]['value']} = {expression[1]['index']}")
            for expression in bad_right_expressions: 
                print(f"    {expression[0]['index']} = {expression[0]['value']} != {expression[1]['value']} = {expression[1]['index']}")
            inverse = False
    
    inverse_check() 
    
    # ------------------------------------------------------------------------------------------------------------------
    
    # Check for idempotency and unipotency 
    def potency(): 
        
        # A single element is idempotent under a binary operation if composition with 
        # itself returns itself, i.e., a ∘ a = a
        
        idempotent_elements = []
        unipotent_elements = []
        
        # Generate list of elements on diagonal of Cayley table
        for element in final_magma: 
            if element["index"] == element["index"][::-1]: 
                unipotent_elements.append(element["value"]) 
                # List of diagonal elements if x ∘ x = x
                if element["value"] == element["index"][0]: 
                    idempotent_elements.append(element["value"]) 
        
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
    
    potency() 
    
    # ------------------------------------------------------------------------------------------------------------------
    
    """
    Properties Summary
    - If properties are met, displays which higher structure the object is 
    """
    
    def structure(): 
        
        global associative
        global identity
        global inverse 
        
        if associative == True and identity == True and inverse == True: 
            print("This magma is a Group! ") 
        elif associative == True and identity == True and inverse != True: 
            print("This magma is a Monoid! ")
        elif associative == True and identity != True and inverse != True: 
            print("This magma is a Semigroup! ")
        elif associative == False and identity == True and inverse != False: 
            if inverse == "Left": 
                print("This magma is a Left Loop! ")
            elif inverse == "Right": 
                print("This magma is a Right Loop! ")
            else: 
                print("This magma is a Loop! ")
        elif associative == False and identity != True and inverse != False: 
            if inverse == "Left": 
                print("This magma is a Left Quasigroup! ") 
            elif inverse == "Right": 
                print("This magma is a Right Quasigroup! ")
            else: 
                print("This magma is a Quasigroup! ")
        elif associative == False and identity == True and inverse == False: 
            print("This magma is a Unital Magma! ")
        else:
            print("This is just a magma with no extra structure. ")
    
    structure() 
    
    # ------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    magma_input() 