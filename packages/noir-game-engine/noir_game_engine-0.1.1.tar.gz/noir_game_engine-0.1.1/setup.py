from setuptools import setup, find_packages

setup(
    name='noir_game_engine',
    version='0.1.1',
    author='Andrew AMur',
    author_email='your_email@example.com',
    description='A simple text adventure game engine for beginners.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AndrewAMur/Noir',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)