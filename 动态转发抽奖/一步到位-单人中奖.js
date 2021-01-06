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