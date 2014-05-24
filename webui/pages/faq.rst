FAQ
======================================================================

This section will include a number of FAQs

:Are there any screenshots?:

  A number of `screenshots </screenshots>`_ is available to showcase some of 
  the features.

Setup 
---------------------------------------------------------------

:How do I login?:

  You need to have a futureGrid account. You can use your FutureGrid
  username and password to login. If you do not have an account note
  that it is easy to apply for an `account and project on FutureGrid
  <http://manual.futuregrid.org/account.html>`_.

:How do I get started?:

  You need to first register clouds and make sure you provide the
  proper credentials to the cloud. If you change the password,
  naturally you also need to update it in cloudmesh, for now.
  
  
:I like to start a VM but get an error with the key ...:

  You need to go to the registration window for the clouds and press
  on the key button for each cloud to register your keys.

  We have not automatized the process of uploading your keys to all
  clouds at once.

Setup - Local deploy
--------------------

:Can I deploy Cloudmesh on my local machine?:

  Yes. We are preparing a manual that describes how to set it up.  We
  have successfully shown cloudmesh has been installed by a number of
  different users. If you like to improve the installation
  instructions please help.


General Questions
---------------------

:Can I install cloudmesh on my local computer?:

  Yes you can. Cloudmesh is developed from the start with the
  principal that you ought to be able to run it in shared user mod, or
  on your local computer. When you run it on your local computer you
  will be able to start it from yaml configuration files containing
  your user data.
  
:Can I use cloudmesh to connect to AWS, Azure, HP cloud, EC2 clouds?:

  Yes you can. We do support the OpenStack native protocols and EC2 via
  our cloudmesh compatibility IaaS library. This library registers
  clouds by name, so you can for example refresh images, flavors, and
  servers from them.  The EC2 integration is done via libcloud
  allowing you in principal to access the many clouds libcloud
  supports. If you need a cloud and it is not supported, please let us
  know.
  
:How do you support other clouds behind firewalls?:

  We are currently developing a proxy service that allows us interact
  with the clouds that are behind a firewall.

:How is it possible that you can support clouds such as Azure that obviously do not have EC2 interfaces?:

  We have developed a very simple abstraction in cloudmesh that allows
  us to integrate custom calls and methods to other clouds. Thus it is
  possible for us to support multiple protocols as well as even
  different access technologies such as API, command line, or REST
  calls. Good examples are OpenStack which we communicate with in the
  native OpenStack REST calls, while we use command line interfaces
  while communicating with other clouds.


Development Questions
----------------------------

:Can I participate in the development?:

  Yes, Yes, Yes. We love your participation. If you have ideas or want
  to help on extending cloudmesh, or even documentation, testing and
  code cleanup let us know. You will be properly acknowledged in our
  future releases.

:I like to contribute my code to cloudmesh?:

  Yes you can do that. We can create you a repository on cloudmesh. We
  need to discuss and agree how to best integrate your code.
  
:You use Flask why not Django?:

  When we started the project we found that the entry level to django
  was too high for students to participate. We originally used
  cherypy, but have since used flask. In a future version we will
  consider django. We look for helpers than can help us with the
  transition. In the meanwhile we will continue to use flask. We
  believe it will not be that difficult to switch to django.

Collaboration
----------------------------------------------------------------------
  
:Can I get credit at my university?:

  At IU you can get credit by enrolling in an independent
  study. Typically 3 credit hours result in 12 hours of work per
  week. You get out of this independent study as much as you put
  in. We us modern software engineering tools so you do not just
  contribute code, but you learn also about software engineering
  aspects in a fast developing project.  We have lots of aspects you
  can work on dependent on your interest and background we can
  determine a project that interests you. Please contact
  laszewski@gmail.com
  
:Can I work with you if I am not at IU?:

  If you are at a different university we you need to find a faculty
  member at your university that allows you to participate in the
  development and issues you credits for it.
  

:What is the time commitment for an independent study?:

  Typically we require you enroll fro 3 credit hours, The total commit
  ment per week is than between 12-20 hours. If you do below 12 hours
  you will not get an A for sure.

  Furthermore we do not accept students that plan to take extensive
  vacation before and after the christmas break. We expect that you
  work till the last day of the semester and be here back on the first
  day of the semester. Exceptions need to be approved at least one
  month ahead of time. Any lost time will result in that you get an
  incomplete and need to catch up later.

  

Student Jobs
----------------------------------------------------------------------

:Can I get a research assistantship at IU to work on cloudmesh?:

  Yes, at this time we require you to take an independent study with
  us at IU so we can make sure you are up to the task. Exceptional
  candidates may be considered without this requirement. Please
  contact laszewski@gmail.com for mor info, but do not ask me for a
  paid job if you have not superior python, flask, git, openstack
  knowledge. For those that want to get started we have independent
  studies.

:If I take an hourly job, what time commitment is this?:

  International students can are required to work 20 hours per
  week. Payment is competitive and depends on background knowledge.

:What are we looking for?:

  It is helpful to be a proven expert in a
  technology that is used in cloudmesh such as
  
  * python
  * javascript including jquery
  * flask
  * django
  * desire to work in a team and contribute
  
:But I am a super java developer and do not have any knowledge about the above can I not just get paid for learning the above technologies?:
  
  In case we would hire you, you are responsible to learn such
  technologies in your free time. It is a prerequisite for
  participation. We offer independent studies.
  
:I am at a different university. Can I get a paid internship with you?:

  No. However we have visitors form China and Turkey, that are paid
  through a government grant of their home country. I am sure you can
  get one to participate here.


