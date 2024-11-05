# __init__.py中写法
1. 使用方式
2. 导包，可选

```
My Common Lib

This package provides utility functions and classes for various projects.
Usage:

    from my_common_lib import greet, add

    # Example usage
    print(greet("Alice"))  # Output: "Hello, Alice!"
    print(add(3, 5))       # Output: 8

Functions:
- greet(name): Returns a greeting string.
- add(a, b): Returns the sum of two numbers.
"""

# Optional: You can also import commonly used functions here for convenience
from .my_module import greet, add
```

# 本地安装和测试

```bash
pip install .
```

# 打包和分发

```bash
python setup.py sdist bdist_wheel
```


