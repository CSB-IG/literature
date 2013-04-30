-- Parse::SQL::Dia       version 0.25                              
-- Documentation         http://search.cpan.org/dist/Parse-Dia-SQL/
-- Environment           Perl 5.014002, /usr/bin/perl              
-- Architecture          x86_64-linux-gnu-thread-multi             
-- Target Database       sqlite3fk                                 
-- Input file            medline.dia                               
-- Generated at          Tue Apr 30 13:45:02 2013                  
-- Typemap for sqlite3fk not found in input file                   

-- get_constraints_drop 

-- get_permissions_drop 

-- get_view_drop

-- get_schema_drop
drop table if exists citation;
drop table if exists journal;
drop table if exists language;
drop table if exists publication_history_status;
drop table if exists author;
drop table if exists subheading;
drop table if exists meshterm;
drop table if exists citation_journal;
drop table if exists citation_author;
drop table if exists citation_history;
drop table if exists citation_lang;
drop table if exists mesh_subheading;
drop table if exists mesh_citation;

-- get_smallpackage_pre_sql 

-- get_schema_create

create table citation (
   pmid                        INTEGER PRIMARY KEY,
   date_created                date                  ,
   date_completed              date                  ,
   date_revised                date                  ,
   article_title               varchar(4000) not null,
   affiliation                 varchar(2000)         ,
   date_electronic_publication date                  ,
   abstract                    varchar(4000)         ,
   publication_type            varchar(200)          ,
   pagination                  varchar(200)          ,
   copyright_information       varchar(2000)         
)   ;

create table journal (
   journal_id       INTEGER PRIMARY KEY,
   issn             varchar(30)           ,
   volume           varchar(200)          ,
   issue            varchar(200)          ,
   pub_date         date                  ,
   title            varchar(2000)         ,
   iso_abbreviation varchar(50)           ,
   country          varchar(50)           
)   ;

create table language (
   language_id INTEGER PRIMARY KEY,
   language    varchar(50)         
)   ;

create table publication_history_status (
   phst_id INTEGER PRIMARY KEY,
   status  varchar(50)         ,
   date    date                ,
   pmid    int         not null
)   ;

create table author (
   author_id INTEGER PRIMARY KEY,
   name      varchar(450)         ,
   full_name varchar(500)         
)   ;

create table subheading (
   id    INTEGER PRIMARY KEY,
   term  varchar         ,
   major bool            
)   ;

create table meshterm (
   id    int     INTEGER PRIMARY KEY,
   term  varchar         ,
   major bool            ,
   other bool            
)   ;

create table citation_journal (
   pmid       int not null,
   journal_id int not null,
   constraint pk_citation_journal primary key (pmid,journal_id),
   foreign key(pmid) references citation(pmid) on delete cascade,
   foreign key(journal_id) references journal(journal_id) on delete cascade
)   ;

create table citation_author (
   pmid      int not null,
   author_id int not null,
   constraint pk_citation_author primary key (pmid,author_id),
   foreign key(pmid) references citation(pmid) on delete cascade,
   foreign key(author_id) references author(author_id) on delete cascade
)   ;

create table citation_history (
   pmid    int not null,
   phst_id int not null,
   constraint pk_citation_history primary key (pmid,phst_id),
   foreign key(pmid) references citation(pmid) on delete cascade,
   foreign key(phst_id) references publication_history_status(phst_id) on delete cascade
)   ;

create table citation_lang (
   pmid        int not null,
   language_id int not null,
   constraint pk_citation_lang primary key (pmid,language_id),
   foreign key(pmid) references citation(pmid) on delete cascade,
   foreign key(language_id) references language(language_id) on delete cascade
)   ;

create table mesh_subheading (
   msh_id int not null,
   sbh_id int not null,
   constraint pk_mesh_subheading primary key (msh_id,sbh_id),
   foreign key(msh_id) references meshterm(id) on delete cascade,
   foreign key(sbh_id) references subheading(id) on delete cascade
)   ;

create table mesh_citation (
   pmid int not null,
   id   int not null,
   constraint pk_mesh_citation primary key (pmid,id),
   foreign key(pmid) references citation(pmid) on delete cascade,
   foreign key(id) references meshterm(id) on delete cascade
)   ;

-- get_view_create

-- get_permissions_create

-- get_inserts

-- get_smallpackage_post_sql

-- get_associations_create
