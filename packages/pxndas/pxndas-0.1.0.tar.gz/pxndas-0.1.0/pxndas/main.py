# main.py

from javak import plot_line

def main():
    # Example data for plotting
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 25, 30, 40]

    # Using the plot_line function from the metplotlib package
    plot_line(x, y, title="Sample Line Plot", xlabel="Time", ylabel="Value")

if __name__ == "__main__":
    main()
