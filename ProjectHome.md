This product is ready to run, please see UserGuide.


# Introduction #
F-Spot Cloud is a synchronization system for the images stored in [F-Spot](http://f-spot.org). It synchronizes between your linux PC and your private server or Google AppEngine, with the purpose of showing the images in a nice gallery on the web.

Note that F-Spot Cloud does not do any writing at your local file-system, it only reads (a file-system copy of) the F-Spot SQLite database and opens the images for reading (This is not meant as a guarantee, but as an intention).

This is achieved by two software components:
  * The peer bot running on your PC
  * The server component running somewhere else

The administration is done from a dashboard running on the server. The imports you issue are stored in a message queue until the peer component picks them up.
When the peer bot runs it checks for new instructions from the server component every 30 seconds.
This means the if you keep the peer bot running when you leave your home, you can show all your images to people your meet. You can add and remove labels you show on the server from any place in the world as long as your peer bot runs.

# Features #
  * Graphical installers for all components that:
    * setup application menus
    * handle the deployment of the server component
  * Two equivalent distributions for:
    * Any J2EE server, we use an embedded Derby database
    * Google AppEngine
  * Per label import/removal from the gallery, done from the web and protected by authentication.
  * Group based access control per label configurable.
  * Two ways of authentication:
    * Builtin authentication with:
      * email-confirmation
      * password-recovery options
    * Google-athentication
  * When you remove a label in F-Spot from an image or you modify an image, F-Spot Cloud picks this up in the next synchronization. So when you add images in F-Spot to a label already imported, they will be picked up on next synchronization too.
  * The gallery supports zooming (under numpad - and +)
  * The gallery has the 'F-Spot-famous' all images category
  * The gallery can perform a slideshow
  * Any authenticated user can request the fullsize of an image she is allowed to see to be send by email. That request is saved to the database and handled the next time the peer connects.
  * The F-Spot Cloud gallery and dashboard online were designed to be used with the keyboard

**Developers, please note that 'everything' happens in the javasrc repository**
