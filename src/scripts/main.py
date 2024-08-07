import pandas as pd
import os
import glob

#caminho para ler os arquivos
folder_path = 'src\\data\\raw'

#lista todos os arquivos de excel (* limita so xlsx)
excel_files = glob.glob(os.path.join(folder_path ,'*.xlsx'))

if not excel_files:
    print("Nenhum arquivo compativel encontrado")
else:

#dataframe = tabela na memoria para guarda os conteudos dos arquivos
   dfs =[]

   for excel_files in excel_files:

      try:
          #leio o arquivo de excel
          df_temp =  pd.read_excel(excel_files)
     
          # pegar o nome do arquivo
          file_name = os.path.basename(excel_files)


          df_temp['filename'] = file_name
     
         #criamos uma nova coluna chamada location
          if 'brasil' in file_name.lower():
            df_temp['lacation'] ='br' 
          elif 'france' in file_name.lower():
            df_temp['lacation'] = 'fr'
          elif 'italia' in file_name.lower():
            df_temp['lacation'] = 'it'

         #criamos uma nova coluna chamada campaing
          df_temp['campaign'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')

          # guarda dados tratados dentro de uma dataframe comum
          dfs.append(df_temp)

      except Exception as e:
            print(f"Erro ao ler o arquivo {excel_files}: {e}")  

if dfs:
   
   # concatena toas as tabelas salvas no dfs em uma unica tabela
   result = pd.concat(dfs, ignore_index=True)

   # Caminho de saida
   output_file = os.path.join('src', 'data', 'ready', 'clean.xlsx')   

   #Configurou o motor de escrita
   writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

   #leva os dados do resultado a serem escritos no motor de excel configurado
   result.to_excel(writer, index=False)   
   
   #Salva o arquivo de excel
   writer._save()  

else:
   print("Nenhum dado para ser salvo")  