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

