FAQ
======================================================================

This section will include a number of FAQs

Are there any screenshots?
---------------------------

* A number of screenshots are available to showcase some of 
  the Cloudmesh features at :doc:`screenshots`

Setup - Register cloud in the cloudmesh.futuregrid.org service
---------------------------------------------------------------

How do I login?

* You need to have a FutureGrid account. You can use your FutureGrid
  username and password to login. If you do not have an account note
  that it is easy to apply for an `account and project on FutureGrid
  <http://manual.futuregrid.org/account.html>`_.

How do I get started? 

* You need to first register clouds and make sure you provide the
  proper credentials to the cloud. If you change the password,
  naturally you also need to update it in Cloudmesh, for now.
  
  
I like to start a VM but get an error with the key ...

* You need to go to the registration window for the clouds and press
  on the key button for each cloud to register your keys.

  We have not automatized the process of uploading your keys to all
  clouds at once.

Setup - Local deploy
--------------------

We developed a manual that is currently under construction. We have
successfully shown that Cloudmesh has been installed by a number of
different users. If you would like to improve the installation instructions, your help is appreciated.


General Questions
---------------------

Can I install Cloudmesh on my local computer?

* Yes you can. Cloudmesh is developed from the start with the
  principle that you ought to be able to run it in shared user mod, or
  on your local computer. When you run it on your local computer, you
  will be able to start it from yaml configuration files containing
  your user data.
  
Can I use Cloudmesh to connect to AWS, Azure, HP cloud, EC2 clouds?

* Yes you can. We support the OpenStack native protocols and EC2 via
  our Cloudmesh compatibility IaaS library. This library registers
  clouds by name, so you can for example refresh images, flavors, and
  servers from them.  The EC2 integration is done via libcloud
  allowing you in principle to access the many clouds libcloud
  supports. If you need a cloud and it is not supported, please let us
  know.
  
How do you support other clouds behind firewalls?

* We are currently developing a proxy service that will allow us to interact
  with clouds that are behind a firewall.

How is it possible that you can support clouds such as tashi that
obviously do not have EC2 interfaces?

* We have developed a very simple abstraction in Cloudmesh that allows
  us to integrate custom calls and methods to other clouds. Thus it is
  possible for us to support multiple protocols as well as even
  different access technologies such as API, command line, or REST
  calls. Good examples are OpenStack which we communicate with in the
  native OpenStack REST calls, while we use command line interfaces
  while communicating with tashi through a firewall.


Development Questions
----------------------------

Cloudmesh is cool. Can I participate in the development?

* Yes, Yes, Yes. We love your participation. If you have ideas or want
  to help on extending Cloudmesh, or even documentation, testing and
  code cleanup let us know. You will be properly acknowledged in our
  future releases.

I would like to contribute my code to Cloudmesh.

* Yes, you can do that. We can create a repository for you on Cloudmesh. We
  need to discuss and agree how to best integrate your code. Please contact us.
  
You use Flask. Why not Django?

* When we started the project we found that the entry level to django
  was too high for students to participate. We originally used
  cherypy, but have since used flask. In a future version we will
  consider django. We look for helpers than can help us with the
  transition. In the meanwhile we will continue to use flask. We
  believe it will not be that difficult to switch to django.
  


