<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html>
            <head>
                <title>RSS Feed</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }
                    h1 {
                        color: #333;
                    }
                    .item {
                        margin-bottom: 20px;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                    .item h2 {
                        margin: 0 0 10px;
                        color: #007BFF;
                    }
                    .item p {
                        margin: 0;
                        color: #555;
                    }
                    .item a {
                        color: #007BFF;
                        text-decoration: none;
                    }
                    .item a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <h1>RSS Feed: <xsl:value-of select="rss/channel/title"/></h1>
                <xsl:for-each select="rss/channel/item">
                    <div class="item">
                        <h2><xsl:value-of select="title"/></h2>
                        <p><xsl:value-of select="description"/></p>
                        <a>
                            <xsl:attribute name="href">
                                <xsl:value-of select="link"/>
                            </xsl:attribute>
                            Читать далее
                        </a>
                    </div>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>