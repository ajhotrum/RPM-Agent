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
import copy


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
        self.alignments = ["inside", "above", "below", "left-of", "right-of"]

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
        answer = 7
        all_attributes = {}
        counter = 0

        if 'D' in problem.figures:

            #Set up figures
                #Use A, C, and G
            A = problem.figures['A']
            B = problem.figures['B']
            C = problem.figures['C']
            D = problem.figures['D']
            E = problem.figures['E']
            F = problem.figures['F']
            G = problem.figures['G']
            H = problem.figures['H']

            #for each object put its name in the dict of dicts
            for object in A.objects:
                all_attributes[object]=A.objects[object].attributes

            for object in C.objects:
                all_attributes[object]=C.objects[object].attributes

            for object in G.objects:
                all_attributes[object]=G.objects[object].attributes


            #change the alignment dict to an array like dict = {'left-of' : ['f', 'g']}
                #Can access with dict['left-of'][0]
            for object in all_attributes:
                for attribute in all_attributes[object]:
                    for i in range(len(self.alignments)):
                        if self.alignments[i] == attribute:
                            all_attributes[object][attribute] = all_attributes[object][attribute].split(',')


            #if there are multiple objects, compare them
            ac_pairs = self.match(A, C)
            ag_pairs = self.match(A, G)
            
            #print(ac_pairs)
            #print(ag_pairs)
            

            #arrays to hold which objects were added
            ac_added = []
            ag_added = []


            #Get A/B and A/C differences.
            differences_ac = {}
            #go through all pairs
            for object in ac_pairs:
                pair = ac_pairs[object]
                #if the object wasn't deleted or added
                if pair != "deleted" and pair != "added":
                    #if object being analyzed is from Figure A (so that b:a doesnt get analyzed after a:b)
                    if pair not in A.objects:
                        diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                        differences_ac[object] = copy.deepcopy(diffs)
                elif pair == "deleted":
                    differences_ac[object] = 'deleted'
                elif pair == "added":
                    differences_ac[object] = 'added'
                    ac_added.append(object)


            differences_ag = {}
            for object in ag_pairs:
                pair = ag_pairs[object]
                #if the object wasn't deleted or added
                if pair != "deleted" and pair != "added":
                    #if object being analyzed is from Figure A (so that c:a doesnt get analyzed after a:c)
                    if pair not in A.objects:
                        diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                        differences_ag[object] = diffs
                elif pair == "deleted":
                    differences_ag[object] = 'deleted'
                elif pair == "added":
                    differences_ag[object] = 'added'
                    ag_added.append(object)

            """

            #code to remove the "inside" attributes from the differences dicts if the objects match
                #so if 'a' and 'c' are matched, then 'inside' : 'a' and 'inside' : 'c' will not be counted as a difference
            for i in range(len(self.alignments)):
                for object in differences_ac:
                    if self.alignments[i] in differences_ac[object] and self.alignments[i] in all_attributes[ac_pairs[object]]:
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

            """

            #Dict for the new I value coming from G
            I_G = {}
            #make same as G
            for object in G.objects:
                I_G[object] = copy.deepcopy(all_attributes[object])


            #Go through all the A/C changes and apply them to G
            for difference in differences_ac:
                #check to see if the corresponding G object was deleted (To reduce redundency)
                    #NOTE: Does not include objects that were added
                if difference in ag_pairs:
                    if ag_pairs[difference] != "deleted":
                        #check to see if the object was added from A -> B
                        if difference in ac_pairs:
                            #check to see if the object was deleted from A -> C
                            if ac_pairs[difference] == "deleted":
                                #if so, delete it from I_G
                                del I_G[ac_pairs[difference]]

                            #if the object was neither deleted nor added between A -> C
                            else:
                                c_object = ac_pairs[difference]
                                g_object = ag_pairs[difference]
                                for attribute_name, attribute in differences_ac[difference].items():
                                    #fill check
                                    if attribute_name == 'fill':
                                        I_G[g_object][attribute_name] = all_attributes[c_object][attribute_name]
                                    #if shape changed, change G shape to whatever C shape is
                                    elif attribute_name == 'shape':
                                        #if it didn't change from a square to a rectangle
                                        if attribute != "rectangle" and  all_attributes[object]["shape"] != 'sqare':
                                            #if it didnt change from a rectangle to a square 
                                            if attribute != "square" and  all_attributes[object]["shape"] != 'rectangle':
                                                if c_object in I_G:
                                                    I_G[c_object][attribute_name] = all_attributes[c_object][attribute_name]
                                        
                                        #if there was a change to a rectangle from a square (or vice versa)
                                        else:
                                            #Get heights and widths of A, C, and G. Check if each is a square or rectangle
                                            if attribute == "rectangle":
                                                c_height = all_attributes[c_object]['height']
                                                c_width = all_attributes[c_object]['width']
                                            elif attribute == "square":
                                                c_height = all_attributes[c_object]['size']
                                                c_width = c_height
                                            if all_attributes[difference]["shape"] == 'square':
                                                a_height = all_attributes[difference]['size']
                                                a_width = a_height
                                            elif all_attributes[difference]["shape"] == 'rectangle':
                                                a_height = all_attributes[difference]['height']
                                                a_width = all_attributes[difference]['width']
                                            if I_G[g_object]["shape"] == 'rectangle':
                                                g_height = I_G[g_object]['height']
                                                g_width = I_G[g_object]['width']
                                            elif I_G[g_object]["shape"] == 'square':
                                                g_height = I_G[g_object]['size']
                                                g_width = g_height
                                            
                                            #fugure out what the I height will be
                                            if g_height in self.sizes and a_height in self.sizes and c_height in self.sizes:
                                                diff = self.sizes.index(c_height) - self.sizes.index(a_height)
                                                i_height = self.sizes[self.sizes.index(g_height) + diff]

                                            
                                            #fugure out what the I width will be
                                            if g_width in self.sizes and a_width in self.sizes and c_width in self.sizes:
                                                diff = self.sizes.index(c_width) - self.sizes.index(a_width)
                                                i_width = self.sizes[self.sizes.index(g_width) + diff]
                                            

                                            #if height and width are the same, make I a square, if they are different, make it a rectangle
                                            if i_height == i_width:
                                                I_G[g_object]['shape'] = 'square'
                                                I_G[g_object]['size'] = i_width
                                                #if it had a width and height (from previously being a rectangle) delete them
                                                if 'width' in I_G[g_object]:
                                                    del I_G[g_object]['width']
                                                if 'height' in I_G[g_object]:
                                                    del I_G[g_object]['height']
                                            
                                            #if heigh and width are different
                                            else:
                                                I_G[g_object]['shape'] = 'rectangle'
                                                I_G[g_object]['width'] = i_width
                                                I_G[g_object]['height'] = i_height
                                                #if it had a size (from previously being a square) delete it
                                                if 'size' in I_G[g_object]:
                                                    del I_G[g_object]['size']


                                    #if size changed from A->C, do the appropriate size jump from G -> I
                                    elif attribute_name == 'size':
                                        if differences_ac[difference]['size'] != "deleted":
                                            a_size = ""
                                            c_size = ""
                                            g_size = ""
                                            #get the sizes for a, c, g
                                            for i in range(len(self.sizes)):
                                                if attribute_name in all_attributes[c_object]:
                                                    if self.sizes[i] == all_attributes[c_object][attribute_name]:
                                                        c_size = i
                                                    if self.sizes[i] == all_attributes[difference][attribute_name]:
                                                        a_size = i
                                                    if self.sizes[i] == all_attributes[g_object][attribute_name]:
                                                        g_size = i

                                            #if no change between a and c, no change between g and i, which is already true so nothing needs to happen
                                            #if change between a and c, apply that same change from G to I
                                            if a_size != c_size:
                                                diff_ac = c_size - a_size
                                                i_size = g_size + diff_ac
                                                I_G[g_object][attribute_name] = self.sizes[i_size]

                                    elif attribute_name == "alignment":
                                        #go through the directions attribute to find the pair that describes what is happening from A to C
                                        for direction in self.directions:
                                            for first, second in self.directions[direction].items():
                                                if all_attributes[difference][attribute_name] == first and all_attributes[c_object][attribute_name] == second:
                                                    #once found, record the direction
                                                    ac_direction = direction
                                        #Use the direction and the G starting position to set the position of I
                                        for first1, second1 in self.directions[ac_direction].items():
                                            if first1 == I_G[g_object][attribute_name]:
                                                I_G[g_object][attribute_name] = second1




                                    #if the same shape, check if angle has changed
                                    if all_attributes[difference]['shape'] == all_attributes[g_object]['shape']:
                                        if attribute_name == 'angle':
                                            #check for mirroring from A to G
                                            mirrored = self.is_mirrored(all_attributes[difference]['angle'], all_attributes[g_object]['angle'], all_attributes[difference]['shape'])

                                            #if it was mirrored, get corresponding mirrored angle
                                            if mirrored:
                                                if I_G[g_object]['shape'] == 'right triangle':
                                                    new_angle = (270.0 - float(I_G[g_object][attribute_name])) % 360.0
                                                    #if there is a decimal, include it in the string. Otherwise just make it an int then a string
                                                    if new_angle == int(new_angle):
                                                        I_G[g_object][attribute_name] = str(int(new_angle))
                                                    else:
                                                        I_G[g_object][attribute_name] = str(new_angle)
                                                elif I_G[g_object]['shape'] == 'pac-man':
                                                    new_angle = (180.0 - float(I_G[g_object][attribute_name])) % 360.0
                                                    if new_angle == int(new_angle):
                                                        I_G[g_object][attribute_name] = str(int(new_angle))
                                                    else:
                                                        I_G[g_object][attribute_name] = str(new_angle)
                                            else:
                                                #if not mirrored, subtract the c angle from the a angle
                                                angle_c = all_attributes[c_object][attribute_name]
                                                angle_a = all_attributes[difference][attribute_name]
                                                delta_angle = (float(angle_c) - float(angle_a))
                                                #apply the change in angle to the current I_G angle to get the final I angle
                                                new_angle = (float(I_G[g_object][attribute_name]) + delta_angle) % 360.0
                                                I_G[g_object][attribute_name] = str(new_angle)

                #if the object has been added between A -> C
                elif differences_ac[difference]=='added':
                    #if the number of objects in E equals the sum of the objects in D and B
                    if len(B.objects) * len(D.objects) == len(E.objects):
                        #for each object originally in G, add this object for I
                        for object in G.objects:
                            #update the counter, this makes the variables "var1", "var2", etc
                            counter = counter + 1
                            #add the object, then manipulate the alignment
                            I_G["var{0}".format(counter)] = copy.deepcopy(all_attributes[difference])

                            
                            # switch the name of the "above" objects to their G counterparts
                            if "above" in I_G["var{0}".format(counter)]:
                                for k in range(len(I_G["var{0}".format(counter)]["above"])):
                                    if I_G["var{0}".format(counter)]["above"][k] in ac_pairs:
                                        if ac_pairs[I_G["var{0}".format(counter)]["above"][k]] != "added":
                                            if ac_pairs[I_G["var{0}".format(counter)]["above"][k]] in ag_pairs:
                                                if ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["above"][k]]] != "deleted":
                                                    I_G["var{0}".format(counter)]["above"][k] = ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["above"][k]]]

                            #Copy the "above" attributes from the current G object
                            if "above" in all_attributes[object]:
                                if "above" not in I_G["var{0}".format(counter)]:
                                    I_G["var{0}".format(counter)]["above"] = []
                                for l in range(len(all_attributes[object]["above"])):
                                    if all_attributes[object]["above"][l] not in I_G["var{0}".format(counter)]["above"]:
                                        I_G["var{0}".format(counter)]["above"].append(all_attributes[object]["above"][l])


                            # switch the name of the "left-of" objects to their G counterparts
                            if "left-of" in I_G["var{0}".format(counter)]:
                                for k in range(len(I_G["var{0}".format(counter)]["left-of"])):
                                    if I_G["var{0}".format(counter)]["left-of"][k] in ac_pairs:
                                        if ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]] != "added":
                                            if ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]] in ag_pairs:
                                                if ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]]] != "deleted":
                                                    I_G["var{0}".format(counter)]["left-of"][k] = ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]]]
                            
                            #Copy the "left-of" attributes from the current G object
                            if "left-of" in all_attributes[object]:
                                if "left-of" not in I_G["var{0}".format(counter)]:
                                    I_G["var{0}".format(counter)]["left-of"] = []
                                for l in range(len(all_attributes[object]["left-of"])):
                                    if all_attributes[object]["left-of"][l] not in I_G["var{0}".format(counter)]["left-of"]:
                                        I_G["var{0}".format(counter)]["left-of"].append(all_attributes[object]["left-of"][l])
                            

                            #go through all objects in G and add new object to anything that current G object is in
                            for object_1 in I_G:
                                if object_1 != object and object_1 != "var{0}".format(counter):
                                    if "above" in I_G[object_1]:
                                        if object in I_G[object_1]["above"]:
                                            I_G[object_1]["above"].append("var{0}".format(counter))
                            
                            
                            for object_2 in I_G:
                                if object_2 != object and object_2 != "var{0}".format(counter):
                                    if "left-of" in I_G[object_2]:
                                        if object in I_G[object_2]["left-of"]:
                                            I_G[object_2]["left-of"].append("var{0}".format(counter))
                            

                            

                    #otherwise, just add the one object
                    else:
                        if len(C.objects) != len(F.objects) or len(G.objects) != len(H.objects):


                            I_G[difference] = copy.deepcopy(all_attributes[difference])

                            

                            #make the left-of and above attributes line up
                            if "above" in I_G[difference]:
                                for k in range(len(I_G[difference]["above"])):
                                    if I_G[difference]["above"][k] in ac_pairs:
                                        if ac_pairs[I_G[difference]["above"][k]] != "added":
                                            if ac_pairs[I_G[difference]["above"][k]] in ag_pairs:
                                                if ag_pairs[ac_pairs[I_G[difference]["above"][k]]] != "deleted":
                                                    I_G[difference]["above"][k] = ag_pairs[ac_pairs[I_G[difference]["above"][k]]]
                            
                            if "above" in I_G[difference]:
                                for i in range(len(I_G[difference]["above"])):
                                    if I_G[difference]["above"][i] in I_G:
                                        if "above" in I_G[I_G[difference]["above"][i]]:
                                            for j in range(len(I_G[I_G[difference]["above"][i]]["above"])):
                                                I_G[difference]["above"].append(I_G[I_G[difference]["above"][i]]["above"][j])

                            if "left-of" in I_G[difference]:
                                for k in range(len(I_G[difference]["left-of"])):
                                    if I_G[difference]["left-of"][k] in ac_pairs:
                                        if ac_pairs[I_G[difference]["left-of"][k]] != "added":
                                            if ac_pairs[I_G[difference]["left-of"][k]] in ag_pairs:
                                                if ag_pairs[ac_pairs[I_G[difference]["left-of"][k]]] != "deleted":
                                                    I_G[difference]["left-of"][k] = ag_pairs[ac_pairs[I_G[difference]["left-of"][k]]]
                                
                                for i in range(len(I_G[difference]["left-of"])):
                                    if I_G[difference]["left-of"][i] in I_G:
                                        if "left-of" in I_G[I_G[difference]["left-of"][i]]:
                                            for j in range(len(I_G[I_G[difference]["left-of"][i]]["left-of"])):
                                                I_G[difference]["left-of"].append(I_G[I_G[difference]["left-of"][i]]["left-of"][j])
                        
                        else:
                            g_attributes = {}
                            h_attributes = {}
                            differences_gh = {}
                            gh_pairs = self.match(G, H)



                            for object in G.objects:
                                all_attributes[object]=G.objects[object].attributes

                            for object in H.objects:
                                all_attributes[object]=H.objects[object].attributes

                            
                            for object in gh_pairs:
                                pair = gh_pairs[object]
                                diffs_gh = self.get_differences(all_attributes[object], all_attributes[pair])
                                differences_gh[object] = copy.deepcopy(diffs_gh)
                            
                            diffs = 0
                            for object in differences_gh:
                                diffs = diffs + len(differences_gh[object]) 

                            diff_newh = [0, 0, 0, 0, 0, 0, 0, 0, 0]

                            for i in range(1, 9):
                                current = str(i)
                                Option = problem.figures[current]
                                fig_total_diff = 0
                                all_h_objects = []
                                for h_obj in H.objects:
                                    all_h_objects.append(h_obj)




                                    
                                new_attributes = {}
                                h_attributes = {}
                                differences_newh = {}
                                newh_pairs = self.match(H, Option)



                                for object in Option.objects:
                                    all_attributes[object]=Option.objects[object].attributes

                                
                                for object in newh_pairs:
                                    pair = newh_pairs[object]
                                    if object in all_attributes and pair in all_attributes:
                                        diffs_newh = self.get_differences(all_attributes[object], all_attributes[pair])
                                        differences_newh[object] = copy.deepcopy(diffs_newh)
                                
                                diffs_1 = 0
                                for object in differences_newh:
                                    diffs_1 = diffs_1 + len(differences_newh[object]) 
                                diff_newh[i-1] = diffs_1
                                #print(self.get_differences(Option.objects[object].attributes, I_G[current_match]))
                                #print(object)
                                #print(current_match)

                            #print(i, fig_total_diff)

                            current_min = 100
                            for i in range(len(diff_newh)):
                                if abs(diffs - diff_newh[i])< current_min:
                                    current_min = abs(diffs - diff_newh[i])
                                    answer = i + 1

                        
                            #print("the answer is ", answer)
                            #dummy = input()
                            return answer
                                            


            #print(I_G)
            #dummy = input()


            #make above and left-of arrays
            A_above_array, A_left_array, A_direct_above, A_direct_left = self.alignment_array(A)
            C_above_array, C_left_array, C_direct_above, C_direct_left = self.alignment_array(C)
            G_above_array, G_left_array, G_direct_above, G_direct_left = self.alignment_array(G)
            I_above_array = copy.deepcopy(G_above_array)
            I_left_array = copy.deepcopy(G_left_array)
            I_direct_above = copy.deepcopy(G_direct_above)
            I_direct_left = copy.deepcopy(G_direct_left)

            #print(A_above_array, A_left_array, A_direct_above, A_direct_left)
            #print(C_above_array, C_left_array, C_direct_above, C_direct_left)
            #print(I_above_array, I_left_array, I_direct_above, I_direct_left)
            #dummy = input()
            


            # Get "left-of" order of C objects that are in G
            temp_left_C = []
            for i in range(len(C_left_array)):
                if C_left_array[i] in ac_pairs:
                    if ac_pairs[C_left_array[i]] != "added":
                        a_pair = ac_pairs[C_left_array[i]] 
                        if a_pair in ag_pairs:
                            if ag_pairs[a_pair] != "deleted":
                                temp_left_C.append(ag_pairs[ac_pairs[C_left_array[i]]])

            # Get "left-of" order of A objects that are in G
            temp_left_A = []
            for i in range(len(A_left_array)):
                if A_left_array[i] in ag_pairs:
                    if ag_pairs[A_left_array[i]] != "deleted":
                        temp_left_A.append(ag_pairs[A_left_array[i]])

            #figure out which changes happened between A and C, apply to I
            temp_left_I = []
            counter = 0
            for i in range(len(temp_left_A)):
                if temp_left_A[i] in temp_left_C:
                    if temp_left_A[i] != temp_left_C[i]:
                        if temp_left_C[i] in I_left_array:
                            temp_left_I.append(temp_left_C[i])
            
            counter = 0
            for i in range(len(I_left_array)):
                if I_left_array[i] in temp_left_I:
                    I_left_array[i] = temp_left_I[counter]
                    counter = counter + 1

            
            # Get "above" order of C objects that are in G
            temp_above_C = []
            for i in range(len(C_above_array)):
                if C_above_array[i] in ac_pairs:
                    if ac_pairs[C_above_array[i]] != "added":
                        a_pair = ac_pairs[C_above_array[i]] 
                        if a_pair in ag_pairs:
                            if ag_pairs[a_pair] != "deleted":
                                temp_above_C.append(ag_pairs[ac_pairs[C_above_array[i]]])

            # Get "above" order of A objects that are in G
            temp_above_A = []
            for i in range(len(A_above_array)):
                if A_above_array[i] in ag_pairs:
                    if ag_pairs[A_above_array[i]] != "deleted":
                        temp_above_A.append(ag_pairs[A_above_array[i]])


            #figure out which changes happened between A and C, apply to I
            temp_above_I = []
            counter = 0
            for i in range(len(temp_above_A)):
                if temp_above_A[i] in temp_above_C:
                    if temp_above_A[i] != temp_above_C[i]:
                        if temp_above_C[i] in I_above_array:
                            temp_above_I.append(temp_above_C[i])
            
            counter = 0
            for i in range(len(I_above_array)):
                if I_above_array[i] in temp_above_I:
                    I_above_array[i] = temp_above_I[counter]
                    counter = counter + 1


            

            

            #if alignment has not changed
            if (temp_left_C != temp_left_A) or (temp_above_A != temp_above_C):

                #Go through each object, make the appropriate left-of
                for object in I_G:
                    if object in I_left_array:
                        I_G[object]["left-of"] = []
                        index = I_left_array.index(object)
                        #put all objects that are to the left in the array in the "left-of" attribute
                        if (index+1) < len(I_left_array):
                            for i in range((index+1), len(I_left_array)):
                                #make sure it is not directly above
                                if object in I_direct_above:
                                    if I_left_array[i] not in I_direct_above[object]:
                                        I_G[object]["left-of"].append(I_left_array[i])
                                else:
                                    I_G[object]["left-of"].append(I_above_array[i])
                        #if nothing to the left, delete the "left-of" attribute
                        if len(I_G[object]["left-of"]) == 0:
                            del I_G[object]["left-of"]
                

                #Go through each object, make the appropriate above
                for object in I_G:
                    if object in I_above_array:
                        I_G[object]["above"] = []
                        index = I_above_array.index(object)
                        #put all objects that are to the left in the array in the "above" attribute
                        if (index+1) < len(I_above_array):
                            for i in range((index+1), len(I_above_array)):
                                #make sure it is not directly above
                                if object in I_direct_left:
                                    if I_above_array[i] not in I_direct_left[object]:
                                        I_G[object]["above"].append(I_above_array[i])
                                else:
                                    I_G[object]["above"].append(I_above_array[i])
                        #if nothing to the left, delete the "above" attribute
                        if len(I_G[object]["above"]) == 0:
                            del I_G[object]["above"]
                    
            

            #print(I_G)
            #dummy = input()
            




            
            """
            #figure out differences between A -> C alignments (above).
            same_flag = True
            #make a temporary array that includes the order of the C objects but does not include any added objects
            temp = C_above_array
            to_delete_from_temp = []
            for j in range(len(temp)):
                if temp[j] in ac_pairs:
                    if ac_pairs[temp[j]] == "added":
                        to_delete_from_temp.append(j)

            for i in range(len(to_delete_from_temp)):
                del temp[to_delete_from_temp[i]]
            
            #if the A array is the same as the temp, then do nothing
            for i in range(len(A_above_array)):
                if ac_pairs[A_above_array[i]] != "deleted":
                    if temp[i] in ac_pairs:
                        if A_above_array[i] != ac_pairs[temp[i]]:
                            same_flag = False

            #if the A array is not the same as the temp, make the ordering the same for G
            if not same_flag:
                #make I the same as temp, then translate to the correct object names
                I_above_array = temp
                for i in range(len(I_above_array)):
                    if ac_pairs[I_above_array[i]] != 'added':
                        I_above_array[i] = ag_pairs[ac_pairs[I_above_array[i]]]


            #figure out differences between A -> C alignments (left-of).
            same_flag = True
            temp = C_left_array
            to_delete_from_temp = []
            for j in range(len(temp)):
                if temp[j] in ac_pairs:
                    if ac_pairs[temp[j]] == "added":
                        to_delete_from_temp.append(j)
            
            for i in range(len(to_delete_from_temp)):
                del temp[to_delete_from_temp[i]]
            
            for i in range(len(A_left_array)):
                if ac_pairs[A_left_array[i]] != "deleted":
                    if temp[i] in ac_pairs:
                        if A_left_array[i] != ac_pairs[temp[i]]:
                            same_flag = False


            #if the A array is not the same as the temp, make the ordering the same for G
            if not same_flag:
                #make I the same as temp, then translate to the correct object names
                I_left_array = temp
                for i in range(len(I_left_array)):
                    if ac_pairs[I_left_array[i]] != "added":
                        I_left_array[i] = ag_pairs[ac_pairs[I_left_array[i]]]


            #update I_G so that each object has the correct above and left-of count
            if len(I_above_array) != 0:
                #start from the left and apply the above attribute
                for i in range(len(I_above_array)):
                    if "above" in I_G[I_above_array[i]]:
                        del I_G[I_above_array[i]]["above"]
                    for j in range((i+1), len(I_above_array)):
                        #if "above" is not currently a feature
                        if 'above' not in I_G[I_above_array[i]]:
                            I_G[I_above_array[i]]['above'] = []
                        I_G[I_above_array[i]]['above'].append(I_above_array[j])
            else:
                if 'above' in I_G[I_above_array[i]]:
                    del I_G[I_above_array[i]]['above']

            
            if len(I_left_array) != 0:
                #start from the left and apply the above attribute
                for i in range(len(I_left_array)):
                    if 'left-of' in I_G[I_left_array[i]]:
                        del I_G[I_left_array[i]]["left-of"]
                    for j in range((i+1), len(I_left_array)):
                        if 'left-of' not in I_G[I_left_array[i]]:
                            I_G[I_left_array[i]]['left-of'] = []
                        I_G[I_left_array[i]]['left-of'].append(I_left_array[j])
            else:
                if 'left-of' in I_G[I_left_array[i]]:
                    del I_G[I_left_array[i]]['left-of']
            """










            #initialize min for changes
            diffs = 300

            #Loop through the answers,
            for i in range(1, 9):
                current = str(i)
                Option = problem.figures[current]
                fig_total_diff = 0

                #if the answer has the same number of objects as the generated guess (I_G)
                if len(Option.objects) == len(I_G):
                    #get the changes between the answer and the object
                    for object in Option.objects:
                        #match the object with a I_G object
                        current_min = 100
                        current_match = 'H'

                        # For object, change left and above to arrays
                        temporary = Option.objects[object].attributes
                        #make a temporary array that is the same as the object array (because you cannot change the figure attributes directly)
                        for attribute in temporary:
                            for j in range(len(self.alignments)):
                                if self.alignments[j] == attribute:
                                    temporary[attribute] = temporary[attribute].split(",")



                        for ig_obj in I_G:
                            diff = len(self.get_differences(temporary, I_G[ig_obj]))
                            if diff < current_min:
                                current_min = diff
                                current_match = ig_obj

                        fig_total_diff = fig_total_diff + current_min
                        #print(self.get_differences(Option.objects[object].attributes, I_G[current_match]))
                        #print(object)
                        #print(current_match)

                    #print(i, fig_total_diff)

                    if fig_total_diff < diffs:
                        diffs = fig_total_diff
                        answer = i
                else:
                    fig_total_diff = 100



            #print("the answer is ", answer)
            #dummy = input()

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
        diff_counter = 0
        #Go through each element in B, compare to current element in A
        for attribute_name, attribute_a in A_dict.items():
            if attribute_name in B_dict:
                if attribute_name == "left-of":
                    if len(B_dict[attribute_name]) != len(A_dict[attribute_name]):
                        diff[attribute_name] = B_dict[attribute_name]
                elif attribute_name == "above":
                    if len(B_dict[attribute_name]) != len(A_dict[attribute_name]):
                        diff[attribute_name] = B_dict[attribute_name]

                elif B_dict[attribute_name] != attribute_a:
                    diff[attribute_name] = B_dict[attribute_name]
            else:
                if attribute_name == "left-of":
                    for i in range(len(A_dict[attribute_name])):
                        diff["left-of_{0}".format(diff_counter)] = "deleted"
                        diff_counter = diff_counter + 1
                elif attribute_name == "above":
                    for i in range(len(A_dict[attribute_name])):
                        diff["left-of_{0}".format(diff_counter)] = "deleted"
                        diff_counter = diff_counter + 1
                else:
                    diff[attribute_name] = 'deleted'


        #Go through each element in A, compare to current element in B. This is to make sure nothing added is left out.
        for attribute_name, attribute_b in B_dict.items():
            if attribute_name not in diff:
                if attribute_name in A_dict:
                    if attribute_name == "left-of":
                        if len(B_dict[attribute_name]) != len(A_dict[attribute_name]):
                            #for j in range(abs(len(B_dict[attribute_name]) - len(A_dict[attribute_name]))):
                                #diff["left-of_{0}".format(diff_counter)] = "deleted"
                                #diff_counter = diff_counter + 1
                            diff[attribute_name] = A_dict[attribute_name]
                    elif attribute_name == "above":
                        if len(B_dict[attribute_name]) != len(A_dict[attribute_name]):
                            diff[attribute_name] = A_dict[attribute_name]
                    elif A_dict[attribute_name] != attribute_b:
                        diff[attribute_name] = A_dict[attribute_name]
                else:
                    if attribute_name == "left-of":
                        for i in range(len(B_dict[attribute_name])):
                            diff["left-of_{0}".format(diff_counter)] = "added"
                            diff_counter = diff_counter + 1
                            
                    elif attribute_name == "above":
                        for i in range(len(B_dict[attribute_name])):
                            diff["left-of_{0}".format(diff_counter)] = "added"
                            diff_counter = diff_counter + 1
                    else:
                        diff[attribute_name] = 'added'

        return diff


    def alignment_array(self, A):
        left_array = []
        above_array = []
        directly_above = {}
        directly_left = {}
        #produces an ordered array for left-of or above
        for object in A.objects:
            #if object is left of other object(s)
            if "left-of" in A.objects[object].attributes:            
                #get list of object(s) it is left of
                left_of =  A.objects[object].attributes["left-of"]
                #see if left_array is empty
                if len(left_array) != 0:
                    leftmost = 100
                    for i in range(len(left_of)):
                        #check if the item is already in the left-of array
                        if left_of[i] in left_array:
                            if i < leftmost:
                                leftmost = i
                        #if the item is not already in the array, add it to the end.
                        else:
                            #add unknown object to the end of left array
                            left_array.append(left_of[i])
                            #see if putting the object second to last works
                            temp = len(left_array) - 2
                            if temp < leftmost:
                                leftmost = temp

                    if object not in left_array:
                        left_array.insert(leftmost, object)
                    else:
                        if left_array.index(object) > leftmost:
                            del left_array[left_array.index(object)]
                            left_array.insert(leftmost, object)

                #if this is the first entry, put the left of items in and make the current object leftmost
                else:
                    left_array = left_of
                    left_array.insert(0, object)

            #if the object does not have a "left-of" attribute, if its not already in the array, put it at rightmost
            else:
                if object not in left_array:
                    left_array.append(object)
            
            
            #Do the same for "above:"
            if "above" in A.objects[object].attributes:
                #get list of object(s) it is above
                above =  A.objects[object].attributes["above"]
                #see if above is empty
                if len(above_array) != 0:
                    topmost = 100
                    for i in range(len(above)):
                        #check if the item is already in the above array
                        if above[i] in above_array:
                            if i < topmost:
                                topmost = i
                        #if the item is not already in the array, add it to the end.
                        else:
                            #add unknown object to the end of left array
                            above_array.append(above[i])
                            #see if putting the object second to last works
                            temp = len(above_array) - 2
                            if temp < topmost:
                                topmost = temp

                    if object not in above_array:
                        above_array.insert(topmost, object)
                    else:
                        if above_array.index(object) > topmost:
                            del above_array[above_array.index(object)]
                            above_array.insert(topmost, object)

                #if this is the first entry, put the left of items in and make the current object topmost
                else:
                    above_array = above
                    above_array.insert(0, object)

            #if the object does not have a "above" attribute, if its not already in the array, put it at bottommost
            else:
                if object not in above_array:
                    above_array.append(object)

            #method for finding which objects are directly above each other
            for object in A.objects:
                if object not in directly_above:
                    directly_above[object] = []
                for object2 in A.objects:
                    if object2 not in directly_above:
                        directly_above[object2] = []
                    if object != object2:
                        if "left-of" in A.objects[object].attributes and "left-of" in A.objects[object2].attributes:
                            if A.objects[object].attributes["left-of"] == A.objects[object2].attributes["left-of"]:
                                if object2 not in directly_above[object]:
                                    directly_above[object].append(object2)
                                if object not in directly_above[object2]:
                                    directly_above[object2].append(object)
                        #if both objects lack a "left-of" attribute, then they are directly above each other
                        elif "left-of" not in A.objects[object].attributes and "left-of" not in A.objects[object2].attributes:
                            if object2 not in directly_above[object]:
                                directly_above[object].append(object2)
                            if object not in directly_above[object2]:
                                directly_above[object2].append(object)
            
            #method for finding which objects are directly above next to each other
            for object in A.objects:
                if object not in directly_left:
                    directly_left[object] = []
                for object2 in A.objects:
                    if object2 not in directly_left:
                        directly_left[object2] = []
                    if object != object2:
                        if "above" in A.objects[object].attributes and "above" in A.objects[object2].attributes:
                            if A.objects[object].attributes["above"] == A.objects[object2].attributes["above"]:
                                if object2 not in directly_left[object]:
                                    directly_left[object].append(object2)
                                if object not in directly_left[object2]:
                                    directly_left[object2].append(object)
                        #if both objects lack a "above" attribute, then they are directly next to each other
                        elif "above" not in A.objects[object].attributes and "above" not in A.objects[object2].attributes:
                            if object2 not in directly_left[object]:
                                directly_left[object].append(object2)
                            if object not in directly_left[object2]:
                                directly_left[object2].append(object)
            
    


        return above_array, left_array, directly_above, directly_left

    
