import pdfplumber, os, string

directoryname = os.getcwd()
folder = os.altsep+'pdfs'+os.altsep


with pdfplumber.open(directoryname+folder+'test.pdf') as pdf:
    italic_phrases = []
    for page in pdf.pages:
        
        text = page.extract_text()
        print(text)
        italics = ''

        found = False
        for char in page.chars:
            if 'Italic' in char['fontname']:
                if not found and italics:
                    italic_phrases.append(italics)
                    italics = char['text']
                    found = True 
                else:
                    italics += char['text']
                    found = True
            else:
                if found and char['text'] not in string.whitespace:
                    found = False
    print(', '.join(italic_phrases))
    input('?')
    
        

        
        
