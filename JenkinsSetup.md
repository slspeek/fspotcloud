# Introduction #

To get better insight in the health of the project we use continuus integration with http://jenkins-ci.org/.


# Installation #

```
cd ~
hg clone https://code.google.com/p/fspotcloud.jenkins/ 
cd fspotcloud.jenkins/
```
Because Debian Wheezy sudo is a bit broken, we su to root
```
su
./setup_jenkins.sh 
```

This should setup jenkins with working directory /home/jenkins and
its webinterface at port 9000.

```
sudo su - jenkins
hg clone https://code.google.com/p/fspotcloud.install/ 
cd fspotcloud.install
./install-gae-sdk.sh
```

This takes care of installing appengine sdk.

Now go to http://localhost:9000/pluginManager/advanced
and actualize now (at the bottom of the screen).

```
./install_jenkins_plugins.sh
```

Now you are ready and you can go http://localhost:9000/