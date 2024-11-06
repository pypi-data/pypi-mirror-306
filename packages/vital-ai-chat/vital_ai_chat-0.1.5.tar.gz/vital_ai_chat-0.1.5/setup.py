from setuptools import setup, find_packages

setup(
    name='vital-ai-chat',
    version='0.1.5',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='VitalSigns chat domain',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/vitalhome-chat',
    packages=find_packages(),
    package_data={
         '': ['*.pyi'],
    },
    license='Apache License 2.0',
    install_requires=[
            'vital-ai-vitalsigns>=0.1.21',
            'vital-ai-domain>=0.1.7',
            'vital-ai-haley-kg>=0.1.5',
            'vital-ai-haley-ml>=0.1.5',
        ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)