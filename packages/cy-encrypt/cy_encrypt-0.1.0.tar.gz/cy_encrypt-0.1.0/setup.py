from setuptools import setup,find_packages

setup(
    name='cy_encrypt',
    version='0.1.0',
    author='Max Cheung',
    author_email='max@maxckm.com',
    description='Convert Python source code to a dynamic link library using Cython',
    packages=find_packages(),
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    install_requires=[
        'Cython',
        'click',
    ],
)
