
# Customer Churn Analysis and Prediction
This project is an analysis of client churn of a telecommunications company. It is divided into two main parts: data analysis and model building, and web application development.

## part 1: Data Analysis and Model Building
The first part analyzes the customer churn dataset using **Jupyter Notebook**, which includes data preprocessing, exploratory data analysis (EDA), and feature engineering. Several machine learning models are trained and evaluated, including Logistic Regression, SVM, and AdaBoost. The performance of each model is assessed using metrics such as accuracy, precision, recall, and F1-score.

Best performing model is saved as a pickle file for later use in the web application, with appropriate JSON schema.

Analised dataset: https://www.kaggle.com/datasets/blastchar/telco-customer-churn

## part 2: Web Application Development
The second part of the project focuses on developing a web application to deploy the best performing churn prediction model. The application provides an interface for users to input customer data and receive predictions on whether the customer is likely to churn or not, with probability scores. 

The web application is built using **Streamlit**. 
API endpoints are created using **Flask** to handle the prediction requests. 
The whole application is containerized using **Docker**, allowing for easy deployment.



