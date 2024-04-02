# This function creates the argument list and launches job managers

import argparse  # for command-line arguments
import glob
import os  # for file operations
import re
import socket  # for netowrk hostname
import subprocess  # for launching detached processes on a local PC
import sys  # to set exit codes
from os import path
import numpy
import pandas

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
    print('Unidentified hostname "' + hostname
          + '". Unable to choose the right code version to launch. Aborting.')
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

    path_ = r'/pasteur/projets/policy02/Larva-Screen/screens/' + \
        ac + '/'
    # print(pat
    dirs = [f for f in [i for i in list(os.listdir(
        path_)) if '.mat' not in i] if path.isdir(path_ + f)]
    # dirs = list(os.listdir(path))
    # DOSSIER = ['JRC_SS04197@UAS_Chrimson_Venus_X_0070',
    #   'JRC_SS04599@UAS_Chrimson_Venus_X_0070']
    # dirs = ['MZZ_R_']
    DOSSIER = []
    #
    # #DOSSIER=['../INFERENCE_DATA/Amplitude/'+type_+'/JRC_SS04533@UAS_Chrimson_Venus_X_0070r_LED100_30s2x15s30s#n#n#n@100.pkl','../INFERENCE_DATA/Amplitude/'+type_+'/GMR_SS01942@UAS_Chrimson_Venus_X_0070r_LED100_30s2x15s30s#n#n#n@100.pkl']
    for ff in dirs:
        # if '.mat' not in ff:
        #    if "MZZ_R_3013849" in ff:
        # if 'MZZ_R_3013849@UAS_Chrimson_Venus_X_0070' in ff or 'GMR_72F11_AE_01@UAS_Chrimson_Venus_X_0070' in ff:
        DOSSIER.append(ff)
    #     if 'MZZ_R_3013849@UAS_TNT_2_0003' in ff:

    #     #print('../GENERATIF_DATA/hihi/Generatif'+ff.split('/')[-1])
    #     #print('../GENERATIF_DATA/'+ff.split('/')[-1])
    #     ffo=(ff.split('/')[-1]).split('#n#n#n')[0]
    #     print(ffo)
    #         print('../FIGURE/fig_new/t15/'+ffo+'r_LED100_30s2x15s30s')
    #     else :
    #         DOSSIER.append(ff)
    # dirs = list(os.walk(path))[0][1:-1][0]
    # print(dirs)

    print(len(DOSSIER))
    id = 0
    # (len(FILES))

    with open(args_file, 'w') as file_object:
        for dir in DOSSIER:
            id += 1
            args_string = '-n=%s --id=%i -s=%s -a=%s \n' % (dir, id, state, ac)
            file_object.write(args_string)

    # Create lock file
    with open(args_lock, 'w'):
        pass

    print("Argument list created. Launching sbatch...")

    line_count = id
else:
    print("Resuming simulation with the same arguments file")


# Launch job managers
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
    # input_args = arg_parser.parse_args()
    # bl_restart = input_args.restart
    # state = input_args.state
    # ac = input_args.ac
    cmd_str = 'sbatch --array=1-%i% %s %s %s' % (
        jobs_count, script_name, state, ac)
    os.system(cmd_str)
