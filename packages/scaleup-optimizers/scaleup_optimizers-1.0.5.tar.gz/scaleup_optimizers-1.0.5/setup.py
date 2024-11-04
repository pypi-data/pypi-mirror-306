from setuptools import find_packages, setup

setup(
    name='scaleup-optimizers',
    packages=find_packages(),
    version='1.0.5',
    description='This library is use to optimize hyperparameter of machine learning with scale up algorithm',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.bird-initiative-dev.com/bird-initiative/scaleup-optimizer',
    author='Bird Initiative',
    author_email='develop@bird-initiative.com',
    install_requires=['numpy>=1.21.0', 'scipy>=1.10.0', 'scikit-optimize>=0.8.1', 'matplotlib>=3.4.0'],
    python_requires='>=3.6',
    keywords='machine learning, hyperparameter optimization, scale up algorithm',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    include_package_data=True,
    package_data={
        '': ['images/*.png'], 
    },
)