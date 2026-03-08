ython 中的**特殊方法（魔法方法 / Magic Methods）** 是类中以 `__` 开头和结尾的方法（如 `__init__`），它们不需要手动调用，而是在特定场景下由 Python 解释器自动触发，能让自定义类拥有和内置类型（如列表、字符串）一样的行为。

我会从**最常用的魔法方法**入手，结合示例讲解用法，帮你快速掌握核心知识点。

### 一、核心魔法方法分类与示例

#### 1. 初始化与销毁（最基础）

表格

|方法|触发场景|作用|
|---|---|---|
|`__init__(self, ...)`|创建实例时自动调用|初始化实例属性（之前讲过）|
|`__del__(self)`|实例被垃圾回收时调用|释放资源（如关闭文件、数据库连接）|

python

运行

```
class Person:
    def __init__(self, name):
        self.name = name
        print(f"初始化 {self.name}")

    def __del__(self):
        print(f"销毁 {self.name}（实例被回收）")

# 测试
p = Person("张三")  # 输出：初始化 张三
del p  # 手动删除实例，触发__del__ → 输出：销毁 张三（实例被回收）
```

#### 2. 字符串表示（自定义打印 / 输出格式）

表格

|方法|触发场景|作用|
|---|---|---|
|`__str__(self)`|`print(实例)` / `str(实例)` 时调用|返回人类可读的字符串（面向用户）|
|`__repr__(self)`|直接输实例 / `repr(实例)` 时调用|返回精准的字符串（面向开发者，用于调试）|

> 提示：如果只定义一个，优先定义 `__repr__`（`print` 会兜底使用它）

python

运行

```
class Book:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return f"《{self.title}》- 价格：{self.price}元"

    def __repr__(self):
        return f"Book(title='{self.title}', price={self.price})"

# 测试
b = Book("Python入门", 59)
print(b)          # 触发__str__ → 输出：《Python入门》- 价格：59元
b                 # 触发__repr__ → 输出：Book(title='Python入门', price=59)
```

#### 3. 运算符重载（让实例支持加减乘除等操作）

通过魔法方法自定义实例的运算符行为，核心示例：

表格

|方法|触发场景|作用|
|---|---|---|
|`__add__(self, other)`|`实例1 + 实例2`|定义加法逻辑|
|`__sub__(self, other)`|`实例1 - 实例2`|定义减法逻辑|
|`__eq__(self, other)`|`实例1 == 实例2`|定义相等判断逻辑|

python

运行

```
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 重载加法：两个点的坐标分别相加
    def __add__(self, other):
        # 确保 other 也是 Point 实例
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError("只能和Point实例相加")

    # 重载相等判断
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

# 测试
p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2       # 触发__add__ → Point(4, 6)
print(p3)          # 输出：Point(4, 6)
print(p1 == Point(1, 2))  # 触发__eq__ → True
```

#### 4. 容器行为（让实例像列表 / 字典一样使用）

实现这些方法，自定义类可以支持 `[]` 索引、遍历、长度获取等：

表格

|方法|触发场景|作用|
|---|---|---|
|`__getitem__(self, key)`|`实例[key]`|获取索引 / 键对应的值|
|`__setitem__(self, key, value)`|`实例[key] = value`|设置索引 / 键对应的值|
|`__len__(self)`|`len(实例)`|返回容器长度|
|`__iter__(self)`|`for 元素 in 实例`|支持遍历（返回迭代器）|

python

运行

```
class MyList:
    def __init__(self):
        self.data = []

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __len__(self):
        return len(self.data)

    # 追加元素（自定义方法）
    def append(self, value):
        self.data.append(value)

# 测试
ml = MyList()
ml.append(1)
ml.append(2)
print(len(ml))     # 触发__len__ → 2
print(ml[0])       # 触发__getitem__ → 1
ml[1] = 3          # 触发__setitem__
print(ml[1])       # → 3
```

#### 5. 上下文管理器（with 语句）

实现 `__enter__` 和 `__exit__`，让实例支持 `with` 语句（如文件操作）：

python

运行

```
class FileHandler:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        # 进入with块时调用：打开文件
        self.file = open(self.filename, self.mode)
        return self.file  # 作为with ... as 的返回值

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 退出with块时调用：关闭文件（无论是否报错）
        if self.file:
            self.file.close()
        # 返回True可忽略异常，返回False会抛出异常
        return False

# 测试：自动打开/关闭文件
with FileHandler("test.txt", "w") as f:
    f.write("Hello Python")
# 退出with块后，文件已自动关闭
```

### 二、魔法方法的核心特点

1. **自动触发**：不需要手动调用（如 `p.__add__(p2)` 很少用，直接 `p1 + p2`）；
2. **遵循约定**：方法名和参数格式是固定的（如 `__add__` 必须接收 `self` 和 `other`）；
3. **增强类能力**：让自定义类拥有内置类型的行为（如加减、索引、遍历）；
4. **可选实现**：只需要实现业务需要的魔法方法，不需要全部实现。

### 三、常用魔法方法速查表（按场景分类）

表格

|场景|核心方法|
|---|---|
|初始化 / 销毁|`__init__`, `__del__`|
|字符串表示|`__str__`, `__repr__`|
|运算符重载|`__add__`, `__sub__`, `__eq__`, `__gt__`（大于）, `__lt__`（小于）|
|容器行为|`__getitem__`, `__setitem__`, `__len__`, `__iter__`|
|上下文管理|`__enter__`, `__exit__`|
|调用行为|`__call__`（让实例像函数一样调用：`实例()`）|

### 总结

1. 魔法方法是类中 `__xxx__` 格式的特殊方法，由 Python 自动触发；
2. 核心用途是**自定义类的行为**：比如让实例支持加减运算、索引、with 语句等；
3. 最常用的是 `__init__`（初始化）、`__str__/__repr__`（字符串表示）、`__add__`（运算符重载）、`__getitem__`（容器索引）。

如果想针对某个具体场景（比如实现一个支持切片的自定义列表、重载乘法运算符）写完整示例，或者想了解某类魔法方法的细节，都可以告诉我。