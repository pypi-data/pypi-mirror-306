from setuptools import setup, find_packages

setup(
    name='sam-plot-extraction',  # Replace with your package name
    version='0.1.0',
    author='Hansae Kim',
    author_email='kim4012@purdue.edu',
    description='Plot extraction using segment anything model',
    long_description=open('README.md').read(),  # Ensure README.md exists
    long_description_content_type='text/markdown',
    url='https://github.com/breadnbutter0/sam-plot-extraction',  # Replace with your GitHub or project URL
    packages=find_packages(),  # Automatically finds package directories
    install_requires=[
        # List dependencies here, e.g., 'numpy', 'pandas'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)