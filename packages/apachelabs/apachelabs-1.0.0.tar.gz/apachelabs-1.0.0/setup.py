from setuptools import setup, find_packages

setup(
    name='apachelabs',  # Replace with your package name
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[
        'mistralai',  # List dependencies here
    ],
    author='Apache Labs',
    author_email='your.email@example.com',
    description='API System (Based on Mistral) to use Apache Lab Models',
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',
    url='',  # Your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version required
)
