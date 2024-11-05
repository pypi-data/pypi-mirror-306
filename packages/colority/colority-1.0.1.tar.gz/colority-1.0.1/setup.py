from setuptools import setup, find_packages

setup(
    name='colority',
    version='1.0.1',
    author='gagzui',
    description='Wonderful colorizer for text in terminal.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data = True,
    python_requires='>=3.6'
)