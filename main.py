from typing import KeysView

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import os
from colour import Color

# dsp = 0, bram = 1, uram = 2
types = [0, 1, 1, 0, 0, 0, 1, 0, 2,
         0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2,
         0, 1, 0, 1, 0, 2,
         0, 0, 1, 0, 1, 0, 2,
         0, 0, 0, 0, 1, 0, 2,
         0, 0, 0, 0, 0, 1, 1, 0]


def readXDC(f):
    # a dict to put result in it
    dict = {}
    with open(f) as fp:
        line = fp.readline()
        while line:
            if not line.startswith('set_property'):
                line = fp.readline()
                continue
            line = line.replace('\t', ' ')
            site = line.split(' ')[2]
            cell = line.split('{')[1].split("}")[0]
            n = int(cell.split('[')[1].split(']')[0], 10)
            if dict.get(n) is None:
                dict[n] = []
            else:
                dict[n].append([site, cell])
            line = fp.readline()

        return dict


def drawDSP(ax, site, color, yOffset=10):
    X = int(site.split('X', 1)[1].split('Y', 1)[0], 10)  # base 10
    Y = int(site.split('Y', 1)[1], 10)  # base 10
    count = 0
    x = 10
    for type in types:
        # move x
        if type == 0:  # DSP
            if count == X:
                break  # time to go!
            x += 10 + 20
            count += 1
        elif type == 1:  # BRAM
            x += 10 + 20
        elif type == 2:  # URAM
            x += 20 + 20

    y = Y * 19.2 + 2.1 + yOffset
    r = patches.Rectangle((x, y), 10, 15, facecolor=color)
    ax.add_patch(r)


def drawBRAM(ax, site, color, yOffset=10):
    X = int(site.split('X', 1)[1].split('Y', 1)[0], 10)  # base 10
    Y = int(site.split('Y', 1)[1], 10)  # base 10
    count = 0
    x = 10
    for type in types:
        # move x
        if type == 0:  # DSP
            x += 10 + 20
        elif type == 1:  # BRAM
            if count == X:
                break  # time to go!
            x += 10 + 20
            count += 1
        elif type == 2:  # URAM
            x += 20 + 20

    y = Y * 18.8 + 0.9 + yOffset
    r = patches.Rectangle((x, y), 10, 17, facecolor=color)
    ax.add_patch(r)


def drawURAM(ax, site, color, yOffset=10):
    X = int(site.split('X', 1)[1].split('Y', 1)[0], 10)  # base 10
    Y = int(site.split('Y', 1)[1], 10)  # base 10
    count = 0
    x = 10
    for type in types:
        # move x
        if type == 0:  # DSP
            x += 10 + 20
        elif type == 1:  # BRAM
            x += 10 + 20
        elif type == 2:  # URAM
            if count == X:
                break  # time to go!
            x += 20 + 20
            count += 1

    y = Y * 28.2 + 1.6 + yOffset
    r = patches.Rectangle((x, y), 20, 25, facecolor=color)
    ax.add_patch(r)


def drawBackGround(ax, width, height):
    dsp_color = '#cdd422'
    bram_color = '#94f0f1'
    uram_color = '#f2b1d8'
    x = 10  # starting point
    y = 10  # bottom-left y
    for type in types:
        r = patches.Rectangle
        if type == 0:  # DSP
            r = patches.Rectangle((x, y), 10, height, facecolor=dsp_color)
            x += 10 + 20
        elif type == 1:  # BRAM
            r = patches.Rectangle((x, y), 10, height, facecolor=bram_color)
            x += 10 + 20
        elif type == 2:  # URAM
            r = patches.Rectangle((x, y), 20, height, facecolor=uram_color)
            x += 20 + 20
        ax.add_patch(r)


if __name__ == "__main__":
    filename = 'data/blockNum=480.xdc'
    # dict = readXDC("data/dsp_conv_chip_orig.xdc")
    dict = readXDC(filename)
    name = filename.split('/',1)[1].split('.',1)[0]
    if not os.path.exists('data/'+ name):
        os.makedirs('data/'+ name)

    # Set up sizes
    width = 1560
    height = 5414.4

    keys = list(dict.keys())
    red = Color("red")
    # colors = list(red.range_to(Color("green"), len(keys)))
    for i in range(len(keys)):

        # color = colors[i].get_rgb()
        color = Color('red').get_rgb()
        # Create figure and axes
        fig, ax = plt.subplots(1)
        fig.set_size_inches(16, 55)
        ax.set_xlim(0, width + 20)
        ax.set_ylim(0, height + 20)

        # Create a Rectangle Patch
        rect = patches.Rectangle((10, 10), 1560, 5414.4, linewidth=1, facecolor='#dddddd')
        ax.add_patch(rect)

        drawBackGround(ax, width, height)

        # draw un-highlighted blocks
        for j in range (len(keys)):
            key = keys[j]
            entries = dict.get(key)
            for pair in entries:
                site = pair[0]
                cell = pair[1]
                if site.startswith('DSP'):
                    drawDSP(ax, site, '#ffdc6a')
                elif site.startswith('RAMB'):
                    drawBRAM(ax, site, '#00c07f')
                elif site.startswith('URAM'):
                    drawURAM(ax, site, '#bf4aa8')

        # draw the highlighted block
        key = keys[i]
        entries = dict.get(key)
        for pair in entries:
            site = pair[0]
            cell = pair[1]
            if site.startswith('DSP'):
                drawDSP(ax, site, color)  # '#ffdc6a'
                # drawDSP(ax, site, '#ffdc6a')
            elif site.startswith('RAMB'):
                drawBRAM(ax, site, color)  # '#8bf0ba'
                # drawBRAM(ax, site, '#00c07f')
            elif site.startswith('URAM'):
                drawURAM(ax, site, color)  # ''#bf4aa8''
                # drawURAM(ax, site, '#bf4aa8')

        # plt.show()
        plt.savefig('data/{}/visualize-{}.png'.format(name,i))
        plt.close()
