from setuptools import setup, find_packages

setup(
    name='ProteomeDataPrep',
    version='0.2.3',
    author='Lillian Tatka',
    description="""A package for loading and preprocessing peptide and protein \
        abundance data from mass spectrometry.""",
    packages=find_packages(), 
    install_requires=[
        'numpy',  
        'pandas',
        'boto3',
        'fsspec',
        's3fs',
        'dataclasses'
        
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,  
    package_data={"proteome_data_prep": ["data/*"]}
)
