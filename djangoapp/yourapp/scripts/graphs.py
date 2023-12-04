import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import numpy as np
import os
from scipy.stats import gaussian_kde, entropy  

class Graphs:
    def __init__(self,original_df, synthetic_df, minority_class, minority_class_column, pure_files_checkbox):
        original_df[minority_class_column] = original_df[minority_class_column].astype(str) 
        synthetic_df[minority_class_column] = synthetic_df[minority_class_column].astype(str) 
        if not pure_files_checkbox:
            try:
                self.original_df_minority = original_df[original_df[minority_class_column]==minority_class]
                self.synthetic_df_minority = synthetic_df[synthetic_df[minority_class_column]==minority_class]
                
            except Exception as e:
                print(e)    
        else:
            self.original_df_minority = original_df.copy()
            self.synthetic_df_minority = synthetic_df.copy()

        self.original_df_minority = self.original_df_minority.drop(columns=[minority_class_column])
        self.synthetic_df_minority = self.synthetic_df_minority.drop(columns=[minority_class_column])
        self.path = os.path.join(os.getcwd(), 'static', 'graphs')

    def plot_heatmaps(self,annot=False) -> None:
        _ , axes = plt.subplots(1, 2, figsize=(18, 10))
        sns.heatmap(self.original_df_minority.corr(), annot=annot, cmap='viridis', ax=axes[0])
        axes[0].set_title('Original')

        sns.heatmap(self.synthetic_df_minority.corr(), annot=annot, cmap='viridis', ax=axes[1])
        axes[1].set_title('Synthetic')
        plt.tight_layout()
        plt.savefig(os.path.join(self.path, 'heatmap_plot.png'))
        plt.close()

    def plot_density(self) -> None:
        num_columns = len(self.synthetic_df_minority.columns)
        num_rows = int(np.ceil(num_columns / 5))
        fig, axes = plt.subplots(num_rows, 5, figsize=(20, 4 * num_rows))

        highlighted_areas = {} 
        kl_divergences = {}  

        for i, column in enumerate(self.original_df_minority.columns):
            row = i // 5
            col = i % 5
            ax = axes[row, col] if num_rows > 1 else axes[col]

            sns.kdeplot(data=self.original_df_minority[column], color='blue', label='original_df', ax=ax)
            sns.kdeplot(data=self.synthetic_df_minority[column], color='green', label='synthetic_df', ax=ax)

            # Fill between the curves
            x = np.linspace(0, 1, 1000)  
            kde_original = gaussian_kde(self.original_df_minority[column])
            kde_synthetic = gaussian_kde(self.synthetic_df_minority[column])
            y1 = kde_original(x)
            y2 = kde_synthetic(x)
            ax.fill_between(x, y1, y2, where=(y1 > y2), interpolate=True, color='lightcoral', alpha=0.3)
            ax.fill_between(x, y1, y2, where=(y1 <= y2), interpolate=True, color='lightgreen', alpha=0.3)

            # Calculate and store the highlighted area for the column
            highlighted_area = np.sum(np.maximum(y1 - y2, 0) * np.diff(x)[0])
            highlighted_areas[column] = highlighted_area

            # Calculate and store the KL divergence for the column
            kl_divergence = entropy(y1, y2) # REF https://www.kaggle.com/code/nhan1212/some-statistical-distances
            kl_divergences[column] = kl_divergence

            ax.set_title(column)
            ax.set_xlabel(column)
            ax.set_xlim(0, 1)
            ax.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(self.path, 'density_plot.png'))
        plt.close()

        # total_highlighted_area = np.sum(list(highlighted_areas.values()))
        # total_kl_divergence = np.sum(list(kl_divergences.values()))

        # for column, area in highlighted_areas.items():
        #     divergence = kl_divergences[column]
        #     print(f"{column}: {area:.2f}, {divergence:.6f}")

        # print(f"Total highlighted area: {total_highlighted_area:.2f}")
        # print(f"Average KL divergence: {total_kl_divergence / num_columns:.6f}")        


    def plot_scatterplot(self, start_index, end_index) -> None:
        num_columns = len(self.original_df_minority.columns)
        num_rows = (num_columns + 4) // 5  

        fig, axs = plt.subplots(num_rows, 5, figsize=(15, num_rows * 3))
        for i, column in enumerate(self.original_df_minority.columns):
            row_idx = i // 5
            col_idx = i % 5

            axs[row_idx, col_idx].scatter(self.original_df_minority.index[start_index:end_index], 
                                        self.original_df_minority[column][start_index:end_index], color='red', label='original_df')
            axs[row_idx, col_idx].scatter(self.synthetic_df_minority.index[start_index:end_index], 
                                        self.synthetic_df_minority[column][start_index:end_index], color='blue', label='synthetic_df')

            axs[row_idx, col_idx].set_title(f"Scatter Plot: {column}")
            axs[row_idx, col_idx].set_xlabel("Index")
            axs[row_idx, col_idx].set_ylabel(column)
            axs[row_idx, col_idx].legend()

        for i in range(num_columns, num_rows * 5):
            row_idx = i // 5
            col_idx = i % 5
            fig.delaxes(axs[row_idx, col_idx])

        plt.tight_layout()

        # Save the scatter plot as an image file
        plt.savefig(os.path.join(self.path, 'scatter_plot.png'))
        plt.close()

    
    def mean_and_std(self) -> pd.DataFrame:
        output = {}
        for column in self.original_df_minority.columns:
            mean_df1 = self.original_df_minority[column].mean()
            std_df1  = self.original_df_minority[column].std()
            mean_df2 = self.synthetic_df_minority[column].mean()
            std_df2  = self.synthetic_df_minority[column].std()
            meandiff = abs(mean_df1 - mean_df2)

            output[column] = {'Mean_diff': meandiff,
                            'Mean_original_df': mean_df1, 'Mean_synthetic_df': mean_df2,
                            'Std_original_df' : std_df1,  'Std_synthetic_df' : std_df2}
        # save op #return pd.DataFrame(output).transpose().sort_values(by='Mean_diff', ascending=False)
