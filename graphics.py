import matplotlib.pyplot as plt

class PlotObject:
    def __init__(self, x_label="", y_label="", show_annotate=False) -> None:
        self.x_label = x_label
        self.y_label = y_label
        self.show_annotate = show_annotate


    def plot_line(self, x_data, y_data, label=""):
        plt.plot(x_data, y_data, label=label)


    def plot_points(self, x_data, y_data, x_error=[], y_error=[], label=""):
        plt.scatter(x_data, y_data, label="")

        if self.show_annotate:
            for i in range(len(x_data)):
                    plt.annotate(x_data[i], (y_data[i], x_data[i]))


    def show_plot(self):
        plt.xlabel = self.x_label
        plt.ylabel = self.y_label
        plt.legend()
        plt.show()

        
    


