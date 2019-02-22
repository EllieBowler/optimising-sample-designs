from matplotlib import pyplot as plt

def plot_design(mask, x, y):
    plt.imshow(mask, cmap='Accent')
    plt.scatter(y, x, c='black', marker='x', linewidth=2)
    plt.axis('off')
    plt.title('{} design with {} sample sites'.format('Stratified', len(x)))
    plt.show()
    return