import os
from markitdown import MarkItDown

class ReadFiles:
    def __init__(self):
        pass
    
    def docs_to_markdown(self, dir_path):
        
        docs = self.read_dir(dir_path)

        for file in docs:
            
            file_path = os.path.join(dir_path, file)
        
            # quero que vc leia o file e diga qual o tipo do arquivo (pdf, doc, docx, image e ect)
            extension = file.split('.')[-1] 
            
            if extension == 'pdf' or \
            extension == 'doc' or \
            extension == 'docx' or \
            extension == "xls" or \
            extension == "xlsx" or \
            extension == "ppt" or \
            extension == "pptx" or \
            extension == "csv" or \
            extension == "txt" or \
            extension == "json" or \
            extension == "xml" or \
            extension == "html" or \
            extension == "htm" or \
            extension == "yaml": 
                
                md = MarkItDown(enable_plugins=True)
                            
            elif extension == 'jpg' or \
                extension == 'png' or \
                extension == 'jpeg' or \
                extension == 'gif' or \
                extension == 'bmp' or \
                extension == 'webp' or \
                extension == 'svg' or \
                extension == 'tiff' or \
                extension == 'ico':
                
                
                client = OpenAI()

                md = MarkItDown(llm_client=client,
                                llm_model="gpt-5-mini",
                                llm_prompt="""Em 3 parágrafos, 
                                descreva a imagem detalhadamente em 
                                pt-br""",
                                enable_plugins=True)
                
                
            result = md.convert(file_path)
            
            # SALVE O RESULTADO EM UM ARQUIVO MD NA PASTA MARKDOWN
            # O nome do arquivo em "file.split" pode conter mais de um ponto
            # por exemplo: 2111.01888v1.pdf
            # entao o nome do arquivo md deve ser: 2111.01888v1.md
            # No código abaixo vc deve pegar no split o último ponto
            # e usar ele para criar o nome do arquivo md
            # por exemplo: 2111.01888v1.pdf
            # o último ponto é o ".pdf"
            # entao o nome do arquivo md deve ser: 2111.01888v1.md
            

            # Remove apenas a última extensão (após o último ponto)
            filename_without_ext = os.path.splitext(file)[0]
            md_path = os.path.join("markdown", filename_without_ext + ".md")
            
            # se não existir a pasta markdown, crie
            if not os.path.exists("markdown"):
                os.makedirs("markdown")
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(result.text_content)            
            
        # LER TODO O CONTEUDO DA PASTA MARKDOWN 
        # E RETORNAR UM STRING COM O CONTEUDO
        md_content = ""
        
        for file in os.listdir("markdown"):
        
            with open(os.path.join("markdown", file), "r", encoding="utf-8") as f:
                md_content += f.read()
        
        return md_content
    
    def read_dir(self, dir_path):
        
        files = os.listdir(dir_path)
        
        return files
        