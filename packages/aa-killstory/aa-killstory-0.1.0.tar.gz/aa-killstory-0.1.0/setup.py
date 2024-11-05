from setuptools import setup, find_packages

setup(
    name='aa-killstory',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='Alliance Auth plugin to display kill stories',
    url='https://github.com/Erkaek/aa-killstory',
    author='Erka Ekanon',
    author_email='erkaekanon@outlook.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    install_requires=[
        'allianceauth>=4',
    ],
)
