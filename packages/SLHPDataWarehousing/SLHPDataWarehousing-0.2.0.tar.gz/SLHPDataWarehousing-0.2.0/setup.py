from setuptools import setup, find_packages

setup(
    name="SLHPDataWarehousing",            # Your package name
    version="0.2.0",              # Initial version
    description="This package is used by the SLHP Data Warehousing Team for their day to day work",  # Description of the package
    long_description=open("README.md").read(),  # Read from README.md
    long_description_content_type="text/markdown",  # Optional, specifies markdown format
    author="Ben Fuqua",          # Author's name
    author_email="fuquac@slhs.org",  # Author's email
    packages=find_packages(),    # Automatically find all packages in the directory
    classifiers=[                # Classifiers to categorize the package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[           # List any dependencies
                        "numpy",
                        "Flask",
                        "SQLAlchemy",
                        "WTForms",
                        "flask-wtf",
                        "wtforms_sqlalchemy",
                        "flask_sqlalchemy",
                        "databricks-sql-connector[sqlalchemy]",
                        "pyodbc"                    # Example dependency
    ],
    python_requires=">=3.9",     # Minimum Python version
)
