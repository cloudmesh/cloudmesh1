FAQ
======================================================================

This section will include a number of FAQs

Are there any screenshots?
---------------------------

* A number of `screenshots </screenshots>`_ is available to showcase some of 
  the features.

Setup - Register cloud in the cloudmesh.futuregrid.org service
---------------------------------------------------------------

How do I login?

* You need to have a futureGrid account. You can use your FutureGrid 
  username and password to login. If you do not have an account note that it is 
  easy to apply for an `account and project on FutureGrid <http://manual.futuregrid.org/account.html>`_.

How do I get started? 

* You need to first register clouds and make sure you provide the proper 
  credentials to the cloud. If you change the password, naturally you also need to 
  update it in cloudmesh, for now.
  
  
I like to start a VM but get an error with the key ...

* You need to go to the registration window for the clouds and press on the key 
  button for each cloud to register your keys.

  We have not automatized the process of uploading your keys to all clouds at once.

Setup - Local deploy
--------------------

We developed a manual that is currently under construction, we have successfully shown 
cloudmesh has been installed by a number of different users. If you like to improve the 
installation instructions please help.


General Questions
---------------------

Can I install cloudmesh on my local computer?

* Yes you can. Cloudmesh is developed from the start with the principal that you 
  ought to be able to run it in shared user mod, or on your local computer. When 
  you run it on your local computer you will be able to start it from yaml 
  configuration files containing your user data.
  
Can I use cloudmesh to connect to AWS, Azure, HP cloud, EC2 clouds?

* Yes you can we do support the OpenStack native protocols and EC2 via our 
  cloudmesh compatibility IaaS library. This library registers clouds by name,
  so you can for example refresh images, flavors, and servers from them.
  The EC2 integration is done via libcloud allowing you in principal to access 
  the many clouds libcloud supports. If you need a cloud and it is not supported, 
  please let us know.
  
How do you support other clouds behind firewalls?

* we are currently developing a proxy service that allows us interact with the clouds that 
  are behind a firewall.

How is it possible that you can support clouds such as tashi that obviously do not have EC2 
interfaces?

* We have developed a very simple abstraction in cloudmesh that allows us to integrate
  custom calls and methods to other clouds. Thus it is possible for us to support multiple 
  protocols as well as even different access technologies such as API, command line, 
  or REST calls. Good examples are OpenStack which we communicate with in the native 
  OpenStack REST calls, while we use command line interfaces while communicating with tashi 
  through a firewall.


Development Questions
----------------------------

Cloudmesh is cool, can I participate in the development?

* Yes, Yes, Yes. We love your participation. If you have ideas or want to help on extending cloudmesh, or even  
  documentation, testing and code cleanup let us know. You will be properly acknowledged in our future releases.

I like to contribute my code to cloudmesh?

* Yes you can do that. We can create you a repository on cloudmesh. We need to
  discuss and agree how to best integrate your code.
  
You use Flask why not Django?

* When we started the project we found that the entry level to django was too 
  high for students to participate. We originally used cherypy, but have since 
  used flask. In a future version we will consider django. We look for helpers 
  than can help us with the transition. In the meanwhile we will continue to use
  flask. We believe it will not be that difficult to switch to django.
  
Can I get credit at my university?
------------------------------------

* At IU you can get credit by enrolling in an independent study. Typically 3 credit 
  hours result in 12 hours of work per week. YOu get out of this independent study as
  much as you put in. We us modern software negeneering tools so you do not just contribute code,
  but you learn also about software negeneering aspects in a fast developing project.
  We have lots of aspects you can work on dependent on your interest and background 
  we can determine a project that interests you. Please contact laszewski@gmail.com
  
* If you are at a different university we you need to find a faculty member 
  at your university that allows you to participate in the development and
  issues you credits for it. 
  
Can I get a research assistentship at IU to work on cloudmesh?
---------------------------------------------------------

* Yes, and no but for this semester we are already maxed out due to administartive deleays.

* We prefer at this time hourly payment. International students can take up to 20 
  hours per week. Payment is competitive and depends on background knowledge
  
* What are we looking for. It is helpful to be a proven expert in a technolgy
  that is used in cloudmesh such as
  
  * python
  * javascript including jquery
  * flask
  * django
  * desire to work in a team and contribute
  
* But I am a super java developer and do not have any knowledge about the above can I not 
  just get paid for learning the above technologies?
  
  In case we would hire you, you are responsible to learn such technologies in 
  your freetime. It is a prerequisit for participation
  
* I am at a different university. CAn I get an internship with you?

  Now, however we have visitors form China and Turkey, that are paid through a 
  government grant of their home country. I am sure you can get one to participate here.


