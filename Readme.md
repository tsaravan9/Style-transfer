# [Team Iris](https://team-iris.me)
This is under the Visitor Engaement module for the Coding [Culture Hackathon](https://https://coding-culture.zkm.de/).

##### [Round 1 submission file](https://github.com/Nikhil-Kasukurthi/Style-transfer/raw/master/Visitor%20engagement.pdf)
# Style Transfer
To increase the vistor interaction in the museum, we propose the Style transfer module. 

When the user likes a particular painting, he/she can scan the name tag and try out their own images in the style of the painting. 

Here is an example. 

![Image](https://github.com/Nikhil-Kasukurthi/Style-transfer/raw/master/Layer%201.png)


## Install Instructions

To run the server

```
python server.py
```

If you want to test the model run

```
python main.py eval --content-image images/content/shenyang.jpg --style-image images/museum_styles/43-15.jpg --model /21styles.model --content-size 1024
```


## API Documentation

### Base URL
```
api.team-iris.me/style-transfer
```
#### Datset of styles available

```/dataset```
 
 ```
 METHOD: GET
 Parameters: None
 
 Response: 
           {
              "images": [
                  {
                      "Title": "The Sword of Damocles",
                      "Database ID": "22-4544",
                      "Link": "https://drive.google.com/open?id=1oVrDaOCQAslJMTyWP-9LW0COj5ZG1phD"
                  }, ... (clipped)
               ]
          }
 ```
 ### Upload content image to transfer onto
 ```/upload```
 
 ```
 METHOD: POST
 Parameters: 
         file (file): file to uplaod
 
 Response:
           {
              "style_image": "/static/flowers.jpg"
            }
 
 ```
