from setuptools import setup, find_packages

setup(
    name='corerec',
    version='0.2.6',
    description='A Framework to built custom recommendation envornments.',
    author='Vishesh Yadav',
    author_email='sciencely98@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'networkx',
        'scikit_learn',
        # 'torch',
        'tqdm',
        'memory_profiler',
        'pandas',
        'torch_geometric',
        'dask',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)