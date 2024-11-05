from setuptools import setup, find_packages

setup(
    name='new_modeling',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的包依赖项，例如：
        # 'numpy',
        # 'requests',
    ],
    author='valencia',
    author_email='valencia.xu@intel.com',
    description='A new package that combines an existing library with new code',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/my_new_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)