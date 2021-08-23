console.log("定义集合存储数据");
let name_set = new Set();
let id_set = new Set();

var referer = "";
var oid = "";
var comment = "";
var num = "";
var jquery = "";
var type;

// 抽奖函数
function draw()
{
    referer = $('#referer').val();
    oid = "";
    comment = $('#comment').val();
    num = $('#num').val();
    jquery = $('#jquery').val();

    if(0 == referer.length || 0 == jquery.length || 0 == num.length || 0 == comment.length)
    {
        alert("请填写完整信息！");
        return;
    }

    var first_time = Math.round(new Date());
    var time = 0;
    var url = "";
    for(var i = 0; i <= comment/20; i++)
    {
        if(0 == i)
        {
            url = "https://api.bilibili.com/x/v2/reply/main?callback=jQuery" + jquery + "_" +
            (first_time + i) + "&jsonp=jsonp&next=0&type=" + type + "&oid=" + oid + "&mode=3&plat=1&_=" + (first_time + 1);
        }
        else
        {
            time = Math.round(new Date());
            url = "https://api.bilibili.com/x/v2/reply/main?callback=jQuery" + jquery + "_" +
                (first_time + i) + "&jsonp=jsonp&next=0&type=" + type + "&oid=" + oid + "&mode=3&plat=1&_=" + time;
        }

        get_data(referer, url);
    }
}

// 获取动态的oid
function get_oid(dynamic_id)
{
    var url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + dynamic_id;
    var obj = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
    obj.Open("GET", url, false);
    // obj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    obj.setRequestHeader("Referer", referer);
    obj.Send();
    var str = obj.responseText;
    console.log(str);

    // 转为JSON对象
    var json = JSON.parse(str);
    console.log(json);

    // 解析json对象获取对应值
    oid = json["data"]["card"]["desc"]["rid"];
    console.log("oid=" + oid);
}

// 提前获取oid
function oid_init()
{
    // 动态页
    if("t" == referer.slice(8, 9))
    {
        var referer2 = referer.substr(0, referer.length - 2);
        var dynamic_id = referer2.replace(/[^0-9]/ig,"");
        // console.log(dynamic_id);
        oid = get_oid(dynamic_id);  
    }
}

// 抽奖函数 例如：get(331030722370851298386)
function get(jquery)
{
    type = 11;

    if("t" == referer.slice(8, 9)) type = 11;
    else type = 1;

    if(0 == referer.length || 0 == jquery.length || 0 == comment.length)
    {
        alert("请填写完整信息！");
        return;
    }

    var first_time = Math.round(new Date());
    var time = 0;
    var url = "";
    for(var i = 0; i <= (comment-1)/20; i++)
    {
        if(0 == i)
        {
            url = "https://api.bilibili.com/x/v2/reply/main?callback=jQuery" + jquery + "_" +
            (first_time + i) + "&jsonp=jsonp&next=0&type=" + type + "&oid=" + oid + "&mode=3&plat=1&_=" + (first_time + 1);
        }
        else
        {
            time = Math.round(new Date());
            url = "https://api.bilibili.com/x/v2/reply/main?callback=jQuery" + jquery + "_" +
                (first_time + i) + "&jsonp=jsonp&next=" + (i + 1) + "&type=" + type + "&oid=" + oid + "&mode=3&plat=1&_=" + time;
        }

        // 结束标志位
        var end = 0;
        if(i == (comment-1)/20) end = 1;
        else end = 0;
        get_data(url, end);

        // 睡眠500毫秒 0.5秒
        setTimeout("console.log('延时500ms')", 500);
    }

    console.log("数据获取完毕！可以调用go(中奖人数)进行抽奖。");
}

// 数据获取
function get_data(url, end)
{
    var obj = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
    obj.Open("GET", url, false);
    // obj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    obj.setRequestHeader("Referer", referer);
    obj.Send();
    var str = obj.responseText;

    var len = str.length;
    var str2 = str.slice(str.indexOf('(') + 1, len - 1);
    // console.log(str2);

    // 转为JSON对象
    var json = JSON.parse(str2);
    console.log(json);

    // 一组20个数据
    for(var i = 0; i < 20; i++)
    {
        // 解析json对象获取对应值
        var mid = json["data"].replies[i]["member"]["mid"];
        var uname = json["data"].replies[i]["member"]["uname"];

        // 插入集合
        name_set.add(uname);
        id_set.add(mid);
    }

    if(1 == end)
    {
        console.log("数据获取完毕！可以调用go(中奖人数)进行抽奖。");
        go(num);
    }
}

// 获取幸运儿
function go(num)
{
	for(var i = 0; i < num; i++)
	{
		// 生成随机数，直接打印中奖者信息
		var lucky_num = parseInt(Math.random()*(name_set.size), 10);

        var id = Array.from(id_set)[lucky_num];
        var name = Array.from(name_set)[lucky_num];
		console.log(" ");
		console.log("中奖用户ID为:" + id);
		console.log("中奖用户名为:" + name);
		console.log(" ");

        $('#area').val($('#area').val() + "中奖用户ID为:" + id + "\n中奖用户名为:" + name + "\n\n");

        id_set.delete(id);
        name_set.delete(name);
	}
}