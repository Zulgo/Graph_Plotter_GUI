import tkinter as tk
import tkinter.filedialog
import csv
import matplotlib.pyplot as plt

class PlotApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CSV Plotter")

        # create the widgets
        self.file_label = tk.Label(self.master, text="CSV File:")
        self.file_entry = tk.Entry(self.master, width=30)
        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_file)
        self.plot_button = tk.Button(self.master, text="Plot", command=self.plot_data)
        self.column_label = tk.Label(self.master, text="Select Column(s):")
        self.column_listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE)
        self.multiplot_var = tk.IntVar()
        self.multiplot_checkbox = tk.Checkbutton(self.master, text="Plot multiple columns on one graph", variable=self.multiplot_var)

        # grid the widgets
        self.file_label.grid(row=0, column=0)
        self.file_entry.grid(row=0, column=1)
        self.browse_button.grid(row=0, column=2)
        self.column_label.grid(row=1, column=0)
        self.column_listbox.grid(row=1, column=1)
        self.multiplot_checkbox.grid(row=2, column=0)
        self.plot_button.grid(row=2, column=1)

    def browse_file(self):
        # open a file dialog to select a CSV file
        filename = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.load_csv()

    def load_csv(self):
        # load the selected CSV file into lists
        self.data = []
        with open(self.file_entry.get()) as csvfile:
            reader = csv.reader(csvfile)
            self.columns = next(reader)
            for row in reader:
                self.data.append([float(x) for x in row])
        self.column_listbox.delete(0, tk.END)
        for column in self.columns:
            self.column_listbox.insert(tk.END, column)

    def plot_data(self):
        # get the selected columns and plot them against the frequency
        selected_columns = [self.columns[i] for i in self.column_listbox.curselection()]
        if len(selected_columns) == 0:
            tk.messagebox.showerror("Error", "No columns selected!")
            return

        fig, ax = plt.subplots()
        for column in selected_columns:
            col_index = self.columns.index(column)
            ax.plot([row[0] for row in self.data], [row[col_index] for row in self.data], label=column)
        ax.set_xlabel("Frequency GHz")
        ax.set_ylabel("Magnitude (dB)")
        ax.legend()

        if self.multiplot_var.get():
            plt.show()
        else:
            plt.show(block=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
