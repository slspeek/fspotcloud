# Release critical improvements for version 1.0 #


## Build challenges ##
  * cobertura, and analysis in separate build files
## Test challenges ##
  * Selenium against live GAE-app (deploy via gradle)
  * have tests run with a fake session in testscope (Make a fake GAE-session)
  * have tests run in server (tomcat, jetty, dev\_app\_server?)
  * more introspection through toString

# Middle term #
  * keyboard action should work with state-flag-set
  * log file for j2ee-war
  * Refactor openid jsps to servlets to include them in a guice module
  * SimpleJpaDao: tests for cached version
  * Manual test description for installer or Sikuli
  * Run-time configuration of image dimensions

# Plans after 1.0 #
  * ImageServlet must return 403 when appropriate.
  * Blobstore caching
  * Look at caching for j2ee
  * Big integration test to test to authorization
  * Guice Modules per package, and factory (GWT)Tests.
  * Use polymorphy for ImageRaster with 0x0.
  * Refactor a Rasterer out of Navigator
  * Status text event with suggestions
  * 'a then b'-style keyboard shortcuts
  * Virtual 'All Images Tag' used when no tag is selected
  * Image horizontally divided by three to tab (click) for previous,
full-screen or next
  * real pager buttons, depending on category size and pagesize
  * Separation of configuration/cache data
  * Cobertura coverage of selenium tests
  * Internationalization
  * Minimum test coverage for a build
  * Threadpool for the peer
  * Horizontal scrollbar under the images
  * Time based photo view
  * Proportional based paging
  * Watch together using channels/sockets

# Project multi-peer #
  * Extra peer\_id in photos
  * Extra peer\_id in tag
  * Modify PeerDatabases
## Client ##
  * One more level in the tree
  * Admin your peers
## Bot-Dispatch ##
  * Dispatch: execution targetId
  * Bot: sends its secret id (as targetId) as it requests work
  * Botdispatch: time out commands




