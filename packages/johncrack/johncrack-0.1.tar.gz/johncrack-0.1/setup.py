from setuptools import setup, find_packages

setup(
    name="johncrack",  # Name of the package
    version="0.1",  # Initial version
    packages=find_packages(),  # Automatically find packages in the current directory
    install_requires=[  # List any dependencies your library needs here (if any)
        "pycryptodome",  # Example dependency (if you're using cryptography)
        "requests",      # Example, if your library makes web requests
    ],
    description="A library for ethical password cracking using John the Ripper",
    long_description=open('README.md').read(),  # Read long description from README file
    long_description_content_type="text/markdown",  # Set the format of long description
    author="Your Name",  # Your name or username
    author_email="your.email@example.com",  # Your contact email
    url="https://github.com/yourusername/johncrack",  # URL of your project (GitHub, etc.)
    license="MIT",  # License for your project
    classifiers=[  # Classifiers help others find your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
