import sys
from md2pdf.core import md2pdf

header = open("template/header.html").read()
footer = open("template/footer.html").read()
style = "template/style.css"
content = open(sys.argv[1]).read()
output = sys.argv[2]

def exportfile():
    global header, footer, style, content, output

    filedata = header + content + footer
    exportfilename = output
    if exportfilename:
        try:
            md2pdf(exportfilename, md_content=filedata, css_file_path=style)
            print ("[+] Export file to %s" % exportfilename)
        except:
            print ("[-] Error exporting to %s" % exportfilename)

exportfile()