from setuptools import setup, find_packages
import os

def package_files(directory):
    # Collecte tous les fichiers dans le sous-dossier spécifié
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

# Inclure explicitement les fichiers et sous-dossiers
extra_files = package_files('aa_killstory/templates') + \
              package_files('aa_killstory/static') + \
              package_files('aa_killstory/migrations') + \
              package_files('aa_killstory/management')

setup(
    name='aa-killstory',
    version='0.1.1.1',  # Version mise à jour pour forcer la réinstallation
    packages=find_packages(),
    data_files=[('', extra_files)],  # Inclut tous les fichiers collectés
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
