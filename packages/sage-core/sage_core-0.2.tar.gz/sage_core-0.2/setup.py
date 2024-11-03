from setuptools import setup, find_packages
import os

# Чтение содержимого README.md и CHANGELOG.md для long_description
def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

setup(
    name='sage-core',
    version='0.2',
    description='Ядро системы плагинов для разработки расширяемых приложений.',
    long_description=read_file('README.md') + '\n\n' + read_file('CHANGELOG.md'),
    long_description_content_type='text/markdown',
    author='AGStudios',
    author_email='amckinatorgames@gmail.com',
    url='https://github.com/yourusername/sage-core',  # Замените на ваш URL репозитория
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
