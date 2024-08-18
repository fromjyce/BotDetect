# BotDetect

Welcome to BotDetect, a comprehensive solution for botnet detection using machine learning and graph analysis. This project leverages Python for model training and Flask to power a web application that allows users to analyze network data and detect botnet activity. With an intuitive frontend built using HTML, CSS, and JavaScript, BotDetect makes it easy to visualize network behavior and identify malicious traffic.

## Overview of BotDetect

BotDetect offers a robust framework for detecting botnets through graph-based analysis and machine learning techniques. Below is an overview of what can be achieved using this project:

- **Graph-Based Botnet Detection:** BotDetect utilizes graph theory to represent network traffic as a graph, where nodes represent IP addresses and edges represent connections. This allows for the extraction of important features such as node degree, centrality measures, and clustering coefficients, which are crucial for identifying botnet behavior.
  
- **Machine Learning Classification:** The extracted graph features are used to train machine learning models, including HistGradientBoosting, Random Forest, and Decision Tree classifiers. These models are then used to classify network traffic as either botnet or non-botnet, providing accurate detection capabilities.

- **Web Interface for Analysis:** BotDetect includes a Flask-based web interface where users can upload network data, perform botnet detection, and visualize the results through interactive graphs and charts. This user-friendly interface simplifies the process of analyzing and interpreting network traffic.

- **Feature Extraction and Preprocessing:** The system preprocesses network flow data, balancing class distributions using SMOTE, and standardizing features for optimal model performance. This ensures that the models receive clean and well-structured input data.

- **Model Deployment:** The trained models are deployed within the Flask application, allowing for real-time detection of botnet activity. Users can interact with the models through the web interface, making the detection process seamless and accessible.

In summary, BotDetect integrates advanced graph analysis with machine learning to provide a powerful tool for detecting botnet activity. The web-based interface further enhances usability, making it an effective solution for both researchers and cybersecurity professionals.

## Running the Project

To run the BotDetect project, follow these steps:

1. **Model Training and Graph Processing**:
   - The model training and graph-related computations were conducted in a Linux environment. Ensure you have a Linux-based system or a compatible virtual machine to replicate this setup.

2. **Hosting the Web Application**:
   - The Flask API for hosting the website was developed and tested on a Windows 11 environment. To host the web application locally, follow these steps:
     1. **Run the Flask Application**: Execute the Flask application using the following command (_After navigating to Website Directory_):
        ```bash
        python app.py
        ```
     3. **Access the Web Interface**: Open a web browser and navigate to `http://localhost:5000` to access the web interface.

3. **Development Environment**:
   - he programs have been tested on the Visual Studio Code IDE in Windows 11 and Google Colab. However, you are free to use any IDE that suits your needs for development and testing.

By following these instructions, you can set up and run the BotDetect project in your preferred environment.

## Contact

For any issues or suggestions for improvement, feel free to contact us at `jaya2004kra@gmail.com`, `nidhi22110041@snuchennai.edu.in`, `saadhvisree22110160@snuchennai.edu.in` and `mridulla22110161@snuchennai.edu.in`. We appreciate any feedback that can help enhance the project.

## License

All the code and resources in this repository are licensed under the GNU GENERAL PUBLIC LICENSE. The project is free to use, modify, and distribute for educational purposes. However, we do not take any responsibility for the accuracy or reliability of the project.

## Our Social Profiles

[**LINKEDIN - Jayashre** ](https://www.linkedin.com/in/jayashrek/) \
[**LINKEDIN - Nidhi Gummaraju** ](https://in.linkedin.com/in/nidhigummaraju) \
[**LINKEDIN - Saadhvi Sree H** ](https://in.linkedin.com/in/saadhvisree) \
[**LINKEDIN - Mridulla K Madhu** ](https://www.linkedin.com/in/mridulla-k-madhu-2b1618258/) \
