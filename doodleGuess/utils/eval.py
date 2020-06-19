import os
import torch
import numpy as np
from utils import models
from utils.preprocess import eval_single

# CLASSES = ['The_Eiffel_Tower', 'The_Great_Wall_of_China', 'The_Mona_Lisa', 'airplane', 'alarm_clock', 'ambulance',
#            'angel', 'animal_migration', 'ant', 'anvil', 'apple', 'arm', 'asparagus', 'axe', 'backpack', 'banana',
#            'bandage', 'barn', 'baseball_bat', 'baseball', 'basket', 'basketball', 'bat', 'bathtub', 'beach', 'bear',
#            'beard', 'bed', 'bee', 'belt', 'bench', 'bicycle', 'binoculars', 'bird', 'birthday_cake', 'blackberry',
#            'blueberry', 'book', 'boomerang', 'bottlecap', 'bowtie', 'bracelet', 'brain', 'bread', 'bridge', 'broccoli',
#            'broom', 'bucket', 'bulldozer', 'bus', 'bush', 'butterfly', 'cactus', 'cake', 'calculator', 'calendar',
#            'camel', 'camera', 'camouflage', 'campfire', 'candle', 'cannon', 'canoe', 'car', 'carrot', 'castle', 'cat',
#            'ceiling_fan', 'cell_phone', 'cello', 'chair', 'chandelier', 'church', 'circle', 'clarinet', 'clock',
#            'cloud', 'coffee_cup', 'compass', 'computer', 'cookie', 'cooler', 'couch', 'cow', 'crab', 'crayon',
#            'crocodile', 'crown', 'cruise_ship', 'cup', 'diamond', 'dishwasher', 'diving_board', 'dog', 'dolphin',
#            'donut', 'door', 'dragon', 'dresser', 'drill', 'drums', 'duck', 'dumbbell', 'ear', 'elbow', 'elephant',
#            'envelope', 'eraser', 'eye', 'eyeglasses', 'face', 'fan', 'feather', 'fence', 'finger', 'fire_hydrant',
#            'fireplace', 'firetruck', 'fish', 'flamingo', 'flashlight', 'flip_flops', 'floor_lamp', 'flower',
#            'flying_saucer', 'foot', 'fork', 'frog', 'frying_pan', 'garden_hose', 'garden', 'giraffe', 'goatee',
#            'golf_club', 'grapes', 'grass', 'guitar', 'hamburger', 'hammer', 'hand', 'harp', 'hat', 'headphones',
#            'hedgehog', 'helicopter', 'helmet', 'hexagon', 'hockey_puck', 'hockey_stick', 'horse', 'hospital',
#            'hot_air_balloon', 'hot_dog', 'hot_tub', 'hourglass', 'house_plant', 'house', 'hurricane', 'ice_cream',
#            'jacket', 'jail', 'kangaroo', 'key', 'keyboard', 'knee', 'ladder', 'lantern', 'laptop', 'leaf', 'leg',
#            'light_bulb', 'lighthouse', 'lightning', 'line', 'lion', 'lipstick', 'lobster', 'lollipop', 'mailbox', 'map',
#            'marker', 'matches', 'megaphone', 'mermaid', 'microphone', 'microwave', 'monkey', 'moon', 'mosquito',
#            'motorbike', 'mountain', 'mouse', 'moustache', 'mouth', 'mug', 'mushroom', 'nail', 'necklace', 'nose',
#            'ocean', 'octagon', 'octopus', 'onion', 'oven', 'owl', 'paint_can', 'paintbrush', 'palm_tree', 'panda',
#            'pants', 'paper_clip', 'parachute', 'parrot', 'passport', 'peanut', 'pear', 'peas', 'pencil', 'penguin',
#            'piano', 'pickup_truck', 'picture_frame', 'pig', 'pillow', 'pineapple', 'pizza', 'pliers', 'police_car',
#            'pond', 'pool', 'popsicle', 'postcard', 'potato', 'power_outlet', 'purse', 'rabbit', 'raccoon', 'radio',
#            'rain', 'rainbow', 'rake', 'remote_control', 'rhinoceros', 'river', 'roller_coaster', 'rollerskates',
#            'sailboat', 'sandwich', 'saw', 'saxophone', 'school_bus', 'scissors', 'scorpion', 'screwdriver',
#            'sea_turtle', 'see_saw', 'shark', 'sheep', 'shoe', 'shorts', 'shovel', 'sink', 'skateboard', 'skull',
#            'skyscraper', 'sleeping_bag', 'smiley_face', 'snail', 'snake', 'snorkel', 'snowflake', 'snowman',
#            'soccer_ball', 'sock', 'speedboat', 'spider', 'spoon', 'spreadsheet', 'square', 'squiggle', 'squirrel',
#            'stairs', 'star', 'steak', 'stereo', 'stethoscope', 'stitches', 'stop_sign', 'stove', 'strawberry',
#            'streetlight', 'string_bean', 'submarine', 'suitcase', 'sun', 'swan', 'sweater', 'swing_set', 'sword',
#            't-shirt', 'table', 'teapot', 'teddy-bear', 'telephone', 'television', 'tennis_racquet', 'tent', 'tiger',
#            'toaster', 'toe', 'toilet', 'tooth', 'toothbrush', 'toothpaste', 'tornado', 'tractor', 'traffic_light',
#            'train', 'tree', 'triangle', 'trombone', 'truck', 'trumpet', 'umbrella', 'underwear', 'van', 'vase',
#            'violin', 'washing_machine', 'watermelon', 'waterslide', 'whale', 'wheel', 'windmill', 'wine_bottle',
#            'wine_glass', 'wristwatch', 'yoga', 'zebra', 'zigzag']
CLASSES = ['埃菲尔铁塔', '中国长城', '蒙娜丽莎', '飞机', '闹钟', '救护车', '天使', '动物迁徙', '蚂蚁', '铁砧', '苹果', '臂',
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
           '洗衣机', '西瓜', '滑水', '鲸鱼', '轮', '风车', '酒瓶', '酒杯', '腕表', '瑜伽', '斑马', '之字形']
class_to_idx = {c: idx for idx, c in enumerate(CLASSES)}
idx_to_class = {v: k for k, v in class_to_idx.items()}

model = models.strokes_to_seresnext50_32x4d(32, 2, 340)
path = os.path.dirname(os.path.abspath(__file__))
model.load_state_dict(torch.load(path + '/quickDraw_weights.pth', map_location=torch.device('cpu')))
model.eval()


def test(drawing):
    test_data = list(eval_single(drawing))
    test_data[0].unsqueeze_(0)
    test_data[1].unsqueeze_(0)

    with torch.no_grad():
        pred = model(*test_data)

    pred = pred.numpy()
    pred = np.argsort(pred)

    return idx_to_class[pred[-1]] + ' ' + idx_to_class[pred[-2]]


def test_person(drawing):
    test_data = list(eval_single(drawing))
    test_data[0].unsqueeze_(0)
    test_data[1].unsqueeze_(0)

    with torch.no_grad():
        pred = model(*test_data)

    pred = pred.numpy()
    pred = np.argsort(pred)

    return '预测：' + idx_to_class[pred[-1]] + ' ' + idx_to_class[pred[-2]] + \
           ' ' + idx_to_class[pred[-3]] + ' ' + idx_to_class[pred[-4]] + \
           ' ' + idx_to_class[pred[-5]] + ' ' + idx_to_class[pred[-6]]
