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
    from sh import glsmachine
    from sh import gchmachine
    from sh import grmmachine
    from sh import glsproject
    from sh import gchproject
    from sh import grmproject
    from sh import glsaccount
    from sh import grmaccount
    from sh import glsalloc
    from sh import gchalloc
    from sh import grmalloc
    from sh import glsres
    from sh import gchres
    from sh import grmres
    from sh import glsquote
    from sh import gchquote
    from sh import grmquote
    from sh import gchpasswd
    from sh import glsjob
    from sh import gmkjob
    from sh import gtransfer

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

    Note for implementation
    set_*, del_* should be merged into single function set_* is preferred to manage add/delete/update?

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

        $ grmuser
        grmuser [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {[-u] user_name}

        $ grmuser bob
        Successfully deleted 1 User
        """
        grmuser()

    def get_machine(self):
        """Querying machine
        
        To display machine information, use the command glsmachine:

        $ glsmachine [-A | -I] [—show
            attribute_name[,attribute_name...]...] [—showHidden] [—showSpecial] [—raw] [—debug] [-? |
            —help] [—man] [—quiet] [[-m] machine_pattern]
                    
        $ glsmachine -I --show Name,Description
        Name Description
        ----- ------------------------
        inert This machine is unusable
        """
        glsmachine()

    def set_machine(self):
        """Modifying machine

        To modify a machine, use the command gchmachine:
        
        $ gchmachine [-A | -I] [—arch architecture] [—opsys operating_system] [-d
            description] [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {[-m] machine_name}

        $ gchmachine -I colony
        Successfully modified 1 Machine
        """
        gchmachine()

    def del_machine(self):
        """Deleting Machines

        To delete a machine, use the command grmmachine:
        
        $ grmmachine [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {[-m] machine_name}

        $ grmmachine colony
        Successfully deleted 1 Machine
        """
        grmmachine()

    def get_project(self):
        """Querying project

        To display project information, use the command glsproject:

        $ glsproject [-A | -I] [—show
        attribute_name [,attribute_name...]...] [—showHidden] [—showSpecial] [-l | —long] [-w |
        —wide] [—raw] [—debug] [-? | —help] [—man] [—quiet] [[-p] project_pattern]

        $ glsproject
        Name Active Users Machines Description
        --------- ------ ------------ -----------------------------
        biology True amy,bob colony Biology Department
        chemistry True amy,dave,bob Chemistry Department

        $ glsproject --show Name,Users -l chemistry
        Name Users
        --------- -----
        chemistry bob
        dave
        amy

        $ glsproject --show Name --quiet
        biology
        chemistry
        """
        glsproject()

    def set_project(self):
        """Modifying project

        To modify a project, use the command gchproject:

        $ gchproject [-A | -I] [-d description] [—addUser(s) [+ | -]user_name [, [+ |
        -]user_name...]] [—addMachines(s) [+ | -]machine_name [, [+ | -]machine_name...]] [—delUser(s)
        user_name [,user_name...]] [—delMachines(s) machine_name [,machine_name...]] [—actUser(s)
        user_name [,user_name...]] [—actMachines(s) machine_name [,machine_name...]] [—deactUser(s)
        user_name [,user_name...]] [—deactMachines(s)
        machine_name [,machine_name...]] [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {[-p]
        project_name}

        $ gchproject -I chemistry
        Successfully modified 1 Project

        $ gchproject --addUsers jsmith,barney chemistry
        Successfully created 2 ProjectUsers

        $ gchproject --addMachines colony chemistry
        Successfully created 1 ProjectMachines
        """
        gchproject()

    def del_project(self):
        """Deleting project

        To delete a project, use the command grmproject:

        $ grmproject [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {[-p] project_name}

        $ grmproject chemistry
        Successfully deleted 1 Project
        """
        grmproject()

    def define_account(self):
        """Defining account

        Next, you can create your accounts (see Creating Accounts). Think of your accounts as bank accounts to
        which you can associate the users, projects and machines that can use them.

        $ gmkaccount -p biology -u MEMBERS -m MEMBERS -n "biology"
        Successfully created Account 1

        $ gmkaccount -p chemistry -u MEMBERS -m colony -n "chemistry on colony"
        Successfully created Account 2

        $ gmkaccount -p chemistry -u amy -n "chemistry for amy"
        Successfully created Account 3

        $ gmkaccount -p chemistry -u MEMBERS,-amy -n "chemistry not amy"
        Successfully created Account 4

        $ glsaccount
        Id Name Amount Projects Users Machines Description
        -- ------------------- ------ --------- ------------ -------- -----------
        1 biology biology MEMBERS MEMBERS
        2 chemistry on colony chemistry MEMBERS colony
        3 chemistry for amy chemistry amy ANY
        4 chemistry not amy chemistry MEMBERS,-amy ANY

        So what we have here is: 1) a single account for biology available to all of its deﬁned members and able
        to be used only on the blue machine (since blue is its only member machine) 2) an account usable toward
        the chemistry project on the colony machine only 3) an account usable anywhere for chemistry by amy
        only 4) an account usable anywhere for chemistry by any member except for amy
        """
        gmkaccount()

    def get_account(self):
        """Querying account

        To display account information, use the command glsaccount:

        $ glsaccount [-A | -I] [-n account_name] [-p project_name] [-u user_name] [-m machine_name] [-s
        start_time] [-e end_time] [—exact-match] [—show
        attribute_name [,attribute_name...]...] [—showHidden] [-l | —long] [-w | —wide] [—raw] [-h |
        —hours] [—debug] [-? | —help] [—man] [—quiet] [[-a] account_id]

        $ glsaccount --long
        Id Name Amount Projects Users Machines Description
        -- ---------- --------- --------- ------- -------- -----------
        1 Biology 360000000 biology MEMBERS blue
        2 Chemistry 360000000 chemistry MEMBERS ANY
        3 Cornucopia 0 ANY ANY ANY
        4 Not Dave 250000 biology -dave -blue

        $ glsaccount -u dave --long
        Id Name Amount Projects Users Machines Description
        -- ---------- --------- --------- ------- -------- -----------
        2 Chemistry 360000000 chemistry MEMBERS ANY
        3 Cornucopia 0 ANY ANY ANY
        """
        glsaccount()

    def set_account(self):
        """Modifying Accounts

        To modify an account, use the command gchaccount:

        $ gchaccount [-n account_name] [-d description] [—addProject(s) [+ | -]project_name [, [+ |
        -]project_name...]] [—addUser(s) [+ | -]user_name [, [+ | -]user_name...]] [—addMachine(s) [+ |
        -]machine_name [, [+ | -]machine_name...]] [—delProject(s)
        project_name [,project_name...]] [—delUser(s) user_name [,user_name...]] [—delMachine(s)
        machine_name [,machine_name...]] [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {[-a]
        account_id}

        $ gchaccount --addUser dave 1
        Successfully created 1 AccountUser
        """
        gchaccount()

    def mybalance(self):
        """Personal Balance

        The mybalance has been provided as a wrapper script to show users their personal balance. It provides a
        list of balances for the projects that they can charge to:

        $ gbalance [-h | —hours] [-? | —help] [—man]

        $ mybalance
        Project Balance
        --------- -------------
        biology 324817276
        chemistry 9999979350400

        $ mybalance -h
        Project Balance
        --------- -------------
        biology 90227.02
        chemistry 2777772041.77
        """
        mybalance()

    def withdrawal(self):
        """Making Withdrawal
        
        To issue a withdrawal, use the command gwithdraw:

        $ gwithdraw {-a account_id | -p project_name} [-i allocation_id] {[-z] amount} [-d
        description] [-h | —hours] [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose]

        $ gwithdraw -z 12800 -a 1 -d "Grid Tax"
        Successfully withdrew 12800 credits from account 1

        If a project has a single account then a withdrawal can be made against the project.

        $ gwithdraw -z 12800 -p chemistry
        Successfully withdrew 12800 credits from account 2
        """
        gwithdraw()

    def transfer(self):
        """Making transfer

        To issue a transfer between accounts, use the command gtransfer. If the allocation id is speciﬁed, then
        only credits associated with the speciﬁed allocation will be transferred, otherwise, only active credits will
        be transferred. Account transfers preserve the allocation time periods associated with the resource credits
        from the source to the destination accounts. If a one-to-one mapping exists between project and account,
        then the fromProject/toProject options may be used in place of the fromAccount/toAccount options.

        $ gtransfer {—fromAccount source_account_id | —fromProject source_project_name | -i
        allocation_id} {—toAccount destination_account_id | —toProject
        destination_project_name} [-d description] [-h | —hours] [—debug] [-? |
        —help] [—man] [—quiet] [-v | —verbose] {[-z] amount}

        $ gtransfer --fromAccount 1 --toAccount 2 10000
        Successfully transferred 10000 credits from account 1 to account 2

        $ gtransfer --fromProject biology --toProject chemistry 10000
        Successfully transferred 10000 credits from account 1 to account 2
        """
        gtransfer()

    def del_account(self):
        """Deleting Account

        To delete an account, use the command grmaccount:

        $ grmaccount [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {[-a] account_id}

        $ grmaccount 2
        Successfully deleted 1 Account
        """
        grmaccount()

    def get_allocation(self):
        """Querying allocation

        To display allocation information, use the command glsalloc:

        $ glsalloc [-A | -I] [-a account_id] [-p project_name] [—show
        attribute_name [,attribute_name...]...] [—showHidden] [—raw] [-h | —hours] [—debug] [-? |
        —help] [—man] [—quiet] [[-i] allocation_id]

        $ glsalloc -a 4
        Id Account StartTime EndTime Amount CreditLimit Deposited Active Description
        -- ------- ---------- ---------- ------ ----------- --------- ------ -----------
        4 4 2005-01-01 2005-04-01 250000 0 250000 False
        5 4 2005-04-01 2005-07-01 250000 0 250000 False
        6 4 2005-07-01 2005-10-01 250000 0 250000 True
        7 4 2005-10-01 2006-01-01 250000 0 250000 False
        """
        glsalloc()

    def set_allocation(self):
        """Modifying allocation

        To modify an allocation, use the command gchalloc:

        $ gchalloc [-s start_time] [-e end_time] [-L credit_limit] [-d description] [-h |
        —hours] [—debug] [-? | —help] [--man] [—quiet] [-v | —verbose] {[-i] allocation_id}

        $ gchalloc -e "2005-01-01" 4
        Successfully modified 1 Allocation
        """
        gchalloc()

    def del_allocation(self):
        """Deleting allocation

        To delete an allocation, use the command grmalloc:

        grmalloc [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {-I | [-i] allocation_id}

        $ grmalloc 4
        Successfully deleted 1 Allocation

        $ grmalloc -I
        Successfully deleted 2 Allocations
        """
        grmalloc()

    def get_reservation(self):
        """Querying reservation

        To display reservation information, use the command glsres:

        $ glsres [-A | -I] [-n reservation_name | job_id_pattern] [-p project_name] [-u
        user_name] [-m machine_name] [—show
        attribute_name [,attribute_name...]...] [—showHidden] [-l | —long] [-w | —wide] [—raw] [-h |
        —hours] [—debug] [-? | —help] [—man] [—quiet] [[-r] reservation_id]

        $ glsres -u bob
        Id Name Amount StartTime EndTime Job User Project Machine Accounts Description
        -- ------------------ ------ ------------------- ------------------- --- ---- --------- ------- -------- -----------
        1 Interactive.789654 3600 2005-01-13 16:48:15 2005-01-13 17:48:15 1 bob chemistry blue 1

        $ glsres -u amy --option name=UseRules value=True
        Id Name Amount StartTime EndTime Job User Project Machine Accounts Description
        -- ------------------ ------ ------------------- ------------------- --- ---- --------- ------- -------- -----------
        1 Interactive.789654 3600 2005-01-13 16:48:15 2005-01-13 17:48:15 1 bob chemistry blue 1
        2 PBS.1234.0 7200 2005-01-13 17:59:09 2005-01-14 02:28:41 2 amy chemistry colo
        """
        glsres()

    def set_reservation(self):
        """Modifying reservation

        To modify a reservation, use the command gchres:

        $ gchres [-s start_time] [-e end_time] [-d description] [—debug] [-? |
        —help] [—man] [—quiet] [-v | —verbose] {[-r] reservation_id}

        $ gchres -e "2004-08-07 14:43:02" 1
        Successfully modified 1 Reservation
        """
        gchres()

    def del_reservation(self):
        """Deleting reservation

        To delete a reservation, use the command grmres:

        $ grmres [—debug] [-? | —help] [—man] [-q | —quiet] [-v | —verbose] {-I | -n reservation_name |
        job_id | [-r] reservation_id}

        $ grmres -n PBS.1234.0
        Successfully deleted 1 Reservation

        $ grmres 1
        Successfully deleted 1 Reservation

        $ grmres -I
        Successfully deleted 2 Reservations
        """
        grmres()

    def get_quotation(self):
        """Querying quotation

        To display quotation information, use the command glsquote:

        $ glsquote [-A | -I] [-p project_name] [-u user_name] [-m machine_name] [—show
        attribute_name [,attribute_name...]...] [—showHidden] [-l | —long] [-w | —wide] [—raw] [-h |
        —hours] [—debug] [-? | —help] [—man] [—quiet] [[-q] quote_id]

        $ glsquote -u amy -m colony
        Id Amount Job Project User Machine StartTime EndTime WallDuration Type Used ChargeRates Description
        -- ------ --- --------- ---- ------- ------------------- ------------------- ------------ ------ ---- --------------------- -----------
        1 57600 1 chemistry amy colony 2005-01-14 10:09:58 2005-09-10 15:27:07 3600 N
        """
        glsquote()

    def set_quotation(self):
        """Modifying quotations

        To modify a quotation, use the command gchquote:

        $ gchquote [-s start_time] [-e expiration_time] [-d description] [—debug] [-? |
        —help] [--man] [—quiet] [-v | —verbose] {[-q] quote_id}

        $ gchquote -e "2005-03-01" 1
        Successfully modified 1 Quotation
        """
        gchquote()

    def del_quotation(self):
        """Deleting quotation

        To delete a quotation, use the command grmquote:

        $ grmquote [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] {-I | [-q] quote_id}

        $ grmquote 1
        Successfully deleted 1 Quotation

        $ grmquote -I
        Successfully deleted 2 Quotations
        """
        grmquote()

    def define_job(self):
        """Creating Job

        In most cases, jobs will be created by the resource management system with the greserve or the gcharge
        command.
        However, it is also possible to create job records using the gmkjob command:

        $ gmkjob [-u user_name] [-p project_name] [-m machine_name] [-o organization] [-C
        queue_name] [-Q quality_of_service] [-P processors] [-N nodes] [-M memory] [-D disk] [-n
        job_name] [—applicationapplication] [—executableexecutable] [-t wallclock_duration] [-s
        start_time] [-e end_time] [-T job_type] [-d description] [-X | —extension
        property=value...] [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] [-V | —version] [[-J]
        job_id]

        $ gmkjob -u jsmith -p chem -m cluster -X Charge=2468 -P 2 -t 1234 -J
        PBS.1234.0
        Successfully created Job 102
        """
        gmkjob()

    def get_job(self):
        """Querying job

        To display job information, use the command glsjob:

        $ glsjob [[-J] job_id_pattern] [-p project_name] [-u user_name] [-m machine_name] [-C
        queue] [-T type] [—stage stage] [-s start_time] [-e end_time] [—show
        attribute_name[,attribute_name...]...] [—showHidden] [—raw] [—debug] [-? |
        —help] [—man] [—quiet] [-V | —version] [[-j] gold_job_id]

        $ glsjob --show=JobId,Project,Machine,Charge -u amy
        JobId Project Machine Charge
        ---------- --------- ------- ------
        PBS.1234.0 chemistry colony 0
        """
        glsjob()


    def set_job(self):
        """Modifying job

        It is possible to modify a job record by using the command gchjob:

        $ gchjob [-u user_name] [-p project_name] [-m machine_name] [-o organization] [-C
        queue_name] [-Q quality_of_service] [-P processors] [-N nodes] [-M memory] [-D disk] [-n
        job_name] [—applicationapplication] [—executableexecutable] [-t wallclock_duration] [-s
        start_time] [-e end_time] [-T job_type] [-d description] [-X | —extension
        property=value...] [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] [-V | —version] [[-j]
        gold_job_id | -J job_id]

        $ gchjob -Q HalfPrice --application=NwChem -X Charge=1234 -d "Benchmark" -J
        PBS.1234.0
        Successfully modified 1 Job
        """

        gchjob()

    def del_job(self):
        """Deleting job

        To delete a job, use the command grmjob:

        $ grmjob [—debug] [-? | —help] [—man] [—quiet] [-v | —verbose] [-V | —version] [[-j] gold_job_id |
        -J job_id]

        $ grmjob -J PBS.1234.0
        Successfully deleted 1 Job
        """
        grmjob()

    def set_password(self):
        """Changing password

        $ gchpasswd
        Usage:
            gchpasswd [--debug] [-?, --help] [--man] [--quiet] [-v, --verbose] [-V,
            --version] [[-u] *user_name*]

        """
        gchpasswd()
