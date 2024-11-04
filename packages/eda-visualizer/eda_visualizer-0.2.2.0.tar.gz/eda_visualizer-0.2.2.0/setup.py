from setuptools import setup, find_packages

setup(
    name='eda_visualizer',
    version='0.2.2.0',
    description='A Python library for automatic univariate analysis using Pandas and Matplotlib',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rohan',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
