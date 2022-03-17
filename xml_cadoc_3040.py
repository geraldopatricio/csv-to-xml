import csv
import xml.etree.ElementTree as ET


def sortchildrenby(parent, attr):
    parent[:] = sorted(parent, key=lambda child: child.get(attr))


#retorna apenas a primeira ocorrencia registrada
def find_index(elements, value, key):
   
    left, right = 0, len(elements) - 1

    while left <= right:
        middle = (left + right) // 2
        middle_element = key(elements[middle])
        if middle_element == value:
            return middle
        
        if middle_element < value:
            left = middle + 1
        elif middle_element > value:
            right = middle - 1

#retorna indice de todas as ocorrencias no array
def find_index2(elements, value, key):
    low, high = 0, len(elements) - 1
    started_index = -1
    while low <= high:
        mid = (high - low) // 2 + low
        middle_element = key(elements[mid])
        if middle_element > value:
            high = mid - 1
        elif middle_element == value:
            started_index = mid
            high= mid -1
        else:
            low = mid + 1 
    # get end index of target
    end_index = -1
    low = 0
    high = len(elements) - 1

    while low <= high:
        mid = (high - low) // 2 + low
        middle_element = key(elements[mid])
        if middle_element > value:
            high = mid - 1
        elif middle_element == value:
            end_index = mid
            low = mid + 1
        else:
            low = mid + 1 

    index_list = []

    if started_index != -1 and end_index != -1:
        for i in range(started_index, end_index + 1):
            index_list.append(i)
    return index_list

if __name__ == '__main__':
    tree = ET.parse("ARQUIVO.xml")
    root = tree.getroot()
    with open("BASE.csv") as file:
        csv = csv.reader(file, delimiter=";")
        sortedlist = sorted(csv, key=lambda row: row[0])       
        alterados = 0
        #para cada cli em root rodar
        for cli in root:
            atributos_cli = cli.attrib
            #retira o Cd do cli
            Cd = atributos_cli.get("Cd")
            if Cd ==  None: 
                continue

            #busca todas as ocorrencias do Cd no csv
            indexs = find_index2(sortedlist, key=lambda row: row[0], value=Cd)
            #cria lista de todas as linhas no csv que contem esse Cd
            list_of_cds = [sortedlist[i] for i in indexs]
            #para cada uma das ocorrencias extrai as informacoes do csv
            for row_csv in list_of_cds:
                csv_Contrt = row_csv[1]
                csv_Mod = row_csv[2]
                #para cada op dentro de cli busca saber se tem algum com mob e contrt da linha do csv. Se tiver atualiza com as informacoes
                for op in cli:
                    atributos_op = op.attrib
                    Contrt = atributos_op.get("Contrt")
                    Mod = atributos_op.get("Mod")
                    if Contrt == None or Mod == None:
                        continue
                    if Contrt == csv_Contrt and Mod == csv_Mod:
                        try:
                            op.set("VlrProxParcela", row_csv[9])
                            op.set("DtaProxParcela", row_csv[10])
                            op.set("QtdParcelas", row_csv[11])
                        except IndexError as e:
                            print(f"Falha ao registrar {row_csv} {str(e)}")
                        alterados += 1

        print(f"Numero de ops alterados: {alterados}")
    tree.write('saida.xml')