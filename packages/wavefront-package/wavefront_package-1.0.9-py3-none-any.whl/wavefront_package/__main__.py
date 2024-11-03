#
from wavefront_package.wavefront_5_pac import Voronoi  
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

def main():
    
    if len(sys.argv) < 2:
        
        vor = Voronoi(500,500) #画像の大きさの指定
        vor.file_input('circle.csv') #入力ファイル指定
        diagram = vor.voronoi_tessellation()
        E,Em,V,Vm = vor.extractEandV(diagram) 
        maze = np.zeros((vor.H,vor.W),np.uint8) 
        for x,y in E:
            maze[y,x] = 1
        path = vor.search_path(maze,(200,180),(273,320),8)  #(200,180),(273,320)はそれぞれスタート点,ゴール点の座標になっています 
        plt.figure()
        plt.imshow(maze, cmap=ListedColormap(['white','black','red','gray'])) # maze 配列を表示するためのカラーマップを設定: 0 = 白, 1 = 黒, 2 = 赤, 3 = 灰色
        for y in range(maze.shape[0]):
            for x in range(maze.shape[1]):
                if maze[y,x] == 1:
                    plt.scatter(x,y,color='black', s= 2) #maze配列が1の時 2倍の大きさで黒くする
                elif maze[y,x] == 4:
                    plt.scatter(x,y,color='red',s=4) #maze 配列が4の時 4倍の大きさで赤くする
        plt.show()
    else:    
        print("Arguments provided: ", sys.argv[1:])

if __name__ == "__main__":
    main()