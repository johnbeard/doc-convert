<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format"
    version="1.0">

<!-- Based on the XSL stylesheet from gtkmm - Lennart -->

<xsl:output method="xml" version="1.0" indent="yes"/>

<xsl:param name="book_base"/>

<xsl:template match="/">
  <book title="{$book_title}"
        name="{$book_name}"
        base="{$book_base}"
        link="index.html">
  <chapters>
    <!-- Could include headers, but not sure they are really useful
    <sub name="Headers" link="files.html">
      <xsl:apply-templates select="doxygenindex/compound[@kind='file']">
        <xsl:sort select="."/>
      </xsl:apply-templates>
    </sub>
    -->
    <xsl:apply-templates select="doxygenindex/compound[@kind='dir' and name='modules']" mode="as-dir"/>

    <!-- TODO what about the top level - there's no namespace file -->
    <sub name="Namespaces" link="namespaces.html">
      <xsl:apply-templates select="doxygenindex/compound[@kind='namespace']">
        <xsl:sort select="."/>
      </xsl:apply-templates>
    </sub>

    <sub name="Classes" link="classes.html">
      <xsl:apply-templates select="doxygenindex/compound[@kind='class' or @kind='struct']">
        <xsl:sort select="."/>
      </xsl:apply-templates>
    </sub>
  </chapters>

  <functions>
    <!-- Select all functions, enumvalues, typedefs and defines -->
    <xsl:apply-templates select="doxygenindex/compound/member[@kind='function' or @kind='enumvalue' or @kind='typedef' or @kind='define']" mode="as-function"/>
  </functions>
  </book>
</xsl:template>


<xsl:template match="compound[@kind='class' or @kind='struct']">
  <xsl:param name="name"><xsl:value-of select="name"/></xsl:param>
  <xsl:param name="link"><xsl:value-of select="@refid"/>.html</xsl:param>
  <sub name="{$name}" link="{$link}">
  <xsl:apply-templates select="member[@kind='enum']" mode="as-sub">
    <xsl:sort select="."/>
  </xsl:apply-templates>
  </sub>
</xsl:template>

<xsl:template match="compound" mode="as-dir">
  <xsl:param name="link"><xsl:value-of select="@refid"/>.html</xsl:param>
  <sub name="Modules" link="{$link}">
      <xsl:apply-templates select="/doxygenindex/compound[@kind='dir' and not(name='modules')]"/>
  </sub>
</xsl:template>

<!-- namespaces and dirs are very simple, just a name and link -->
<xsl:template match="compound[@kind='dir' or @kind='namespace']">
  <xsl:param name="name"><xsl:value-of select="name"/></xsl:param>
  <xsl:param name="link"><xsl:value-of select="@refid"/>.html</xsl:param>
  <sub name="{$name}" link="{$link}"/>
</xsl:template>

<xsl:template match="member" mode="as-function">
  <!--
  <keyword type="function" name="Class::func" link="classClass.html#XXXXXX"/>
  -->
  <xsl:param name="name_parent"><xsl:value-of select="parent::node()/name"/></xsl:param>
  <xsl:param name="name"><xsl:value-of select="name"/></xsl:param>
  <xsl:param name="kind"><xsl:value-of select="@kind"/></xsl:param>
  <!-- Link is refid attribute of parent element + "#" + diff between refid of parent and own refid -->
  <xsl:param name="refid_parent"><xsl:value-of select="parent::node()/@refid"/></xsl:param>
  <xsl:param name="own_refid"><xsl:value-of select="@refid"/></xsl:param>
  <xsl:param name="offset"><xsl:value-of select="string-length($refid_parent) + 3"/></xsl:param>
  <xsl:param name="ref_diff"><xsl:value-of select="substring($own_refid, $offset, 33)"/></xsl:param>
  <xsl:param name="link"><xsl:value-of select="$refid_parent"/>.html#<xsl:value-of select="$ref_diff"/></xsl:param>
  <keyword type="{$kind}" name="{$name_parent}::{$name}" link="{$link}"/>
</xsl:template>

<xsl:template match="member" mode="as-sub">
  <xsl:param name="name"><xsl:value-of select="name"/></xsl:param>
  <!-- Link is refid attribute of parent element + "#" + diff between refid of parent and own refid -->
  <xsl:param name="refid_parent"><xsl:value-of select="parent::node()/@refid"/></xsl:param>
  <xsl:param name="own_refid"><xsl:value-of select="@refid"/></xsl:param>
  <xsl:param name="offset"><xsl:value-of select="string-length($refid_parent) + 3"/></xsl:param>
  <xsl:param name="ref_diff"><xsl:value-of select="substring($own_refid, $offset, 33)"/></xsl:param>
  <xsl:param name="link"><xsl:value-of select="$refid_parent"/>.html#<xsl:value-of select="$ref_diff"/></xsl:param>
  <sub name="{$name}" link="{$link}"/>
</xsl:template>

</xsl:stylesheet>
