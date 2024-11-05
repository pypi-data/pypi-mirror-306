from setuptools import setup, Extension
import sysconfig

# Định nghĩa extension
c_on_py_extension = Extension(
    'cpylib',  # Tên module sẽ tạo ra (c_on_py.so)
    sources=['cpylib/main.c'],  # Đường dẫn đến file mã nguồn C
    include_dirs=[sysconfig.get_path('include')],  # Lấy đường dẫn đến thư viện header Python
    extra_compile_args=['-fPIC'],  # Thêm cờ biên dịch nếu cần
)

# Thiết lập gói
setup(
    name='cpylib',  # Tên gói
    version='0.1.0',  # Phiên bản gói
    description='A Python package for executing C code',  # Mô tả ngắn gọn
    long_description=open('README.md').read(),  # Đọc mô tả dài từ README
    long_description_content_type='text/markdown',  # Định dạng mô tả dài
    author='Bobby',  # Tên tác giả
    author_email='akirasumeragi699@gmail.com',  # Email tác giả
    url='https://github.com/hqmdokkai/cpylib.git',  # Đường dẫn đến repo GitHub
    ext_modules=[c_on_py_extension],  # Danh sách các extension
    packages=['cpylib'],  # Thư mục chứa module
    install_requires=[],  # Các thư viện phụ thuộc (nếu có)
    classifiers=[  # Phân loại gói
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',  # Yêu cầu phiên bản Python tối thiểu
)
