from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name = 'socho',
	packages = ['socho'],
	version = '1.3.3',
	description = 'Social choice functions and CLI tool',
	install_requires = ['numpy', 'pandas'],
	long_description = long_description,
    long_description_content_type = "text/markdown",
	author = 'Luke Harold Miles, Bernardo Trevizan',
	author_email = 'lukem@sent.com, trevizanbernardo@gmail.com',
	url = 'https://github.com/qpwo/socho',
	entry_points = {
        'console_scripts': ['socho=socho.cli:main'],
    },
)
