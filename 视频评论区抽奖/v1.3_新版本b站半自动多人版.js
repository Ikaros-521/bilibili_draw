console.log("程序开始运行");
console.log("定义集合存储数据");
let name_set = new Set();
let id_set = new Set();
console.log("开始载入数据");

// 循环变量
var my_loop;
// 下滑延时 500毫秒 网速/加载速度较慢的朋友们最好放慢速度 提高准确性
var r_time = 500;

// 评论数
var comment_num = 1;
if(document.getElementsByClassName("b-head-t")[0].innerText.indexOf("万") != -1)
{
	comment_num = 10000 * (parseInt(document.getElementsByClassName("b-head-t")[0].innerText) + 1);
}
else
{
	comment_num = parseInt(document.getElementsByClassName("b-head-t")[0].innerText);
}

// 下滑
function r()
{
	window.scroll(0, 1920*comment_num);
	// 没有评论后自动停止下滑 并 抽奖
	if(document.getElementsByClassName("loading-state")[0].innerText == "没有更多评论")
	{
		// 停止下滑循环
		stop_r();
		// 抽奖函数
		draw();
	}
}

// 停止下滑循环
function stop_r()
{
	clearInterval(my_loop);
}

// 抽奖函数
function draw()
{
    // 循环次数
    var len = document.getElementsByClassName("con").length;
	for(var i=0; i<len; i++)
	{
		var name = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].innerText;
		var id = document.getElementsByClassName("list-item reply-wrap")[i].getElementsByClassName("con")[0].getElementsByClassName("user")[0].getElementsByTagName("a")[0].getAttributeNode("data-usercard-mid").value;
		// console.log(name+"，加入集合");
		name_set.add(name);
		id_set.add(id);
	}
	
	console.log("全部数据加载完毕");
	console.log("总共"+name_set.size+"名用户");
	
	// 这就是注释
	//return false;
}

// 获取幸运儿
function go(num)
{
	for(var i=0; i<num; i++)
	{
		// 生成随机数，直接打印中奖者信息
		var lucky_num = parseInt(Math.random()*(name_set.size), 10);

		console.log(" ");
		console.log("中奖用户ID为:"+Array.from(id_set)[lucky_num]);
		console.log("中奖用户名为:"+Array.from(name_set)[lucky_num]);
		console.log(" ");
	}
}

// 开始自动下滑 r_time毫秒一次
my_loop = setInterval(r, r_time);

// 全部数据加载完毕后，使用 go(中奖数) 抽取中奖者