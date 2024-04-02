# This function creates the argument list and launches job managers

import numpy
import glob
import re
import argparse

import os    # for file operations
import socket   # for netowrk hostname
import numpy
import argparse  # for command-line arguments
import subprocess   # for launching detached processes on a local PC
import sys      # to set exit codes
# Constants
from constants import *


# Define arguments
arg_parser = argparse.ArgumentParser(
    description='Job manager. You must choose whether to resume simulations or restart and regenerate the arguments file')
arg_parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + str(version))
mode_group = arg_parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument('--restart', action='store_true')
mode_group.add_argument('--resume', action='store_true')
arg_parser.add_argument('--ac', action='store', type=str)
arg_parser.add_argument('--state', action='store', type=str)


# Identify the system where the code is running
hostname = socket.gethostname()
if hostname.startswith('tars-submit'):
    script_name = 'sbatch_tars.sh'
    jobs_count = jobs_count_tars
elif hostname == 'patmos':
    script_name = 'sbatch_t_bayes.sh'
    jobs_count = jobs_count_t_bayes
elif hostname == 'onsager-dbc':
    script_name = 'job_manager.py'
    jobs_count = jobs_count_onsager
elif hostname == "thales.dbc.pasteur.fr":
    script_name = 'job_manager.py'
    jobs_count = jobs_count_chloe
else:
    print('Unidentified hostname "' + hostname +
          '". Unable to choose the right code version to launch. Aborting.')
    exit()


# Analyze if need to restart or resume
input_args = arg_parser.parse_args()
bl_restart = input_args.restart
state = input_args.state
ac = input_args.ac

# If restart is required, regenerate all files
if bl_restart:
    print("Creating arguments list...")

    # Clear the arguments file
    try:
        os.remove(args_file)
    except:
        pass

    # Clean the logs and output folders
    for folder in ([logs_folder]):
        if os.path.isdir(folder):
            print("Cleaning up the folder: '" + folder + "'.")
            cmd = "rm -rfv " + folder
            try:
                os.system(cmd)
            except Exception as e:
                print(e)

        # Recreate the folder
        try:
            os.makedirs(folder)
        except Exception as e:
            print(e)

    # Clean slurm files in the root folder
    cmd = "rm -fv ./slurm-*"
    try:
        os.system(cmd)
    except Exception as e:
        print(e)

 #   procdossier = subprocess.Popen(['ls -d ../INITIALIZATION_DATA/*'], stdout=subprocess.PIPE, shell=True)
 #   (dossier, err) = procdossier.communicate()
 #   dossier=str(dossier)
    # print(dossier)
  #  DOSSIER=dossier.split('\\n')
 #   DOSSIER=DOSSIER[0:-1]
#    print(len(DOSSIER))
    LISTE = glob.glob('../INITIALIZATION_DATA/' + state
                      + '/' + ac + '/' + '*.pkl')

    #Dossier = LISTE
    # print(LISTE)
    Dossier = []
    for ff in LISTE:
        print(ff)
        if not os.path.exists('../INFERENCE_DATA/' + state + '/' + ac + '/t15_5s/' + ff.split('/')[-1]):
            Dossier.append(ff)

    # for doss in LISTE :
    #     Dossier.append('../INITIALIZATION_DATA_TEST/'+style+'/'+type_+'/'+doss.split("/")[-1])

    # Dossier=['../INITIALIZATION_DATA_TEST/Amplitude/'+type+'/GMR_16E11_AE_01@UAS_Chrimson_Venus_X_0070r_LED100_30s2x15s30s#n#n#n@100.pkl']
    print(Dossier)
    id = 0
    with open(args_file, 'w') as file_object:
        for files in Dossier:
            # print('../INFERENCE_DATA/t5/'+files_.split('/')[-1])
            # if not os.path.exists('../INFERENCE_DATA/t5/'+files.split('/')[-1]):
            id += 1
            args_string = '-n=%s --id=%i -s=%s -a=%s\n' % (
                files, id, state, ac)
            file_object.write(args_string)
            # print('../INFERENCE_DATA/t5/'+files.split('/')[-1])
            # print(len(Dossier))
            #del Dossier[Dossier.index(files_)]
    # print(len(args_string))

    # with open(args_file, 'w') as file_object:
    #     for files in Dossier:
    #         id += 1
    #         args_string = '-n=%s --id=%i \n' % (files, id)
    #         file_object.write(args_string)
    # print(len(Dossier))

    # Create lock file
    with open(args_lock, 'w'):
        pass

    print("Argument list created. Launching sbatch...")

    line_count = id
else:
    print("Resuming simulation with the same arguments file")


# Launch job

if script_name == 'job_manager.py':
    cmd_str = 'python3 %s' % (script_name)
    popens = []
    pids = []
    for j in range(1, jobs_count + 1):
        cur_popen = subprocess.Popen(["python3", script_name])
        popens.append(cur_popen)
        pids.append(cur_popen.pid)
    print("Launched %i local job managers" % (jobs_count))
    print("PIDs: ")
    print(pids)

    # Collect exit codes
    for j in range(jobs_count):
        popens[j].wait()
    print("All job managers finished successfully")

else:
    # -o /dev/null
    cmd_str = 'sbatch --array=1-%i %s' % (jobs_count, script_name)
    os.system(cmd_str)
