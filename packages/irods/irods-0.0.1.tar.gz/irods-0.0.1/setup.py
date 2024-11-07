from setuptools import setup
import codecs

# get description
with codecs.open("README.md", "r", "utf-8") as file:
    long_description = file.read()

# setup
setup(
    name="irods",
    version="0.0.1",
    description="Metapackage for irods",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="iRODS Consortium",
    author_email="support@irods.org",
    install_requires=["python-irodsclient"],
    license="BSD",
    url="https://github.com/irods/irods_python_metapackage",
    keywords="irods",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
