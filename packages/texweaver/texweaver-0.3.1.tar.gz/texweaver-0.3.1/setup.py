from setuptools import setup, find_packages

setup(
    name='texweaver',
    version='0.3.1',
    description='A simple converter from Markdown to LaTeX',
    author='Eric025',
    author_email='erix025@outlook.com',
    url='https://github.com/erix025/texweaver',
    packages=find_packages(),
    package_data={
        'texweaver': ['default.yaml'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'texweaver = texweaver.entrypoint:main',
        ],
    },
    install_requires=[
        'argparse'
    ],
)