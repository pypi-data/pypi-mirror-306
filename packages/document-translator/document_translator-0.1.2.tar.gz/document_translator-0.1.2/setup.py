from setuptools import setup, find_packages

setup(
    name='document_translator',
    version='0.1.2',
    description='A simple and fast translator for translating documents in google translate supported languages',
    author='Nirmal Patel',
    author_email='nirmalpatel1705@gmail.com',
    url='',  # Update this with your repository link
    packages=find_packages(),
    install_requires=[
        'selenium',  # Add any other dependencies your package needs
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
