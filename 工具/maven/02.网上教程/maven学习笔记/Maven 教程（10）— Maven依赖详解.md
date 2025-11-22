1、何为依赖？

比如你是个男的，你要生孩子，呸呸呸…男的怎么生孩子，所以你得依赖你老婆，不过也不一定咯，你也可以依赖其她妹子。

我们在平时的项目开发中也是同理，你需要依赖一些东西才能实现相应的功能，但相应的功能或许也可以依赖其它的东西实现，比如数据库操作吧，你可以依赖hibernate，但你也可以通过mybatis来做。

这就是所谓的依赖关系咯。

以前我们需要手动的去找hibernate或者mybatis的jar包，系统抛异常我们还不知哪里报错，通过琢磨才明白没有引入相应的jar包，然后就去找啊找，找到了然后引入到工程当中。在这里我们就看到maven的好处了，它就是一个仓库，仓库里面有各种各样的包，想要什么就在pom.xml中依赖一下就好了，就算仓库中没有的包也可以把它扔到仓库中，想用的时候就依赖一下。

2、依赖的配置

           junit

           junit

           3.8.1

           ...

           test

           ...

                   ...

                   ...

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

根元素下project下的dependencies可以包含一个或者多个dependency元素，以声明一个或者多个项目依赖。每个依赖可以包含的元素有：

- groupId,artifactId和version：依赖的基本坐标，对于任何一个依赖来说，基本坐标是最重要的，Maven根据坐标才能找到需要的依赖。
- type：依赖的类型，对应于项目坐标定义的packaging。大部分情况下，该元素不必声明，其默认值是jar。
- scope：依赖的范围，后面会进行详解。
- optional：标记依赖是否可选。
- exclusions：用来排除传递性依赖，后面会进行详细介绍。

大部分依赖声明只包含基本坐标，然而在一些特殊情况下，其他元素至关重要，我们来看看。

3、依赖范围说明

由于不同的包在不同的地方用到，像junit我们只有在做测试的时候会用到这个包，在我们项目发布的时候，用不到这个包；还有servlet-api，在项目编译的时候将会用到这个包，而项目发布的时候就不会用到这个包，因为一般容器已经自带这个包，如果我们导入，有可能会出现冲突，所以maven引入了依赖范围这个概念，即我们上面提到的scope来解决这个问题。Maven中有主要有以下这几种依赖范围：

1. test：指的是测试范围有效，在编译打包、运行时都不会使用这个依赖。例如：junit jar包。
2. compile：指的是编译范围有效，在编译、测试、打包、运行时都会将依赖存储进去。如果没有指定，就会默认使用该依赖范围。例如：hibernate.jar包。
3. provided：在编译和测试的过程有效，最后生成包时不会加入，运行时自然也没效果。例如：servlet-api，因为servlet-api，tomcat等web服务器已经存在该jar包了，如果再打包可能会有冲突。
4. runtime：在测试、运行的时候依赖，在编译的时候不依赖。例如：JDBC驱动，项目代码只需要jdk提供的jdbc接口，只有在执行测试和运行项目的时候才需要实现jdbc的功能。
5. system：系统依赖范围。该依赖范围与provided所表示的依赖范围一致，对于编译和测试有效，但在运行时无效。只是使用system范围依赖时必须通过systemPath元素显式地指定依赖文件的路径。由于此类依赖不是通过Maven仓库解析的，而且往往与本机系统绑定，可能造成构建的不可移植，因此应该谨慎使用，systemPath元素可以引用环境变量。例如： 

![0](https://note.youdao.com/yws/res/2318/6C873EEEF3114DB4973595BDAA66D798)

6. import(Maven 2.0.9及以上)：导入依赖范围。该依赖范围不会对三种classpath产生实际的影响。

上述除import以外的各种依赖范围与三种classpath的关系如下： 

![0](https://note.youdao.com/yws/res/2320/0C51D46ACFD54FD49ED4EB51A061FD4D)

4、传递性依赖和依赖范围

Maven的依赖是具有传递性的，比如A->B,B->C,那么A间接的依赖于C，这就是依赖的传递性，其中A对于B是第一直接依赖，B对于C是第二直接依赖，C为A的传递性依赖。

在平时的开发中，如果我们的项目依赖了spring-core，依赖范围是compile，spring-core又依赖了commons-logging，依赖范围也是compile，那么我们的项目对于commons-logging这一传递性依赖的范围也就是compile。第一直接依赖的范围和第二直接依赖的范围决定了传递性依赖的范围。我们通过下面这个表格来说明，其中最左边一栏是第一直接依赖，最上面那一栏为第二直接依赖。中间交叉的是传递性依赖范围。 

![0](https://note.youdao.com/yws/res/2319/05AB11E515D443A9838C85CF4E8C3E45)

例如：第一直接依赖范围是Test，第二直接依赖范围是Compile，那么传递性依赖的范围就是Test，大家可以根据这个表去判断。

仔细观察一下表格，我们可以发现这样的规律：

- 当第二直接依赖的范围是compile的时候，传递性依赖的范围与第一直接依赖的范围一致；
- 当第二直接依赖的范围是test的时候，依赖不会得以传递；
- 当第二直接依赖的范围是provided的时候，只传递第一直接依赖的范围也为provided的依赖，且传递性依赖的范围同样为provided；
- 当第二直接依赖的范围是runtime的时候，传递性依赖的范围与第一直接依赖的范围一致，但compile例外，此时传递性依赖的范围为runtime。

5、依赖调解

下面我们来思考这样一个问题，如果A->B->C->X(1.0),A->D-X(2.0),即A间接依赖X，我们可以看到有两条路径都依赖X，那么maven将会选择哪个版本的X？maven当中有一套自己的规则，我们来说明一下，maven传递性依赖的一些规则以及如何排除依赖冲突。

Maven里面对于传递性依赖有以下几个规则：

1. 最短路径原则：如果A对于依赖路径中有两个相同的jar包，那么选择路径短的那个包，路径最近者优先，上述会选X(2.0)。
2. 第一声明优先原则：如果A对于依赖路径中有两个相同的jar包，路径长度也相同，那么依赖写在前面的优先。例如：A->B->F(1.0),A->C->F(2.0)，会选F(1.0)。
3. 可选依赖不会被传递，如A->B，B->C，B->D，A对B直接依赖，B对C和D是可选依赖，那么在A中不会引入C和D。可选依赖通过optional元素配置，true表示可选。如果要在A项目中使用C或者D则需要显式地声明C或者D依赖。

6、排除依赖

传递性依赖会给项目隐式的引入很多依赖，这极大的简化了项目依赖的管理，但是有些时候这种特性也会带来问题，它可能会把我们不需要的jar包也引入到了工程当中，使项目结构变得更复杂。或者你想替换掉默认的依赖换成自己想要的jar包，这时候就需要用到依赖排除。

例如：

    org.springframework  

    spring-core  

    3.2.8  

               commons-logging          

               commons-logging  

1

2

3

4

5

6

7

8

9

10

11

例子中spring-core包依赖了commons-logging包，我们使用exclusions元素声明排除依赖，exclusions可以包含一个或者多个exclusion子元素，因此可以排除一个或者多个传递性依赖。需要注意的是，声明exclusions的时候只需要groupId和artifactId，而不需要version元素，这是因为只需要groupId和artifactId就能唯一定位依赖图中的某个依赖。换句话说，Maven解析后的依赖中，不可能出现groupId和artifactId相同，但是version不同的两个依赖。

7、把依赖归为一类

在项目开发中往往会引入同一个项目中的多个jar包，比如最常见的spring，如果我们项目中用到很多关于Spring Framework的依赖，它们分别是spring-core-3.2.8.RELEASE，spring-beans-3.2.8.RELEASE，spring-context-3.2.8.RELEASE，它们都是来自同一项目的不同模块。因此，所有这些依赖的版本都是相同的，而且可以预见，如果将来需要升级Spring Framework，这些依赖的版本会一起升级。因此，我们应该在一个唯一的地方定义版本，并且在dependency声明引用这一版本，这一在Spring Framework升级的时候只需要修改一处即可。

首先使用properties元素定义Maven属性，实例中定义了一个子元素，其值为3.2.8.RELEASE，有了这个属性定义之后，Maven运行的时候会将pom.xml中所有的${springframework.version}替换成实际的值：3.2.8.RELEASE。也就是可以使用$和{}的方式引用Maven的属性。然后将所有springframework依赖的版本替换成${springframework.version}这个样子，就和在Java代码中定义了一个不变的常量一样，以后要升级版本就只需要把这个值改了。

给大家一个完整的Maven配置实例，如果有在使用maven+spring+springMVC+Mybatis+Oracle数据库的朋友可以直接拿去改造成自己项目所需的父pom，配置如下：

   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

   4.0.0

​

   com.uidp

   UidpParent

   0.0.1-SNAPSHOT

   pom

​

   UidpParent

   http://maven.apache.org

​

       UTF-8

​

       http://192.168.0.70:8081/content/groups/public/

​

       3.1

       2.4

       2.9.1

       2.4.1

       2.7

​

       4.11

       10.2.0.4

       3.2.8.RELEASE

       3.2.2

       1.2.0

       5.1.25

       1.7.3

​

       1.4

       1.5.5

       1.2.2

​

       1.2.17

       1.7.5

       1.7.5

​

       2.3.19

​

       2.5.0

       1.9.7

​

       3.0.1

       2.2

       1.04

       1.8

       2.0.0

       2.6

​

​

       1.8.5

       1.4.9

       1.4.9

       1.4.9

​

​

​

               junit

               junit

               ${junit.version}

               test

​

               org.springframework

               spring-web

               ${springframework.version}

​

               org.springframework

               spring-webmvc

               ${springframework.version}

​

               org.springframework

               spring-beans

               ${springframework.version}

​

               org.springframework

               spring-context

               ${springframework.version}

​

               org.springframework

               spring-context-support

               ${springframework.version}

​

               org.springframework

               spring-core

               ${springframework.version}

​

               org.springframework

               spring-jdbc

               ${springframework.version}

​

               org.springframework

               spring-tx

               ${springframework.version}

​

               org.springframework

               spring-test

               ${springframework.version}

​

               org.springframework

               spring-expression

               ${springframework.version}

​

               org.springframework

               spring-aop

               ${springframework.version}

​

               org.mybatis

               mybatis

               ${mybatis.version}

​

               org.mybatis

               mybatis-spring

               ${mybatis-spring.version}

​

               mysql

               mysql-connector-java

               ${mysql-driver.version}

​

               com.oracle

               ojdbc14

               ${oracle.version}

​

               org.aspectj

               aspectjweaver

               ${aspectjweaver.version}

​

​

               commons-dbcp

               commons-dbcp

               ${commons-dbcp.version}

               commons-pool

               commons-pool

               ${commons-pool.version}

               commons-fileupload

               commons-fileupload

               ${commons-fileupload.version}

​

​

               log4j

               log4j

               ${log4j.version}

               org.slf4j

               slf4j-api

               ${slf4j-api.version}

               org.slf4j

               slf4j-log4j12

               ${slf4j-log4j12.version}

​

               org.freemarker

               freemarker

               ${freemarker.version}

​

​

               com.fasterxml.jackson.core

               jackson-core

               ${jackson-core.version}

               org.codehaus.jackson

               jackson-mapper-asl

               ${jackson-mapper-asl.version}

​

               javax.servlet

               javax.servlet-api

               ${javax.servlet-api.version}

               provided

​

               javax.servlet.jsp

               jsp-api

               ${jsp-api.version}

               provided

​

               com.googlecode

               kryo

               ${kryo.version}

​

               org.yaml

               snakeyaml

               ${snakeyaml.version}

​

               redis.clients

               jedis

               ${jedis.version}

​

               commons-lang

               commons-lang

               ${commons-lang.version}

​

​

               org.mockito

               mockito-core

               ${mockito-core.version}

               test

​

               org.powermock

               powermock-core

               ${powermock-core.version}

               test

​

               org.powermock

               powermock-api-mockito

               ${powermock-api-mockito.version}

               test

​

               org.powermock

               powermock-module-junit4

               ${powermock-module-junit4.version}

               test

​

​

           releases

           public

           http://59.50.95.66:8081/nexus/content/repositories/releases

           snapshots

           Snapshots

           http://59.50.95.66:8081/nexus/content/repositories/snapshots

​

               org.apache.maven.plugins

               maven-compiler-plugin

               ${maven-compiler-plugin.version}

                   1.7

                   1.7

​

               org.apache.maven.plugins

               maven-javadoc-plugin

               ${maven-javadoc-plugin.version}

​

​

               org.apache.maven.plugins

               maven-release-plugin

               ${maven-release-plugin.version}

​

               org.apache.maven.plugins

               maven-deploy-plugin

               ${maven-deploy-plugin.version}

                   true

​

           nexus

           nexus

           ${repository-url}

               true

               true

​

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

181

182

183

184

185

186

187

188

189

190

191

192

193

194

195

196

197

198

199

200

201

202

203

204

205

206

207

208

209

210

211

212

213

214

215

216

217

218

219

220

221

222

223

224

225

226

227

228

229

230

231

232

233

234

235

236

237

238

239

240

241

242

243

244

245

246

247

248

249

250

251

252

253

254

255

256

257

258

259

260

261

262

263

264

265

266

267

268

269

270

271

272

273

274

275

276

277

278

279

280

281

282

283

284

285

286

287

288

289

290

291

292

293

294

295

296

297

298

299

300

301

302

303

304

305

306

307

308

309

310

311

312

313

314

315

316

317

318

319

320

321

322

323

324

325

326

327

328

329

330

331

332

333

334

335

336

337

338

339

340

341

342

343

344

345

346

347

348

349

350

351

352

353

354

355

356

结束语：日月如梭，光阴似箭。不知不觉马上就要到2017年了，很多时候真的觉得不是我们年轻人不想做的更好，大多数时候是被前面的人给压迫的越来越油条了，所谓前人如此，却要求后人如何如何，其实想想也觉得蛮搞笑的。前人尽情的挥洒着智慧，玩着小心思不断的在压榨着年轻人，年轻人无奈的在这么个环境中挣扎求存。本以为离开了一个坑会迎来一个美好的未来，没想到的是不知不觉又跳入了一个更深的大坑，甚至有些坑还是隐形的，没有点特异功能还真不一定能够发现。不过话虽如此，作为新一代的年轻人，一定要经得过惊涛骇浪，何况是这点小风小浪。