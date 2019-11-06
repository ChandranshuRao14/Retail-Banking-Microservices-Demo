
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
    
3.  Setup the gcloud tool, if you haven't already.
    
    ```
    gcloud init
    ```
    
 
4.  Use gcloud to deploy your app.
    
    ```
    gcloud app deploy app.yaml --project [project-id]
    ```
    
5.  Congratulations! You can now set up your profile service at  `your-app-id.appspot.com`



## Pipeline

                     +------------------------+     
                     |          |             |  
                     |  Web UI  |             |                  
              +------|          |  Golang     |                                     
              |      +----------+  AppEngine  |
              |      |          |             |
              |      | JSON List|             |
              |      +-----^------------+-----+
              |            |            |                          
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

