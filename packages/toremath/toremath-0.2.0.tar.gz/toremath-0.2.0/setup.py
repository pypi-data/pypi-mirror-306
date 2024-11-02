from setuptools import setup, find_packages

setup(
    name="toremath",
    version="0.2.0",
    author="Torrez Tsoi",
    author_email="that1.stinkyarmpits@gmail.com",
    description="A clone of the builtin math module",
    license="MIT",
    packages=find_packages(),  # Automatically finds packages in the directory
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=["sympy"],
    extras_require={
        "dev": ["check-manifest", "pytest"],  # Development dependencies
        "docs": ["sphinx", "sphinx_rtd_theme"],  # Documentation dependencies
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Minimum Python version
)
