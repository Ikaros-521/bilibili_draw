console.log("定义集合存储数据");
let name_set = new Set();
let id_set = new Set();

// 抽奖函数
function draw(type)
{
    var referer = $('#referer').val();
    var type = $('#type').val();
    var jquery = $('#jquery').val();
    var oid = $('#oid').val();
    var num = $('#num').val();
    var comment = $('#comment').val();

    if(0 == referer.length || 0 == jquery.length || 0 == oid.length || 0 == num.length || 0 == comment.length)
    {
        alert("请填写完整信息！");
        return;
    }

    if(21 != jquery.length)
    {
        alert("jQuery后的21位字符填写有误！");
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

// 数据获取
function get_data(referer, url)
{
    var obj = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
    obj.Open("GET", url, false);
    // obj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    obj.setRequestHeader("Referer", referer);
    obj.Send();
    var str = obj.responseText;
    console.log(str);
    $('#area').val(str);
}

// 数据获取
function get_data2(referer, url)
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

                // 转为JSON对象
                var json = JSON.parse(str);
                console.log(json);
                // var address = json["regeocode"]["formatted_address"];
                // console.log(address);
                // document.getElementById("address").innerText = "你的地址大概是" + address;

                
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
    xmlhttp.setRequestHeader("referer", referer);
    xmlhttp.send();
}