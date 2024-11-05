from setuptools import setup, find_packages

setup(
    name="rl_visualizer",
    version="0.1.1",
    author="Bedirhan Sen",
    author_email="bdrhnsen@gmail.com",
    description="A package for visualizing action probabilities, entropy, and rewards in reinforcement learning models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bdrhnsen/rl_visualizer", 
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "gymnasium",
        "gym",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
