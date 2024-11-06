from setuptools import setup, find_packages

setup(
    name="rsr45-sudoku_solver",
    version="0.1.1",
    author="Raunaq Rai",
    author_email="rsr45@cam.ac.uk",
    description="A command-line Sudoku solver using a backtracking algorithm.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raunaq-rai/Sudoku-Solver-RR.git", 
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "rsr45-sudoku-solver=sudoku_solver.solver:main",
        ],
    },
)
