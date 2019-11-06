

# Profileservice

A microservice where users can create, update, retrieve, and delete their profile information.

## Prerequisites

1.  Use the [Google Cloud Console](https://console.cloud.google.com/) to create a Google Cloud Platform project.
2.  [Enable billing](https://support.google.com/cloud/answer/6293499#enable-billing) for your project.
3. (Skip this step if you are using Cloud Shell) Install the [Google Cloud SDK](https://cloud.google.com/sdk/install).
4. Clone this repo.

   ```
   git clone https://github.com/AppDev-Eng-Initative/Retail-Banking-Microservices-Demo.git
   cd profileservice
   ```


## Deployment

1. (Optional but recommended) Set up an App Engine service account for authentication
    * In the GCP Console, go to the **[Create service account key](https://console.cloud.google.com/apis/credentials/serviceaccountkey?_ga=2.142840501.-1637323123.1562822098)** page.
    * From the **Service account** list, select **New service account**.
    * In the **Service account name** field, enter a name.
    * From the **Role** list, select **Datastore** > **Cloud Datastore User** and  **App Engine** > **App Engine Admin**
    * Click **Create**. A JSON file that contains your key downloads to your computer.
	    * If you are using Cloud Shell, move the JSON file to the shell
    * Save the JSON file path as an environment varibale
    ```export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"``` 
     
	     For example:
     ```  export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"```
    (note: this variable only applies to your current shell session, so you need to set the variable again if you open a new session.)
2. Enable APIs
    * Go to the [GCP Console API Library](https://console.cloud.google.com/apis/library?project=_). 
	* Search Cloud Build. 
	* On the Cloud Build API page, click **ENABLE**.
3. Setup the gcloud tool, if you haven't already.
    
    ```
    gcloud init
    ```
    
 
4.  Use gcloud to deploy your app.
    
    ```
    gcloud app deploy app.yaml --project [project-id]
    ```
    
5.  Congratulations! You can now set up your profile service at  `your-app-id.appspot.com/user`



## Pipeline

                             +------------------------+     
                             |          |             |  
                             |  Web UI  |             |                  
              +--------------|          |  Golang     |                                     
              |              +----------+  AppEngine  |
              |              |          |             |
              |              | JSON List|             |
              |              +-----^------------+-----+
              |                    |            |                          
              +--v------------+----+            |                   
              |    User Profile    |            |                           
              |                    |            |                            
              |Username            |            | +----------+                              
              |Email               |            +-> Datastore|                              
              |Account blance      |              |          |                              
              |Address             |              |          |                              
              |                    |              +----------+                              
              +--------------------+    

Golang Google AppEngine (GAE) stores user profiles in Datastore and allow users to create, read, update, and delete their profile using REST APIs


## License



## Acknowledgments

