a. Description

This project utilizes cutting-edge technologies to extract valuable insights and identify key themes from earnings call transcripts of S&P 500 companies between 2014 and 2024. The main objective is to develop an intuitive dashboard that visualizes trends and highlights emerging themes across these corporate earnings calls over the past decade.

To accomplish this, the project follows a structured approach:

1. Transcript Retrieval: Earnings call data will be fetched using an API to gather the necessary transcripts.

2. Topic Modeling: Advanced topic modeling will be applied using Latent Dirichlet Allocation (LDA) to uncover prominent themes within the calls.

3. Hierarchical Clustering: A hybrid clustering method combining Large Language Models (LLMs) and human input will be used to ensure meaningful and accurate groupings of themes.

4. Visualization: The extracted insights will be presented in a dynamic dashboard, created with Tableau for general visualization. A custom Circle Packing chart built in D3.js will provide an interactive and detailed exploration of the data.

All scripts and resources needed to execute this project are located in the CODE directory.


b. Installation

To set up and run this project, please follow the steps outlined below:

1.Virtual Environment Setup: It is recommended to run this project in a virtual environment to ensure consistency in package versions and improve reproducibility. The preferred approach is to use venv (https://docs.python.org/3/library/venv.html). Follow these steps to set up a virtual environment:

python -m venv <your_environment_name>

Linux/Mac OS users: source <your_environment_name>/bin/activate
Windows users: <your_environment_name>\Scripts\activate

2.Install Required Packages: Once your virtual environment is activated, install the necessary dependencies by running the following command:

pip install -r /path/to/requirements.txt

3. Running the Code: Once the environment is set up and dependencies are installed, you can proceed with executing the scripts in the CODE directory. File specific instructions will be documented in the following Execution section


c. Execution

Within the CODE directory are a number of directories corresponding to the outlined steps in the Description section. Listed will be the intended order, expected input/outputs of the inidivudal files, as well as the implied function


1. data_generation

Code: data_generation.py
Input: s&p_consitituents.csv, sector_info.csv
Output: earnings_transcripts.json

Description

This script retrieves earnings call transcript data using the API Ninjas /v1/earningstranscript endpoint. Full API documentation can be found here: https://www.api-ninjas.com/api/earningscalltranscript

To run this script, an API key must be inserted into the NINJAS_API_KEY variable at the top of the data_generation.py file. A free key can be obtained from API Ninjas; however, it will be subject to rate limits and only provides access to the most recent 12 months of data.

To access the full 10-year archive of transcripts, a premium subscription is required. If using the free tier, in addition to updating the API key, the date range in the get_earnings_call_transcripts() function will also need to be adjusted to fall within the accessible time window.

2. topic_modelling

Code: topic_modelling_full_data.ipynb, topic_modelling_sample_data.ipynb
Input: full_combined.json (outputted file from data_generation.py)
Output: LDA100_doc_topic_norm_augmented.csv, LDA100_topic_word_norm.csv

General Note: The topic_modelling_full_data.ipynb notebook requires significant processing power to run efficiently. For optimal performance, it is recommended to use a cloud-based solution like Azure Machine Learning. If running locally or on the cloud, ensure you have at least 4 CPU cores and 32GB of RAM for the best results.

Description

These notebooks seek to perform Exploratory Data Analysis and qualitative and quantitative analysis across various topic sizes and NLP models. Ultimately, it was found that Latent Dirichlet Allocation (LDA) with a topic size of 100 provided the best fit for our use case, balancing interpretability and coherence across topics. The analysis includes preprocessing the data, evaluating multiple topic sizes, and generating document-topic and topic-word distributions. The final outputs are used to assess thematic structure across the dataset and support downstream clustering and visualization

3. clustering

Code: clustering.py, sub_clustering.py
Input: LDA100_topic_word_norm.csv
Output: LDA100_topic_word_norm_with_4_clusters.csv LDA100_topic_word_norm_with_4_subclusters.csv


Description

These scripts perform hierarchical agglomerative clustering on topic-word distributions generated from the topic_modelling section. Using cosine similarity as the distance metric, the code clusters similar topics into groups ranging from 2 to 4 clusters. For each configuration, it outputs the topic-word matrix with assigned cluster labels and aggregates summary statistics (such as the number of topics per cluster). The final outputs are utilized in the visualizations.

4. visualization

Code: flatten.py, index.html
Input: LDA_100_doc_topic_norm_augmented.csv, LDA_100_topic_word_norm_with_4_with_subclusters.csv
Output: Tableau Dashboard

Description

This section focuses on building an interactive Tableau dashboard that visualizes the results from topic modeling and clustering. The dashboard incorporates cluster-level insights, enabling users to explore topics filtered by metadata such as year and sector. Additionally, a custom D3.js Circle Packing visualization is integrated via index.html, providing a dynamic and intuitive representation of topic clusters and their hierarchical structure.

