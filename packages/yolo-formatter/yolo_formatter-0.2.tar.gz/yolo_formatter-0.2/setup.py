from setuptools import setup, find_packages

setup(
    name='yolo_formatter',
    version='0.2',
    description='A Python package to create a proper structured dataset that YOLO understands.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/yolo_formatter',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
