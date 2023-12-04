from graphs import Graphs
import os

def visualize(original_df, pure_files_checkbox, synthetic_df, minority_class, minority_class_column):
    # Housekeeping
    print("Housekeeping")
    path = os.path.join(os.getcwd(), 'static', 'graphs')
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

    obj = Graphs(original_df, pure_files_checkbox, synthetic_df, minority_class, minority_class_column)
    obj.plot_heatmaps()
    obj.plot_density()
    obj.plot_scatterplot(0,50)
    return 1