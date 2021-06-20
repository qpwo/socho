from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
	name = 'socho',
	packages = ['socho'],
	version = '1.3.3',
	description = 'Social choice functions and CLI tool',
	install_requires = required,
	long_description = long_description,
    long_description_content_type = "text/markdown",
	author = 'Luke Harold Miles, Bernardo Trevizan',
	author_email = 'lukem@sent.com, trevizanbernardo@gmail.com',
	url = 'https://github.com/qpwo/socho',
	entry_points = {
        'console_scripts': ['socho=socho.cli:main'],
    },
)
