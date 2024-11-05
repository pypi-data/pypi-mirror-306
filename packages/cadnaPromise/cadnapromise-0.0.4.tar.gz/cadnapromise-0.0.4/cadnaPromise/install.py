import os

def initCADNA():
    
    import subprocess
    import platform


    opt_system = platform.system()
    curr_loc = os.path.dirname(os.path.realpath(__file__))

    install_cadna = True

    if 'CADNA_PATH' in os.environ:    
        import logging
        logging.basicConfig()
        log = logging.getLogger()

        log.warning("It looks like your machine has CADNA installed, are you sure to proceed CADNA installation? ")

        check_point = input("Please answer 'yes' or 'no':")

        if check_point.lower() in {'yes', 'y'}:
            install_cadna = True

        else:
            install_cadna = False

    if install_cadna:
        # must set environmental variables
        if not os.path.isfile('a.out'):
            if opt_system == 'Linux':
                os.chdir(curr_loc+r'/cadna')
                # subprocess.call('pwd', shell=True)
                subprocess.call('bash run_linux.sh', shell=True)
                
            elif opt_system == 'Windows':
                os.chdir(curr_loc+r'/cadna')
                # subprocess.call('pwd', shell=True)
                subprocess.call(
                    './configure CXX=g++ --prefix=`cd` --enable-half-emulation --disable-dependency-tracking', 
                    shell=True
                )
                
                subprocess.call('make install', shell=True)
                
            elif opt_system == 'posix' or opt_system == 'Darwin':
                os.chdir(curr_loc+r'/cadna')
                # subprocess.call('pwd', shell=True)
                subprocess.call('bash run_mac.sh', shell=True)

    return 1
