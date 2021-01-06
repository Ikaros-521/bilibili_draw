## 视频演示+讲解
[video(video-s7fQpSk6-1591059362023)(type-bilibili)(url-https://player.bilibili.com/player.html?aid=968279192)(image-https://ss.csdn.net/p?http://i2.hdslb.com/bfs/archive/0c312ef200f06b3489d8517a109267cca987462a.jpg)(title-b站“动态抽奖” 较公平方案 讲解)]

[传送门](https://www.bilibili.com/video/bv1Zp4y1Q7yH)
## 前期
因为非官方途径无法获取全部的转发人员信息，但评论的人员信息可以全部获取（暂时看来一百多页加载都没有问题）
参考链接：[JS实现b站动态转发抽奖（小人数）新方案讲解](https://blog.csdn.net/Ikaros_521/article/details/105974275)
[JS实现b站动态评论区抽奖（含去重）](https://blog.csdn.net/Ikaros_521/article/details/106404483)
当然还有一种比较费劲的方式就是**发起抽奖到开奖为止**，后台一直保持数据爬取（服务器），将数据整合后最后抽取中奖者的方式。
## 公平抽奖实现方案讲解
因为评论获取数是全的，那么只需要转发+评论双管齐下，就可以通过在评论区抽奖，再对中奖用户的动态继续检索，中奖者会有评论时间，当天查看他的动态是否有转发抽奖动态，从而判断其资格。
### 抽奖代码
打开“动态”，保持评论第一页，鼠标右键打开“检查”（或者按F12），来到“console”，贴入代码运行即可。
代码如下：

```javascript
console.log("程序开始运行");
console.log("定义集合存储数据");
let name_set = new Set();
let id_set = new Set();
console.log("开始载入数据");
var page = 1;
var my_loop;

// 抽奖函数
function draw()
{
    // 循环次数
	var len = document.getElementsByClassName("con").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		console.log(name+"，加入集合");
		name_set.add(name);
		var id = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
		id_set.add(id);
	}
	console.log("第"+page+"页数据存入Set完毕");
	if(null != document.getElementsByClassName("next")[0])
	{
		page++;
		console.log("自动翻页...");
		document.getElementsByClassName("next")[0].click();
		//return true;
	}
	else
	{
		console.log("全部数据加载完毕");
		console.log("总共"+name_set.size+"名用户");
		// 生成随机数，直接打印中奖者信息
		var lucky_num = parseInt(Math.random()*(name_set.size),10);
		console.log("中奖用户ID为:"+Array.from(id_set)[lucky_num]);
		console.log("中奖用户名为:"+Array.from(name_set)[lucky_num]);
		console.log("中奖者大概位于 第" +parseInt(lucky_num/20+1)+ "页");
		clearInterval(my_loop);
		// 这就是注释
		//return false;
	}
}

// 定时调用函数
my_loop = setInterval(draw, 1500);

```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200601222748733.gif#pic_center)
### 相关问题
最后一行```my_loop = setInterval(draw, 1500);```，这里的1500代表毫秒数，你可以修改这个数字来实现延长自动翻页时间差，因为翻页加载数据会受网络影响，网速慢的话，数据加载慢，可能会丢失数据，所以可以相对的延长翻页时间。
如果打印的内容不需要，可以注释掉相关 `console.log`代码，注释就是在这个代码前加 `//`，这2个反斜杠就是注释。注释后就不会打印了。

### 美化代码

```javascript
// 获取时间
function get_date() {
    var date = new Date();
    var currentDate = "[" + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds() + "] ";
    return currentDate;
}

console.log(get_date() + "程序开始运行");
console.log(get_date() + "定义集合存储数据(自动去重)");
let name_set = new Set();
let id_set = new Set();
console.log(get_date() + "开始载入数据");
var page = 1;
var my_loop;

// 抽奖函数
function draw()
{
    // 循环次数
	var len = document.getElementsByClassName("con").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		//console.log(name+"，加入集合");
		name_set.add(name);
		var id = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
		id_set.add(id);
	}
	console.log(get_date() + "第"+page+"页数据存入Set完毕");
	if(null != document.getElementsByClassName("next")[0])
	{
		page++;
		//console.log("自动翻页...");
		document.getElementsByClassName("next")[0].click();
		//return true;
	}
	else
	{
		console.log(get_date() + "全部数据加载完毕");
		console.log(get_date() + "总共"+name_set.size+"名用户");
		// 生成随机数，直接打印中奖者信息
		var lucky_num = parseInt(Math.random()*(name_set.size),10);
		console.log("中奖用户ID为:"+Array.from(id_set)[lucky_num]);
		console.log("中奖用户名为:"+Array.from(name_set)[lucky_num]);
		console.log("中奖者大概位于 第" +parseInt(lucky_num/20+1)+ "页");
		clearInterval(my_loop);
		// 这就是注释
		//return false;
	}
}

// 定时调用函数
my_loop = setInterval(draw, 1500);


```

### 2.0版本，获取准确页数，使用Map存储

```javascript
// 获取时间
function get_date() {
    var date = new Date();
	var h = date.getHours();
	var m = date.getMinutes();
	var s = date.getSeconds();
	h = h < 10 ? ('0' + h) : h;
	m = m < 10 ? ('0' + m) : m;
	s = s < 10 ? ('0' + s) : s;
    var currentDate = "[" + h + ":" + m + ":" + s + "] ";
    return currentDate;
}

// 从map获取下标为index的键
function get_map_key(map, index)
{
	var i = 0;
	for (var [key, value] of map) {
		if(i == index)
		{
			return key;
		}
		i++;
	}
}

// 从map获取下标为index的值
function get_map_value(map, index)
{
	var i = 0;
	for (var [key, value] of map) {
		if(i == index)
		{
			return value;
		}
		i++;
	}
}

// 遍历map
function get_map(map)
{
	for (var [key, value] of map) {
		console.log(key + " = " + value);
	}
}

console.log(get_date() + "程序开始运行");
console.log(get_date() + "定义图存储数据(自动去重)");
let name_map = new Map();
let id_map = new Map();
console.log(get_date() + "开始载入数据");
var page = 1;
var my_loop;

// 抽奖函数
function draw()
{
    // 循环次数
	var len = document.getElementsByClassName("con").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		var id = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
		//console.log(name+"，加入图");
		name_map.set(name, page);
		id_map.set(id, page);
	}
	console.log(get_date() + "第"+page+"页数据存入Map完毕");
	if(null != document.getElementsByClassName("next")[0])
	{
		page++;
		//console.log("自动翻页...");
		document.getElementsByClassName("next")[0].click();
		//return true;
	}
	else
	{
		console.log(get_date() + "全部数据加载完毕");
		console.log(get_date() + "总共" + name_map.size + "名用户");
		// 生成随机数，直接打印中奖者信息
		var lucky_num = parseInt(Math.random()*(name_map.size),10);
		console.log(" ");
		console.log("中奖用户ID为:" + get_map_key(id_map, lucky_num));
		console.log("中奖用户名为:" + get_map_key(name_map, lucky_num));
		console.log("中奖者位于页:" + get_map_value(name_map, lucky_num));
		console.log(" ");
		console.log("程序运行结束");
		clearInterval(my_loop);
		// 这就是注释
		//return false;
	}
}

// 定时调用函数
my_loop = setInterval(draw, 1500);


```

### 2.1版本 新增多次抽奖功能
使用方式是 贴入代码后，等待翻页完毕，数据加载完毕后，调用 `go()`函数进行抽奖。

```javascript
// 获取时间
function get_date() {
    var date = new Date();
	var h = date.getHours();
	var m = date.getMinutes();
	var s = date.getSeconds();
	h = h < 10 ? ('0' + h) : h;
	m = m < 10 ? ('0' + m) : m;
	s = s < 10 ? ('0' + s) : s;
    var currentDate = "[" + h + ":" + m + ":" + s + "] ";
    return currentDate;
}

// 从map获取下标为index的键
function get_map_key(map, index)
{
	var i = 0;
	for (var [key, value] of map) {
		if(i == index)
		{
			return key;
		}
		i++;
	}
}

// 从map获取下标为index的值
function get_map_value(map, index)
{
	var i = 0;
	for (var [key, value] of map) {
		if(i == index)
		{
			return value;
		}
		i++;
	}
}

// 遍历map
function get_map(map)
{
	for (var [key, value] of map) {
		console.log(key + " = " + value);
	}
}

console.log(get_date() + "程序开始运行");
console.log(get_date() + "定义图存储数据(自动去重)");
let name_map = new Map();
let id_map = new Map();
console.log(get_date() + "开始载入数据");
var page = 1;
var my_loop;

// 抽奖函数
function draw()
{
    // 循环次数
	var len = document.getElementsByClassName("con").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		var id = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
		//console.log(name+"，加入图");
		name_map.set(name, page);
		id_map.set(id, page);
	}
	console.log(get_date() + "第"+page+"页数据存入Map完毕");
	if(null != document.getElementsByClassName("next")[0])
	{
		page++;
		//console.log("自动翻页...");
		document.getElementsByClassName("next")[0].click();
		//return true;
	}
	else
	{
		console.log(get_date() + "全部数据加载完毕");
		console.log(get_date() + "总共" + name_map.size + "名用户");
		clearInterval(my_loop);
		// 这就是注释
		//return false;
	}
}

function go()
{
	var lucky_num = parseInt(Math.random()*(name_map.size),10);

	console.log(" ");
	console.log("中奖用户ID为:" + get_map_key(id_map, lucky_num));
	console.log("中奖用户名为:" + get_map_key(name_map, lucky_num));
	console.log("中奖者位于页:" + get_map_value(name_map, lucky_num));
	console.log(" ");
}

// 定时调用函数
my_loop = setInterval(draw, 1500);



```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200704131749118.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
### 2.2版本 多次抽奖功能（半自动化）
使用方式是 贴入代码后，等待翻页完毕，数据加载完毕后，调用 `go(抽奖数)`函数进行抽奖。

```javascript
// 获取时间
function get_date() {
    var date = new Date();
	var h = date.getHours();
	var m = date.getMinutes();
	var s = date.getSeconds();
	h = h < 10 ? ('0' + h) : h;
	m = m < 10 ? ('0' + m) : m;
	s = s < 10 ? ('0' + s) : s;
    var currentDate = "[" + h + ":" + m + ":" + s + "] ";
    return currentDate;
}

// 从map获取下标为index的键
function get_map_key(map, index)
{
	var i = 0;
	for (var [key, value] of map) {
		if(i == index)
		{
			return key;
		}
		i++;
	}
}

// 从map获取下标为index的值
function get_map_value(map, index)
{
	var i = 0;
	for (var [key, value] of map) {
		if(i == index)
		{
			return value;
		}
		i++;
	}
}

// 遍历map
function get_map(map)
{
	for (var [key, value] of map) {
		console.log(key + " = " + value);
	}
}

console.log(get_date() + "程序开始运行");
console.log(get_date() + "定义图存储数据(自动去重)");
let name_map = new Map();
let id_map = new Map();
console.log(get_date() + "开始载入数据");
var page = 1;
var my_loop;

// 抽奖函数
function draw()
{
    // 循环次数
    var len = document.getElementsByClassName("con").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		var id = document.getElementsByClassName("con")[i].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
		//console.log(name+"，加入图");
		name_map.set(name, page);
		id_map.set(id, page);
	}
	console.log(get_date() + "第"+page+"页数据存入Map完毕");
	if(null != document.getElementsByClassName("next")[0])
	{
		page++;
		//console.log("自动翻页...");
		document.getElementsByClassName("next")[0].click();
		//return true;
	}
	else
	{
		console.log(get_date() + "全部数据加载完毕");
		console.log(get_date() + "总共" + name_map.size + "名用户");
		clearInterval(my_loop);
		// 这就是注释
		//return false;
	}
}

function go(num)
{
	for(var i=0; i<num; i++)
	{
		var lucky_num = parseInt(Math.random()*(name_map.size),10);

		console.log(" ");
		console.log("中奖用户ID为:" + get_map_key(id_map, lucky_num));
		console.log("中奖用户名为:" + get_map_key(name_map, lucky_num));
		console.log("中奖者位于页:" + get_map_value(name_map, lucky_num));
		console.log(" ");
	}
}

// 定时调用函数
my_loop = setInterval(draw, 1500);

```
例如抽3个人
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200910165253335.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70#pic_center)


