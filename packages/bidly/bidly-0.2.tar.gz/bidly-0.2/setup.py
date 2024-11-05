import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bidly',
    version='0.2',
    packages=["bidly"],  # Finds all packages
    install_requires=['Django'],
    description='A bidding logic library for Django applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Priya Shanmugam',
    author_email='priyashan112002@example.com',
    url='https://github.com/Priya-1110/bidly',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
