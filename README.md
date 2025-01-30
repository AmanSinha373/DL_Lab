# Emotion Detection CNN - DL Project  
**Deep Learning Project for Emotion Detection with Docker and Jenkins Pipeline**

This repository contains a deep learning-based **Emotion Detection** project. It uses **Docker** for containerization and **Jenkins** for continuous integration and deployment. The project is designed to predict emotions from images using a pre-trained neural network and can be easily deployed and managed in a CI/CD pipeline.

## Project Structure

- **Dockerfile**: Defines the environment required to run the project in a Docker container.  
- **requirements.txt**: Contains all necessary Python dependencies for the project, including libraries like TensorFlow, Keras, and OpenCV.  
- **Jenkinsfile**: Contains the Jenkins pipeline configuration to automate the build, test, and deployment process.  
- **Dl_Final_Lab_Exam_(Aman_Kumar_Sinha).ipynb**: Jupyter Notebook that contains the deep learning code for emotion detection from images using a neural network.  
- **dl_final_lab_exam_(aman_kumar_sinha).py**: Python script that executes the emotion detection deep learning model.
- **README.md**: This file, which provides an overview of the project.

## Installation

### Prerequisites

- **Docker**: Ensure Docker is installed and running on your machine.
- **Jenkins**: Set up Jenkins for continuous integration.
- **Git**: You need Git to clone the repository.
- **TensorFlow/Keras**: For the deep learning model, TensorFlow or Keras is required.
- **OpenCV**: For image processing.
  
To install the required Python packages, create a virtual environment and use the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Steps to Run the Project Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/AmanSinha373/DL_Lab.git
    cd DL_Lab
    ```

2. Build the Docker image:
    ```bash
    docker build -t emotion_detection_project .
    ```

3. Run the Docker container:
    ```bash
    docker run -d --name emotion_detection_container emotion_detection_project
    ```

4. Clean up after running:
    ```bash
    docker rm -f emotion_detection_container
    docker rmi emotion_detection_project
    ```

## Jenkins Pipeline Setup

1. Create a new Pipeline job in Jenkins.
2. Under Pipeline, choose **Pipeline script from SCM** and configure it to use the Git repository where this `Jenkinsfile` is stored.
3. Run the Jenkins job to automatically build the Docker image, run the container, and clean up.

## Using MLflow 

1. **Tracking Experiments**  
   Add the following code to your Python script to start tracking experiments with **MLflow**.

   Example code for tracking an emotion detection model experiment:
   ```python
   import mlflow
   import mlflow.tensorflow

   # Start MLflow experiment
   mlflow.set_experiment("Emotion Detection Experiment")

   with mlflow.start_run():
       mlflow.log_param("batch_size", batch_size)
       mlflow.log_metric("accuracy", accuracy)
       mlflow.tensorflow.log_model(model, "model")
   ```

2. **Running MLflow UI**  
   After running your experiments, you can view the results in the MLflow UI.

   To start the **MLflow tracking server**, run:
   ```bash
   mlflow ui
   ```

   You can then access the UI at:  
   [http://localhost:5000](http://localhost:5000)

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.
