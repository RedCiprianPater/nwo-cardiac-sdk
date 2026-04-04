from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nwo-cardiac",
    version="1.0.0",
    author="NWO Capital",
    author_email="ciprian.pater@publicae.org",
    description="Dual-modal cardiac biometrics SDK - WiFi CSI + BLE Wearables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nwocapital/nwo-cardiac-sdk",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Security",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "bleak>=0.19.0",  # BLE support
        "pyserial>=3.5",  # For CSI hardware
        "websockets>=10.0",  # For RuView integration
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.20",
            "black>=22.0",
            "mypy>=0.991",
        ],
        "clinical": [
            "hl7>=0.4",  # HL7 FHIR support
            "pydicom>=2.3",  # DICOM support
        ],
        "robotics": [
            "roslibpy>=1.5",  # ROS integration
        ],
    },
    entry_points={
        "console_scripts": [
            "nwo-cardiac=nwo_cardiac.cli:main",
        ],
    },
)
