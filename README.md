## 🚀 Problem Statement

```
Create an End to End Machine Learning architecture which includes 
Model Training, Testing and operationalization, 
Infrastructure and endpoint monitoring.
```

### ✨ Architecture
![test drawio (2)](https://user-images.githubusercontent.com/40850370/166421284-ae6e632f-2633-4f7a-b1be-8538ebab6b42.png)

### 🔥 Technologies Used
``` 
1. Python 
2. shell scripting 
3. aws cloud Provider 
4. Prometheus And grafana
5. FastApi for endpoint 
6. S3bucket - as feature store and model registry 
7. CI-CD tool Jenkins
```

## 👷 Initial Setup 
```commandline
conda create --prefix ./env python=3.9
conda activate ./env 
pip install -r requirements.txt 
```
## 💭 Setup S3 bucket
```
1. Feature Store s3 bucket with lambda call on put event
2. Model Registry - Testing 
                  - production
```
### 🔅 Configuration for jenkins
![image](https://user-images.githubusercontent.com/40850370/166425649-dfc7e79f-ff89-455b-bb9b-58e744549785.png)
![image](https://user-images.githubusercontent.com/40850370/166425685-ae6b90ca-1a09-43e2-b3d8-8be633e30fa8.png)

```
Install jenkins on ec2 and make a webhook with github repository to access it whenever updated on push.
Create 3 jobs Train, Test and Deploy. While creating Seperate jobs remember to put jenkins-jobs-script in it.
I have written 3 sepreate script in it.

Create a master pipeline to run different train,test and deploy.
```
## 📐 Develop Lambda Trigger
![image](https://user-images.githubusercontent.com/40850370/166426136-7c635c4f-8bfd-4dab-8b4a-1aca754b1d1a.png)
![image](https://user-images.githubusercontent.com/40850370/166426204-17e3f781-6d86-4484-b66c-4025f4ec60f0.png)
```
Create Lambda Trigger on S3 Feature store on put event, use python3.7 in lambda as it has request library pre-installed
Remote trigger Master pipeline to run all the stages.
```
### 📊 Configuration File
```
Maintain Configuration file. Changes required in 
- Feature-Store
- Model Registry 
- Email Params
    - Please put gmail application key in it else you will get error
- Ml_Model_params
```

### ✏️ Configuration for Prometheus 
![image](https://user-images.githubusercontent.com/40850370/166425509-e34fb61f-cc43-451d-b720-99cfb3df6bb3.png)

```
Install prometheus on Ec2 machine. In configuration file add scrape job set in endpoints.

 
  - job_name: "python_endpoint"
  
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:5000"]
      
  - job_name: "wmi_exporter"
  
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9182"]

```
### 📉 Configuration for Grafana
![image](https://user-images.githubusercontent.com/40850370/166425584-d2f66757-aaa7-4417-a611-29efe57f0fed.png)
```
Install grafana and it will run on port 3000 by default.
Configure prometheus in it and create monetoring dash board.
```
### ❄️ END
```
Free free to improve this project and remove issues if you find any as nothing is perfect.
```


