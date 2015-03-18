# Introduction #

As the AppEngine becomes more commercial, you may want to deploy to an other server platform


# Program abstract #

## Data Abstraction ##
We use interfaces and DAO interfaces for our persistent data. Implementation via Objectify anf Hibernate.

## Task Abstraction ##
We will extend GWT-Dispatch to support asynchrone calling on the server side. This for the 30-secs limit on GAE.
On Tomcat these calls will be direct.

## OpenId Authentication ##