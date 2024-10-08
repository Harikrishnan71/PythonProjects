from datetime import datetime
import re
import pandas as pd
import sys
import time
import tqdm
from tqdm import tqdm

#Function to convert the string type date and time to Datetime object
def convert_to_date(date_str):
    # Define the format of the input date string
    date_format = "%Y-%m-%d"  # Adjust the format as per your date string
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj

#Global stacks used for storing Log fragments and other data in to the CSV output file
T_on=[]# Main list containing processed Xray start time
T_off=[] #Main list containing processed Xray stop time[ Not logged in csv]
fps=[] #Main list containing processed FPS
kV=[]#Main list containing processed kV
image=[]#Main list containing processed Images
mode=[]#Main list containing processed Mode
log_on_off=[]#Main list containing processed log string[not logged in csv]
D_on=[]#Main list containing processed Xray start date
LoR=[]#Main list containing processed Left or Right


#global stacks used for storing Log fragments and other data in to the txt file.
stack_left_on_time=[] #Xray on time
stack_left_on_date=[] #Xray on date
stack_left_off_time=[] #Xray off time
stack_left_off_date=[] #Xray off date
stack_right_on_time=[] #Xray on time
stack_right_on_date=[] #Xray on date
stack_right_off_time=[] #Xray off time
stack_right_off_date=[] #Xray off date
mvs_switch_off_time=[] #MVS switch off time
mvs_switch_off_date=[] #MVS switch off date
shot_stack=[] #Xray shot stack
image_stack=[] #Images received stack
kv_actual_stack=[] #kV actual stack
# Data related to Mode and fps
mode_stack=[] #6
mode_2_stack=[]#7
mode_3_stack=[]#8
mode_4_stack=[]#9
mode_5_stack=[]#10
mode_6_stack=[]#11
mode_7_stack=[]#12
mode_8_stack=[]#13
mode_9_stack=[]#14
mode_10_stack=[]#15
#Left or right exposure
current_exposure_left=[]
current_exposure_right=[]

#List that contains processed logs
story_stack=[]
time_format = "%H:%M:%S.%f"
pattern = r"There were \d+ images received at"
number_pat=r"\d+"


#Main function called by MAIN
def investigate_file(file_path,date):
    listofwords=[]
    count =0
    lsw=0
    rsw=0
    try:
        with open(file_path, 'r') as file:
            for line in file:
                content2 = line.strip().split()
                if len(content2)>=1:
                    if content2[0]==date:  
                        #To check for Xray shots
                        if "USR switch off LEFT at" in line:
                            #print(line)
                            content=line.strip().split()
                            timestamp_off = datetime.strptime(content[1], time_format)
                            stack_left_off_time.append(timestamp_off) #append OFF time
                            stack_left_off_date.append(content[0]) #append OFF date
                            lsw=1
                            current_exposure_left.append("ON")
                            story_stack.append(line)
                        if "USR switch on LEFT at" in line:
                            #print(line)
                            if lsw==1 and current_exposure_left[-1]=="ON":
                                content=line.strip().split()
                                timestamp_on = datetime.strptime(content[1], time_format)
                                stack_left_on_time.append(timestamp_on)
                                stack_left_on_date.append(content[0])
                                shot_stack.append("LEFT")
                                lsw=0
                                current_exposure_left.pop()
                                story_stack.append(line)
                            else:
                                print(line)
                        #return xray_session
                        if "USR switch off RIGHT at" in line:
                            #print(line)
                            content=line.strip().split()
                            timestamp_off = datetime.strptime(content[1], time_format)
                            stack_right_off_time.append(timestamp_off)
                            stack_right_off_date.append(content[0])
                            rsw=1
                            current_exposure_right.append("ON")
                            story_stack.append(line)
                        if "USR switch on RIGHT at" in line:
                            #print(line)
                            if rsw==1 and current_exposure_right[-1]=="ON":
                                content=line.strip().split()
                                timestamp_on = datetime.strptime(content[1], time_format)
                                stack_right_on_time.append(timestamp_on)
                                stack_right_on_date.append(content[0])
                                rsw=0
                                shot_stack.append("RIGHT")
                                current_exposure_right.pop()
                                story_stack.append(line)
                        if "MVS Switch Off by User" in line:
                            content=line.strip().split()
                            timestamp = datetime.strptime(content[1], time_format)
                            mvs_switch_off_time.append(timestamp)
                            mvs_switch_off_date.append(content[0])
                            story_stack.append(line)
                        
                        #Images received string check
                        if re.search(pattern, line):
                            #print(line)
                            image_stack.append(line)
                            count+=1
                            img_r=1
                            #print(count)
                            story_stack.append(line)
                        
                        if "actual kV setting" in line:
                            if img_r==1:
                                content= line.strip().split()

                                kv_actual_stack.append(content[10])
                                img_r=0
                                story_stack.append(line)

                        if "AMS" and "DMC" in line:
                            #item index 6 to 15 are of importance to us
                            content = line.strip().split()
                            mode_stack.append(content[6])
                            mode_2_stack.append(content[7])
                            mode_3_stack.append(content[8])
                            mode_4_stack.append(content[9])
                            mode_5_stack.append(content[10])
                            mode_6_stack.append(content[11])
                            mode_7_stack.append(content[12])
                            mode_8_stack.append(content[13])
                            mode_9_stack.append(content[14])
                            

                            #print(content[15])
                            story_stack.append(content[6]+" "+content[7]+" "+content[8]+" "+content[9]+" "+content[10]+" "+content[11]+" "+content[12]+" "+content[13]+" "+content[14]+" "+content[-1])
                            if len(content)>=15:
                                mode_10_stack.append(content[14])
                                story_stack.append(" "+content[14])


        file.close()
        #Now we have all the Xray shots taken 
        #We now proceed to calculate the individual time taken for each shot
        print("stack_left_off_time",len(stack_left_off_time))
        print("stack_left_off_date",len(stack_left_off_date))
        print("stack_left_on_time",len(stack_left_on_time))
        print("stack_left_on_date",len(stack_left_on_date))

        print("stack_right_off_time",len(stack_right_off_time))
        print("stack_right_off_date",len(stack_right_off_date))
        print("stack_right_on_time",len(stack_right_on_time))
        print("stack_right_on_date",len(stack_right_on_date))

        print("kv_actual_stack",len(kv_actual_stack))
        print("image_stack",len(image_stack))
        print("mode stack",len(mode_stack))
        print("Story stack",len(story_stack))

        if len(stack_left_on_time)!=len(stack_left_off_time)+1:
            print("Left Stack shots are not equal")
        if len(stack_right_on_time)!=len(stack_right_off_time)+1:
            print("Right Stack shots are not equal")

        #Printing the stacks to create a story of the logs
        #This also reverses the time line as our logs appear from Latest to oldest in the file
        with open(r"D:\\story.txt","w") as file1:
            for i in range(len(story_stack) - 1, -1, -1):  # Loop in decreasing order
                file1.write(str(story_stack[i]) + "\n")
        file1.close()

        for _ in tqdm(range(20), desc="Processing", ncols=100):
            time.sleep(1)
        #This delay is added so that the txt file can be generated and saved.

        #Further processing of the story to create CSV
        with open(r"D:\\story.txt","r") as file1:
            for line in file1:
        #Sno  | Date | Left/Right | On Time | Off Time | Kv Actual | Images | Mode | FPS |  Calculated Duration
        #content 
        #[1, '24-08-29', '07:25:22.135', 'TID:', '1696', 'Information', 'SYS', 'USR', 'switch', 'off', 'LEFT', 'at', '4028734739']
                content2 = line.strip().split()
                acq_mode=""
                if "USR switch off LEFT at" in line:
                    content=line.strip().split()
                    timestamp_off = datetime.strptime(content[1], time_format)
                    T_off.append(timestamp_off)

                    

                if "USR switch on LEFT at" in line:
                    content=line.strip().split()
                    timestamp_on = datetime.strptime(content[1], time_format)
                    T_on.append(timestamp_on)
                    log_on_off.append(line)
                    LoR.append("LEFT")
                    acq_mode="LEFT"
                    


                if "USR switch off RIGHT at" in line:
                    content=line.strip().split()
                    timestamp_off = datetime.strptime(content[1], time_format)
                    T_off.append(timestamp_off)
 


                if "USR switch on RIGHT at" in line:
                    content=line.strip().split()
                    timestamp_on = datetime.strptime(content[1], time_format)
                    T_on.append(timestamp_on)
                    log_on_off.append(line)
                    LoR.append("RIGHT")
                    acq_mode="RIGHT"

                
                if "actual kV setting" in line:
                    content = line.strip().split()
                    kV.append(content[10])




                if re.search(pattern, line):
                    content = line.strip().split()
                    image.append(content[8])


                
                if "AMS" and "DMC" in line:
                    #content[5] is the deciding factor
                    #content[3] 
                    #content[4]
                    if "Digi RAD" in line:
                        #Digital Exposure(No Pulse Rate)
                        mode.append("Digi RAD")
                        fps.append(0)
                        #log_on_off.append(line)
                        #LoR.append(acq_mode)
                        
                        pass # make it 0
                    
                    else:
                        content = line.strip().split()
                        #print(content[3],content[4])
                        mode.append(content[3])
                        fps.append(content[-1])
                        #log_on_off.append(line)
                        #LoR.append(acq_mode)

                     
                        

                #calculate the Duration based on FPS and images
                
        file1.close
        print("Tons",len(T_on))
        print("D_on",len(D_on))
        print("Toffs",len(T_off))
        print("kV",len(kV))
        print("Image",len(image))
        print("Mode",len(mode))
        print("LOGs",len(log_on_off))
        print("AcqMode",len(LoR))
        data ={
            "Exposure Start time":T_on,
               "kV Actual":kV,
               "Images":image,
               "Mode":mode,
               "FPS":fps,
               "LeftorRight":LoR,
               }
        df = pd.DataFrame(data)
        pd.DataFrame.to_csv(df,r"D:\\log{}.csv".format(date))
        #print(df)


    except FileNotFoundError:
        return "File not found."

#Read the file


######################################################MAIN############################################################
print ('argument list', sys.argv)
dateval = sys.argv[1]
file_path = sys.argv[2]
print ("Hello \n {} is the date \n File Location : {} \n".format(dateval,file_path))
investigate_file(file_path,dateval)







