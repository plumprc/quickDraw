import sys
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import pandas as pd


if __name__ == '__main__':
    df1 = pd.read_csv(sys.argv[1])
    df2 = pd.read_csv(sys.argv[1][:-4] + '_simplified.csv')
    drawing = eval(df1['drawing'][int(sys.argv[2])])
    simplified_drawings = eval(df2['drawing'][int(sys.argv[2])])

    for x, y, t in drawing:
        plt.subplot(1,2,1)
        plt.plot(x, y, marker='.')
        plt.axis('off')
        
    plt.gca().invert_yaxis()
    plt.axis('equal')

    for x, y, t in simplified_drawings:
        plt.subplot(1,2,2)
        plt.plot(x, y, marker='.')
        plt.axis('off')

    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.show()