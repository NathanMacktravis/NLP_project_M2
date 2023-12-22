# NLP_project_M2
This is an application to fetch youtube videos that fit a certain criteria.

* Collect of data ("collect_ytbe_data.ipynb") : 
    Using Youtube API to get data that contains this informations:
        - channel_id: ID of channel 	
        - channel_title: Title of the channel 
        - channel_Description: Description of the channel 
        - video_id: Id of a video in a channel 
        - video_title: Title of the video 
        - video_description: Description of the video 
        - video_publishedAt: Publication date of the video
        - video_transcript: Transcript of the video 

* Application ("ytbe_fetch_application.ipynb") :
    Preprocessing: 
        -> tokenization 
        -> Normalization of text data 


    Model : 
        -> Similarity cosinus approach 
        -> BM25 approach 
        -> LSI  models 
