from setuptools import setup, find_packages

setup(
    name="prognosic_fetch", 
    version="0.1.0",     
    author="Mukund Gupta",
    author_email="mukund@prognosic.com",
    description="Prognosic, backed by Hack Club (501(c)(3) EIN: 81-2908499), offers instant dataset access in just 2 lines of code, making ML model training easy.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.prognosic.com/",  
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",        
        "boto3",
        "tqdm",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "prognosic=prognosic.app:main", 
        ]
    },
)
