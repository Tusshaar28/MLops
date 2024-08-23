from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
def getreq(filepath : str)->List[str]:
    reqmnt = []
    with open(filepath) as fileobj:
        reqmnt = fileobj.readlines()
        reqmnt = [req.replace("\n","") for req in reqmnt]

        if (HYPEN_E_DOT) in reqmnt:
            reqmnt.remove(HYPEN_E_DOT)

    return  reqmnt
setup(
    name='MLProject',
    version='0.0.1',
    author='Tushar Sharma',
    author_email='tush28103@gmail.com',
    packages=find_packages(),
    install_requires = getreq('requirements.txt')
)