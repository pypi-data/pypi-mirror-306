import os

def initCADNA():
    
    import subprocess
    import platform

    opt_system = platform.system()
    curr_loc = os.path.dirname(os.path.realpath(__file__))


    if not os.path.isfile('a.out'):
        if opt_system == 'Linux':
            os.chdir(curr_loc+r'/cadna')
            subprocess.call('pwd', shell=True)
            subprocess.call('bash run_linux.sh', shell=True)
        elif opt_system == 'Windows':
            os.chdir(curr_loc+r'/cadna')
            subprocess.call('pwd', shell=True)
            subprocess.call('bash run_mac.sh', shell=True)
        elif opt_system == 'posix' or opt_system == 'Darwin':
            os.chdir(curr_loc+r'/cadna')
            subprocess.call('pwd', shell=True)
            subprocess.call('bash run_win.sh', shell=True)

    return 1