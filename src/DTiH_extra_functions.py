predictor_data = {
    'rmssd': {"AF":45,  "NAF":27}, 
    'pnn50': {"AF":0.11,"NAF":0.04}, 
    'lf/hf': {"AF":0.88,"NAF":2.75}
}


def interpolation(x: float, p: str = 'rmssd') -> float:
    value = (x - predictor_data[p]["NAF"]) * ((1)/(predictor_data[p]["AF"] - predictor_data[p]["NAF"]))

    if value > 1:
        return 1

    if value < 0:
        return 0

    return value

    



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0,150,500)
    y = [interpolation(i) for i in x]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x,y, 'r')

    # show the plot
    plt.show()
