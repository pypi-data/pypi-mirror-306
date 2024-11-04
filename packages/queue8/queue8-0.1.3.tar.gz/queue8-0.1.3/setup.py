from setuptools import setup, find_packages

setup(
    name="queue8",  # Tên thư viện của bạn
    version="0.1.3",  # Phiên bản hiện tại của thư viện
    packages=find_packages(),  # Tự động tìm các gói trong thư mục dự án
    install_requires=[
        'pika',  # Các gói phụ thuộc cần cài đặt khi sử dụng thư viện
    ],
    author="Vu D.",
    author_email="vubakninh@gmail.com",
    description="A custom library for handling message queues with timeout and message batching.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://nexus.x51.vn/repository/queue_lib/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
