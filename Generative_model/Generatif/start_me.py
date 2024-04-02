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

    # LISTE=glob.glob('../INFERENCE_DATA/Amplitude/first/'+type_+'/*.pkl')
    # DOSSIER=[]
    # for ff in LISTE :
    #     if not os.path.exists('../DONNE/'+type_+'/'+'Sequence_first_'+ff.split('/')[-1]):
    #         print('../DONNE/'+type_+'/'+ff.split('/')[-1].split('#n')[0]+'/Sequence_first_'+ff.split('/')[-1])
    #         DOSSIER.append(ff)
    DOSSIER = glob.glob('../INFERENCE_DATA/' + state + '/' + ac
                        + '/*.pkl')
    Dossier = DOSSIER
    # Dossier = []
    # for ff in DOSSIER:
    #     #     # print((ff.split('/')[-1]).split('.pkl'))
    #     if not os.path.exists('../FIGURE/fig_new/' + ac + '/' + (ff.split('/')[-1]).split('#n#n')[0] + '/' + state + '_Probability_' + ff.split('/')[-1].split('#n#n')[0] + '.pdf'):
    #         Dossier.append(ff)
    # #         print(ff)
    # # print('../FIGURE/fig_new/'+type_+'/'+(ff.split('/')[-1]).split('#n#n')[0]+'/'+style+'_Probability_'+ff.split('/')[-1].split('#n#n')[0]+'.pdf')
    # print(len(Dossier))

    # procdossier = subprocess.Popen(['find  ../INFERENCE_DATA/ -name *.pkl'], stdout=subprocess.PIPE, shell=True)
    # (dossier, err) = procdossier.communicate()
    # dossier=str(dossier)
    # print(DOSSIER)
    # DOSSIER=dossier.split('\\n')
    # DOSSIER=DOSSIER[0:-1]
    # DOSSIER[0]=DOSSIER[0][2:]

    # print(len(Dossier))

    # Dossier=['../INFERENCE_DATA/small/t5/FCF_w1118_1500005@UAS_TNT_2_0003p_8_45s1x30s0s#p_8_105s10x2s10s#s_020per_0s1x227s0s#n@100.pkl']
    id = 0

    with open(args_file, 'w') as file_object:
        for files in Dossier:
            id += 1
            args_string = '-n=%s --id=%i -s=%s -a=%s \n' % (
                files, id, state, ac)
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
    cmd_str = 'sbatch --array=1-%i %s' % (jobs_count, script_name)
    os.system(cmd_str)
