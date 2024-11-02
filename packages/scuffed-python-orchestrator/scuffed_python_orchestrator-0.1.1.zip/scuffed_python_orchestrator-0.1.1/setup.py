from setuptools import find_packages, setup


setup(
    name="scuffed_python_orchestrator",
    version="0.1.1",
    author="Michael Howard",
    author_email="",
    description="A semi-reliable orchestrator",
    packages=find_packages(),
    package_data={'scuffed_python_orchestrator': ['data/*']}, 
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
        ], 
    install_requires=[],
    python_requires=">=3.9"
)

