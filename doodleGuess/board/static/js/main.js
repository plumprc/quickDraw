let type = ['埃菲尔铁塔', '中国长城', '蒙娜丽莎', '飞机', '闹钟', '救护车', '天使', '动物迁徙', '蚂蚁', '铁砧', '苹果', '臂',
    '芦笋', '斧头', '背包', '香蕉', '绷带', '谷仓', '棒球棒', '棒球', '篮子', '篮球', '蝙蝠', '浴缸', '海滩', '熊',
    '胡须', '床', '蜜蜂', '皮带', '长凳', '自行车', '双筒望远镜', '鸟', '生日蛋糕', '黑莓', '蓝莓', '书', '回力标',
    '瓶盖', '蝴蝶结', '手镯', '脑', '面包', '桥', '西兰花', '扫帚', '水桶', '推土机', '公共汽车', '灌木', '蝴蝶',
    '仙人掌', '蛋糕', '计算器', '日历', '骆驼', '照相机', '伪装', '篝火', '蜡烛', '大炮', '独木舟', '汽车', '胡萝卜',
    '城堡', '猫', '吊扇', '手机', '大提琴', '椅子', '吊灯', '教堂', '圆圈', '单簧管', '时钟', '云', '咖啡杯', '指南针',
    '计算机', '曲奇饼', '冷却器', '沙发', '奶牛', '蟹', '蜡笔', '鳄鱼', '王冠', '游轮', '杯子', '钻石', '洗碗机', '跳水板',
    '狗', '海豚', '甜甜圈', '门', '恶龙', '梳妆台', '钻头', '鼓', '鸭子', '哑铃', '耳朵', '肘部', '大象', '信封', '橡皮擦',
    '眼睛', '眼镜', '脸', '风扇', '羽毛', '栅栏', '手指', '消防栓', '壁炉', '消防车', '鱼', '火烈鸟', '手电筒', '人字拖',
    '落地灯', '花', '飞碟', '脚', '叉子', '青蛙', '煎锅', '灌溉橡皮管', '花园', '长颈鹿', '山羊胡', '高尔夫俱乐部', '葡萄',
    '草', '吉他', '汉堡包', '铁锤', '手', '竖琴', '帽子', '耳机', '刺猬', '直升机', '头盔', '六角形', '冰球', '曲棍球棒',
    '马', '医院', '热气球', '热狗', '热水浴缸', '沙漏', '室内盆栽', '房子', '飓风', '冰淇淋', '夹克', '监狱', '袋鼠',
    '钥匙', '键盘', '膝部', '梯子', '灯笼', '笔记本电脑', '叶子', '腿', '灯泡', '灯塔', '闪电', '线', '狮子', '唇膏',
    '龙虾', '棒棒糖', '邮箱', '地图', '标记', '火柴', '扩音器', '美人鱼', '麦克风', '微波炉', '猴子', '月亮', '蚊子',
    '摩托车', '山', '老鼠', '小胡子', '嘴巴', '马克杯', '蘑菇', '指甲', '项链', '鼻子', '海洋', '八角形', '章鱼', '洋葱',
    '烤箱', '猫头鹰', '油漆罐', '画笔', '棕榈树', '熊猫', '裤子', '回形针', '降落伞', '鹦鹉', '护照', '花生', '梨', '豌豆',
    '铅笔', '企鹅', '钢琴', '皮卡车', '相框', '猪', '枕头', '菠萝', '披萨', '钳子', '警车', '池塘', '水塘', '冰棒', '明信片',
    '马铃薯', '电源插座', '钱包', '兔子', '浣熊', '收音机', '雨', '彩虹', '耙子', '遥控器', '犀牛', '河', '过山车', '溜冰鞋',
    '帆船', '三明治', '锯', '萨克斯', '校车', '剪刀', '蝎子', '螺丝刀', '海龟', '跷跷板', '鲨鱼', '羊', '鞋', '短裤', '铲子',
    '下沉', '滑板', '颅骨', '摩天大楼', '睡袋', '笑脸', '蜗牛', '蛇', '通气管', '雪花', '雪人', '足球', '短袜', '快艇',
    '蜘蛛', '勺子', '电子表格', '广场', '蠕动', '松鼠', '楼梯', '星星', '牛排', '立体声音响', '听诊器', '缝针', '停车标志',
    '火炉', '草莓', '路灯', '菜豆', '潜艇', '手提箱', '太阳', '天鹅', '毛衣', '摆盘', '剑', 't恤衫', '桌子', '茶壶',
    '玩具熊', '电话', '电视', '网球拍', '帐篷', '老虎', '烤面包机', '脚趾', '厕所', '牙齿', '牙刷', '牙膏', '龙卷风',
    '拖拉机', '红绿灯', '火车', '树', '三角形', '长号', '卡车', '小号', '雨伞', '内衣', '厢式货车', '花瓶', '小提琴',
    '洗衣机', '西瓜', '滑水', '鲸鱼', '轮', '风车', '酒瓶', '酒杯', '腕表', '瑜伽', '斑马', '之字形'];

let aim = "";
let aims = [];
let aims_pred = [false, false, false, false, false, false];
let round = 1;
let jump = false;

function canvas2svg(draw) {
    let xmin = 1000, xmax = 0, ymin = 1000, ymax = 0;
    let path = "";
    for (let seg = 0; seg < draw.length; seg++) {
        for (let p = 0; p < draw[seg].length; p++) {
            xmin = Math.min(xmin, draw[seg][p].x);
            xmax = Math.max(xmax, draw[seg][p].x);
            ymin = Math.min(ymin, draw[seg][p].y);
            ymax = Math.max(ymax, draw[seg][p].y);
        }
    }
    let x_scale = xmax - xmin;
    let y_scale = ymax - ymin;

    if (x_scale > y_scale) {
        if (x_scale / y_scale >= 2) {
            y_scale = y_scale * 120 / x_scale;
            x_scale = 120;
        } else {
            x_scale = x_scale * 60 / y_scale;
            y_scale = 60;
        }
    } else {
        x_scale = x_scale * 60 / y_scale;
        y_scale = 60;
    }

    let x_m = (xmin + xmax) / 2 / (xmax - xmin) * x_scale;
    let y_m = (ymin + ymax) / 2 / (ymax - ymin) * y_scale;

    for (let seg = 0; seg < draw.length; seg++) {
        path += 'M' + (draw[seg][0].x / (xmax - xmin) * x_scale - x_m + 65)
            + ' ' + (draw[seg][0].y / (ymax - ymin) * y_scale - y_m + 35) + ' ';
        for (let p = 1; p < draw[seg].length; p++) {

            path += 'L' + (draw[seg][p].x / (xmax - xmin) * x_scale - x_m + 65)
                + ' ' + (draw[seg][p].y / (ymax - ymin) * y_scale - y_m + 35) + ' ';
        }
    }
    return path;
}

function predict(drawing) {
    if (drawing.length === 0)
        console.info("您还没有作画哦~~");
    else {
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/board/",
            data: JSON.stringify(drawing),
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function (info) {
                // console.log("success");
                $("#pred").html(info);
                info = info.split(" ");
                if (info[0] === aim) {
                    aims_pred[round - 2] = true;
                    let audio = document.getElementById("audio");
                    $("#pred").html("bingo! " + aim);
                    audio.play();
                    $("#button-skip").click();
                }
            },
        });
    }
}

function init() {
    $("#challengetext-level").html("涂鸦：" + round + "/6");
    round++;
    aim = type[Math.round(Math.random() * 339)];
    aims.push(aim);
    $("#challengetext-word").html(aim);
    $("#topbar-text").html("画出：" + aim);
    $("#newround-card").toggleClass("visible");
    $(".text-blink").css("color", "black");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setCanvasBg('white');
    draw = [];
    draw_list = [];
    $("#pred").html("。。。。。。");
}

function check() {
    let cnt = 0;
    for (let x = 0; x < aims.length; x++) {
        if (aims_pred[x]) {
            $("#type" + (x + 1)).html("√ " + aims[x]);
            cnt++;
        } else $("#type" + (x + 1)).html("✕ " + aims[x]);
    }
    if(cnt >= 5){
        $("#timesup-title").html("画的很棒！(≧ω≦)");
        $("#timesup-subtitle").html("AI 猜出了您画的 " + cnt + " 幅涂鸦~");
    }
    else if(cnt >= 3){
        $("#timesup-title").html("画的不错！(*^▽^*)");
        $("#timesup-subtitle").html("AI 猜出了您画的 " + cnt + " 幅涂鸦~");
    }
    else{
        $("#timesup-title").html("继续加油！ヾ(°∀°ゞ)");
        $("#timesup-subtitle").html("AI 猜出了您画的 " + cnt + " 幅涂鸦~");
    }
    aims = [];
    aims_pred = [false, false, false, false, false, false];
}

function end() {
    $("#timesup-card").toggleClass("visible");
}

$("#button-about").click(function () {
    $("#about-card").toggleClass("visible");
});

$("#close").click(function () {
    $("#about-card").toggleClass("visible");
});

$("#button-play").click(function () {
    init();
});

$("#button-newround-play").click(function () {
    $("#clock-time").html("00:20");
    $("#newround-card").toggleClass("visible");
    $("#game").show();
    $("#splash").hide();
    let interval = setInterval(() => {
        let time = $("#clock-time").text();
        let second = time.substring(time.indexOf(':') + 1, time.length) - 1 + "";
        if (second.length === 2) {
            $("#clock-time").html("00:" + second);
        } else $("#clock-time").html("00:0" + second);
        if (time === "00:04")
            $(".text-blink").css("color", "#FF5000");
        if (time === "00:01") {
            console.info("end...");
            if (round === 7) {
                let path = canvas2svg(draw_list);
                $("#svg" + (round - 1)).attr("d", path);
                round = 1;
                check();
                end();
            } else {
                let path = canvas2svg(draw_list);
                $("#svg" + (round - 1)).attr("d", path);
                init();
            }
            clearInterval(interval);
        }
        if (jump) {
            jump = false;
            console.info("jump...");
            if (round === 7) {
                let path = canvas2svg(draw_list);
                $("#svg" + (round - 1)).attr("d", path);
                round = 1;
                check();
                end();
            } else {
                let path = canvas2svg(draw_list);
                $("#svg" + (round - 1)).attr("d", path);
                init();
            }
            clearInterval(interval);
        }
    }, 1000);
});

$("#game-close").click(function () {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setCanvasBg('white');
    draw = [];
    draw_list = [];
    $("#pred").html("。。。。。。");
    $("#game").hide();
    $("#splash").show();
});

$("#button-skip").click(function () {
    jump = true;
});

$("#button-timesup-play").click(function () {
    $("#timesup-card").toggleClass("visible");
    init();
});

$("#over-close").click(function(){
    $("#timesup-card").toggleClass("visible");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setCanvasBg('white');
    draw = [];
    draw_list = [];
    $("#pred").html("。。。。。。");
    $("#game").hide();
    $("#splash").show();
});
