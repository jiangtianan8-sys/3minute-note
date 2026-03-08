`@staticmethod`（静态方法）和 `@classmethod`（类方法）是 Python 中修饰类方法的两个核心装饰器，它们都属于**类的方法**（而非实例方法），但适用场景和使用方式有本质区别。我会用「对比 + 示例」的方式讲清楚，新手也能快速区分和使用。

### 一、核心区别（先看结论）

表格

|特性|`@staticmethod`（静态方法）|`@classmethod`（类方法）|普通实例方法|
|---|---|---|---|
|第一个参数|无强制参数（可无参数）|必须是 `cls`（代表类本身）|必须是 `self`（实例）|
|访问权限|不能直接访问类 / 实例属性|可访问类属性，不能直接访问实例属性|可访问类 + 实例属性|
|调用方式|类名。方法 () / 实例。方法 ()|类名。方法 () / 实例。方法 ()|只能实例。方法 ()|
|核心用途|独立功能，和类弱关联|操作类属性、创建类实例|操作实例属性|

### 二、逐个拆解（示例 + 用法）

先定义一个基础类，再分别实现三种方法，对比效果：

python

运行

```
class Person:
    # 类属性
    species = "人类"

    def __init__(self, name, age):
        # 实例属性
        self.name = name
        self.age = age

    # 1. 普通实例方法（必须带self）
    def introduce(self):
        return f"我是{self.name}，今年{self.age}岁，属于{Person.species}。"

    # 2. 静态方法（@staticmethod）
    @staticmethod
    def is_adult(age):
        """判断是否成年（独立功能，只和逻辑相关，和类/实例属性无关）"""
        return age >= 18

    # 3. 类方法（@classmethod）
    @classmethod
    def update_species(cls, new_species):
        """修改类属性（cls代表Person类本身）"""
        cls.species = new_species
        return f"类属性已更新：{cls.species}"

    # 类方法经典场景：工厂方法（创建实例）
    @classmethod
    def create_child(cls, name):
        """快速创建“儿童”实例（年龄固定为10）"""
        return cls(name, 10)  # 等价于 Person(name, 10)
```

#### 1. 静态方法（@staticmethod）

- **本质**：和类关联的「普通函数」，只是放在类的命名空间里，没有 `self`/`cls` 参数，无法直接访问类 / 实例属性。
- **调用方式**：类名调用（推荐）或实例调用都可以。

python

运行

```
# 调用静态方法（推荐：类名.方法）
print(Person.is_adult(20))  # 输出：True
print(Person.is_adult(15))  # 输出：False

# 实例调用（不推荐，但语法允许）
p = Person("张三", 18)
print(p.is_adult(25))  # 输出：True
```

- **适用场景**：
    
    - 功能独立，只是逻辑上属于这个类（比如工具函数）；
    - 不需要访问类 / 实例的任何属性，仅依赖传入的参数。
    

#### 2. 类方法（@classmethod）

- **本质**：绑定到类的方法，第一个参数 `cls` 代表类本身（可以理解为「类的 self」），能直接操作类属性。
- **调用方式**：类名调用（推荐）或实例调用都可以。

python

运行

```
# 1. 修改类属性
print(Person.update_species("智人"))  # 输出：类属性已更新：智人
print(Person.species)                # 输出：智人

# 2. 工厂方法（创建实例）
child = Person.create_child("小明")
print(child.name, child.age)  # 输出：小明 10
print(child.introduce())      # 输出：我是小明，今年10岁，属于智人。
```

- **适用场景**：
    
    - 需要操作**类属性**（而非实例属性）；
    - 工厂方法：根据不同参数快速创建实例（比如批量创建特定类型的实例）；
    - 继承场景：子类调用时，`cls` 会自动指向子类（而非父类）。
    

### 三、继承场景的关键差异（进阶）

类方法的 `cls` 会自动适配子类，而静态方法不会，这是类方法的核心优势：

python

运行

```
class Student(Person):
    species = "学生"

# 1. 类方法：cls指向子类Student
stu = Student.create_child("小红")
print(stu.species)  # 输出：学生（继承子类的类属性）

# 2. 静态方法：仍需手动指定，无自动适配
print(Student.is_adult(18))  # 输出：True（和普通函数无区别）
```

### 四、什么时候用？（新手速记）

表格

|场景|选哪个？|
|---|---|
|写一个工具函数，和类 / 实例无关|@staticmethod|
|操作类属性、批量创建实例|@classmethod|
|操作实例属性（比如改名字 / 年龄）|普通实例方法|

### 五、常见误区

1. **静态方法里想访问类属性**：
    
    ❌ 错误：`@staticmethod` 里直接用 `self.species` 或 `cls.species`；
    
    ✅ 正确：手动指定类名（如 `Person.species`），但不推荐（失去静态方法的意义）。
    
2. **类方法里想访问实例属性**：
    
    ❌ 错误：`cls.name`（类没有 `name` 属性，`name` 是实例属性）；
    
    ✅ 正确：先通过 `cls()` 创建实例，再访问（如 `obj = cls(name, age); print(obj.name)`）。
    
3. **没必要的装饰器**：
    
    如果方法既不访问类属性也不访问实例属性，优先用 `@staticmethod`（而非类方法）；
    
    如果只是想通过类名调用，却没有操作类属性，用静态方法更合适。
    

### 总结

1. `@staticmethod` 是「类里的普通函数」，无 `self/cls`，和类弱关联，适合独立工具逻辑；
2. `@classmethod` 绑定类，第一个参数 `cls` 指向类本身，适合操作类属性、创建实例；
3. 调用时优先用「类名。方法 ()」（而非实例），更符合设计意图。

如果想写一个具体场景的示例（比如用类方法实现不同格式的实例创建、静态方法做数据校验），可以告诉我，我帮你写完整代码。