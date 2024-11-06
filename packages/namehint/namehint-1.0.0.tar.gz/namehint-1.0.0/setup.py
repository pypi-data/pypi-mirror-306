from setuptools import setup, find_packages

setup(
    name='namehint',
    version='1.0.0',
    description="A tool that provides English synonyms for Korean words to assist in English naming.",
    author="gongboo",
    author_email="gongboolearn@gmail.com",
    py_modules=['namehint'],  # hello.py 모듈 포함
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'namehint': ['dictionary.json'],  # 모든 패키지에 dictionary.json 포함
    },
    entry_points={
        'console_scripts': [
            'namehint=namehint.namehint:main',  # 'namehint' 명령어를 namehint.py의 main 함수에 연결
        ],
    },
    install_requires=[                 # 필요한 패키지들
        "jamo",
    ],
    # PyPI 페이지에 README.md 내용이 표시
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)
