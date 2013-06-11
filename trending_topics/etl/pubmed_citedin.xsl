<xsl:stylesheet version='1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
<xsl:output method="text"/> 
  <xsl:template match="/">
    <xsl:for-each select="//LinkSetDb[LinkName='pubmed_pubmed_citedin']/Link/Id"><xsl:value-of select="."/>,</xsl:for-each>
  </xsl:template>
  
</xsl:stylesheet>
