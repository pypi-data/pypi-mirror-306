from setuptools import setup, find_packages

setup(
    name="dharmamitra-sanskrit-grammar",
    version="0.1.3",
    packages=find_packages(include=['dharmamitra_sanskrit_grammar', 'dharmamitra_sanskrit_grammar.*']),    
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
)