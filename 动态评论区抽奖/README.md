## 此版本以停止维护，建议使用 动态转发+评论抽奖

动态转发抽奖可以参考我其他的2篇文章
[JS实现b站动态转发抽奖（小人数）新方案讲解](https://www.bilibili.com/read/cv5957946)
[B站动态转发抽奖教程(python)](https://www.bilibili.com/read/cv3911862)
## 视频演示

[video(video-2LhA8ORV-1590671128110)(type-bilibili)(url-https://player.bilibili.com/player.html?aid=840757507)(image-https://ss.csdn.net/p?http://i1.hdslb.com/bfs/archive/9bada3fad44e2de0bcd6606980d271e73846bd89.jpg)(title-JS实现b站动态评论区抽奖视频演示)]

## 前期
测试页面链接：https://t.bilibili.com/394309046095520212?tab=2
动态评论数量为**226**，这个数量是**全楼层的评论数量**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200528143433420.png)
共分为**8**页展示，一页首层人数**20**人
![在这里插入图片描述](https://img-blog.csdnimg.cn/202005281435009.png)
## 教程
### 1、访问页面
PC端打开浏览器，访问你的**动态抽奖页面**。点在评论上，不用点转发。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200528144203974.png)
### 2、打开“检查”
鼠标**右键**，打开“检查”，一般的快捷键都是F12
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200507155409254.png)
长这样，我们需要在console（控制台）下输入代码。
### 3、贴入代码
**评论记得翻到第一页!!!**超人性化设计，一步到位，还会打印所有用户名和ID，如果不需要可以注释掉打印代码，就是下面那些console.log代码，注释使用 **//** ,不会的可以自行百度JS注释。
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
实际运行测试如下，如果评论人数较多或者网速较慢，请修改最后一行 `my_loop = setInterval(draw, 1000);` 把这里的1000调大，1000代表1s，这是自动翻页的时间。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200528144916686.gif)
10页数据加载完毕后，这就是中奖者信息
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200528145144888.png)
