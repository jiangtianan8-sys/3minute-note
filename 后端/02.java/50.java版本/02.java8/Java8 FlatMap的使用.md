给定单词列表[“Hello”,“World”]，你想要返回列表[“H”,“e”,“l”, “o”,“W”,“r”,“d”]

你可能首先想到的是：可以把每个单词映射成一张字符表，然后调用distinct来过滤重复的字符。

即：
```java
words.stream() .map(word -> word.split("")) .distinct() .collect(toList());
```
这个方法的问题在于，传递给map方法的Lambda为每个单词返回了一个String[]（String 列表）。因此，map返回的流实际上是Stream<String[]>类型的。你真正想要的是用 Stream 来表示一个字符流，如图：
![](assets/Java8%20FlatMap的使用/file-20251231161334246.png)

尝试使用map和Arrays.stream()
首先，你需要一个字符流，而不是数组流。有一个叫作Arrays.stream()的方法可以接受一个数组并产生一个流，例如：

```java
String[] arrayOfWords = {"Goodbye", "World"}; 
Stream<String> streamOfwords = Arrays.stream(arrayOfWords);
```

把它用在前面的那个流水线里，看看会发生什么：

```java
words.stream() 

 .map(word -> word.split("")) //将每个单词转换为由其字母构成的数组

 .map(Arrays::stream)//让每个数组变成一个单独的流

 .distinct() 

 .collect(toList()); 
```
当前的解决方案仍然搞不定！这是因为，你现在得到的是一个流的列表（更准确地说是Stream）。的确，你先是把每个单词转换成一个字母数组，然后把每个数组变成了一个独立的流。

使用flatMap
你可以像下面这样使用flatMap来解决这个问题：

```java
List<String> uniqueCharacters = 

 words.stream() 

 .map(w -> w.split("")) //将每个单词转换为由其字母构成的数组

 .flatMap(Arrays::stream) //将各个生成流扁平化为单个流

 .distinct() 
```
使用flatMap方法的效果是，各个数组并不是分别映射成一个流，而是映射成流的内容。所有使用map(Arrays::stream)时生成的单个流都被合并起来，即扁平化为一个流。下图说明了使用flatMap方法的效果。
![](assets/Java8%20FlatMap的使用/file-20251231161525830.png)

总而言之，flatmap方法让你把一个流中的每个值都换成另一个流，然后把所有的流连接起来成为一个流。

举一反三
给定两个数字列表，如何返回所有的数对呢？例如，给定列表[1, 2, 3]和列表[3, 4]，应该返回[(1, 3), (1, 4), (2, 3), (2, 4), (3, 3), (3, 4)]。为简单起见，你可以用有两个元素的数组来代表数对。

解答：
你可以使用两个map来迭代这两个列表，并生成数对。但这样会返回一个Stream-<Stream<Integer[]>>。你需要让生成的流扁平化，以得到一个Stream<Integer[]>。这
正是flatMap所做的：

```java
List<Integer> numbers1 = Arrays.asList(1, 2, 3); 
List<Integer> numbers2 = Arrays.asList(3, 4); 
List<int[]> pairs = numbers1.stream() 
						.flatMap(i -> numbers2.stream() 
							.map(j -> new int[]{i, j}) 
						) 
 					.collect(toList());
```

版权声明：本文为CSDN博主「杨幂等」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/Xumuyang_/article/details/120951979