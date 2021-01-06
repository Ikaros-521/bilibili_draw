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


