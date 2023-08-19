import graphs

def visualize(original_df, pure_files_checkbox, synthetic_df, minority_class, minority_class_column):
    obj = graphs.Graphs(original_df, pure_files_checkbox, synthetic_df, minority_class, minority_class_column)

    obj.plotHeatMaps()

    
    pass