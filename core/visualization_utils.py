import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_static_visualizations():
    # Example data
    data = sns.load_dataset('iris')

    # Create a plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='sepal_length', y='sepal_width', hue='species')
    plt.title('Iris Sepal Dimensions')

    # Save the plot as an image
    static_dir = os.path.join('core', 'static', 'core', 'images')
    os.makedirs(static_dir, exist_ok=True)
    plt.savefig(os.path.join(static_dir, 'iris_sepal.png'))
    plt.close()