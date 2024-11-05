#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

// Hàm thực thi mã C từ chuỗi truyền vào từ Python
static PyObject* c_execute_code(PyObject* self, PyObject* args) {
    const char* code; // Mã C được truyền vào từ Python dưới dạng chuỗi

    // Đọc đối số từ Python, lấy chuỗi mã C
    if (!PyArg_ParseTuple(args, "s", &code)) {
        return NULL;
    }

    // Tạo file tạm để lưu mã C
    FILE *temp_file = fopen("code.c", "w");
    if (temp_file == NULL) {
        return PyErr_Format(PyExc_RuntimeError, "Không thể tạo file tạm.");
    }

    // Ghi mã C vào file tạm, bao gồm main để có thể chạy
    fprintf(temp_file, "#include <stdio.h>\nint main() { %s; return 0; }\n", code);
    fclose(temp_file);

    // Biên dịch mã C trong file tạm thành file thực thi
    int compile_result = system("clang -o code_executable code.c");  // Dùng clang thay vì gcc
    if (compile_result != 0) {
        remove("code.c");  // Xóa file tạm
        return PyErr_Format(PyExc_RuntimeError, "Biên dịch thất bại.");
    }

    // Thực thi file đã biên dịch
    int run_result = system("./code_executable");

    // Xóa các file tạm
    remove("code.c");
    remove("code_executable");

    if (run_result != 0) {
        return PyErr_Format(PyExc_RuntimeError, "Thực thi mã thất bại.");
    }

    Py_RETURN_NONE;
}

// Định nghĩa các hàm của module
static PyMethodDef COnPyMethods[] = {
    {"c", c_execute_code, METH_VARARGS, "Execute C code from a string"},
    {NULL, NULL, 0, NULL}
};

// Định nghĩa module với tên `cpylib`
static struct PyModuleDef conpy_module = {
    PyModuleDef_HEAD_INIT,
    "cpylib",  // Tên module
    NULL,      // Mô tả module
    -1,        // Kích thước module
    COnPyMethods
};

// Khởi tạo module
PyMODINIT_FUNC PyInit_cpylib(void) {
    return PyModule_Create(&conpy_module);
}
