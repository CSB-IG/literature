/*======================================================================*/
/*                                                                      */ 
/*                                                                      */
/*                         SQL Medline Schema                           */
/*                                                                      */
/*                           Diane E. Oliver                            */
/*                            Jan. 20, 2004                             */
/*                                                                      */
/*                              Based on:                               */
/*                         nlmmedline_021101.dtd                        */
/*                      nlmmedlinecitation_021101.dtd                   */
/*                         nlmcommon_021101.dtd                         */
/*                                                                      */
/*                             Located at:                              */
/*     http://www.nlm.nih.gov//databases//dtd//nlmmedline_021101.dtd    */
/* http://www.nlm.nih.gov/databases/dtd/nlmmedlinecitation_021101.dtd   */
/*      http://www.nlm.nih.gov/databases/dtd/nlmcommon_021101.dtd       */
/*                                                                      */
/*======================================================================*/


/*==============================================================*/
/* TABLE: xml_file                                              */
/*==============================================================*/


CREATE TABLE xml_file (
        xml_file_name                   VARCHAR2(50)    NOT NULL,
        doc_type_name                   VARCHAR2(100),
        dtd_public_id                   VARCHAR2(200)   NOT NULL,
        dtd_system_id                   VARCHAR2(200)   NOT NULL,
        time_processed                  VARCHAR2(50),
        CONSTRAINT pk_xml_file
                PRIMARY KEY (xml_file_name)
)
/


/*==============================================================*/
/* TABLE: medline_citation                                      */
/*==============================================================*/


CREATE TABLE medline_citation (
        pmid                            VARCHAR2(20) 	NOT NULL,  
        medlineid                       VARCHAR2(20),
        date_created                    VARCHAR2(30),
        date_completed                  VARCHAR2(30),
        date_revised                    VARCHAR2(30),
        number_of_references            NUMBER,
        keyword_list_owner              VARCHAR2(30),   
        citation_owner                  VARCHAR2(30) 	DEFAULT 'NLM',     
        citation_status                 VARCHAR2(50),   
        article_title                   VARCHAR2(4000)  NOT NULL,
        start_page                      VARCHAR2(10),
        end_page                        VARCHAR2(10),
        medline_pgn                     VARCHAR2(200),
        article_affiliation             VARCHAR2(2000),
        article_author_list_comp_yn     CHAR(1) DEFAULT 'Y',
        data_bank_list_complete_yn      CHAR(1) DEFAULT 'Y',
        grant_list_complete_yn          CHAR(1) DEFAULT 'Y',
        vernacular_title                VARCHAR2(4000),
        date_of_electronic_publication  VARCHAR2(100),
        CONSTRAINT pk_medline_citation
                PRIMARY KEY (pmid),
        CONSTRAINT ck1_medline_citation
                CHECK (keyword_list_owner IN ('NLM', 'NASA', 'PIP', 'KIE', 'HSR', 'HMD', 'SIS', 'NOTNLM')),
        CONSTRAINT ck2_medline_citation
                CHECK (citation_owner IN ('NLM', 'NASA', 'PIP', 'KIE', 'HSR', 'HMD', 'SIS', 'NOTNLM')),
        CONSTRAINT ck3_medline_citation
                CHECK (citation_status IN ('In-Process', 'Completed', 'Out-of-scope', 'PubMed-not-MEDLINE')), 
        CONSTRAINT ck4_medline_citation
        	CHECK (article_author_list_comp_yn IN ('Y', 'N', 'y', 'n')),
        CONSTRAINT ck5_medline_citation
                CHECK (data_bank_list_complete_yn IN ('Y', 'N', 'y', 'n')),
        CONSTRAINT ck6_medline_citation
                CHECK (grant_list_complete_yn IN ('Y', 'N', 'y', 'n'))
)
/


/*==============================================================*/
/* TABLE: journal                                               */
/*==============================================================*/


CREATE TABLE journal (
	pmid				VARCHAR2(20)	NOT NULL,
        issn                            VARCHAR2(30),
        volume                          VARCHAR2(200),
        issue                           VARCHAR2(200),
        pub_date_year                   VARCHAR2(4),
        pub_date_month                  VARCHAR2(20),
        pub_date_day                    VARCHAR2(2),
        pub_date_season                 VARCHAR2(10),
        medline_date                    VARCHAR2(30),
        coden                           VARCHAR2(100),
        title                           VARCHAR2(2000),
        iso_abbreviation                VARCHAR2(50),
        CONSTRAINT pk_journal
                PRIMARY KEY (pmid),
        CONSTRAINT fk_journal
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/

/*==============================================================*/
/* INDEX: journal_idx1                                          */
/*==============================================================*/


CREATE INDEX journal_idx1 ON journal (
   issn ASC
)
/

/*==============================================================*/
/* INDEX: journal_idx2                                          */
/*==============================================================*/


CREATE INDEX journal_idx2 ON journal (
   pub_date_year ASC
)
/


/*==============================================================*/
/* TABLE: medline_journal_info                                  */
/*==============================================================*/


CREATE TABLE medline_journal_info (
        pmid         			VARCHAR2(20)	NOT NULL,
        nlm_unique_id                   VARCHAR2(20),
        medline_ta                      VARCHAR2(200)   NOT NULL,
        country                         VARCHAR2(50),
        CONSTRAINT pk_medline_journal_info
                PRIMARY KEY (pmid)
        CONSTRAINT fk_medline_journal_info
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* INDEX: medline_journal_info_idx1                             */
/*==============================================================*/


CREATE INDEX medline_journal_info_idx1 ON medline_journal_info (
   nlm_unique_id ASC
)
/


/*==============================================================*/
/* INDEX: medline_journal_info_idx2                             */
/*==============================================================*/


CREATE INDEX medline_journal_info_idx2 ON medline_journal_info (
   medline_ta ASC
)
/


/*==============================================================*/
/* TABLE: pmids_in_file                                         */
/*==============================================================*/


CREATE TABLE pmids_in_file(
        xml_file_name        		VARCHAR2(50)    NOT NULL,
        pmid                            VARCHAR2(20)    NOT NULL,
        CONSTRAINT pk_pmids_in_file
                PRIMARY KEY (xml_file_name, pmid),
        CONSTRAINT fk1_pmids_in_file
                FOREIGN KEY (xml_file_name) 
                        REFERENCES xml_file (xml_file_name),
        CONSTRAINT fk2_pmids_in_file
                FOREIGN KEY (pmid) 
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* TABLE: abstract                                              */
/*==============================================================*/


CREATE TABLE abstract (
        pmid                            VARCHAR2(20)    NOT NULL,
        abstract_text                   VARCHAR2(4000)	NOT NULL,
        copyright_information           VARCHAR2(2000),
        abstract_type                   VARCHAR2(100)   NOT NULL,
        CONSTRAINT pk_abstract
                PRIMARY KEY (pmid, abstract_type),
        CONSTRAINT fk_abstract
                FOREIGN KEY (pmid) 
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* TABLE: chemical_list                                         */
/*==============================================================*/


CREATE TABLE chemical_list (
        pmid                            VARCHAR2(20)    NOT NULL,
        registry_number                 VARCHAR2(20)	NOT NULL,
        name_of_substance               VARCHAR2(3000)  NOT NULL,
        CONSTRAINT pk_chemical_list
                PRIMARY KEY (pmid, registry_number, name_of_substance),
        CONSTRAINT fk_chemical_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* INDEX: chemical_list_idx1                                    */
/*==============================================================*/


CREATE INDEX chemical_list_idx1 ON chemical_list (
   name_of_substance ASC
)
/


/*==============================================================*/
/* TABLE: citation_subsets                                       */
/*==============================================================*/


CREATE TABLE citation_subsets(
        pmid                            VARCHAR2(20)    NOT NULL,
        citation_subset                 VARCHAR2(500)	NOT NULL,
        CONSTRAINT pk_citation_subsets
                PRIMARY KEY (pmid, citation_subset),
        CONSTRAINT fk_citation_subsets
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* TABLE: comments_corrections                                  */
/*==============================================================*/


CREATE TABLE comments_corrections (
        pmid                            VARCHAR2(20)    NOT NULL,
        ref_source                      VARCHAR2(4000),
        ref_pmid_or_medlineid           CHAR(9),
        ref_pmid                        VARCHAR2(20),
        ref_medlineid                   VARCHAR2(20),
        note                            VARCHAR2(4000),
        type                            VARCHAR2(30)    NOT NULL,
        CONSTRAINT fk_comments_corrections
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid),
        CONSTRAINT ck1_comments_corrections
                CHECK (type IN ('CommentOn', 'CommentIn', 'ErratumIn', 'ErratumFor', 'RepublishedFrom', 'RepublishedIn', 'RetractionOf', 'RetractionIn',  'UpdateIn', 'UpdateOf', 'SummaryForPatientsIn', 'OriginalReportIn')),
        CONSTRAINT ck2_comments_correction
                CHECK (ref_pmid_or_medlineid IN ('p', 'm', 'P', 'M'))
)
/


/*==============================================================*/
/* INDEX: coments_corrections_idx1                              */
/*==============================================================*/


CREATE INDEX comments_corrections_idx1 ON comments_corrections (
   pmid ASC
)
/


/*==============================================================*/
/* TABLE: gene_symbol_list                                      */
/*==============================================================*/

CREATE TABLE gene_symbol_list (
        pmid                            VARCHAR2(20)    NOT NULL,
        gene_symbol                     VARCHAR2(30)    NOT NULL,
        CONSTRAINT pk_gene_symbol_list
                PRIMARY KEY (pmid, gene_symbol),
        CONSTRAINT fk_gene_symbol_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/

/*==============================================================*/
/* INDEX: gene_symbol_list_idx2                                 */
/*==============================================================*/


CREATE INDEX gene_symbol_list_idx2 ON gene_symbol_list (
   gene_symbol ASC
)
/


/*==============================================================*/
/* TABLE: mesh_heading_list                                     */
/*==============================================================*/


CREATE TABLE mesh_heading_list (
        pmid                            VARCHAR2(20)    NOT NULL,
        descriptor_name                 VARCHAR2(500),
        descriptor_name_major_yn        CHAR(1)         DEFAULT 'N',
        CONSTRAINT pk_mesh_heading_list
                PRIMARY KEY (pmid, descriptor_name),
        CONSTRAINT fk_mesh_heading_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid),
        CONSTRAINT ck1_mesh_heading_list
                CHECK (descriptor_name_major_yn IN ('Y', 'N', 'y', 'n'))
)
/


/*==============================================================*/
/* TABLE: qualifier_names                                       */
/*==============================================================*/


CREATE TABLE qualifier_names (
        pmid                            VARCHAR2(20)    NOT NULL,
        descriptor_name                 VARCHAR2(500),
        qualifier_name                  VARCHAR2(500),
        qualifier_name_major_yn         CHAR(1)         DEFAULT 'N',
        CONSTRAINT pk_qualifier_names
                PRIMARY KEY (pmid, descriptor_name, qualifier_name),
        CONSTRAINT fk_qualifier_names
                FOREIGN KEY (pmid) 
                        REFERENCES medline_citation (pmid),
        CONSTRAINT ck1_qualifiers_names
                CHECK (qualifier_name_major_yn IN ('Y', 'N', 'y', 'n'))
)
/


/*==============================================================*/
/* INDEX: qualifier_names_idx1                                  */
/*==============================================================*/


CREATE INDEX qualifier_names_idx1 ON qualifier_names (
   descriptor_name ASC
)       
/


/*==============================================================*/
/* INDEX: qualifier_names_idx2                                  */
/*==============================================================*/


CREATE INDEX qualifier_names_idx2 ON qualifier_names (
   qualifier_name ASC
)       
/


/*==============================================================*/
/* TABLE: personal_name_subject_list                            */
/*==============================================================*/


CREATE TABLE personal_name_subject_list (
        pmid			        VARCHAR2(20)  	NOT NULL,
        last_name                       VARCHAR2(300)   NOT NULL,
        fore_name                       VARCHAR2(100),
        first_name                      VARCHAR2(100),
        middle_name                     VARCHAR2(50),
        initials                        VARCHAR2(10),
        suffix                          VARCHAR2(10),
        CONSTRAINT fk_personal_name_subject_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* INDEX: pname_subject_list_idx1                               */
/*==============================================================*/


CREATE INDEX pname_subject_list_idx1 ON personal_name_subject_list (
   last_name ASC
)
/


/*==============================================================*/
/* INDEX: pname_subject_list_idx2                               */
/*==============================================================*/


CREATE INDEX pname_subject_list_idx2 ON personal_name_subject_list (
   pmid ASC
)
/


/*==============================================================*/
/* TABLE: other_ids                                             */
/*==============================================================*/


CREATE TABLE other_ids(
        pmid                            VARCHAR2(20)    NOT NULL,
        other_id                        VARCHAR2(30)    NOT NULL,
        other_id_source                 VARCHAR2(20)    NOT NULL,
        CONSTRAINT pk_other_ids
                PRIMARY KEY (pmid, other_id, other_id_source),
        CONSTRAINT fk_other_ids
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid),
        CONSTRAINT ck1_other_ids
                CHECK (other_id_source IN ('NASA', 'KIE', 'PIP', 'POP', 'ARPL', 'CPC', 'IND', 'CPFH', 'CLML', 'IM', 'SGC', 'NCT', 'NRCBL'))
)
/


/*==============================================================*/
/* TABLE: keyword_list                                          */
/*==============================================================*/


CREATE TABLE keyword_list (
        pmid                            VARCHAR2(20)    NOT NULL,
        keyword                         VARCHAR2(500)   NOT NULL,
        keyword_major_yn                CHAR(1)      	DEFAULT 'N',
        CONSTRAINT pk_keyword_list
                PRIMARY KEY (pmid, keyword),
        CONSTRAINT fk_keyword_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid),
        CONSTRAINT ck1_keyword_list
                CHECK (keyword_major_yn IN ('Y', 'N', 'y', 'n'))
)
/


/*==============================================================*/
/* INDEX: keyword_list_idx1                                     */
/*==============================================================*/


CREATE INDEX keyword_list_idx1 ON keyword_list (
   keyword ASC
)
/


/*==============================================================*/
/* TABLE: space_flight_missions                                 */
/*==============================================================*/


CREATE TABLE space_flight_missions(
        pmid                            VARCHAR2(20)    NOT NULL,
        space_flight_mission            VARCHAR2(500)   NOT NULL,
        CONSTRAINT pk_space_flight_missions
                PRIMARY KEY (pmid, space_flight_mission),
        CONSTRAINT fk_space_flight_missions
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* TABLE: investigator_list                                     */
/*==============================================================*/


CREATE TABLE investigator_list (
        pmid                            VARCHAR2(20)    NOT NULL,
        last_name                       VARCHAR2(50),
        fore_name                       VARCHAR2(50),
        first_name                      VARCHAR2(50),
        middle_name                     VARCHAR2(50),
        initials                        VARCHAR2(10),
        suffix                          VARCHAR2(10),
        investigator_affiliation        VARCHAR2(200),
        CONSTRAINT fk_investigator_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* INDEX: investigator_list_idx1                                */
/*==============================================================*/


CREATE INDEX investigator_list_idx1 ON investigator_list (
   last_name ASC
)
/


/*==============================================================*/
/* INDEX: investigator_list_idx2                                */
/*==============================================================*/


CREATE INDEX investigator_list_idx2 ON investigator_list (
   pmid ASC
)
/


/*==============================================================*/
/* TABLE: general_notes                                         */
/*==============================================================*/


CREATE TABLE general_notes (
        pmid                            VARCHAR2(20)    NOT NULL,
        general_note                    VARCHAR2(2000)  NOT NULL,
        general_note_owner              VARCHAR2(20),
        CONSTRAINT pk_general_notes
                PRIMARY KEY (pmid, general_note),
        CONSTRAINT fk_general_notes
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid),
        CONSTRAINT ck1_general_notes
                CHECK (general_note_owner IN ('NLM', 'NASA', 'PIP', 'KIE', 'HSR', 'HMD', 'SIS', 'NOTNLM'))
)
/


/*==============================================================*/
/* TABLE: author_list                                           */
/*==============================================================*/


CREATE TABLE author_list (
        pmid	                      	VARCHAR2(20)     NOT NULL,
        personal_or_collective          CHAR(1),
        last_name                       VARCHAR2(300),
        fore_name                       VARCHAR2(50),
        first_name                      VARCHAR2(50),
        middle_name                     VARCHAR2(50),
        initials                        VARCHAR2(10),
        suffix                          VARCHAR2(10),
        collective_name                 VARCHAR2(2000),
        author_affiliation              VARCHAR2(2000),
        CONSTRAINT fk_author_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* INDEX: author_list_idx1                                      */
/*==============================================================*/


CREATE INDEX author_list_idx1 ON author_list (
   last_name ASC
)
/


/*==============================================================*/
/* INDEX: author_list_idx2                                      */
/*==============================================================*/


CREATE INDEX author_list_idx2 ON author_list (
   collective_name ASC
)
/


/*==============================================================*/
/* INDEX: author_list_idx3                                      */
/*==============================================================*/


CREATE INDEX author_list_idx3 ON author_list (
   author_affiliation ASC
)
/


/*==============================================================*/
/* INDEX: author_list_idx4                                      */
/*==============================================================*/


CREATE INDEX author_list_idx4 ON author_list (
   pmid ASC
)
/


/*==============================================================*/
/* TABLE: languages                                             */
/*==============================================================*/


CREATE TABLE languages (
        pmid                            VARCHAR2(20)    NOT NULL,
        language                        VARCHAR2(50)    NOT NULL,
        CONSTRAINT pk_languages
                PRIMARY KEY (pmid, language),
        CONSTRAINT fk_languages
        	FOREIGN KEY (pmid)
        		REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* TABLE: data_bank_list                                        */
/*==============================================================*/


CREATE TABLE data_bank_list (
        pmid                            VARCHAR2(20)    NOT NULL,
        data_bank_name                  VARCHAR2(300)   NOT NULL,
        CONSTRAINT pk_data_bank_list
                PRIMARY KEY (pmid, data_bank_name),
        CONSTRAINT fk_data_bank_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* TABLE: accession_number_list                                 */
/*==============================================================*/


CREATE TABLE accession_number_list (
        pmid                            VARCHAR2(20)    NOT NULL,
        data_bank_name                  VARCHAR2(300)   NOT NULL,
        accession_number                VARCHAR2(100)   NOT NULL,
        CONSTRAINT pk_accession_number_list
                PRIMARY KEY (pmid, data_bank_name, accession_number),
        CONSTRAINT fk_accession_number_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* TABLE: grant_list                                            */
/*==============================================================*/


CREATE TABLE grant_list (
        pmid                           	VARCHAR2(20) 	NOT NULL,
        grantid                        	VARCHAR2(200),
        acronym                        	VARCHAR2(20),
        agency                          VARCHAR2(200),
        CONSTRAINT fk_grant_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/


/*==============================================================*/
/* INDEX: grant_list__idx1                                      */
/*==============================================================*/


CREATE INDEX grant_list_idx1 ON grant_list (
   pmid ASC
)
/


/*==============================================================*/
/* INDEX: grant_list__idx2                                      */
/*==============================================================*/


CREATE INDEX grant_list_idx2 ON grant_list (
   grantid ASC
)
/


/*==============================================================*/
/* TABLE: publication_type_list                                 */
/*==============================================================*/


CREATE TABLE publication_type_list (
        pmid                            VARCHAR2(20)   	NOT NULL,
        publication_type                VARCHAR2(200)   NOT NULL,
        CONSTRAINT pk_publication_type_list
                PRIMARY KEY (pmid, publication_type),
        CONSTRAINT fk_publication_type_list
                FOREIGN KEY (pmid)
                        REFERENCES medline_citation (pmid)
)
/

