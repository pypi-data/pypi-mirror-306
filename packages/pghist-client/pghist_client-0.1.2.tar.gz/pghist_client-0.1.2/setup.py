import codecs
from os.path import (
    dirname,
)
from pathlib import (
    Path,
)

from setuptools import (
    find_packages,
    setup,
)


def read(fn):
    return codecs.open(Path(__file__).resolve().parent / fn).read()


setup(
    name='pghist-client',
    url='https://stash.bars-open.ru/projects/M3/repos/pghist-client',
    version='0.1.2',
    description='Клиент для взаимодействия с сервисом логирования действий пользователя (PGHist).',
    author='BARS Group',
    author_email='bars@bars.group',
    license='MIT',
    keywords='django pghist client',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('dev_project', 'dev_project.*',)),
    install_requires=read('requirements.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    set_build_info=dirname(__file__),
)
