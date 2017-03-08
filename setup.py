from setuptools import setup, find_packages
import modisSuite
setup(
    name='modisSuite',
    version='0.9.5',
    description='Python module to download modis data',
    url='https://github.com/Gabriel-Desharnais/Modis-python-suite',
    author='Gabriel Desharnais',
    author_email='gabriel.desharnais@hotmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        
        'License :: OSI Approved :: MIT License',
        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
        ],
    keywords='modis NSIDC USGS downloader bulk',
    packages=find_packages(),
    
    install_requires=['requests'],
    
    
    )
