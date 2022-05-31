## 此版本以停止维护，建议使用 动态转发+评论抽奖

## 前情
即 [B站动态转发抽奖脚本+教程](https://blog.csdn.net/Ikaros_521/article/details/102815938) 之后。
因b站数据包地址生成做了改动，猜测通过某种方式进行了加密后减去某一数值的方式。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507154904588.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
原抽奖脚本难以获取全部转发者信息。
ps：即使是手动翻页记录，也无法获取所有转发者信息。即：前面的信息已不被动态页面记录。
再次提供另一种方案，可以极大程度的提高抽奖的准确性和真实性（小人数）。
## 教程
### 1、访问页面
PC端打开浏览器，访问你的**动态抽奖页面**。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020050715530533.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
### 2、打开“检查”
鼠标**右键**，打开“检查”，一般的快捷键都是F12
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507155409254.png)
长这样，我们需要在console（控制台）下输入代码。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507155550287.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
## 3、手动加载所有可加载数据
点击“转发”图标，并一直滚动到没有新数据刷新为止！
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507155842357.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507155818229.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)

## 4、执行代码
### 获取可加载转发者的人数
在“检查”的控制台下输入以下命令，获取所有**可加载转发者的人数**。
```javascript
document.getElementsByClassName("user-name c-pointer").length
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507160055355.png)
可以看到，2k多的转发，但是实际加载到570的时候就不能加载新数据了。
### 将转发者信息存入集合（集合自带去重）
在“检查”的控制台下输入以下命令，定义一个集合，叫my_set。记得按**回车**啊！！！

```javascript
let my_set = new Set();
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507160304223.png)
循环将数据存入集合

```javascript
for(var i=0; i<document.getElementsByClassName("user-name c-pointer").length; i++)
{
	my_set.add(document.getElementsByClassName("user-name c-pointer")[i].innerText);
}
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507160420415.png)
可以看到得到的Set在下面已经打印了，我们点击Set左侧的小三角，展开。
可以看到，我们一共获取到 249条数据，已经去重后的转发者的昵称。可以继续展开查看。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507160545592.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
可以看到已经成功去重了。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507160830123.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
## 5、抽取幸运儿
### 直接生成随机数并打印幸运儿
在“检查”的控制台输入以下代码，my_set.size就是 Set的长度。可以改成数字，例如：249。
这个代码会生成 0到my_set.size-1 的整数。将这个整数做为Set转Array后的下标，打印结果。

```javascript
Array.from(my_set)[parseInt(Math.random()*(my_set.size),10)]
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020050716384822.png)


### 其他程序生成随机数进行抽取
将Set的长度记录下来，即 249名用户。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507160939816.png)
抽奖方式很简单，随便百度个随机数生成程序。例子：[http://www.99cankao.com/numbers/random-number-generator.php](http://www.99cankao.com/numbers/random-number-generator.php)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507161122136.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
注意是从 0开始，到Set长度减1。
生成结果 203 后，我们继续在“检查”下的控制台下执行代码，转Set为Array，打印其值。

```javascript
Array.from(my_set)[203]
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507163008917.png)
或是直接翻开来找。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507163117754.png)
## 6、一步到位 单人中奖

```javascript
console.log("程序开始运行");
console.log("定义集合存储数据");
let my_set = new Set();
var offset = document.getElementsByClassName("text-bar selected")[0].getElementsByClassName("text-offset")[0].innerText;
if(offset/20 > 25)
{
	offset = 500;
}
console.log("开始载入数据");
var my_loop;
function r()
{
	window.scroll(0, 1920*100);
}
function stop_r()
{
	clearInterval(my_loop);
}
function draw()
{
	for(var i=0; i<document.getElementsByClassName("user-name c-pointer").length; i++)
	{
		my_set.add(document.getElementsByClassName("user-name c-pointer")[i].innerText);
	}
	console.log("全部数据加载完毕");
	console.log("总共"+my_set.size+"名用户");
	console.log("中奖用户为:"+Array.from(my_set)[parseInt(Math.random()*(my_set.size),10)]);
	
}
my_loop = setInterval(r, 3000);
setTimeout(stop_r, 3000 * (parseInt(offset)/10 + 5));
setTimeout(draw, 3000 * (parseInt(offset)/10 + 6));


```
## 7、一步到位 多人中奖
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200707114126157.gif#pic_center)
```javascript
console.log("程序开始运行");
console.log("定义集合存储数据");
let my_set = new Set();
var offset = document.getElementsByClassName("text-bar selected")[0].getElementsByClassName("text-offset")[0].innerText;
if(offset/20 > 25)
{
	offset = 500;
}
console.log("开始载入数据");
var my_loop;
function r()
{
	window.scroll(0, 1920*100);
}
function stop_r()
{
	clearInterval(my_loop);
}
function draw()
{
	// 修改num为你需要抽奖的人数
	var num = 3;
	
	for(var i=0; i<document.getElementsByClassName("user-name c-pointer").length; i++)
	{
		my_set.add(document.getElementsByClassName("user-name c-pointer")[i].innerText);
	}
	
	let num_set = new Set();
	
	while(1)
	{
		if(num_set.size >= num)
			break;
		var lucky_num = parseInt(Math.random()*(my_set.size),10);
		num_set.add(lucky_num);
	}
	
	for(var i=0; i<num; i++)
	{
		console.log("中奖用户为:"+Array.from(my_set)[i]);
	}
	
}
my_loop = setInterval(r, 3000);
setTimeout(stop_r, 3000 * (parseInt(offset)/10 + 5));
setTimeout(draw, 3000 * (parseInt(offset)/10 + 6));


```

## 8、多人数二步到位脚本
自动翻页到底部时，再输入 draw(中奖数) 回车即可

```javascript
console.log("程序开始运行");
console.log("定义集合存储数据");
let my_set = new Set();

console.log("开始载入数据");
var my_loop;
function r()
{
	window.scroll(0, 1920*100);
}

function draw(num)
{
	clearInterval(my_loop);
	for(var i=0; i<document.getElementsByClassName("user-name c-pointer").length; i++)
	{
		my_set.add(document.getElementsByClassName("user-name c-pointer")[i].innerText);
	}
	console.log("全部数据加载完毕");
	console.log("总共"+my_set.size+"名用户");
	
	let num_set = new Set();
	
	while(1)
	{
		if(num_set.size >= num)
			break;
		var lucky_num = parseInt(Math.random()*(my_set.size),10);
		num_set.add(lucky_num);
	}
	
	for(var i=0; i<num; i++)
	{
		console.log("中奖用户为:"+Array.from(my_set)[i]);
	}
}
my_loop = setInterval(r, 3000);
// 当页面到底时， 输入 draw(你要抽的人的数量) 即可



```

