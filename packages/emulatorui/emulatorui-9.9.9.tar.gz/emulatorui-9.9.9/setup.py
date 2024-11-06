#!/usr/bin/python

import setuptools

setuptools.setup(
	name="emulatorui",
	version="9.9.9",
	author="Aliz",
	author_email="randomdude@gmail.com",
	packages=['emulatorui'],
	install_requires=[
		'PySDL2~=0.9.9',
		'pysdl2-dll~=2.0.16',
		'PyYAML'
	],
	python_requires='>=3.11',
	entry_points={
		'console_scripts': [
			'emulatorui = emulatorui.main:consoleEntryPoint'
		]
	},
	package_data=
	{
		'emulatorui':
		[
        	'assets/*',
	        'consoles/*'
    	],
	},
)
