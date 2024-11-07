from setuptools import setup, find_packages

setup(
	name = 'sputchedtools',
	version = '0.17.0',
	packages = find_packages(),
	py_modules = ['sputchedtools'],
	install_requires = [
		'aiohttp>=3.10.10',
		'aiofile>=3.9.0',
		# uvloop/winloop
	],
	author = 'Sputchik',
	author_email = 'sputchik@gmail.com',
	url = 'https://github.com/Sputchik/sputchedtools',
	python_requires = '>=3.8'
)