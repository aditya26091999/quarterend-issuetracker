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