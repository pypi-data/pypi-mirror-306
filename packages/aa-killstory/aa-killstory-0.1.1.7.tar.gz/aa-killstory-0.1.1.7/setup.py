from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

extra_files = package_files('killstory/templates') + \
              package_files('killstory/static') + \
              package_files('killstory/migrations') + \
              package_files('killstory/management/commands')

setup(
    name='aa-killstory',
    version='0.1.1.7',  # Incrémentez le numéro de version
    packages=find_packages(),
    include_package_data=True,
    data_files=[('', extra_files)],  # Utilisation de data_files pour inclure management
    license='MIT License',
    description='A plugin for Alliance Auth to manage kill stories.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Erkaek/aa-killstory',
    author='Erkaek',
    author_email='erkaekanon@outlook.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'django>=3.2',
        'requests',
    ],
)
