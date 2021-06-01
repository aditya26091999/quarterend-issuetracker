companyRegisteration_sql = "INSERT INTO globalcompany_schema.company (company_id, company_name,company_address,company_admin_email,company_admin_password) VALUES (%s, %s, %s, %s, %s)"
companySpecificSchemaCreation_sql = "CREATE SCHEMA "
userTableCreation_sql = "CREATE TABLE {}.user (  user_id VARCHAR(64) NOT NULL,  user_name VARCHAR(255) NOT NULL,  user_email VARCHAR(255) NOT NULL,  user_password VARCHAR(30) NOT NULL,  PRIMARY KEY (user_id),  UNIQUE INDEX user_email_UNIQUE (user_email ASC) VISIBLE)"
issueTrackerTableCreation_sql = """CREATE TABLE {}.issuetracker (
  issue_id VARCHAR(64) NOT NULL,
  issue_title VARCHAR(255) NOT NULL,
  issue_description VARCHAR(255) NOT NULL,
  issue_submittedby VARCHAR(64) NOT NULL,
  issue_assignedto VARCHAR(64) NULL,
  issue_date DATE NOT NULL,
  issue_priority INT NOT NULL DEFAULT 3,
  issue_resolved TINYINT NOT NULL DEFAULT 0,
  issue_solution VARCHAR(255) NULL,
  PRIMARY KEY (issue_id),
  INDEX fk_submittedby_idx (issue_submittedby ASC) VISIBLE,
  INDEX fk_assignedto_idx (issue_assignedto ASC) VISIBLE,
  CONSTRAINT fk_submittedby
    FOREIGN KEY (issue_submittedby)
    REFERENCES {}.user (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_assignedto
    FOREIGN KEY (issue_assignedto)
    REFERENCES {}.user (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE);"""

adminLogin_sql = "SELECT company.company_id,company.company_name,company.company_address, company.company_admin_email FROM globalcompany_schema.company WHERE company.company_admin_email=%s AND company.company_admin_password=%s"

lookupCompanyUIDForUserRegisteration_sql = "SELECT company_id from globalcompany_schema.company where company_name=%s"
userRegisteration_sql = "INSERT INTO {}.user(user_id,user_name,user_email,user_password) VALUES (%s,%s,%s,%s)"
userLogin_sql = "SELECT user_name FROM {}.user WHERE user_email=%s AND user_password=%s"

userIdlookup_sql = "SELECT user_id FROM {}.user where user_email=%s"
issueTrackerIssueCreation_sql = "INSERT INTO {}.issuetracker (issue_id,issue_title,issue_description,issue_submittedby,issue_assignedto,issue_date,issue_priority,issue_resolved,issue_solution) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
issueTrackerShowIssues_sql = """SELECT T1_id,issue_title,issue_description, issue_date, issue_priority, issue_resolved, issue_solution, T2_username,T2_useremail,T3_username,T3_useremail   FROM (
	(SELECT A.issue_id AS T1_id, A.issue_title, A.issue_description, A.issue_date, A.issue_priority, A.issue_resolved, A.issue_solution FROM {}.issuetracker A) AS T1
    INNER JOIN (SELECT A.issue_id AS T2_id, B.user_name AS T2_username,B.user_email AS T2_useremail FROM {}.issuetracker A, {}.user B where B.user_id=A.issue_submittedby) AS T2 ON T1.T1_id=T2.T2_id
    INNER JOIN (SELECT C.issue_id AS T3_id, D.user_name AS T3_username,D.user_email AS T3_useremail FROM {}.issuetracker C, {}.user D where D.user_id=C.issue_assignedto) AS T3 ON T1.T1_id=T3.T3_id
) ORDER BY T1_id"""
