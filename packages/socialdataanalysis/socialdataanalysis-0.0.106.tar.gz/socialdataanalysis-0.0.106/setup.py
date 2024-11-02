from setuptools import setup, find_packages

#import glob

# Listando todos os arquivos .ipynb na pasta notebooks
#notebooks_files = glob.glob('notebooks/*.ipynb')

setup(
    name='socialdataanalysis',
    version='0.0.106',
    packages=find_packages(),
    #include_package_data=True,
    #package_data={
    #    'socialdataanalysis': ['notebooks/*.ipynb'],
    #},
    #data_files=[
    #    ('share/socialdataanalysis', notebooks_files),
    #],
    install_requires=[
        'altair',
        #'matplotlib', # estava dando problema na reinstalação
        'factor-analyzer',
        'ipython',
        'itertools',
        #'tempfile', # é um módulo da biblioteca padrão do Python e não deve ser listado como uma dependência instalável 
        #'os', # é um módulo da biblioteca padrão do Python e não deve ser listado como uma dependência instalável 
        'pandas',
        'prince',
        'pyreadstat',
        'pingouin',
        'plotly',
        'networkx',
        'numpy',
        'requests',
        'statsmodels',
        'scipy',
        'sklearn',
        'seaborn',
        'sympy',
        'tabulate',
        'warnings', 

    ],
    author='Ricardo Mergulhão, Maria Helena Pestana, Maria de Fátima Pina',
    author_email='ricardomergulhao@gmail.com, gageiropestana@gmail.com, mariafatimadpina@gmail.com',
    description='Funções personalizadas para análise de dados nas ciências sociais.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rcmergulhao/socialdataanalysis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
