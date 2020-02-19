import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gutcli",
    version="0.0.25",
    author="Edgardo Gutierrez Jr",
    author_email="edgardogutierrezjr@gmail.com",
    description="Quick project navigator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gutiere/gutcli",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'gut = gutcli.gut:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
