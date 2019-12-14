from setuptools import setup, find_packages


setup(
    name='guess-the-capital',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['guess_the_capital'],
    install_requires=[
        'pyqt5-tools', 'requests'
    ],
)
