# 프로젝트 패키지화 코드
from setuptools import setup, find_packages

setup(
    name='baille_program_pkg',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python==4.9.0.80'
        'path==16.10.0',
        'GTTs==2.5.1',
        'playsound==1.2.2',
    ]
)