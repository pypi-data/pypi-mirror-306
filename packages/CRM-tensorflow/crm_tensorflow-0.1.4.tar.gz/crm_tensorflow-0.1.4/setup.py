from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name='CRM_tensorflow',
    version='0.1.4',
    description='A non-official implementation of the Complex Ratio Mask (CRM) technique as a Tensorflow layer.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/narrietal/CRM_tensorflow",
    author='Nicolas Arrieta Larraza',
    author_email='n.arrieta.larraza@gmail.com',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0.0'
    ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
