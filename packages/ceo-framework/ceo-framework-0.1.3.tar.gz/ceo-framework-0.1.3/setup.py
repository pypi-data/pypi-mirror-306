from setuptools import setup

setup(
    name='ceo-framework',
    version='0.1.3',
    description='Conditional Equality Operator Framework for conditional transformations in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Eric D. McCullar',
    author_email='MASAGDT@gmail.com',
    url='https://github.com/MASAGDT/ceo_framework',
    py_modules=['ceo_core', 'conditions', 'transformations', 'utils'],
    install_requires=[
        'numpy',
        'Pillow',
        'joblib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
