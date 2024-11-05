from setuptools import setup, find_packages

setup(
    name='PyCodeCommenter',  
    version='0.0.5', 
    package_dir={'': 'src'},  
    packages=find_packages(where='src'),  
    install_requires=[  
        
    ],
    author='NABASA AMOS',
    author_email='amosnabasa256@gmail.com',
    description='A Python library for generating Google-style docstrings.',
    long_description=open('C:\\Users\\DSN\\Desktop\\Library\\code\\PyCodeCommenter\\README.md').read(),  # Path to your README file (ensure this is relative)
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

