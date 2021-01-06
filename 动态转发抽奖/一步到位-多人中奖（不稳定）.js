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


