

Para usar las caopsci galaxy tools:

Instalar galaxy cual se describe acá:

http://wiki.galaxyproject.org/Admin/Get%20Galaxy

   1 % hg clone https://bitbucket.org/galaxy/galaxy-dist/
   2 % cd galaxy-dist
   3 % hg update stable
   4 236 files updated, 0 files merged, 152 files removed, 0 files unresolved






Hay que incluir la parte de las Caopsci tools en el archivo
tool_conf.xml, o sustituirlo por el que distribuimos, así:

~/galaxy-dist$ rm tool_conf.xml
~/galaxy-dist$ ln -s ~/caopsci/meddle/galaxy_tools/tool_conf.xml .



En el directorio tools/ hay que poner una liga a nuestro directorio de
herramientas.

~/galaxy-dist$ cd tools
~/galaxy-dist$ ln -s ~/caopsci/meddle/galaxy_tools/ caopsci






