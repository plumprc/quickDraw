import warnings
warnings.filterwarnings("ignore")
import argparse
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.utils.data

import data_set
import models
import draw

parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint', action='store', type=str, default='checkpoints/kaggle-quickdraw-weights.pth')
parser.add_argument('--img',type=int, default=0)
args = parser.parse_args()

CLASSES = ['The_Eiffel_Tower', 'The_Great_Wall_of_China', 'The_Mona_Lisa', 'airplane', 'alarm_clock', 'ambulance',
           'angel', 'animal_migration', 'ant', 'anvil', 'apple', 'arm', 'asparagus', 'axe', 'backpack', 'banana',
           'bandage', 'barn', 'baseball_bat', 'baseball', 'basket', 'basketball', 'bat', 'bathtub', 'beach', 'bear',
           'beard', 'bed', 'bee', 'belt', 'bench', 'bicycle', 'binoculars', 'bird', 'birthday_cake', 'blackberry',
           'blueberry', 'book', 'boomerang', 'bottlecap', 'bowtie', 'bracelet', 'brain', 'bread', 'bridge', 'broccoli',
           'broom', 'bucket', 'bulldozer', 'bus', 'bush', 'butterfly', 'cactus', 'cake', 'calculator', 'calendar',
           'camel', 'camera', 'camouflage', 'campfire', 'candle', 'cannon', 'canoe', 'car', 'carrot', 'castle', 'cat',
           'ceiling_fan', 'cell_phone', 'cello', 'chair', 'chandelier', 'church', 'circle', 'clarinet', 'clock',
           'cloud', 'coffee_cup', 'compass', 'computer', 'cookie', 'cooler', 'couch', 'cow', 'crab', 'crayon',
           'crocodile', 'crown', 'cruise_ship', 'cup', 'diamond', 'dishwasher', 'diving_board', 'dog', 'dolphin',
           'donut', 'door', 'dragon', 'dresser', 'drill', 'drums', 'duck', 'dumbbell', 'ear', 'elbow', 'elephant',
           'envelope', 'eraser', 'eye', 'eyeglasses', 'face', 'fan', 'feather', 'fence', 'finger', 'fire_hydrant',
           'fireplace', 'firetruck', 'fish', 'flamingo', 'flashlight', 'flip_flops', 'floor_lamp', 'flower',
           'flying_saucer', 'foot', 'fork', 'frog', 'frying_pan', 'garden_hose', 'garden', 'giraffe', 'goatee',
           'golf_club', 'grapes', 'grass', 'guitar', 'hamburger', 'hammer', 'hand', 'harp', 'hat', 'headphones',
           'hedgehog', 'helicopter', 'helmet', 'hexagon', 'hockey_puck', 'hockey_stick', 'horse', 'hospital',
           'hot_air_balloon', 'hot_dog', 'hot_tub', 'hourglass', 'house_plant', 'house', 'hurricane', 'ice_cream',
           'jacket', 'jail', 'kangaroo', 'key', 'keyboard', 'knee', 'ladder', 'lantern', 'laptop', 'leaf', 'leg',
           'light_bulb', 'lighthouse', 'lightning', 'line', 'lion', 'lipstick', 'lobster', 'lollipop', 'mailbox', 'map',
           'marker', 'matches', 'megaphone', 'mermaid', 'microphone', 'microwave', 'monkey', 'moon', 'mosquito',
           'motorbike', 'mountain', 'mouse', 'moustache', 'mouth', 'mug', 'mushroom', 'nail', 'necklace', 'nose',
           'ocean', 'octagon', 'octopus', 'onion', 'oven', 'owl', 'paint_can', 'paintbrush', 'palm_tree', 'panda',
           'pants', 'paper_clip', 'parachute', 'parrot', 'passport', 'peanut', 'pear', 'peas', 'pencil', 'penguin',
           'piano', 'pickup_truck', 'picture_frame', 'pig', 'pillow', 'pineapple', 'pizza', 'pliers', 'police_car',
           'pond', 'pool', 'popsicle', 'postcard', 'potato', 'power_outlet', 'purse', 'rabbit', 'raccoon', 'radio',
           'rain', 'rainbow', 'rake', 'remote_control', 'rhinoceros', 'river', 'roller_coaster', 'rollerskates',
           'sailboat', 'sandwich', 'saw', 'saxophone', 'school_bus', 'scissors', 'scorpion', 'screwdriver',
           'sea_turtle', 'see_saw', 'shark', 'sheep', 'shoe', 'shorts', 'shovel', 'sink', 'skateboard', 'skull',
           'skyscraper', 'sleeping_bag', 'smiley_face', 'snail', 'snake', 'snorkel', 'snowflake', 'snowman',
           'soccer_ball', 'sock', 'speedboat', 'spider', 'spoon', 'spreadsheet', 'square', 'squiggle', 'squirrel',
           'stairs', 'star', 'steak', 'stereo', 'stethoscope', 'stitches', 'stop_sign', 'stove', 'strawberry',
           'streetlight', 'string_bean', 'submarine', 'suitcase', 'sun', 'swan', 'sweater', 'swing_set', 'sword',
           't-shirt', 'table', 'teapot', 'teddy-bear', 'telephone', 'television', 'tennis_racquet', 'tent', 'tiger',
           'toaster', 'toe', 'toilet', 'tooth', 'toothbrush', 'toothpaste', 'tornado', 'tractor', 'traffic_light',
           'train', 'tree', 'triangle', 'trombone', 'truck', 'trumpet', 'umbrella', 'underwear', 'van', 'vase',
           'violin', 'washing_machine', 'watermelon', 'waterslide', 'whale', 'wheel', 'windmill', 'wine_bottle',
           'wine_glass', 'wristwatch', 'yoga', 'zebra', 'zigzag']
class_to_idx = {c: idx for idx, c in enumerate(CLASSES)}
idx_to_class = {v: k for k, v in class_to_idx.items()}

preds = []

if __name__ == '__main__':
    test_data_set = data_set.TestDataSet()
    test_data = list(test_data_set[args.img])

    test_data[0].unsqueeze_(0)
    test_data[1].unsqueeze_(0)

    df = pd.read_csv('myDraw.csv')
    img = ast.literal_eval(df['drawing'][args.img])
    s_img = draw.normalize_resample_simplify(img)
    # test_loader = torch.utils.data.DataLoader(
    #     test_data_set, batch_size=args.batch_size, shuffle=False, drop_last=False, num_workers=1)
    
    model = models.strokes_to_seresnext50_32x4d(32, 2, 340)
    model.load_state_dict(torch.load(args.checkpoint))
    model.eval()
    # model.cuda()

    with torch.no_grad():
        # batch = [b.cuda() for b in batch]
        output = model(*test_data)
        preds.append(output)

    p = []
    for i in preds:
        i = i.data.cpu().numpy()
        p.append(i)

    # np.save('test.npy', p[0])
    pred = np.argsort(p[0])
    print(idx_to_class[pred[-1]], idx_to_class[pred[-2]], idx_to_class[pred[-3]])

    plt.figure(figsize=(6,3))    
    for x,y,t in img:
        plt.subplot(1,2,1)
        plt.plot(x, y, marker='.')
        plt.axis('off')

        plt.gca().invert_yaxis()
        plt.axis('equal')

    for x,y in s_img:
        plt.subplot(1,2,2)
        plt.plot(x, y, marker='.')
        plt.axis('off')

        plt.gca().invert_yaxis()
        plt.axis('equal')

    plt.show()
