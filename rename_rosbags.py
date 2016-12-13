#!/usr/bin/env python
import os
import glob
import re
import subprocess, shlex

folder = "/mnt/synology/STORAGE/radio_dataset/final/test_copy/"

def start():
    global folder
    
    a = glob.glob(folder + "*.bag")
    a.sort()

    found = []

    name_id_file = open(folder + "names_to_ids.txt", "w")

    for i in a:
        s = re.search('_ru(.*)_cg', i)
        s = s.group(1)
        if s not in found:
            found.append(s)
            name_id_file.write("Name: " + s + " ID: " + str(len(found)) + "\n")

    name_id_file.close()


    for i in a:
        f = i
        for j in found:
            if j in f:
                id = found.index(j)
                if id < 10:
                    id = "0" + str(id)
                print j
                print id
                print f
                f = f.replace(str(j), str(id))
                print f
        os.rename(i,f)
    

    
    a = glob.glob(folder + "*.bag")
    a.sort()

    for i in a:
        # Only laser scans and depth
        new_name = i[:-4] + "_laser_depth.bag"
        #command = "ls -l " + i
        command = "rosbag filter " + i + " " +  new_name + " \"topic == '/scan' or topic == '/camera/depth/image_raw'\""
        command = shlex.split(command)
        p = subprocess.Popen(command)
        out, err = p.communicate()
        new_name = i[:-4] + "_mic.bag"
        # Only microphone data (audio) and doa
        command = "rosbag filter " + i + " " +  new_name + " \"topic == '/audio' or topic == '/acoustic_magic_doa/data_raw'\""
        command = shlex.split(command)
        p = subprocess.Popen(command)
        out, err = p.communicate()


    a = glob.glob(folder + "*.bag")
    a.sort()

    if not os.path.exists(folder+"scenario1A_"):
        os.makedirs(folder+"scenario1A_")
    if not os.path.exists(folder+"scenario1B_"):
        os.makedirs(folder+"scenario1B_")
    if not os.path.exists(folder+"scenario2_"):
        os.makedirs(folder+"scenario2_")
    if not os.path.exists(folder+"scenario3A_"):
        os.makedirs(folder+"scenario3A_")
    if not os.path.exists(folder+"scenario3B_"):
        os.makedirs(folder+"scenario3B_")
    if not os.path.exists(folder+"scenario4_"):
        os.makedirs(folder+"scenario4_")

    if not os.path.exists(folder+"scenario1A_/scenario1A"):
        os.makedirs(folder+"scenario1A_/scenario1A")
    if not os.path.exists(folder+"scenario1B_/scenario1B"):
        os.makedirs(folder+"scenario1B_/scenario1B")
    if not os.path.exists(folder+"scenario2_/scenario2"):
        os.makedirs(folder+"scenario2_/scenario2")
    if not os.path.exists(folder+"scenario3A_/scenario3A"):
        os.makedirs(folder+"scenario3A_/scenario3A")
    if not os.path.exists(folder+"scenario3B_/scenario3B"):
        os.makedirs(folder+"scenario3B_/scenario3B")
    if not os.path.exists(folder+"scenario4_/scenario4"):
        os.makedirs(folder+"scenario4_/scenario4")

    if not os.path.exists(folder+"scenario1A_/scenario1A_mic"):
        os.makedirs(folder+"scenario1A_/scenario1A_mic")
    if not os.path.exists(folder+"scenario1B_/scenario1B_mic"):
        os.makedirs(folder+"scenario1B_/scenario1B_mic")
    if not os.path.exists(folder+"scenario2_/scenario2_mic"):
        os.makedirs(folder+"scenario2_/scenario2_mic")
    if not os.path.exists(folder+"scenario3A_/scenario3A_mic"):
        os.makedirs(folder+"scenario3A_/scenario3A_mic")
    if not os.path.exists(folder+"scenario3B_/scenario3B_mic"):
        os.makedirs(folder+"scenario3B_/scenario3B_mic")
    if not os.path.exists(folder+"scenario4_/scenario4_mic"):
        os.makedirs(folder+"scenario4_/scenario4_mic")

    if not os.path.exists(folder+"scenario1A_/scenario1A_laser_depth"):
        os.makedirs(folder+"scenario1A_/scenario1A_laser_depth")
    if not os.path.exists(folder+"scenario1B_/scenario1B_laser_depth"):
        os.makedirs(folder+"scenario1B_/scenario1B_laser_depth")
    if not os.path.exists(folder+"scenario2_/scenario2_laser_depth"):
        os.makedirs(folder+"scenario2_/scenario2_laser_depth")
    if not os.path.exists(folder+"scenario3A_/scenario3A_laser_depth"):
        os.makedirs(folder+"scenario3A_/scenario3A_laser_depth")
    if not os.path.exists(folder+"scenario3B_/scenario3B_laser_depth"):
        os.makedirs(folder+"scenario3B_/scenario3B_laser_depth")
    if not os.path.exists(folder+"scenario4_/scenario4_laser_depth"):
        os.makedirs(folder+"scenario4_/scenario4_laser_depth")

    for i in a:
        s = re.search('_sc(.*)_ru', i)
        s = s.group(1)
        i = i.rsplit('/', 1)[-1]
        if s == "1A":
            os.rename(folder+i, folder+"scenario1A_/"+i)
        elif s == "1B":
            os.rename(folder+i, folder+"scenario1B_/"+i)
        elif s == "2":
            os.rename(folder+i, folder+"scenario2_/"+i)
        elif s == "3A":
            os.rename(folder+i, folder+"scenario3A_/"+i)
        elif s == "3B":
            os.rename(folder+i, folder+"scenario3B_/"+i)
        elif s == "4":
            os.rename(folder+i, folder+"scenario4_/"+i)

    scenarioFolders("scenario1A_/")
    scenarioFolders("scenario1B_/")
    scenarioFolders("scenario2_/")
    scenarioFolders("scenario3A_/")
    scenarioFolders("scenario3B_/")
    scenarioFolders("scenario4_/")

    tarFolders()


def scenarioFolders(subf):
    global folder
    folder_ = folder + subf
    a = glob.glob(folder_ + "*.bag")
    a.sort()

    for i in a:
        i = i.rsplit('/', 1)[-1]
        new_folder = ""
        if '_mic.bag' in i:
            new_folder = subf[:-2] + "_mic/"
        elif 'laser_depth.bag' in i:
            new_folder = subf[:-2] + "_laser_depth/"
        else:
            new_folder = subf[:-2] + "/"
        os.rename(folder_ + i, folder_+new_folder+i)

def tarFolders():
    global folder
    a = glob.glob(folder+"*_")
    for i in a:
        i = i.rsplit('/', 1)[-1]
        b = glob.glob(folder+i+"/*")
        for j in b:
            if os.path.isdir(j):
                j = j.rsplit('/', 1)[-1]
                command = "tar -zvcf " + folder + i + "/" + j + ".tar.gz " + folder + i + "/" + j
                command = shlex.split(command)
                p = subprocess.Popen(command)
                out, err = p.communicate()


if __name__ == '__main__':
    start() 

