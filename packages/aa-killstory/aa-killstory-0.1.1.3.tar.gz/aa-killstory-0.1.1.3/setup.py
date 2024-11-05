from setuptools import setup, find_packages

setup(
    name='aa-killstory',
    version='0.1.1.3',  # Mettez à jour le numéro de version
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'killstory': [
            'templates/**/*',
            'static/**/*',
            'migrations/**/*',
            'management/**/*',
        ],
    },
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
