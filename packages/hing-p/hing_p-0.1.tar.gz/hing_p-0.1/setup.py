from setuptools import setup, find_packages

setup(
    name="hing_p",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # 패키지가 의존하는 다른 패키지가 있으면 여기에 추가
    author="yongjin",
    author_email="kimyongjin0305@gmail.com",
    description="A package for managing school courses and students",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
