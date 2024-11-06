
from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='FinamPy',
  version='0.0.2',
  author='vpresweb',
  author_email='vpresweb@gmail.com',
  description='This is the simplest module for trading.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://cpravo.ru',
  packages=find_packages(),
  install_requires=['requests', 'pytz', 'grpcio>=1.63.0', 'protobuf>=5.26.0', 'types-protobuf', 'googleapis-common-protos'],
  classifiers=[
    ''
  ],
  keywords='auto trading ',
  project_urls={
    'GitHub': 'https://github.com/vpresweb'
  },
  python_requires='>=3.9.20'
)