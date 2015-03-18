# The build #
```
which hg || sudo apt-get install mercurial
hg clone https://code.google.com/p/fspotcloud.install/ 
cd fspotcloud.install
sudo ./install-as-root.sh
./install.sh
./install-gae-sdk.sh
./checkout.sh
source env.sh
ffbuild
```
This takes a long time and may need to be restarted one or more times
(When it fails quickly there is no need to restart).
# Setup your environment #
Use a terminal to
```
echo 'source ~/fspotcloud.install/env.sh'>>~/.bashrc
```
Any terminal started after this moment has the proper enviroment for
building and deploying this application.

As the main building tool is gradle I recommend IDEA as IDE.
First issue
```
reidea #The alias for "gradle cleanIdea idea"
```
Then open the ~/fspotcloud folder as project in IDEA.