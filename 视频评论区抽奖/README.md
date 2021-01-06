## 前言
如有 动态评论区 抽奖需要，可以参考：[JS实现b站动态抽奖“公平”方案——动态+转发](https://blog.csdn.net/Ikaros_521/article/details/106483311)
因为转发抽奖只支持小人数，如果人少，可以使用：[JS实现b站动态转发抽奖（小人数）新方案讲解](https://blog.csdn.net/Ikaros_521/article/details/105974275)
[B站动态转发抽奖脚本+教程](https://blog.csdn.net/Ikaros_521/article/details/102815938)
## 视频讲解

[video(video-xkiJGol3-1596864652942)(type-bilibili)(url-https://player.bilibili.com/player.html?aid=884157550)(image-https://ss.csdn.net/p?http://i0.hdslb.com/bfs/archive/633618e427e39cb56b577306b9d9cd18adcad19d.jpg)(title-B站“视频评论区”抽奖 讲解【JS】)]
[传送门](https://www.bilibili.com/video/BV1yK4y1v7wB)
## 正文
### 1.打开视频页面
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200808133328468.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
### 2.鼠标右键打开“检查”工具 或 按F12
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200808133417692.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
### 3.直接贴入代码，直捣黄龙
代码如下，复制粘贴进入“console”，然后回车

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
    var len = document.getElementsByClassName("list-item reply-wrap").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		var id = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
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
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200808133813426.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
### 4.等待结果即可
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200808133928181.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)
ok 结束。
## 抽取多人版本
### 1.2 同理 控制台贴入代码，页数加载完后 然后输入 go(人数) 回车即可

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
	var len = document.getElementsByClassName("list-item reply-wrap").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		var id = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
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
	if(num > name_map.size)
	{
		console.log("？？？搞事情？？？，一共都没那么多人");
		return;
	}
	
	var arr = [];
	var lucky_num;
	for(var i = 0; i < num; i++)
	{
		lucky_num = parseInt(Math.random()*(name_map.size), 10);
		if (arr.toString().indexOf(lucky_num) > -1) {
			i--;
			continue;
		}
		else
		{
			arr.push(lucky_num);
		}

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
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021010517221629.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)


### 1.1 同理 控制台贴入代码，页数加载完后 然后输入 go() 回车即可

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
	var len = document.getElementsByClassName("list-item reply-wrap").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		var id = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
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
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200808210128739.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0lrYXJvc181MjE=,size_16,color_FFFFFF,t_70)

