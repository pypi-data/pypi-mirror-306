from setuptools import setup, find_packages

setup(
    name='nerdron',
    version='0.3.2',  # Version of your package
    description='A simple and flexible neural network package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Muhammad Ramzy',
    author_email='mhdramzy777@gmail.com',
    url='https://github.com/MuhammadRamzy/nerdron',
    packages=find_packages(),  # Automatically finds all packages in the nerdron directory
    install_requires=[          # External dependencies
        'numpy>=1.19.2',        # Make sure to specify your dependencies
    ],
    test_suite='tests',         # Test suite location
    classifiers=[               # Classification metadata
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',    # Specify the required Python version
)
