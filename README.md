# SoundStream: Microservices-Based Video to MP3 Converter

Welcome to SoundStream, a microservices-based application designed to convert videos to MP3 format. This project leverages a variety of modern technologies to provide a scalable, efficient, and reliable service. It includes microservice architectures and distributed systems using Python, Kubernetes, RabbitMQ, MongoDB, and MySQL.

## Architecture Overview

![System Architecture](/Users/naman/Downloads/SoundStream_SystemDesign.png)

### Components

1. **Client**: The user-facing application that allows users to upload videos for conversion.
2. **API Gateway**: The central hub that routes requests to the appropriate services.
3. **Auth Service**: Handles user authentication and interacts with the Auth DB.
4. **Video to MP3 Service**: Converts uploaded videos to MP3 format and stores the results in the storage DB.
5. **Notification Service**: Sends notifications to users once their MP3 files are ready.
6. **Queue (RabbitMQ)**: Manages communication between services, ensuring reliable message passing.
7. **Auth DB**: Stores user authentication data.
8. **Storage DB**: Stores video and MP3 file metadata and links.

## Features

- **Microservices Architecture**: Each component is a separate microservice, making the system modular and easy to scale.
- **API Gateway**: Provides a single entry point for all client requests, improving security and manageability.
- **Authentication**: Secure user authentication and authorization.
- **Asynchronous Processing**: Uses RabbitMQ to handle tasks asynchronously, improving system responsiveness.
- **Notifications**: Sends real-time notifications to users about the status of their requests.
- **Scalable**: Built using Kubernetes for easy scaling and management.

## Technologies Used

- **Python**: The core programming language used for developing the microservices.
- **Kubernetes**: Manages containerized applications, providing scaling and reliability.
- **RabbitMQ**: Handles message queuing for asynchronous processing.
- **MongoDB**: NoSQL database for storing unstructured data.
- **MySQL**: Relational database for structured data storage.

## Getting Started

### Prerequisites

- **Docker**: To containerize the application.
- **Kubernetes**: For managing containers.
- **Python**: Programming language.
- **RabbitMQ**: Message broker.
- **MongoDB & MySQL**: Databases.

### Installation

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/yourusername/SoundStream.git
    cd SoundStream
    ```

2. **Set Up Environment Variables**:

    Create a `.env` file in the root directory and add your environment variables.

    ```sh
    GMAIL_ADDRESS=your-email@gmail.com
    GMAIL_PASSWORD=your-app-password
    ```

3. **Start Services**:

    Start Minikube Tunnel:

    ```sh
    minikube tunnel
    ```

    Apply Kubernetes Configurations:

    ```sh
    kubectl apply -f .
    ```

    Use Postman to send a request to the API Gateway to upload a video.

    Apply the Kubernetes configurations located in the `k9s/` directory.

    ```sh
    kubectl apply -f k9s/
    ```

## Usage

1. **Upload a Video**:

    Use the client application to upload a video.

2. **Conversion Process**:

    - The API Gateway routes the request to the Video to MP3 Service.
    - The service processes the video and stores the MP3 file in the storage DB.
    - A message is sent to the Notification Service via RabbitMQ.

3. **Receive Notification**:

    The Notification Service sends an email to the user with a link to download the MP3 file.

## Contributing

We welcome contributions from the community! Please follow these steps to contribute:

1. **Fork the Repository**:

    Click the "Fork" button at the top right of this page.

2. **Create a Branch**:

    Create a new branch for your feature or bugfix.

    ```sh
    git checkout -b feature-name
    ```

3. **Make Your Changes**:

    Develop your feature or fix the bug.

4. **Commit Your Changes**:

    Commit your changes with a clear message.

    ```sh
    git commit -m "Add feature-name"
    ```

5. **Push to Your Branch**:

    Push the changes to your forked repository.

    ```sh
    git push origin feature-name
    ```

6. **Create a Pull Request**:

    Go to the original repository and create a pull request.

## Contact

For any questions or feedback, feel free to reach out at [gujarathi.n@northeasatern.edu].
