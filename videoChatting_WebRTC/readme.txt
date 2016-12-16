1. first download and install node js. https://nodejs.org/en/

2. Create your project folder and navigate to project folder path using command prompt.

3. now, type   npm init    command to setup the project and click enter. It will ask bunch of questions, so keep hiting enter.
   this will create package.json file preloaded with some content.

4. Now, we need to install two libraries, called budo and watchify.
   type npm install budo watchify --save-dev    to install.
   --save-dev It will add dependencies to our package.json file.

5. update script section in package.json  "start": "budo home.js --live"  and to run the budo server, type npm start.  
   to check it open browser and type   localhost:9966   as it runs on port 9966.
   So, whatever changes you do in index.js file, it will be reflected on webpage   localhost:9966.

6. So, This was our setup for the project now let's start coding.


This project is purely based on the javascript and it will run on web browser. We are going to use webRTC library to build this application.

webRTC is used for real time communication and basically it is set of API's in the browser that allows us to stream video or audio back and forth to each other.
Even we can send data with it.

We are using another package called simple-peer which is used to exchange signaling data between the two browsers until a peer-to-peer connection is established.

PS: npm is a NodeJS package manager. As its name would imply, you can use it to install node programs.

7. To install simple-peer package type     npm install simple-peer --save     on command prompt.

budo library is only used for bundling our js file and not used for any of the peer to peer or networking stuff. It provides server platform for 
us to do networking stuff.






