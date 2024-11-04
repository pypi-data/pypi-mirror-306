# EMRRunner (EMR Job Runner)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![Amazon EMR](https://img.shields.io/badge/Amazon%20EMR-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

A powerful command-line tool and API for managing and deploying Spark jobs on Amazon EMR clusters. EMRRunner simplifies the process of submitting and managing Spark jobs while handling all the necessary environment setup.

## 🚀 Features

- Command-line interface for quick job submission
- RESTful API for programmatic access
- Support for both client and cluster deploy modes
- Automatic S3 synchronization of job files
- Configurable job parameters
- Easy dependency management
- Bootstrap action support for cluster setup

## 📋 Prerequisites

- Python 3.9+
- AWS Account with EMR access
- Configured AWS credentials
- Active EMR cluster

## 🛠️ Installation

### From PyPI
```bash
pip install emrrunner
```

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/EMRRunner.git
cd EMRRunner

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install the package
pip install -e .
```

## ⚙️ Configuration

### AWS Configuration
Create a `.env` file in the project root with your AWS configuration:

`Note: Export these variables in your terminal before running:`
```env
export AWS_ACCESS_KEY=your_access_key
export AWS_SECRET_KEY=your_secret_key
export AWS_REGION=your_region
export EMR_CLUSTER_ID=your_cluster_id
export S3_PATH=s3://your-bucket/path
```

### Bootstrap Actions
For EMR cluster setup with required dependencies, create a bootstrap script (`bootstrap.sh`):

```bash
#!/bin/bash -xe

# Example structure of a bootstrap script
# Create and activate virtual environment
python3 -m venv /home/hadoop/myenv
source /home/hadoop/myenv/bin/activate

# Install system dependencies
sudo yum install python3-pip -y
sudo yum install -y [your-system-packages]

# Install Python packages
pip3 install [your-required-packages]

deactivate
```

Upload the bootstrap script to S3 and reference it in your EMR cluster configuration.

## 📁 Project Structure

```
EMRRunner/
├── Dockerfile
├── LICENSE.md
├── README.md
├── app/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── emr_client.py       # EMR interaction logic
│   ├── emr_job_api.py      # Flask API endpoints
│   ├── run_api.py          # API server runner
│   └── schema.py           # Request/Response schemas
├── bootstrap/
│   └── bootstrap.sh        # EMR bootstrap script
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_emr_job_api.py
│   └── test_schema.py
├── pyproject.toml
├── requirements.txt
└── setup.py
```

## 📦 S3 Job Structure

The `S3_PATH` in your configuration should point to a bucket with the following structure:

```
s3://your-bucket/
├── jobs/
│   ├── job1/
│   │   ├── dependencies.py   # Shared functions and utilities
│   │   └── job.py           # Main job execution script
│   └── job2/
│       ├── dependencies.py
│       └── job.py
```

### Job Organization

Each job in the S3 bucket follows a standard structure:

1. **dependencies.py**
   - Contains reusable functions and utilities specific to the job
   - Example functions:
     ```python
     def process_data(df):
         # Data processing logic
         pass

     def validate_input(data):
         # Input validation logic
         pass

     def transform_output(result):
         # Output transformation logic
         pass
     ```

2. **job.py**
   - Main execution script that uses functions from dependencies.py
   - Standard structure:
     ```python
     from dependencies import process_data, validate_input, transform_output

     def main():
         # 1. Read input data
         input_data = spark.read.parquet("s3://input-path")
         
         # 2. Validate input
         validate_input(input_data)
         
         # 3. Process data
         processed_data = process_data(input_data)
         
         # 4. Transform output
         final_output = transform_output(processed_data)
         
         # 5. Write results
         final_output.write.parquet("s3://output-path")

     if __name__ == "__main__":
         main()
     ```

## 💻 Usage

### Command Line Interface

Start a job in client mode:
```bash
emrrunner start --job job1 --step process_daily_data
```

Start a job in cluster mode:
```bash
emrrunner start --job job1 --step process_daily_data --deploy-mode cluster
```

### API Endpoints

Start a job via API in client mode (default):
```bash
curl -X POST http://localhost:8000/api/v1/emr/job/start \
     -H "Content-Type: application/json" \
     -d '{"job_name": "job1", "step": "process_daily_data"}'
```

Start a job via API in cluster mode:
```bash
curl -X POST http://localhost:8000/api/v1/emr/job/start \
     -H "Content-Type: application/json" \
     -d '{"job_name": "job1", "step": "process_daily_data", "deploy_mode": "cluster"}'
```

## 🔧 Development

To contribute to EMRRunner:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 💡 Best Practices

1. **Bootstrap Actions**
   - Keep bootstrap scripts modular
   - Version control your dependencies
   - Use specific package versions
   - Test bootstrap scripts locally when possible
   - Store bootstrap scripts in S3 with versioning enabled

2. **Job Dependencies**
   - Maintain a requirements.txt for each job
   - Use virtual environments
   - Document system-level dependencies
   - Test dependencies in a clean environment

3. **Job Organization**
   - Follow the standard structure for jobs
   - Keep dependencies.py focused and modular
   - Use clear naming conventions
   - Document all functions and modules

## 🔒 Security

- Supports AWS credential management
- Validates all input parameters
- Secure handling of bootstrap scripts

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Bug Reports

If you discover any bugs, please create an issue on GitHub with:
- Your operating system name and version
- Any details about your local setup that might be helpful in troubleshooting
- Detailed steps to reproduce the bug

---

Built with ❤️ using Python and AWS EMR