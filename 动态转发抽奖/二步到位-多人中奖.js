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