from setuptools import setup, find_packages

setup(
    name='pgmenus',
    version='0.0.1',
    author='Chris',
    description='Make menus with Buttons and Labels inside Pygame easily!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/christianlde/pgmenus',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package dependencies here
        'pygame',  
    ],
)