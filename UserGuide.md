# Prerequisites #
Install openjdk-6-jre and imagemagick
```
$sudo apt-get install openjdk-6-jre imagemagick 
```
In order to use FSpotCloud you need to have F-Spot version 0.8.2. This version is in debian Wheezy. You can build it from source on debian-Squeeze based systems using this [script](http://code.google.com/p/fspotcloud/source/browse/build_f-spot.sh?repo=install).

# Choose your hosting #
You can host the server-component at Google AppEngine or
run a tomcat server with embedded derby database yourself.

## AppEngine hosting ##
### Register on http://appengine.google.com ###
Register a application and note the application-id.

### Download and run the installer ###
Download the latest fspotcloud-appegine.X-installer.jar from the downloads area.
Right-click the downloaded file and open it with the OpenJDK jre.
### Start the peer component ###
Using the FSpotCloud menu you start the peerbot.
It will poll every thirty seconds for instructions from your fspotcloud-appengine-component.

## Hosting from your home directory ##
To be able to use your server it must be visible on internet. This is for the openid authentication used to protect the dashboard. To get this done your can set up port forwarding for port 8080 in your modem.
### Download and run the installers ###
Download the latest fspotcloud-j2ee-X.X-installer.jar and fspotcloud-X.X-peer-installer from the downloads area.
Right-click the downloaded files and open them with the OpenJDK jre.

Use the menus created by the installer to
  1. Start the server
  1. Start the peer
  1. Launch a browser at your instance

# Importing images #
Again using the menu you go the your instance.
Press d to get to the dashboard. Your will have to authenticate using your Google-account.
Then you press Synchronize and wait a little.
Your Labels defined in F-Spot should become visible in the tree.
You select one and press Import.

Soon a lot of action must be going on in the peer-terminal window as it is picking up commands and executing them.

Press f to go back to your instance photo page and see your pictures.
To make this category publicly visible however, a little more must be
done:
Press m to manage groups and press c to create a new group. Select this
group and press e to edit it. You can name it whatever you like, but
check the 'visible for everyone' checkbox. Now save this group and press
escape to return to the dashboard. Now press A to manage the groups that may see your imported category. Select your public group on the right and press i to grant access to that group.
You can open a anynomous-browsing window and go to your instance to see that the category you granted public access to is now visible for all.
