from setuptools import setup
import sys
from os.path import dirname, realpath


def read_requirements_file(filename):
    req_file_path = '%s/%s' % (dirname(realpath(__file__)), filename)
    with open(req_file_path) as f:
        return [line.strip() for line in f]


if sys.version_info < (3, 7):
    print('Sorry, Python < 3.7 is not supported, please install Python 3.5.2')
    sys.exit()

setup(name='interval-action-spaces',
      version='0.0.1',
      packages=['interval_spaces'],
      python_requires='>=3.7',
      install_requires=read_requirements_file('requirements.txt'),
      description='Extensions to OpenAI Gym for action spaces in form of intervals.',
      url='https://github.com/InES-MAS-Research/discontinuous-action-space',
      )
