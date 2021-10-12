console.log("定义集合存储数据");
// 存储数据的集合
let name_set = new Set();
let id_set = new Set();

// 存储中奖者的数组
var lucky_index = new Array();
var lucky_name = new Array();
var lucky_id = new Array();

// 全局变量
var dynamic_id = "";
var oid = "";
var comment = "";
var lucky_num = 1;
var have_pic = 1;

// 获取动态的oid
function get_oid(dynamic_id)
{
    var url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + dynamic_id;
    var xmlhttp;
    if(window.XMLHttpRequest)
    {
        //code for IE7+,Firefox,Chrome,Opera,Safari
        xmlhttp = new XMLHttpRequest();
    }
    else
    {
        //code for IE6,IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function()
    {
        if(xmlhttp.readyState == 4)
        {
            if(xmlhttp.status == 200)
            {
                //将接收到的字符串存入str
                var str = xmlhttp.responseText;
                if(str.length == 0)
                {
                    return "";
                }

                //console.log(str);

                // 转为JSON对象
                var json = JSON.parse(str);
                console.log(json);

                // 解析json对象获取对应值
                oid = json["data"]["card"]["desc"]["rid"];
                comment = json["data"]["card"]["desc"]["comment"];
                var type = json["data"]["card"]["desc"]["type"];
                if(type == "2") have_pic = 1;
                else have_pic = 0;
                console.log("oid=" + oid);
                console.log("comment=" + comment);
            }
            else
            {
                //alert(xmlhttp.status);
            }

        }
        else
        {
            //alert(xmlhttp.readyState);
        }
    }
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

// 提前获取oid
function oid_init()
{
    var referer = window.location.href;
    // 动态页
    if("t" == referer.slice(8, 9))
    {
        var referer2 = referer.substr(0, referer.length - 2);
        dynamic_id = referer2.replace(/[^0-9]/ig,"");
        // console.log(dynamic_id);
        oid = get_oid(dynamic_id);

        //var temp = document.getElementsByClassName("text-offset")[1].innerText;

        //if(temp.indexOf("万") != -1)
        //{
        //    comment = 10000 * (parseFloat(temp.slice(1, temp.length - 2)) + 0.1);
        //}
        //else
        //{
        //    comment = parseInt(temp);
        //}
    }
    // 视频页
    else
    {
        oid = window.aid;
        console.log("oid=" + oid);
        comment = parseInt(document.getElementsByClassName("b-head")[0].getElementsByClassName("results")[0].innerText);
        console.log("comment=" + comment);
    }
}

oid_init();

// 睡眠多少毫秒
function sleep(ms)
{
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 抽奖函数 例如：get(3)
async function get(num)
{
	lucky_num = num;
    var referer = window.location.href;
    var type = 11;

    if("t" == referer.slice(8, 9) && have_pic == 1) type = 11;
    else if("t" == referer.slice(8, 9) && have_pic == 0) { type = 17; oid = dynamic_id;}
    else type = 1;

    if(0 == referer.length || 0 == comment.length)
    {
        alert("请填写完整信息！");
        return;
    }

    await sleep(1000);

    var first_time = Math.round(new Date());
    var time = 0;
    var url = "";
    // 结束标志位
    var end = 0;
    
    for(var i = 0; i <= Math.floor((comment-1)/20); i++)
    {
        if(0 == i)
        {
            url = "https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=" + type + "&oid=" + oid + "&mode=3&plat=1&_=" + (first_time + 1);
        }
        else
        {
            time = Math.round(new Date());
            url = "https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=" + (i + 1) + "&type=" + type + "&oid=" + oid + "&mode=3&plat=1&_=" + time;
        }

        if(i == Math.floor((comment-1)/20)) end = 1;
        else end = 0;
        get_data(url, end);

        // 睡眠500毫秒 0.5秒
        await sleep(500);
    }
}

// 获取幸运儿
function go(num)
{
	for(var i = 0; i < num; i++)
	{
		// 生成随机数，直接打印中奖者信息
		var random_num = parseInt(Math.random()*(name_set.size), 10);

        var id = Array.from(id_set)[random_num];
        var name = Array.from(name_set)[random_num];
        
        // 数据加入数组
        lucky_index.push(random_num);
        lucky_id.push(id);
        lucky_name.push(name);
        
		console.log(" ");
		console.log("中奖用户ID为:" + id);
		console.log("中奖用户名为:" + name);
		console.log(" ");

        id_set.delete(id);
        name_set.delete(name);
	}
	
	console.table([lucky_index, lucky_id, lucky_name]);
}

// 数据获取
function get_data(url, end)
{
    var xmlhttp;
    if(window.XMLHttpRequest)
    {
        //code for IE7+,Firefox,Chrome,Opera,Safari
        xmlhttp = new XMLHttpRequest();
    }
    else
    {
        //code for IE6,IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function()
    {
        if(xmlhttp.readyState == 4)
        {
            if(xmlhttp.status == 200)
            {
                //将接收到的字符串存入str
                var str = xmlhttp.responseText;
                if(str.length == 0)
                {
                    return;
                }

                // console.log(str);

                // 转为JSON对象
                var json = JSON.parse(str);
                console.log(json);

				// 可能为null
				if(json["data"].replies != null)
				{
					// 一组最多20个数据
					for(var i = 0; i < json["data"].replies.length; i++)
					{
						// 解析json对象获取对应值
						var mid = json["data"].replies[i]["member"]["mid"];
						var uname = json["data"].replies[i]["member"]["uname"];

						// 插入集合
						name_set.add(uname);
						id_set.add(mid);
					}
				}

                if(1 == end)
                {
                    console.log("数据获取完毕！开始调用go(中奖人数)进行抽奖。");
                    go(lucky_num);
                }
            }
            else
            {
                //alert(xmlhttp.status);
            }

        }
        else
        {
            //alert(xmlhttp.readyState);
        }
    }
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

console.log("贴入代码后，使用get(中奖人数)函数，进行数据获取和抽奖");
