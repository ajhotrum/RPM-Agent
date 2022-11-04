# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image
#import numpy

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        #self.tri_dict = {"0":"270", "90":"180", "270":"0", "180":"90"}
        #self.pac_dict = {"45":"135", "315":"225", "135":"45", "225":"315", "0":"180", "180":"0"}
        self.directions = {"up":{"bottom-left":"top-left", "bottom-right": "top-right"}, "down":{"top-left":"bottom-left", "top-right": "bottom-right"},
                            "left":{"top-right":"top-left", "bottom-right":"bottom-left"}, "right":{"top-left":"top-right", "bottom-left":"bottom-right"}}
        self.alignments = ["inside", "above", "below"]
        self.sizes = ["very small", "small", "medium", "large", "very large", "huge"]

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        answer = -1
        all_attributes = {}

        #Set up figures
        A = problem.figures['A']
        B = problem.figures['B']
        C = problem.figures['C']

        #for each object put its name in the dict of dicts
        for object in A.objects:
            all_attributes[object]=A.objects[object].attributes

        for object in B.objects:
            all_attributes[object]=B.objects[object].attributes

        for object in C.objects:
            all_attributes[object]=C.objects[object].attributes

        #if there are multiple objects, compare them
        ab_pairs = self.match(A, B)
        ac_pairs = self.match(A, C)

        #Get A/B and A/C differences.
        differences_ab = {}
        #go through all pairs
        for object in ab_pairs:
            pair = ab_pairs[object]
            #if the object wasn't deleted or added
            if pair != "deleted" and pair != "added":
                #if object being analyzed is from Figure A (so that b:a doesnt get analyzed after a:b)
                if pair not in A.objects:
                    diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                    differences_ab[object] = diffs
            elif pair == "deleted":
                differences_ab[object] = 'deleted'
            elif pair == "added":
                differences_ab[object] = 'added'

        differences_ac = {}
        for object in ac_pairs:
            pair = ac_pairs[object]
            #if the object wasn't deleted or added
            if pair != "deleted" and pair != "added":
                #if object being analyzed is from Figure A (so that c:a doesnt get analyzed after a:c)
                if pair not in A.objects:
                    diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                    differences_ac[object] = diffs
            elif pair == "deleted":
                differences_ac[object] = 'deleted'
            elif pair == "added":
                differences_ac[object] = 'added'


        #code to remove the "inside" attributes from the differences dicts if the objects match
            #so if 'a' and 'c' are matched, then 'inside' : 'a' and 'inside' : 'c' will not be counted as a difference
        for i in range(len(self.alignments)):
            for object in differences_ab:
                if self.alignments[i] in differences_ab[object] and self.alignments[i] in all_attributes[ab_pairs[object]]:
                    if differences_ab[object][self.alignments[i]] in ab_pairs and self.alignments[i] in all_attributes[ab_pairs[object]]:
                        if differences_ab[object][self.alignments[i]] == all_attributes[ab_pairs[object]][self.alignments[i]]:
                            del differences_ab[object][self.alignments[i]]


        #code to remove the "inside" attributes from the differences dicts if the objects match
            #so if 'a' and 'c' are matched, then 'inside' : 'a' and 'inside' : 'c' will not be counted as a difference
        for i in range(len(self.alignments)):
            for object in differences_ac:
                if self.alignments[i] in differences_ac[object] and self.alignments[i] in all_attributes[ac_pairs[object]]:
                    if differences_ac[object][self.alignments[i]] in ac_pairs and self.alignments[i] in all_attributes[ac_pairs[object]]:
                        if differences_ac[object][self.alignments[i]] == all_attributes[ac_pairs[object]][self.alignments[i]]:
                            del differences_ac[object][self.alignments[i]]


        #Dict for the new D value coming from C
        D_C = {}
        #make same as C
        for object in C.objects:
            D_C[object] = all_attributes[object]


        #Go through all the A/B changes and apply them to C
        for difference in differences_ab:
            #check to see if the corresponding C object was deleted (To reduce redundency)
            if difference in ac_pairs:
                if ac_pairs[difference] != "deleted":
                    #check to see if the object was added from A -> B
                    if difference in ab_pairs:
                        if ab_pairs[difference] == "added":
                            #add the object directly to D_C
                            D_C[difference] = all_attributes[difference]
                    
                        #check to see if the object was deleted from A -> B
                        elif ab_pairs[difference] == "deleted":
                            #if so, delete it from D_C
                            del D_C[ac_pairs[difference]]

                        #if the object was neither deleted nor added between A -> B
                        else:
                            b_object = ab_pairs[difference]
                            c_object = ac_pairs[difference]
                            for attribute_name, attribute in differences_ab[difference].items():
                                #fill check
                                if attribute_name == 'fill':
                                    D_C[c_object][attribute_name] = all_attributes[b_object][attribute_name]
                                #if shape changed, change C shape to whatever B shape is
                                elif attribute_name == 'shape':
                                    D_C[c_object][attribute_name] = all_attributes[b_object][attribute_name]
                                #if shape changed, change C shape to whatever B shape is
                                elif attribute_name == 'size':
                                    a_size = ""
                                    b_size = ""
                                    c_size = ""
                                    #get the sizes for a, b, c
                                    for i in range(len(self.sizes)):
                                        if attribute_name in all_attributes[b_object]:
                                            if self.sizes[i] == all_attributes[b_object][attribute_name]:
                                                b_size = i
                                            if self.sizes[i] == all_attributes[difference][attribute_name]:      
                                                a_size = i
                                            if self.sizes[i] == all_attributes[c_object][attribute_name]:      
                                                c_size = i

                                    #if no change between a and b, no change between c and d, which is already true so nothing needs to happen
                                    #if change between a and b, apply that same change from A to C
                                    if a_size != b_size:
                                        diff_ab = b_size - a_size
                                        d_size = c_size + diff_ab
                                        D_C[c_object][attribute_name] = self.sizes[d_size]

                                elif attribute_name == "alignment":
                                    #go through the directions attribute to find the pair that describes what is happening from A to B
                                    for direction in self.directions:
                                        for first, second in self.directions[direction].items():
                                            if all_attributes[difference][attribute_name] == first and all_attributes[b_object][attribute_name] == second:
                                                #once found, record the direction
                                                ab_direction = direction
                                    #Use the direction and the C starting position to set the position of D
                                    for first1, second1 in self.directions[ab_direction].items():
                                        if first1 == D_C[c_object][attribute_name]:
                                            D_C[c_object][attribute_name] = second1
                                                


                                
                                #if the same shape, check if angle has changed
                                if all_attributes[difference]['shape'] == all_attributes[b_object]['shape']:
                                    if attribute_name == 'angle':
                                        #check for mirroring from A to B
                                        mirrored = self.is_mirrored(all_attributes[difference]['angle'], all_attributes[b_object]['angle'], all_attributes[difference]['shape'])

                                        #if it was mirrored, get corresponding mirrored angle
                                        if mirrored:
                                            if D_C[c_object]['shape'] == 'right triangle': 
                                                new_angle = (270.0 - float(D_C[c_object][attribute_name])) % 360.0
                                                #if there is a decimal, include it in the string. Otherwise just make it an int then a string
                                                if new_angle == int(new_angle):
                                                    D_C[c_object][attribute_name] = str(int(new_angle))
                                                else:
                                                    D_C[c_object][attribute_name] = str(new_angle)
                                            elif D_C[c_object]['shape'] == 'pac-man': 
                                                new_angle = (180.0 - float(D_C[c_object][attribute_name])) % 360.0
                                                if new_angle == int(new_angle):
                                                    D_C[c_object][attribute_name] = str(int(new_angle))
                                                else:
                                                    D_C[c_object][attribute_name] = str(new_angle)
                                        else:
                                            #if not mirrored, subtract the b angle from the a angle
                                            angle_b = all_attributes[b_object][attribute_name]
                                            angle_a = all_attributes[difference][attribute_name]
                                            delta_angle = (float(angle_b) - float(angle_a)) 
                                            #apply the change in angle to the current D_C angle to get the final D angle
                                            new_angle = (float(D_C[c_object][attribute_name]) + delta_angle) % 360.0
                                            D_C[c_object][attribute_name] = str(new_angle)





        #initialize min for changes
        diffs = 3

        #Loop through the answers, 
        for i in range(1, 7):
            current = str(i)
            Option = problem.figures[current]
            fig_total_diff = 0

            #if the answer has the same number of objects as the generated guess (D_C)
            if len(Option.objects) == len(D_C):
                #get the changes between the answer and the object
                for object in Option.objects:
                    #match the object with a D_C object
                    current_min = 100
                    current_match = 'H'
                    for dc_obj in D_C:
                        diff = len(self.get_differences(Option.objects[object].attributes, D_C[dc_obj]))
                        if diff < current_min:
                            current_min = diff
                            current_match = dc_obj

                    fig_total_diff = fig_total_diff + current_min            

                if fig_total_diff < diffs:
                    diffs = fig_total_diff
                    answer = i
            else:
                fig_total_diff = 100


                
        print("the answer is ", answer)
        dummy = input()

        return answer


    def is_mirrored(self, angle_A, angle_B, shape):
        mirrored = False

        #Check triangle mirroring
        if shape == 'right triangle':
            mirrored_angle = (270.0 - float(angle_A)) % 360.0
            if mirrored_angle == float(angle_B):
                mirrored = True

        #check pac-man mirroring
        if shape == 'pac-man':
            mirrored_angle = (180.0 - float(angle_A)) % 360.0
            if mirrored_angle == float(angle_B):
                mirrored = True
        return mirrored


    def match(self, A, B):
        pairs = {}
        unmatched = []

        #select the figure to iterate through. Should usually be the one with fewer objects. If same number of objects, make it B.
        iterate = B
        tester = A
        if len(A.objects) < len(B.objects):
            iterate = A
            tester = B

        #make an array of the objects that have not yet been matched from the larger figure.
        for object in tester.objects:
            unmatched.append(object) 
        
        #iterate through the objects in the smaller figure
        for object_i in iterate.objects:
            current_min = 100
            current_obj = 'W'
            
            #go through the yet unmatched objects of the bigger figure
            for i in range(len(unmatched)):
                num_diff = len(self.get_differences(tester.objects[unmatched[i]].attributes, iterate.objects[object_i].attributes))
                #if it is the smallest number of differences so far
                if num_diff < current_min:
                    current_min = num_diff
                    current_obj = unmatched[i]

                #if it equals the smallest number of differences found so far, find out which one has the most similarities
                if num_diff == current_min:
                    similar1 = 0
                    similar2 = 0

                    #Count similarities for each.
                    for attribute_name, attribute_value in iterate.objects[object_i].attributes.items():
                        if attribute_name in tester.objects[unmatched[i]].attributes:
                            if attribute_value == tester.objects[unmatched[i]].attributes[attribute_name]:
                                similar1 = similar1 + 1
                        if attribute_name in tester.objects[current_obj].attributes:
                            if attribute_value == tester.objects[current_obj].attributes[attribute_name]:
                                similar2 = similar2 + 1
                    
                    #only if the new object has more similarities than the old
                    if similar2 < similar1:
                        current_min = num_diff
                        current_obj = unmatched[i]

            #remove the matched object from the unmatched list  
            unmatched.remove(current_obj)
            
            #add pair to paired list in both directions.
            pairs[object_i] = current_obj
            pairs[current_obj] = object_i

        for i in range(len(unmatched)):
            if iterate == B:
                pairs[unmatched[i]] = 'deleted'
            else:
                pairs[unmatched[i]] = 'added'

        return pairs

    
    def get_differences(self, A_dict, B_dict):
        diff = {}
        #Go through each element in B, compare to current element in A
        for attribute_name, attribute_a in A_dict.items():
            if attribute_name in B_dict:
                if B_dict[attribute_name] != attribute_a:
                    diff[attribute_name] = B_dict[attribute_name]
            else:
                diff[attribute_name] = 'deleted'
        
        #Go through each element in A, compare to current element in B. This is to make sure nothing added is left out.
        for attribute_name, attribute_b in B_dict.items():
            if attribute_name not in diff:
                if attribute_name in A_dict:
                    if A_dict[attribute_name] != attribute_b:
                        diff[attribute_name] = A_dict[attribute_name]
                else:
                    diff[attribute_name] = 'added'
        return diff