这里是根据员工年龄来得到年龄最大的那个对象.(仅适用于JDK1.8及以上)

Employee 是员工类

age  是它的年龄

getAge() 是 age的getter方法

```java
Optional<Employee > userOp= userList.stream().max(Comparator.comparingInt(Employee ::getAge));
    
Employee maxEmp = userOp.get();
```

 
```java
Optional<Employee > userOp= userList.stream().filter(Objects::nonNull).filter(item -> item.getAge() != null)
.sorted(Comparator.comparing(Employee::getAge).reversed()).findFirst().get();
 Employee maxEmp = userOp.get();
```
避免空指针,添加一个filter,判断age不能为空,

```java
filter(item -> item.getAge() != null)
```
,或者使用orElse防止空指针。

```java

Optional<Employee > userOp= employees.stream().filter(Objects::nonNull).max(Comparator.comparingInt(Employee ::getAge));
Employee maxEmp = userOp.orElse(new Employee());
```
 
————————————————
版权声明：本文为CSDN博主「潇兮水寒」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u012190514/article/details/83036610