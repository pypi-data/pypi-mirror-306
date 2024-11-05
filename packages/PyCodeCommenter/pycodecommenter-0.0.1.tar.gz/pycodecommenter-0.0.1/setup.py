from setuptools import setup, find_packages

setup(
    name='PyCodeCommenter',  
    version='0.0.1', 
    packages=find_packages(),
    install_requires=[  
        'ast' 
    ],
    author='NABASA AMOS',
    author_email='amosnabasa256@gmail.com',
    description='A Python library for generating Google-style docstrings.',
    long_description=open('C:\\Users\\DSN\\Desktop\\Library\\code\\PyCodeCommenter\\README.md').read(),  # Path to your README file
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/yourproject',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
