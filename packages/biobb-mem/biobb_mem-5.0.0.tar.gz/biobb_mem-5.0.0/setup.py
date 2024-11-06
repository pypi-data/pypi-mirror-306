import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_mem",
    version="5.0.0",
    author="Biobb developers",
    author_email="ruben.chaves@irbbarcelona.org",
    description="Biobb_mem is a complete code template to promote and facilitate the creation of new Biobbs by the community.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_mem",
    project_urls={
        "Documentation": "http://biobb-mem.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['adapters', 'docs', 'test']),
    package_data={'biobb_mem': ['py.typed']},
    install_requires=['biobb_common==5.0.0'],
    python_requires='>=3.9',
    entry_points={
        "console_scripts": [
            "chap_run = biobb_mem.chap.chap_run:main",
            "cpptraj_density = biobb_mem.ambertools.cpptraj_density:main",
            "assign_leaflets = biobb_mem.lipyphilicBB.assign_leaflets:main",
        ]
    },
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix"
    ),
)
