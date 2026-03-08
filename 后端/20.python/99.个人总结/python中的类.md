在 Python 中定义类是面向对象编程（OOP）的核心，我会从**基础语法**到**进阶用法**一步步教你，用简单易懂的例子帮你理解，新手也能快速上手。

### 一、类的基础定义（最核心）

Python 中用 `class` 关键字定义类，基本结构分为 3 部分：**类名**、**属性**、**方法**。

#### 1. 最简示例（空类）

python

运行

```
# 定义一个空类（类名首字母建议大写，遵循大驼峰命名法）
class Person:
    # 类体（暂时为空，用 pass 占位）
    pass

# 创建类的实例（对象）
p1 = Person()
print(p1)  # 输出：<__main__.Person object at 0x0000021F8A78D100>（对象内存地址）
```

#### 2. 带属性和方法的完整示例（常用）

python

运行

```
# 定义一个「人」类，包含属性和方法
class Person:
    # 1. 类属性（所有实例共享的属性）
    species = "人类"  # 所有Person实例的物种都是“人类”

    # 2. 初始化方法（__init__）：创建实例时自动执行，用于初始化实例属性
    def __init__(self, name, age):
        # self 代表当前实例本身，必须作为第一个参数
        # 实例属性（每个实例独有的属性）
        self.name = name  # 姓名
        self.age = age    # 年龄

    # 3. 实例方法（必须带 self 参数）
    def introduce(self):
        # 方法内可以访问实例属性和类属性
        return f"大家好，我是{self.name}，今年{self.age}岁，属于{self.species}。"

    # 4. 方法：修改实例属性
    def grow_up(self):
        self.age += 1  # 年龄加1
        return f"{self.name}长大了一岁，现在{self.age}岁。"

# ====================== 使用类 ======================
# 1. 创建实例（对象）：传入 __init__ 要求的参数（self 无需传）
p2 = Person("张三", 18)
p3 = Person("李四", 20)

# 2. 访问实例属性
print(p2.name)  # 输出：张三
print(p3.age)   # 输出：20

# 3. 访问类属性（实例和类都能访问）
print(p2.species)  # 输出：人类
print(Person.species)  # 输出：人类

# 4. 调用实例方法
print(p2.introduce())  # 输出：大家好，我是张三，今年18岁，属于人类。
print(p3.grow_up())    # 输出：李四长大了一岁，现在21岁。

# 5. 修改实例属性
p2.age = 19
print(p2.introduce())  # 输出：大家好，我是张三，今年19岁，属于人类。
```

### 二、关键概念解释（新手必懂）

#### 1. `class` 关键字

- 用于声明 “定义一个类”，类名**首字母大写**（大驼峰命名法，如 `Person`、`Student`），这是 Python 约定俗成的规范。

#### 2. `__init__` 方法（构造方法）

- 这是**初始化方法**，创建实例时自动执行，用来给实例绑定属性。
- `self` 是必须的第一个参数，代表当前创建的实例本身（名字可以改，但没人会改，约定用 `self`）。
- 除了 `self`，可以自定义参数（如 `name`、`age`），创建实例时需要传入这些参数。

#### 3. 类属性 vs 实例属性

表格

|类型|定义位置|访问方式|特点|
|---|---|---|---|
|类属性|类内部、**init** 外部|类名。属性 / 实例。属性|所有实例共享，修改后全局生效|
|实例属性|**init** 内部（self.xxx）|实例。属性|每个实例独立，互不影响|

示例：修改类属性会影响所有实例

python

运行

```
Person.species = "智人"
print(p2.species)  # 输出：智人（p2的类属性也变了）
print(p3.species)  # 输出：智人
```

#### 4. 实例方法

- 定义在类内部的函数，**第一个参数必须是 self**。
- 只能通过实例调用（不能直接用类名调用，除非手动传 self）。
- 方法内可以通过 `self` 访问 / 修改实例属性、调用其他方法。

### 三、进阶用法（常用）

#### 1. 带默认参数的类

python

运行

```
class Student:
    def __init__(self, name, age=18):  # age 有默认值
        self.name = name
        self.age = age

# 创建实例时可以不传 age
s1 = Student("王五")
print(s1.age)  # 输出：18

s2 = Student("赵六", 20)
print(s2.age)  # 输出：20
```

#### 2. 私有属性 / 方法（约定）

Python 没有真正的私有，而是通过**前缀下划线**约定：

- `_xxx`：受保护的属性 / 方法（约定不对外访问）；
- `__xxx`：私有属性 / 方法（会被改名，外部无法直接访问）。

python

运行

```
class Person:
    def __init__(self, name, id_card):
        self.name = name        # 公开属性
        self.__id_card = id_card  # 私有属性（双下划线）

    def __check_id(self):       # 私有方法
        return f"身份证校验：{self.__id_card}"

    def get_id_info(self):      # 公开方法，间接访问私有属性/方法
        return self.__check_id()

p4 = Person("张三", "110101199001011234")
print(p4.name)  # 正常访问：张三
# print(p4.__id_card)  # 报错：AttributeError（无法直接访问）
# print(p4.__check_id())  # 报错：AttributeError
print(p4.get_id_info())  # 输出：身份证校验：110101199001011234
```

### 总结

1. **核心语法**：用 `class 类名:` 定义类，`__init__(self, ...)` 初始化实例属性，方法必须带 `self` 参数；
2. **关键区分**：类属性（所有实例共享）和实例属性（每个实例独有）；
3. **使用流程**：定义类 → 创建实例（`实例名 = 类名(参数)`）→ 访问属性 / 调用方法（`实例名.属性`/`实例名.方法()`）。

如果想进一步了解**继承**、**多态**、**类方法 / 静态方法**等进阶内容，或者想针对某个场景（比如定义一个 “汽车” 类）写示例，都可以告诉我。