# Importing packages
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering

topic_modelling_output = ["LDA_75", "LDA_100", "NMF_50"]

# For 2, 3 and 4 clusters
for topic_modelling in topic_modelling_output:
    for num_clusters in range(2,5):
        input_data_file = "output/" + topic_modelling + "_topic_word_norm_with_" + str(num_clusters) + "_clusters.csv"

        print("Loading data...")
        topic_word_matrix = pd.read_csv(input_data_file)
        print("Data Loaded!...")
        topic_word_matrix.drop(topic_word_matrix.filter(regex="Unname"), axis=1, inplace=True)
        print(topic_word_matrix.head())

        existing_columns = list(topic_word_matrix.columns)
        new_columns = existing_columns + ["Topic_Sub_Clusters"]
        output_df = pd.DataFrame(columns=new_columns)
        print(output_df)

        for cluster_label in range(0,num_clusters):
            sub_topic_word_matrix = topic_word_matrix[topic_word_matrix["Topic_Clusters"]==cluster_label]
            print(sub_topic_word_matrix.head())

            if len(sub_topic_word_matrix) > 3:
                distance_matrix = 1 - cosine_similarity(sub_topic_word_matrix.iloc[:,1:])
                cluster = AgglomerativeClustering(n_clusters=3, linkage='ward')

                topic_labels = cluster.fit_predict(distance_matrix)
                topic_labels = np.char.add(str(cluster_label)+"_", topic_labels.astype(str))
                #topic_labels = np.char.add(str(), arr.astype(str))

                sub_df = pd.DataFrame(sub_topic_word_matrix)
                # Insert sub cluster labels as a new column
                sub_df.insert(0, "Topic_Sub_Clusters", topic_labels)
            else:
                sub_df = pd.DataFrame(sub_topic_word_matrix)
                sub_df["Topic_Sub_Clusters"] = "no_sub_cluster"

            output_df = pd.concat([output_df, sub_df])

            print(output_df.head())
            print(output_df[["Topic_Clusters", "Topic_Sub_Clusters"]])

        # Specify the columns you want to bring to the front
        front_cols = ["Topic_Clusters", "Topic_Sub_Clusters"]
        # Get the rest of the columns
        other_cols = [col for col in output_df.columns if col not in front_cols]
        # Reorder DataFrame
        output_df = output_df[front_cols + other_cols]

        output_data_file = "output/" + topic_modelling + "_topic_word_norm_with_" + str(num_clusters) + "_with_subclusters.csv"
        output_df.to_csv(output_data_file)





