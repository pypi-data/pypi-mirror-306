from setuptools import setup, find_packages

setup(
    name="simply_blockchain",  # Package name
    version="0.1.0",  # Version of the package
    description="A simple blockchain implementation",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Jay Jethwa",
    packages=find_packages(),  # Automatically finds all packages in the directory
    install_requires=[  # Any dependencies your package needs (if any)
        # 'requests', 'numpy', etc.
    ],
    classifiers=[  # PyPI classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',  # Minimum Python version
)
