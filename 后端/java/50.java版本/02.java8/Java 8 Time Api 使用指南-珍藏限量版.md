1.概述

Java 8为Date和Time引入了新的API，以解决旧java.util.Date和java.util.Calendar的缺点。

作为本文的一部分，让我们从现有Date和Calendar API存在的一些问题入手，来探讨新的Java 8 Date和Time API如何解决这些问题。

我们还将搞一搞Java 8时间类库中的核心类，比如LocalDate, LocalTime, LocalDateTime, ZonedDateTime, Period, Duration以及它们的api。

2. 旧的时间API（java8之前）的问题

- 线程安全 - Date 和Calendar类不是线程安全的，使开发者难以调试这些api的并发问题，需要编写额外的代码来处理线程安全。Java 8中引入的新的Date和Time API是不可变的和线程安全的，使得这些痛点得以解决。
- API设计和易于理解 - 旧的时间api非常难以理解，操作都非常复杂，非常绕口，没有提供一些常用的解析转换方法。新的时间API是以ISO为中心的，并遵循 date, time, duration 和 periods的一致域模型。提供了一些非常实用方法以支持最常见的操作。不再需要我们自己封装一些时间操作类。
- ZonedDate和Time - 在旧的时间api中开发人员必须编写额外的逻辑来处理旧API的时区逻辑，而使用新的API，可以使用 Local和ZonedDate / Time API来处理时区。无需过多关心时区转换问题。

3.使用LocalDate，LocalTime和LocalDateTime

最常用的类是LocalDate，LocalTime和LocalDateTime。正如他们的名字所示，它们代表与上下文相结合的本地日期/时间。

这些类主要用于不需要在上下文中明确指定时区的情况。作为本节的一部分，我们将介绍最常用的API。

3.1。使用LocalDate

LocalDate表示在ISO格式（YYYY-MM-DD）下的不带具体时间的日期。

常用于表示生日或者我们最关心的发工资的日期。

获取当前系统时钟下的日期，如下所示：

LocalDate localDate = LocalDate.now();

表示特定日，月和年的LocalDate可以使用“ of ”方法或使用“ parse ”方法获得。例如，以下代码段代表2015年2月20日的LocalDate：

LocalDate.of(2015, 02, 20);

LocalDate.parse("2015-02-20");

是不是非常直观而且方便呢！LocalDate提供各种实用方法，以获得各种日期信息。让我们快速浏览一下这些API方法。

以下代码段获取当前本地日期并添加一天：

LocalDate tomorrow = LocalDate.now().plusDays(1);

此示例获取当前日期并减去一个月。请注意它是如何接受枚举作为时间单位的：

LocalDate previousMonthSameDay = LocalDate.now().minus(1, ChronoUnit.MONTHS);

在以下两个代码示例中，我们分析日期“2016-06-12”并分别获取星期几和月中的某天。注意返回值，第一个是表示DayOfWeek的对象，而第二个是表示月份的序数值的int：

DayOfWeek sunday = LocalDate.parse("2016-06-12").getDayOfWeek();

int twelve = LocalDate.parse("2016-06-12").getDayOfMonth();

我们可以测试一个日期是否发生在闰年，如果用老方法怕不是要上天：

boolean leapYear = LocalDate.now().isLeapYear();

判断日期的先后：

boolean notBefore = LocalDate.parse("2016-06-12").isBefore(LocalDate.parse("2016-06-11"));

boolean isAfter = LocalDate.parse("2016-06-12").isAfter(LocalDate.parse("2016-06-11"));

日期边界可以从给定日期获得。在以下两个示例中，我们得到LocalDateTime，它代表给定日期的一天的开始（2016-06-12T00：00）和代表月初的LocalDate（2016-06-01）：

LocalDateTime beginningOfDay = LocalDate.parse("2016-06-12").atStartOfDay();

LocalDate firstDayOfMonth = LocalDate.parse("2016-06-12")

.with(TemporalAdjusters.firstDayOfMonth());

现在让我们来看看我们如何使用当地时间。

3.2。使用LocalTime

在本地时间表示不带日期的时间。

与LocalDate类似，可以从系统时钟或使用“parse”和“of”方法创建LocalTime实例。快速浏览下面的一些常用API。

可以从系统时钟创建当前LocalTime的实例，如下所示：

LocalTime now = LocalTime.now();

在下面的代码示例中，我们通过解析字符串表示创建表示06:30 AM 的LocalTime：

LocalTime sixThirty = LocalTime.parse("06:30");

方法“of”可用于创建LocalTime。例如，下面的代码使用“of”方法创建表示06:30 AM的LocalTime：

LocalTime sixThirty = LocalTime.of(6, 30);

下面的示例通过解析字符串来创建LocalTime，并使用“plus”API为其添加一小时。结果将是代表07:30 AM的LocalTime：

LocalTime sevenThirty = LocalTime.parse("06:30").plus(1, ChronoUnit.HOURS);

各种getter方法可用于获取特定的时间单位，如小时，分钟和秒，如下所示获取小时：

int six = LocalTime.parse("06:30").getHour();

同LocalDate一样检查特定时间是否在另一特定时间之前或之后。下面的代码示例比较结果为true的两个LocalTime：

boolean isbefore = LocalTime.parse("06:30").isBefore(LocalTime.parse("07:30"));

一天中的最大，最小和中午时间可以通过LocalTime类中的常量获得。在执行数据库查询以查找给定时间范围内的记录时，这非常有用。例如，下面的代码代表23：59：59.99：

LocalTime maxTime = LocalTime.MAX

现在让我们深入了解LocalDateTime。

3.3。使用LocalDateTime

所述LocalDateTime用于表示日期和时间的组合。

当我们需要结合日期和时间时，这是最常用的类。该类提供了各种API，我们将介绍一些最常用的API。

类似于LocalDate和LocalTime从系统时钟获取LocalDateTime的实例：

LocalDateTime.now();

下面的代码示例解释了如何使用工厂“of”和“parse”方法创建实例。结果将是代表2015年2月20日06:30 AM 的LocalDateTime实例：

LocalDateTime.of(2015, Month.FEBRUARY, 20, 06, 30);

LocalDateTime.parse("2015-02-20T06:30:00");

有一些实用的API可以支持特定时间单位的时间运算，例如天，月，年和分钟。以下代码示例演示了“加”和“减”方法的用法。这些API的行为与LocalDate和LocalTime中的 API完全相同：

localDateTime.plusDays(1);

localDateTime.minusHours(2);

Getter方法可用于提取类似于日期和时间类的特定单位。鉴于上面的LocalDateTime实例，下面的代码示例将返回2月份的月份：

localDateTime.getMonth();

4.使用ZonedDateTime API

当我们需要处理时区特定的日期和时间时，Java 8提供了ZonedDateTime 类。ZoneID是用于表示不同区域的标识符。大约有40个不同的时区，使用ZoneID表示它们，如下所示

下面的代码我们来获取下“亚洲/上海”时区:

ZoneId zoneId = ZoneId.of("Aisa/Shanghai");

获取所有的时区：

Set allZoneIds = ZoneId.getAvailableZoneIds();

LocalDateTime转化为特定的时区中的时间：

ZonedDateTime zonedDateTime = ZonedDateTime.of(localDateTime, zoneId);

ZonedDateTime提供解析方法来获取时区的特定日期时间：

ZonedDateTime.parse("2015-05-03T10:15:30+01:00[Aisa/Shanghai]");

使用时区的另一种方法是使用OffsetDateTime。OffsetDateTime是具有偏移量的日期时间的不可变表示形式。此类存储所有日期和时间字段，精确到纳秒，以及从UTC/格林威治的偏移量。可以使用ZoneOffset创建OffsetDateTime实例。这里我们创建一个LocalDateTime来表示2015年2月20日上午6:30：

LocalDateTime localDateTime = LocalDateTime.of(2015, Month.FEBRUARY, 20, 06, 30);

然后我们通过创建ZoneOffset并为LocalDateTime实例设置来增加两个小时：

ZoneOffset offset = ZoneOffset.of("+02:00");

OffsetDateTime offSetByTwo = OffsetDateTime.of(localDateTime, offset);

我们现在的本地日期时间为2015-02-20 06:30 +02：00。现在让我们继续讨论如何使用Period和Duration类修改日期和时间值。

5.使用Period和Duration

- Period : 用于计算两个日期（年月日）间隔。
- Duration : 用于计算两个时间（秒，纳秒）间隔。

5.1。使用Period

Period 类被广泛地用于修改给定的日期的值或者获取两个日期之间的差值：

LocalDate initialDate = LocalDate.parse("2007-05-10");

LocalDate finalDate = initialDate.plus(Period.ofDays(5));

Period 类有各种getter方法，如getYears，getMonths和getDays从获取值周期对象。下面的代码示例返回一个int值为5，是基于上面示例的逆序操作：

int five = Period.between(finalDate, initialDate).getDays();

该Period 可以在特定的单元获得两个日期之间的如天或月或数年，使用ChronoUnit.between：

int five = ChronoUnit.DAYS.between(finalDate , initialDate);

此代码示例返回五天。让我们继续看看Duration类。

5.2。使用Duration

类似Period ，该Duration类是用来处理时间。在下面的代码中，我们创建一个本地时间上午6:30，然后加30秒的持续时间，以使本地时间上午6时三十〇分30秒的：

LocalTime initialTime = LocalTime.of(6, 30, 0);

LocalTime finalTime = initialTime.plus(Duration.ofSeconds(30));

两个时刻之间的持续时间可以作为持续时间或作为特定单位获得。在第一个代码片段中，我们使用Duration类的between（）方法来查找finalTime和initialTime之间的时间差，并以秒为单位返回差异：

int thirty = Duration.between(finalTime, initialTime).getSeconds();

在第二个例子中，我们使用ChronoUnit类的between（）方法来执行相同的操作：

int thirty = ChronoUnit.SECONDS.between(finalTime, initialTime);

现在我们来看看如何将旧的Date 和Calendar 转换为新的Date和Time。

6.与日期和日历的兼容性

Java 8添加了toInstant（）方法，该方法有助于将旧API中的Date和Calendar实例转换为新的Date Time API，如下面的代码片段所示：

LocalDateTime.ofInstant(date.toInstant(), ZoneId.systemDefault());

LocalDateTime.ofInstant(calendar.toInstant(), ZoneId.systemDefault());

所述LocalDateTime可以从如下“ofEpochSecond"方法来构造。以下代码的结果将是代表2016-06-13T11：34：50 的LocalDateTime：

LocalDateTime.ofEpochSecond(1465817690, 0, ZoneOffset.UTC);

现在让我们继续进行日期和时间格式化。

7. 日期和时间格式化

Java 8提供了用于轻松格式化日期和时间的 API ：

LocalDateTime localDateTime = LocalDateTime.of(2015, Month.JANUARY, 25, 6, 30);

以下代码传递ISO日期格式以格式化本地日期。结果将是2015-01-25：

String localDateString = localDateTime.format(DateTimeFormatter.ISO_DATE);

该DateTimeFormatter提供多种标准格式选项。也可以提供自定义模式来格式化方法，如下所示，它将返回LocalDate为2015/01/25：

localDateTime.format(DateTimeFormatter.ofPattern("yyyy/MM/dd"));

我们可以将格式样式传递为SHORT，LONG或MEDIUM作为格式化选项的一部分。下面的代码示例输出2015年1月25日06:30:00 me的输：

localDateTime

.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM)

.withLocale(Locale.UK);

最后让我们看看Java 8 Core Date / Time API 可用的替代方案。

8.替代方案

8.1。使用Threeten 类库

对于从Java 7或Java 6这些老项目来说可以使用Threeten ,然后可以像在上面java 8一样使用相同的功能，一旦你迁移到java 8 只需要修改你的包路径代码而无需变更：

org.threeten

threetenbp

LATEST

8.2。Joda-Time类库

Java 8 日期和时间库的另一种替代方案是Joda-Time库。事实上，Java 8 Date Time API由Joda-Time库（Stephen Colebourne）和Oracle共同领导。该库提供了Java 8 Date Time项目中支持的几乎所有功能。通过在项目中引用以下pom依赖项就可以立即使用：

joda-time

joda-time

LATEST

以上就是我辛苦总结的java 8 time api 的一些知识，希望帮助你更好的理解和使用它们。