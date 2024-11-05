from setuptools import find_packages, setup

setup(
    name='hayashi',
    packages=find_packages(),
    version='1.1.1',
    description='Python library for computing the number of absorption features of the 21 cm forest in a semianalytic formalism.',
    long_description_content_type="text/markdown",
    author='Pablo Villanueva-Domingo',
    author_email='pablo.villanueva.domingo@gmail.com',
    install_requires=["numpy",
                      "scipy",
                      "tqdm",
                      "colossus"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
