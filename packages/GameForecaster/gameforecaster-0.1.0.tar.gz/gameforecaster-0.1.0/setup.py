from setuptools import setup, find_packages

setup(
    name='GameForecaster',
    version='0.1.0',
    description='A library to predict the success of video games based on various features.',
    author='si aziz bahloul ',
    author_email='azizbahloul3@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'joblib'
    ],
)
