from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'Flow-related diagrammes'
LONG_DESCRIPTION = 'Flow-related diagrammes, cycles, and assessment tools'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="flowplot", 
        version=VERSION,
        author="Mikhail Smilovic",
        author_email="<smilovic@mail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'hydrological modeling'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ]
)