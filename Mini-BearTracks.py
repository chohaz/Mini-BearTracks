'''
This program is the mini-version of beartracks.
Using the information of the matching file, it allows the user to 
print the timetable, enroll in the course, drop the course. 
name: Hazel Cho
date: Fri Oct 13
'''



class minibear:
    def __init__(self):
        '''
        Initializes an multiple dictionaries that is used through out the function along with printing the header
        Inputs: none
        Returns: None

        '''
        welcome = 'Welcome to Mini-BearTracks'
        print(f"{'='*len(welcome)}\n{welcome}\n{'='*len(welcome)}")        
        self.dic = {} 
        lit = []
        with open('students.txt', 'r') as f:  # save the file in a seperate dictionary
            for line in f:
                line = line.rstrip('\n') # remove new line
                sav = line.split(',') # split and save the list by the comma
                lit.append(sav)
            
        for sub in lit:
            self.dic[sub[0].strip()] = sub[1].strip(), sub[2].strip()
        
        self.enro = {}
        self.cenro = {} 
        self.cours = {}
        
        with open ('courses.txt','r') as f: # save the course information as a dictionary
            for line in f:
                line = line.strip('\n')
                li = line.split(';')
                for i in range(len(li)):
                    li[i] = li[i].strip()
                self.cours[li[0]] = li[1], li[2], li[3]         
        for v in self.cours.keys():
            self.cenro[v] = 0        
        with open ('enrollment.txt','r') as f: # save the enrollment info as a dictionary with student ID as key and course name as value
            for line in f:
                line = line.strip('\n')
                l = line.split(':')
                for i in range(len(l)):
                    l[i] = l[i].strip()
                value = l[0]
                if len(l) >= 2:
                    key = l[1]
                for k in self.dic.keys():
                    if key == k:
                        try:
                            self.enro[key]
                        except:                
                            self.enro[key] = [value]
                        else:
                            self.enro[key].append(value)
                    else:
                        try:
                            self.enro[k]
                        except:
                            self.enro[k] = []

                    # save the number of students enrolled in certain courses
                    
                try:
                    self.cenro[value] + 1 == 2
                except:
                    self.cenro[value] = 1
                else:
                    temp = self.cenro[value] + 1
                    self.cenro[value] = temp
            print(self.cours)
            print(self.enro)
    def menu(self):
        '''
    Prompts the user to enter a valid choice from the given menu
    Input: None
    Return: valid choice
    '''
        choice = input("\nWhat would you like to do?\n1. Print timetable\n2. Enroll in course\n3. Drop course\n4. Quit\n")
        while choice != '1' and choice != '2' and choice != '3' and choice != '4':
            ("Sorry, invalid entry. Please enter a choice from 1 to 4.")
            choice = input("Sorry, invalid entry. Please enter a choice from 1 to 4.\n")
        return choice
    
    #option 1
    def checkid(self):
        '''
    Checks if the given ID is a existing student ID in the students.txt
    Input: None
    Return: Valid student ID if there is one and if there isn't, it returns False
    '''
        
        inp = input('\nStudent ID: ')
        if inp in self.dic.keys():
            return inp
        else:
            return False

    
    #option 2
    def timetable(self,studentid):
        '''
    Creates the timetable of the given ID
    Input: Student ID
    Return: Valid timetable for the matching student ID
    '''
        print(f'Timetable for {self.dic[studentid][1].upper()}, in the faculty of {self.dic[studentid][0]}')
        
        sktime = []
        time = []
        i = 8.00
        while i < 17: # make a list of the time(used in the time table)  
            sktime.append(("{:.2f}".format(i)))
            i = i + .30
            sub = round(i - int(i))
            if sub == 1:
                i =i + 0.40
                
        for t in sktime: # replace the decimal point with ':'
            t = t.replace('.',':')
            time.append(t)    
        
        ctime = {}
        enstud = self.enro[studentid]
        for course in enstud: # dictionary of time and days of the week of the course student is registered into
            ctime[course] = self.cours[course][0].split()
        
        # first row of the table (column name)
        week = ['Mon','Tues','Wed','Thurs','Fri']
        table = '     '
        for i in week:
            table = table + ' '
            table = table + "{:^10}".format(i)
        table = table + '\n'
        table = table + '     '+ '+'+ (('-'*10) +'+')*5+ '\n'
        
        for ti in time:
            dl = []
            tl = []
            omwf = ''
            otr = ''
            table = table + '{:^5}'.format(ti) + '|'        
            for course in ctime:
                t = ctime[course][1]
                d = ctime[course][0]
                c = course.split() # divide course name into two list
                if len(c[0]) > 4: # when the abbreviation code is longer than 4 characters, it is truncated into 3 letters with an asterlisk at the end
                    cn = c[0][:-2]
                    cn = cn + '*' + ' ' + c[1]
                else:
                    cn = course
                if 'MWF' in d and t == ti:
                    dl.append(cn)
                    omwf = course
                #table = table + "{:^10}".format(cn) + '|' 
                elif 'TR' in d and t == ti:
                    tl.append(cn)
                    otr = course
    
            i = 1
            o = 0 # display the course name in correct place
            while i <= 5:
                if i % 2 != 0:
                    if dl == []:
                        table = table + "{:>11}".format('|')
                        i = i + 1
                    else:    
                        table = table + "{:^10}".format(dl[o]) + '|'
                        i = i + 1    
                elif i % 2 == 0:
                    if tl == []:
                        table = table + "{:>11}".format('|')
                        i = i + 1
                    else:    
                        table = table + "{:^10}".format(tl[o]) + '|'
                        i = i + 1
                        
                                
            table = table + '\n' + "{:>6}".format('|')
            i = 1 # display the opened seat under the corresponding 
            while i <= 5:
                if i % 2 != 0:
                    if dl == []:
                        table = table + "{:>11}".format('|')
                        i = i + 1
                    else:
                        num = int(self.cours[omwf][1]) - self.cenro[omwf]
                        table = table + "{:^10}".format(num) + '|'
                        i = i + 1    
                elif i % 2 == 0:
                    if tl == []:
                        table = table + "{:>11}".format('|')
                        i = i + 1
                    else:
                        num = int(self.cours[otr][1]) - self.cenro[otr]                    
                        table = table + "{:^10}".format(num) + '|'
                        i = i + 1        
           
            i = 1 
            index = (time.index(ti)+1)*3
            if index % 18 != 0:
                table = table + '\n' + "{:>6}".format('|')
            elif index % 18 == 0:
                table = table + '\n' + "{:>6}".format('+')
                    
            while i <= 5: # divdes the timetable differently according to the week and time of the day
                if i % 2 != 0:
                    if index % 18 == 0:
                        table = table + format('-'*10) + '+'
                        i = i + 1                    
                    elif index % 6 != 0:
                        table = table + "{:>11}".format('|')
                        i = i + 1
                    elif index % 6 == 0:
                        table = table + format('-'*10) + '|'
                        i = i + 1    
                elif i % 2 == 0:
                    if index % 18 == 0:
                        table = table + format('-'*10) + '+'
                        i = i + 1                    
                    elif index % 9 != 0:
                        table = table + "{:>11}".format('|')
                        i = i + 1
                    elif index % 9 == 0:
                        table = table + format('-'*10) + '|'
                        i = i + 1                
            table = table + '\n'
            
        return table
    
    # option 3        
    def enroll(self,studentid):
        '''
        Updates the enrollment info from the given input
        This function enrolls the wanted class that user inputs.
        Inputs: Valid student ID
        Returns: None
        '''         
        b = True
        inps = input('Course name: ') #input for course name
        temp = inps.split()
        temp1 = temp[0].upper() # changes the alphabets in the input to a caplital letter
        inp = f'{temp1} {temp[1]}' # marges the capatal alphabets with possible class number
        if inp in self.cours.keys():
            if inp not in self.enro[studentid]:
                for i in self.enro[studentid]:
                    if self.cours[inp][0] == self.cours[i][0]:
                        b = False
                if b == True:
                    if int(self.cours[inp][1]) - int(self.cenro[inp]) > 0:
                        with open("enrollment.txt", 'a') as f:
                            f.write(f"{inp}: {studentid}\n")
                        print(f"{self.dic[studentid][1]} has successfully been enrolled in {inp}, on {self.cours[inp][0]}")
                        count = self.cenro[inp]
                        self.cenro[inp] = count + 1
                        self.enro[studentid].append(inp)
                    else:
                        print(f"Cannot enroll. {inp} is already at capacity. Please contact advisor to get on waiting list.")
                if b == False:
                    print(f"Schedule conflict: already registered for course on {self.cours[inp][0]}")
                  
            else:
                print(f"Schedule conflict: already registered for course on {self.cours[inp][0]}")
        else:
            print('Invalid course name.')
            
    def drop(self, studentid):
        '''
        Updates the enrollment information from the given user input.
        This function drops the unwanted class that user inputs.
        Inputs: Valid student ID
        Returns: None
        '''
        
        if self.enro[studentid] != []:       
            print('Select course to drop:')
            for i in self.enro[studentid]:
                print(f"-{i}")
            inps = input()
            #if inps not in self.enro[studentid]:
            #    print(f"Drop failed. {self.dic[studentid][1]} is not currently registered in {inps}.")
            try:    
                temp = inps.split()
                temp1 = temp[0].upper()
                inp = f'{temp1} {temp[1]}' 
            except:
                print(f"Drop failed. {self.dic[studentid][1]} is not currently registered in {inps}.")
            else:     
                if inp in self.enro[studentid]:
                    lines = []
                    with open('enrollment.txt','r') as f:
                        for line in f:
                            sline = line.strip('\n')
                            l = sline.split(':')
                            for i in range(len(l)):
                                l[i] = l[i].strip()
                            if l[0] != inp and l[1] == studentid:
                                lines.append(line)
                            elif l[0] == inp and l[1] != studentid:
                                lines.append(line)
                            elif l[0] != inp and l[1] != studentid:
                                lines.append(line)                        
                                
                    with open('enrollment.txt','w') as f:
                        f.writelines(lines)
                    print(f"{self.dic[studentid][1]} has successfully droped in {inp}")
                    count = self.cenro[inp]               
                    self.cenro[inp] = count - 1
                    self.enro[studentid].remove(inp)                
           # else:
              #  print(f"Drop failed. {self.dic[studentid][1]} is not currently registered in {inp}.")
        else:
            print("There is no course to drop")
            
            

if __name__ == "__main__": 
    '''
    Controls main flow of mini beartracks
    Inputs: N/A
    Returns: None
    '''     
    mini = minibear()
    quit = False
    while not quit:
        choice = mini.menu()            
        if choice == '1':
            student = mini.checkid()
            if student != False:
                print(mini.timetable(student))                    
            else:
                print('Invalid student ID.  Cannot print timetable.')
        if choice =='2':
            student = mini.checkid()
            if student != False:
                mini.enroll(student)
            else:
                print('Invalid student ID. Cannot continue with course enrollment.')
        if choice == '3':
            student = mini.checkid()
            if student != False:
                mini.drop(student)
            else:
                print('Invalid student ID. Cannot continue with course drop.')            
        if choice == '4':
            quit = True
                    
    print("Goodbye")
