from setuptools import setup, find_packages
import pathlib

# Read the contents of your README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='nicegui-react',
    version='0.1.1',
    description='Integrate React components into NiceGUI applications',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Pablo Schaffner',
    author_email='pablo@puntorigen.com',
    url='https://github.com/puntorigen/nicegui-react',
    packages=find_packages(),
    install_requires=[
        'nicegui>=2.3.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
