from setuptools import setup, find_packages

setup(
    name="colortype",               # Tên module của bạn
    version="1",                  # Phiên bản
    description="A module that use ANSI code to change your text color, text type",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dang Vo Anh Kiet",
    author_email="himnnha23@gmail.com",
    license="MIT",
    packages=find_packages(),       # Tự động tìm và thêm các package trong thư mục
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.0",        # Phiên bản Python yêu cầu
    install_requires=[              # Các module phụ thuộc
        # "dependency_package>=1.0",
    ],
)
