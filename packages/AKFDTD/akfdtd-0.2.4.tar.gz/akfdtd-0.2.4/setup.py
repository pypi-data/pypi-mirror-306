from setuptools import setup, find_packages
from Cython.Build import cythonize


setup(
    name='AKFDTD',
    version='0.2.4',
    author="Alexander V. Korovin",
    author_email="a.v.korovin73@gmail.com",
    url='http://avkor.epizy.com',  # Homepage URL

    # packages=find_packages(),

    # ext_modules=cythonize("FDTD/*.py"),  # Adjust for your files
    # packages=find_packages(include=["tests"]),

    packages=find_packages(include=["FDTD", "tests"]),

    # packages=['FDTD'],

    package_dir={
    'FDTD': './FDTD',
    },  # Optional: specify the root directory of your package
    include_package_data=True,  # Include files specified in MANIFEST.in
    package_data={
        "": ["tests/*.py", "images/*.png", "images/*.jpg"],  # Include all test files and image files
    },

    install_requires=[
        'cupy',
        'numpy',
        'matplotlib',
        ],  # Add any dependencies here
    zip_safe=False,  # This allows the package to be installed as an egg
    description='Finite difference time domain simulation (for slit diffraction)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',  # License type
)
