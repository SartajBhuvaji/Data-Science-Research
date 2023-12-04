import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def IKC(original_df, minority_class_column:str, minority_class_label:str):

    if original_df.empty:
        raise ValueError("Empty dataframe.")
    
    original_df[minority_class_column] = original_df[minority_class_column].astype(str)  
    minority_df = original_df[original_df[minority_class_column] == minority_class_label]
    majority_df = original_df[original_df[minority_class_column] != minority_class_label]

    if minority_df.empty:
        raise ValueError("Minority class label not found in the dataset.")

    minority_df = minority_df.drop(columns=[minority_class_column])
    input_shape = minority_df.shape[1]
    minority_df_copy = minority_df.copy()

    minority_df_numpy = minority_df.to_numpy()
    numAttributes = minority_df_numpy.shape[1]
    
    numToSynthesize = majority_df.shape[0] - minority_df.shape[0]
    syntheticArray = np.empty((0, numAttributes))
        
    clusterNum = 2
    rows, columns = minority_df_numpy.shape

    iterVal = 1
    while (rows + clusterNum < majority_df.shape[0]):
        kmeans = KMeans(n_clusters=clusterNum, init='random')
        kmeans.fit(minority_df_numpy)
        label = kmeans.labels_
        for i in range(clusterNum):
            cluster = minority_df_numpy[np.where(label==i)]
            average = np.mean(cluster, axis=0)
            average = np.reshape(average, (1, numAttributes))
            syntheticArray = np.concatenate((syntheticArray, average))
            X = np.vstack((minority_df_numpy,average))
        clusterNum+=1
        iterVal+=1
        rows, columns = minority_df_numpy.shape
        
    syntheticData = pd.DataFrame(syntheticArray, columns=minority_df.columns)

    if minority_class_label.isnumeric():
        syntheticData[minority_class_column] = int(minority_class_label)
    else:
        syntheticData[minority_class_column] = minority_class_label
        
    syntheticData[minority_class_column] = minority_class_label
    synthetic_df = pd.concat([syntheticData, original_df], ignore_index=True)
    synthetic_df = synthetic_df.sample(frac=1).reset_index(drop=True)

    return synthetic_df