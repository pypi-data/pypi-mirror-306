from setuptools import setup, find_packages

setup(
    name='LECPython',
    version='1.2.3.6',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'LECPythonLib': ['*.pdb', '*.dll', '*.so', '*.json'],
    },
    install_requires=[
        'pythonnet==3.0.4',  # 固定安装pythonnet版本为3.0.4
    ],
    author='xeden3',
    author_email='james@sctmes.com',
    description='LECPython is a Python component developed in C# that enables seamless communication between Python and PLCs...',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/xeden3/LECPython',
    project_urls={  # 添加项目相关的额外URL
        'Documentation': 'http://lecpserver.com:3003/',  # 替换为你的文档地址
        'Source': 'https://github.com/xeden3/LECPython',
        'Bug Tracker': 'https://github.com/xeden3/LECPython/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
