from setuptools import setup, find_packages

setup(
    name='nicegui-react',
    version='0.1.0',
    description='Integrate React components into NiceGUI applications',
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
