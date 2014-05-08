literature
==========

Data mining, mostly medline. Used to be CAOPSCI project.


For the time being we shall provide this functionality:

 - update local cache, a mongo document database, from a query to PubMed
 - build mesh term networks from queries to mongodb, as networkX graphs, save them to python pickle files
 - plot these networks using matplotlib
 - plot these networks using d3
 - convert these networks to CSV files
 - a CSV to networkX loader, inputs CVS, outputs pickle
 
 These functions shall have a command line interface and those scripts shall have PSU Galaxy wrappers.
 
 We hope to share this tool online from our own Galaxy instance.
