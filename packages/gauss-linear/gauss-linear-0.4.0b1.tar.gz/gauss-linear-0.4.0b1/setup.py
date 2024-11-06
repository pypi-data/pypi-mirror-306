from setuptools import setup, find_packages

setup(
    name='gauss-linear', 
    version='0.4.0b1', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gauss=gauss.gauss:main', 
        ],
    },
    install_requires=['sympy>=1.10'],  
    author='Rishi Rao',
    author_email='rao068048@gmail.com',
    description='A simple command line tool to do linear algebra',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/22raor/gauss', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', 
)
