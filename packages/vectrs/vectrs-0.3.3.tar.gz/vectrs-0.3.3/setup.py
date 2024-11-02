from setuptools import setup, find_namespace_packages

setup(
    name="vectrs",
    version="0.3.3",
    packages=find_namespace_packages(include=['vectrs*']),
    install_requires=[
        "numpy",
        "kademlia",
        "networkx",
        "anthropic",
        "sentence_transformers",
        "hnswlib",  
        "scipy",    
    ],
    author="Mir Sakib",
    author_email="sakib@paralex.tech",
    description="Decentralized & Distributed Vector Database",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ParalexLabs/Vectrs-beta",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
