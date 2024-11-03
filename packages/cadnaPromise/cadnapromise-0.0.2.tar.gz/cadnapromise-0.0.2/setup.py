# coding: utf-8

import logging
from setuptools import setup
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError


def readme():
	"""import the readme file"""
	with open('README.rst') as f:
		return f.read()

__version__ = '0.0.2'
ext_errors = (CCompilerError, ModuleNotFoundError, DistutilsExecError, DistutilsPlatformError, IOError, SystemExit)

logging.basicConfig()
log = logging.getLogger(__file__)

setup_args = {'name':'cadnaPromise',
		'version':__version__,
		'description':'Precision auto-tuning of floating-point variables in program',
		'long_description':readme(),
		# packages = setuptools.find_packages(),
		'classifiers':["Intended Audience :: Science/Research",
					"Intended Audience :: Developers",
					"Programming Language :: C",
					"Programming Language :: Python",
					"Topic :: Software Development",
					"Topic :: Scientific/Engineering",
					'Operating System :: Microsoft :: Windows',
					'Operating System :: POSIX',
					'Operating System :: Unix',
					'Operating System :: MacOS',
					"Programming Language :: Python :: 3",
					],
		'keywords':'computer arithmetic mixed-precision, precision auto-tuning',
		'url':'https://github.com/PEQUAN/cadnaPromise',
		'author':'PEQUAN team',
		'author_email':'thibault.hilaire@lip6.fr; fabienne.jezequel@lip6.fr',
		'license':'GNU General Public License v3.0',
		'packages':{"cadnaPromise", "cadnaPromise.cadna", 
					"cadnaPromise.deltadebug",  "cadnaPromise.extra", 
					#  "cadnaPromise.cadna.admin",
					#  "cadnaPromise.cadna.m4",
					#  "cadnaPromise.cadna.srcC",
			    	#  "cadnaPromise.cadna.doc",
					# "cadnaPromise.cadna.examples_half",
					# "cadnaPromise.cadna.examplesC",
					# "cadnaPromise.cadna.examplesC_mpi",
					# "cadnaPromise.cadna.examplesC_omp",
					# "cadnaPromise.cadna.examplesC_mpiomp",
					# "cadnaPromise.cadna.srcC_mpi",
					# "cadnaPromise.cadna.srcFortran",
					# "cadnaPromise.cadna.srcFortran_mpi",
					# "cadnaPromise.cadna.examplesFortran",
					# "cadnaPromise.cadna.examplesFortran_mpi"
					},
		'package_data':{"cadnaPromise": ["deltadebug/*", "cadna/*", "extra/*"
									# "cadna/admin/*",
									# "cadna/doc/*",
									# "cadna/m4/*",
									# "cadna/srcC/*", 
									# "cadna/examples_half/*",
									# "cadna/examplesC/*",
									# "cadna/examplesC_mpi/*",
									# "cadna/examplesC_omp/*",
									# "cadna/examplesC_mpiomp/*",
									# "cadna/srcC_mpi/*",
									# "cadna/srcFortran/*",
									# "cadna/srcFortran_mpi/*",
									# "cadna/examplesFortran/*",
									# "cadna/examplesFortran_mpi/*",
									]},
		'tests_require':['pytest', 'pytest-cov'],
		'setup_requires':['colorlog', 'colorama', 'docopt', 'pyyaml', 'regex'],
		'install_requires':['colorlog', 'colorama', 'docopt', 'pyyaml', 'tqdm', 
						'regex', 'pytest', 'pytest-cov'],
		'extras_require':{'with_doc': ['sphinx', 'sphinx_bootstrap_theme']},
		'include_package_data':True,
		'data_files':[('extra/', ['cadnaPromise/extra/promise.h', 'cadnaPromise/extra/cadnaizer'])],
		'zip_safe':False,
		'entry_points':{'console_scripts': ['runPromise=cadnaPromise.run:runPromise',
										'promise=cadnaPromise.run:runPromise_custom', 
										'activate-promise=cadnaPromise.install:initCADNA']
				}}


try:	
	setup(**setup_args)

except ext_errors as ext_reason:
    log.warning("The installation is not successful, please contact the maintenance team.")
