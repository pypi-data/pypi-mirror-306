from setuptools import find_packages, setup

setup(
    name="fraudaverse",
    packages=find_packages(include=["fraudaverse"]),
    version="0.0.3",
    description="Python lib to access FraudAverse analytical capabilities",
    author="FraudAverse GmbH",
    install_requires=["pyarrow==15.0.0"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
