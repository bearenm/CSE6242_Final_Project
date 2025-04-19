# Importing packages
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering

def h_clustering(distance_matrix, num_clusters):
    cluster = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
    topic_labels = cluster.fit_predict(distance_matrix)
    # Create DataFrame with topic-word matrix
    df = pd.DataFrame(topic_word_matrix)
    # Insert cluster labels as a new column
    df.insert(0, "Topic_Clusters", topic_labels)

    summary = pd.DataFrame(df.groupby("Topic_Clusters").agg({"Topic_Clusters": "count"}))
    summary.index.name = "Cluster_label"
    summary.reset_index(inplace=True)
    summary.rename(columns={"Topic_Clusters": "No_of_Topics"}, inplace=True)
    summary["Topic_modelling_technique"] = topic_modelling
    summary["No_of_Clusters"] = num_clusters
    return summary, df

# Reading data
# Format of topic-word matrix (rows = topics, columns = words)
topic_modelling_output = ["LDA_75", "LDA_100", "NMF_50"]

summary_cluster = pd.DataFrame(columns=["Topic_modelling_technique", "No_of_Clusters", "Cluster_label", "No_of_Topics"])

for topic_modelling in topic_modelling_output:

    input_data_file = "input_data/" + topic_modelling + "_topic_word_norm.csv"

    print(input_data_file)

    print("Loading data...")
    topic_word_matrix = pd.read_csv(input_data_file)

    distance_matrix = 1 - cosine_similarity(topic_word_matrix)

    for num_clusters in range(2,5):
        summary, df = h_clustering(distance_matrix, num_clusters)

        output_data_file = "output/" + topic_modelling + "_topic_word_norm_with_" + str(num_clusters) + "_clusters.csv"
        df.to_csv(output_data_file)

        summary_cluster = pd.concat([summary_cluster, summary])
        print(summary_cluster)

summary_cluster.to_csv("output/cluster_summary.csv")




