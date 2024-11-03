from setuptools import setup, find_packages

setup(
    name = "mzml2gnps",
    version = "1.0.0",
    packages=find_packages(),
    install_requires=[
    "pandas == 2.0.3",
    "numpy >=1.22.0, <2.0.0",
    "pyopenms == 3.1.0",
    ],
    entry_points={
        'console_scripts': [
            'mzml2gnps = mzml2gnps.command_line:main',  
        ],
    },
    author='YunyingXie',
    author_email='xieyy@imb.pumc.edu.cn', 
    description='A package for preprocessing mzML files for GNPS molecular networking',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/xieyying/mzml2gnps',  # 替换为你的实际URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)