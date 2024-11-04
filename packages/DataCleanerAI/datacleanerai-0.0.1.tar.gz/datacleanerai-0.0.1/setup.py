from setuptools import setup, find_packages

setup(
    name='DataCleanerAI',
    version='0.0.1',
    description='An interactive, intelligent data-cleaning library with ML-based user adaptation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Harsha Vardhan',
    author_email='harshav.vanukuri@gmail.com',
    url='https://github.com/harshv-v/DataCleanerAI',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'dask',
        'matplotlib',
        'spacy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license="MIT",  # Add this line
    python_requires='>=3.6',
)
