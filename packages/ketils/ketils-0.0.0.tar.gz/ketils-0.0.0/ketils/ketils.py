
import warnings
import numpy as np
import pandas as pd
import cv2
import requests
from PIL import Image
from bs4 import BeautifulSoup
from bioservices import KEGG

from ketils.utils import *


class kegg_utils :
    
    def __init__(self) :
        
        self.func_list = ['search_kegg_pathway', 'search_kegg', 'get_kegg_info', 'gene_id_to_symbol', 'get_kgml', 'kgml_id_to_keggid',
                         'get_relatives' , 'pathway_mapping']
    
    
    ## KEGG search.

    def search_kegg_pathway(self, query, org='hsa', by_gene=False) :

        """
        Search KEGG pathway.
        
        Parameters
        ----------
        query : str
            Can be pathway name, pathway ID, gene symbol, gene ID, etc.

        org : str 
            KEGG organism code.

        by_gene : bool
            If True, pathways containing the required gene(query) are returned. 
            If False, pathways containing the query in the pathway name or ID are returned.

        Returns
        -------
        pandas.DataFrame
        """

        assert type(query) == str, "argument 'query' must be str"
        
        k = KEGG()

        query = query.strip()
        query = replace_all(query, ' ', '+')
        query = ''.join(query)

        if by_gene == False :
            result = k.find('pathway', query)
            if result == '\n' or type(result) != str :
                raise Exception('no results')        
            res_df = tabular_to_df(result)
        elif by_gene == True :
            if query.split(':')[0] == org :
                query = query.split(':')[1]

            result = k.get_pathway_by_gene(query, org)
            if result == None :
                raise Exception('no results')
            res_df = pd.DataFrame.from_dict(data=result, orient='index')
            res_df = res_df.reset_index()
            res_df.columns = range(len(res_df.columns))       

        return res_df

    
    def search_kegg(self, db, query, option=None) :
    
        """
        Search KEGG object.
        
        Parameters
        ----------
        db : str
            Can be one of module, disease, drug,environ, ko, 
            genome, compound, glycan, reaction, rpair, rclass,
            enzyme, genes, ligand or an kegg organism code or T number.
        
        query : str
        
        option : str
            If option provided, database can be only 'compound' or 'drug'. 
            Option can be 'formula', 'exact_mass' or 'mol_weight'.

        Returns
        -------
        pandas.DataFrame
        """
        
        assert db != 'pathway', 'Use search_kegg_pathway() method'

        k = KEGG()

        query = query.strip()
        query = replace_all(query, ' ', '+')
        query = ''.join(query)

        result = k.find(db, query, option)
        if result == '\n' or type(result) != str :
            raise Exception('no results')

        res_df = tabular_to_df(result)

        return res_df


    def get_kegg_info(self, kegg_id) :
    
        """
        Get KEGG information text from the KEGG object ID.
        
        Parameters
        ----------
        kegg_id : str
            KEGG object ID.

        Returns
        -------
        dict
        """

        k = KEGG() 

        kegg_info = k.get(kegg_id)
        
        if kegg_info == '\n' or type(kegg_info) != str :
            raise Exception('no results') 

        kegg_info = k.parse(kegg_info)

        return kegg_info


    def gene_id_to_symbol(self, gene_id) :

        """
        Get gene symbols from the gene ID.
        
        Parameters
        ----------
        gene_id :
            KEGG gene ID.

        Returns
        -------
        list
            List of gene symbols corresponding to the gene ID.
        """

        gene_info = self.get_kegg_info(gene_id)

        if 'SYMBOL' in gene_info.keys() :
            symbols = gene_info['SYMBOL'].split(',')
            symbols = [symbol.strip() for symbol in symbols]
        else :
            symbols = []

        return symbols    
    
    
    ## KGML
    
    def get_kgml(self, pathway_id) : 
    
        """
        Get KGML in dictionary form.
        
        Parameters
        ----------
        pathway_id : str
            KEGG pathway ID.

        Returns
        -------
        dict
            keys : 'pathway ID', 'entries', 'relations'
        """

        warnings.filterwarnings('ignore')
        
        k = KEGG()

        kgml = {'pathway ID':None, 'entries':{}, 'relations':[]}
        
        try : 
            result = k.parse_kgml_pathway(pathway_id)
        except :
            raise Exception('no results')

        kgml['pathway ID'] = pathway_id
        
        for entry_info in result['entries'] :
            kgml_id = int(entry_info.pop('id'))
            entry_info['kegg_id'] = remove_all(entry_info.pop('name').split(' '), '')
            if 'gene_names' in entry_info.keys() :
                if entry_info['gene_names'] != None :
                    names = entry_info.pop('gene_names').split(',')
                    names = [name.strip() for name in names]
                    if entry_info['type'] == 'gene' :
                        entry_info['symbols'] = names
                    else :
                        entry_info['names'] = names
                else :
                    entry_info.pop('gene_names')
            entry_info.pop('link')
            kgml['entries'][kgml_id] = entry_info
            
        for rel_dict in result['relations'] :
            entry1 = int(rel_dict['entry1'])
            entry2 = int(rel_dict['entry2'])
            rel_type = [rel_dict[key] for key in ['link','value','name']]
            kgml['relations'].append([entry1] + rel_type + [entry2])

        return kgml

    
    def kgml_id_to_keggid(self, kgml, kgml_id) :
    
        """
        Get KEGG ID from the KGML ID.
        
        Parameters
        ----------
        kgml : dict
            KGML dict.
        
        kgml_id : int
            KGML ID.

        Returns
        -------
        list
            List of KEGG IDs corresponding to the KGML ID.
        """

        entries = kgml['entries']
        
        if kgml_id in entries.keys() :
            info = entries[kgml_id]
            kegg_id = info['kegg_id']
        else :
            kegg_id = [] 

        return kegg_id


    def get_relatives(self, kgml, kgml_id) :
    
        """
        Extract entries related to a specific entry.
        
        Parameters
        ----------
        kgml : dict 
            KGML dict.
        
        kgml_id : int
            KGML ID.

        Returns
        -------
        dict
            keys : 'from', 'to'
        """

        entries = kgml['entries']
        relations = kgml['relations']

        related = {'from':[], 'to':[]}
        
        for relation in relations :
            if kgml_id == relation[-1] :
                related['from'].append(relation[0])
            elif kgml_id == relation[0] :
                related['to'].append(relation[-1])

        return related 


    ## KEGG mapper
    def pathway_mapping(self, pathway_id, keggid_list, save_path=None) :
    
        """
        Parameters
        ----------
        pathway_id : str
            KEGG pathway ID.

        keggid_list : list
            List of KEGG IDs.
        
        save_path : str or None
            Path of directory to save the result.

        Returns
        -------
        PIL.Image
        """

        assert type(keggid_list) == list, "argument 'keggid_list' must be list" 
        
        k = KEGG()

        for keggid in keggid_list :
            if len(keggid.split(':')) == 1 :
                raise ValueError('there must be a organism code in front of the KEGG ID. ')
        
        url = k.show_pathway(pathway_id, keggid=keggid_list, show=False)
        html = requests.get(url)    
        html = BeautifulSoup(html.text, "html.parser")

        links_to_png = [tag.get('src') for tag in html.find_all('img')]
        link_to_png = [link for link in links_to_png if 'png' in link][0]
        
        whole_image = requests.get("https://www.kegg.jp/{}".format(link_to_png))
        whole_image = cv2.imdecode(np.frombuffer(whole_image.content, np.uint8), -1)
        whole_image = rgba_to_rgb(whole_image)

        areas = [html.find('area', href='/entry/{}'.format(keggid)) for keggid in keggid_list]
        areas = remove_all(areas, None)
        if areas == [] :
            raise Exception('no results')
        
        rects = [area for area in areas if area.get('shape') == 'rect']
        circles = [area for area in areas if area.get('shape') == 'circle']

        for rect in rects :
            x1, y1, x2, y2 = map(int, rect.get('coords').split(','))
            row_slice = slice(y1, y2+1)
            col_slice = slice(x1, x2+1)

            entry_image = whole_image[row_slice, col_slice]
            nrow, ncol = entry_image.shape[0], entry_image.shape[1]

            entry_image = entry_image.reshape(nrow*ncol, 3)
            entry_image = [np.array((255,153,153), dtype='uint8') if tuple(rgb) not in [(255,153,153), (0,0,0)] else rgb for rgb in entry_image]
            entry_image = np.array(entry_image).reshape(nrow, ncol, 3)

            whole_image[row_slice, col_slice] = entry_image

        for circle in circles :
            x, y, r = map(int, circle.get('coords').split(','))
            whole_image = cv2.circle(whole_image, (x,y), r, (255,153,153) ,thickness=-1)

        whole_image = Image.fromarray(whole_image, 'RGB')
        
        if save_path != None :
            whole_image.save(save_path)

        return whole_image

