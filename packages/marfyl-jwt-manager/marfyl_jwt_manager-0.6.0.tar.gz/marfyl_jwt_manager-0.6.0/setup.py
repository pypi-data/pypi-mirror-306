from setuptools import setup, find_packages

setup(
    name='marfyl_jwt_manager',
    version='0.6.0',
    description='A service to process jwt from headers',
    author='Eduardo Ponce',
    author_email='poncejones@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyJWT',
        'cryptography',
        'fastapi',
        'starlette'
    ],
    python_requires='>=3.9',
)