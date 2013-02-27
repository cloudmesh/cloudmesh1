try:
    # Expect to have gold command line tools pre-installed
    from sh import gmkuser
    from sh import gmkmachine
    from sh import gmkproject
    from sh import gdeposit
    from sh import gbalance
    from sh import gquote
    from sh import gcharge
    from sh import greserve
    from sh import grefund
    from sh import gchaccount
    from sh import glstxn
    from sh import gstatement
    from sh import gusage
    from sh import goldsh
    from sh import glsuser
    from sh import gchuser
    from sh import grmuser
    """
    $ ls /opt/gold/bin/
    gbalance    gchquote    glsproject  gmkproject  grmjob      gusage
    gchaccount  gchres      glsquote    gmkuser     grmmachine  gwithdraw
    gchalloc    gchuser     glsres      goldsh      grmproject  mybalance
    gcharge     gdeposit    glstxn      gquote      grmquote
    gchjob      glsaccount  glsuser     grefund     grmres
    gchmachine  glsalloc    gmkaccount  greserve    grmuser
    gchpasswd   glsjob      gmkjob      grmaccount  gstatement
    gchproject  glsmachine  gmkmachine  grmalloc    gtransfer
    """

except:
    pass

class FGGoldAccounting:

    """ 
        futuregrid.flask.cm
       
        Python GOLD Accounting Manager API based on command line tools. (DRAFT)
        SSSRMAP can be used (SSSRMAP is a XML based message format for Gold)

    Reference
    User Guide (including command line tools): http://www.clusterresources.com/products/gold/docs/userguide-2.2.0.pdf
    SSRMAP format: http://www.clusterresources.com/products/gold/docs/SSSRMAP%20Message%20Format%203.0.4.doc
    Gold documentation: http://www.clusterresources.com/products/gold/docs/

    """

    def define_user(self):
        """Add/Create a user

        Args:

        Returns:

        Raises:

        >>> gmkuser
        Usage:
            gmkuser [-A|-I] [-n *common_name*] [-F *phone_number*] [-E
            *email_address*] [-p *default_project*] [-d *description*] [-X |
            --extension *property*=*value*]* [--debug] [-?, --help] [--man]
            [--quiet] [-v, --verbose] [-V, --version] {[-u] *user_name*}

        >>> gmkuser -n "Wilkes, Amy" -E "amy@western.edu" amy
        Successfully created 1 User

        """

        gmkuser()

    def define_machine(self):
        """Add/Create a machine

        $ gmkmachine
        Usage:
            gmkmachine [-A|-I] [--arch *architecture*] [--opsys *operating_system*]
            [-d *description*] [-X | --extension *property*=*value*]* [--debug] [-?,
            --help] [--man] [--quiet] [-v, --verbose] [-V, --version] {[-m]
            *machine_name*}

        $ gmkmachine -d "Linux Cluster" colony
        Successfully created 1 Machine

        """
        gmkmachine()

    def define_project(self):
        """Add/Create a project

        $ gmkproject
        Usage:
            gmkproject [-A|-I] [-u *user_name*[,*user_name*]*] [-m
            *machine_name*[,*machine_name*]*] [-d *description*] [-X | --extension
            *property*=*value*]* [--createAccount=True|False] [--debug] [-?, --help]
            [--man] [--quiet] [-v, --verbose] [-V, --version] {[-p] *project_name*}

        $ gmkproject -d "Biology Department" biology
        Successfully created 1 Project
        Auto-generated Account 1

        """
        gmkproject()
    
    def make_deposit(self):
        """Make deposit

        $ gdeposit
        Usage:
            gdeposit {-a *account_id* | { -p *project_name* &| -u *user_name* &| -m
            *machine_name*}} [-i *allocation_id*] [-s *start_time*] [-e *end_time*]
            [-L *credit_limit*] [-d *description*] [-h, --hours] [--debug] [-?,
            --help] [--man] [--quiet] [-v, --verbose] [-V, --version] [[-z]
            *amount*]

        $ gdeposit -s 2005-01-01 -e 2006-01-01 -z 360000000 -p biology
        Successfully deposited 360000000 credits into account 1
        """

        gdeposit()

    def check_balance(self):
        """Check the balance

        $ gbalance -u amy
        Id Name Amount Reserved Balance CreditLimit Available
        -- --------- --------- -------- --------- ----------- ---------
        1 biology 360000000 0 360000000 0 360000000
        2 chemistry 360000000 0 360000000 0 360000000

        $ gbalance
        Id Name     Amount    Reserved Balance   CreditLimit Available
        -- -------- --------- -------- --------- ----------- ---------
        1  fg       309988581        0 309988581           0 309988581
        2  fgdiablo  -7619393        0  -7619393           0  -7619393

        """
            
        gbalance()

    def obtain_jobquote(self):
        """Obtain a job quote
        When a job is submitted, it is useful to check that the user.s account has enough funds to run the job.
        This will be veri.ed when the job starts, but by that point the job may have waited some time in the
        queue only to .nd out it never could have run in the .rst place. The job quotation step (see Obtaining Job
        Quotes) can .ll this function. Additionally, the quote can be used to determine the cheapest place to run,
        and to guarantee the current rates will be used when the job is charged.

        $ gquote -p chemistry -u amy -m colony -P 16 -t 3600
        Successfully quoted 57600 credits

        """
        gquote()

    def chart_job(self):
        """Charge a job
        After a job completes, any associated reservations are removed and a charge is issued against the
        appropriate allocations based on the actual wallclock time used by the job (see Charging Jobs).

        $ gcharge
        Usage:
            gcharge [-u *user_name*] [-p *project_name*] [-m *machine_name*] [-C
            *queue_name*] [-Q *quality_of_service*] [-P *processors*] [-N *nodes*]
            [-M *memory*] [-D *disk*] [-S *job_state*] [-n *job_name*]
            [--application *application*] [--executable *executable*] [-t
            *charge_duration*] [-s *charge_start_time*] [-e *charge_end_time*] [-T
            *job_type*] [-d *charge_description*] [--incremental] [-X | --extension
            *property*=*value*]* [--debug] [-?, --help] [--man] [--quiet] [-v,
            --verbose] [-V, --version] [[-j] *gold_job_id*] [-q *quote_id*] [-r
            *reservation_id*] {-J *job_id*}

        $ gcharge -J PBS.1234.0 -u amy -p chemistry -m colony -P 16 -t 1234 -X
        WallDuration=1234
        Successfully charged job PBS.1234.0 for 19744 credits
        1 reservations were removed

        """
        gcharge()

    def make_reservation(self):
        """Make a job reservation
        When a job starts, the resource management system creates a reservation (or pending charge) against the
        appropriate allocations based on the estimated wallclock limit speci.ed for the job (see Making a Job
        Reservation).

        $ greserve
        Usage:
            greserve [-u *user_name*] [-p *project_name*] [-m *machine_name*] [-o
            *organization*] [-C *queue_name*] [-Q *quality_of_service*] [-P
            *processors*] [-N *nodes*] [-M *memory*] [-D *disk*] [-n *job_name*]
            [--application *application*] [-t *reservation_duration*] [-s
            *reservation_start_time*] [-e *reservation_end_time*] [-T *job_type*]
            [-d *reservation_description*] [-X | --extension *property*=*value*]*
            [--replace] [--debug] [-?, --help] [--man] [--quiet] [-v, --verbose]
            [-V, --version] [[-j] *gold_job_id*] [-q *quote_id*] {-J *job_id*}

        $ greserve -J PBS.1234.0 -p chemistry -u amy -m colony -P 16 -t 3600
        Successfully reserved 57600 credits for job PBS.1234.0
        """

        greserve()

    def refund_job(self):
        """Make a refund for a job
        Now, since this was an imaginary job, you had better refund the user.s account (see Issuing Job Refunds).

        $ grefund
        Usage:
            grefund [-z *amount*] [-a *account_id*] [-d *description*] [-h, --hours]
            [--debug] [-?, --help] [--man] [--quiet] [-v, --verbose] [-V, --version]
            {-J *job_id* | [-j] *gold_job_id*}

        $ grefund -J PBS.1234.0
        Successfully refunded 19744 credits for job PBS.1234.0
        """
        grefund()

    def modify_account(self):
        """Modify account
       
        $ gchaccount
        Usage:
            gchaccount [-n *account_name*] [-d *description*] [--addProjects
            *project_name*[,*project_name*]*] [--addUsers
            *user_name*[,*user_name*]*] [--addMachines
            *machine_name*[,*machine_name*]*] [--delProjects
            *project_name*[,*project_name*]*] [--delUsers
            *user_name*[,*user_name*]*] [--delMachines
            *machine_name*[,*machine_name*]*] [-X | --extension *property*=*value*]*
            [--debug] [-?, --help] [--man] [--quiet] [-v, --verbose] [-V, --version]
            {[-a] *account_id* | { -p *project_name* &| -u *user_name* &| -m
            *machine_name*}}

        $ gchaccount --addUser dave 1
        Successfully created 1 AccountUser

        """

        gchaccount()

    def list_transaction(self):
        """List transactions
        $ glstxn -O Job
        --show="RequestId,TransactionId,Object,Action,JobId,Project,User,Machine,Amount"
        RequestId TransactionId Object Action JobId Project User Machine Amount
        --------- ------------- ------ ------- ---------- --------- ---- ------- ------
        298 299 Job Create
        298 303 Job Quote chemistry amy colony 57600
        299 304 Job Modify
        299 307 Job Reserve PBS.1234.0 chemistry amy colony 57600
        300 311 Job Charge PBS.1234.0 chemistry amy colony 19744
        300 312 Job Modify
        301 314 Job Refund PBS.1234.0
        301 315 Job Modify
        """
        glstxn()

    def get_statement(self):
        """Examine Account Statement

        $ gstatement -p chemistry
        ################################################################################
        #
        # Statement for account 2 (chemistry) generated on Tue Aug 3 16:06:15 2005.
        #
        # Reporting account activity from -infinity to now.
        #
        ################################################################################
        Beginning Balance: 0
        ------------------ --------------------
        Total Credits: 360019744
        Total Debits: -19744
        ------------------ --------------------
        Ending Balance: 360000000
        ############################### Credit Detail ##################################
        Object Action JobId Amount Time
        ------- ------- ---------- --------- ----------------------
        Account Deposit 360000000 2005-08-03 16:01:15-07
        Job Refund PBS.1234.0 19744 2005-08-03 16:04:02-07
        ############################### Debit Detail ###################################
        Object Action JobId Project User Machine Amount Time
        ---------- ---------- ---------- --------- ---- ------- ------ ----------------------
        Job Charge PBS.1234.0 chemistry amy colony -19744 2005-08-03 16:03:39-07
        24
        """
        gstatement()

    def get_usage(self):
        """Examine project usage
        $ gusage -p chemistry
        ################################################################################
        #
        # Usage Summary for project chemistry
        # Generated on Tue Feb 8 11:05:06 2005.
        # Reporting user charges from 2006-07-01 to 2006-10-01
        #
        ################################################################################
        User Amount
        ---- ------
        amy 19744
        """
        gusage()

    def define_charge_rate(self):
        """Define chart rates
        Gold allows you to de.ne how much you will charge for your resources (see Creating Charge Rates).
        In the Getting Started chapter, we relied on the fact that the default Gold installation prede.nes a
        Processors charge rate for you. This means that the total charge for a job will be calculated by taking the
        number of processors used in the job multiplied by the Processors charge rate which is then multiplied by
        the wallclock limit. For example: ( ( 16 [Processors] * 1 [ChargeRate{VBR}{Processors}] ) ) * 1234
        [WallDuration] = 19744

        $ goldsh ChargeRate Query
        Type Name Instance Rate Description
        ---- ---------- -------- ---- -----------
        VBR Processors 1

        $ goldsh ChargeRate Create Type=VBR Name=Memory Rate=0.001
        Successfully created 1 ChargeRate
        """
        goldsh()

    def get_user(self):
        """Querying users

        To display user information, use the command glsuser:
        $ glsuser
        Usage:
            glsuser [-A|-I] [--show *attribute_name*[,*attribute_name*]*]
            [--showHidden] [--showSpecial] [-l, --long] [-w, --wide] [--raw]
            [--debug] [-?, --help] [--man] [--quiet] [-V, --version] [[-u]
            *user_pattern*]
        
        $ glsuser -A
        Name Active CommonName PhoneNumber EmailAddress DefaultProject Description
        ---- ------ ---------------- -------------- ---------------- -------------- -----------
        amy True Wilkes, Amy (509) 555-8765 amy@western.edu
        bob True Smith, Robert F. (509) 555-1234 bob@western.edu


        $ glsuser --show PhoneNumber bob --quiet
        (509) 555-1234
        """
        glsuser()

    def set_user(self):
        """modifying user

        $ gchuser -A bob
        Successfully modified 1 User
        """
        gchuser()

    def del_user(self):
        """Deleting user

        $ grmuser bob
        Successfully deleted 1 User
        """
        grmuser()

# MORE to COME
