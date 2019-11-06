
# Profileservice

A microservice where users can create, update, retrieve, and delete their profile information.

## Prerequisites

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/), including the [gcloud tool](https://cloud.google.com/sdk/gcloud/), and [gcloud app component](https://cloud.google.com/sdk/gcloud-app).

2. Setup the gcloud tool. This provides authentication to Google Cloud APIs and services.

   ```
   gcloud init
   ```

3. Clone this repo.

   ```
   git clone https://github.com/AppDev-Eng-Initative/Retail-Banking-Microservices-Demo.git
   cd profileservice
   ```


## Deployment

1.  Use the [Google Cloud Console](https://console.cloud.google.com/) to create a Google Cloud Platform project.
2.  [Enable billing](https://support.google.com/cloud/answer/6293499#enable-billing) for your project.
3. (Optional but recommended) Set up an App Engine service account for authentication
    * In the GCP Console, go to the **[Create service account key](https://console.cloud.google.com/apis/credentials/serviceaccountkey?_ga=2.142840501.-1637323123.1562822098)** page.
    * From the **Service account** list, select **New service account**.
    * In the **Service account name** field, enter a name.
    * From the **Role** list, select **Datastore** > **Cloud Datastore User**.
    * Click **Create**. A JSON file that contains your key downloads to your computer.
    * ```export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"``` 
     For example:
     ```  export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"```
    (note: this variable only applies to your current shell session, so you need to set the variable again if you open a new session.)
4.  Setup the gcloud tool, if you haven't already.
    
    ```
    gcloud init
    ```
    
 
5.  Use gcloud to deploy your app.
    
    ```
    gcloud app deploy app.yaml --project [project-id]
    ```
    
6.  Congratulations! You can now set up your profile service at  `your-app-id.appspot.com`



#### Pipeline

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

